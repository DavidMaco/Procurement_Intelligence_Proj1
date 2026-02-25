"""
Advanced Analytics Module: FX Risk & Supplier Performance
Includes Monte Carlo FX simulation and composite risk scoring
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime

# =========================
# 1. DATABASE CONNECTION
# =========================

engine = create_engine(
    "mysql+pymysql://root:Maconoelle86@localhost:3306/pro_intel_2"
)

# =========================
# 2. FX MONTE CARLO MODULE
# =========================

def detect_volatility_regimes(log_returns: pd.Series, window: int = 20) -> dict:
    """
    Split return history into low-vol and high-vol regimes, then estimate
    regime-specific drift and volatility and regime probabilities.
    """
    clean = pd.Series(log_returns).dropna().astype(float)
    if clean.empty:
        raise ValueError("No valid returns available for regime detection")

    rolling_vol = clean.rolling(window=window).std().dropna()
    if rolling_vol.empty:
        mu = float(clean.mean())
        sigma = float(clean.std())
        sigma = sigma if sigma > 0 else 1e-6
        return {
            "window": window,
            "threshold": sigma,
            "p_low": 0.5,
            "p_high": 0.5,
            "mu_low": mu,
            "sigma_low": sigma,
            "mu_high": mu,
            "sigma_high": sigma,
        }

    threshold = float(rolling_vol.median())
    aligned_returns = clean.loc[rolling_vol.index]
    high_mask = rolling_vol > threshold

    low_returns = aligned_returns[~high_mask]
    high_returns = aligned_returns[high_mask]

    if low_returns.empty:
        low_returns = aligned_returns
    if high_returns.empty:
        high_returns = aligned_returns

    mu_low = float(low_returns.mean())
    sigma_low = float(low_returns.std())
    mu_high = float(high_returns.mean())
    sigma_high = float(high_returns.std())

    sigma_low = sigma_low if sigma_low > 0 else 1e-6
    sigma_high = sigma_high if sigma_high > 0 else 1e-6

    p_high = float(high_mask.mean())
    p_low = 1.0 - p_high

    return {
        "window": window,
        "threshold": threshold,
        "p_low": p_low,
        "p_high": p_high,
        "mu_low": mu_low,
        "sigma_low": sigma_low,
        "mu_high": mu_high,
        "sigma_high": sigma_high,
    }


def simulate_regime_weighted_paths(
    current_rate: float,
    days: int,
    simulations: int,
    regime_stats: dict,
    seed: int = 42,
):
    """Simulate FX paths using weighted low/high volatility regime probabilities."""
    dt = 1 / 252
    rng = np.random.default_rng(seed)

    p_high = regime_stats["p_high"]
    mu_low = regime_stats["mu_low"]
    sigma_low = regime_stats["sigma_low"]
    mu_high = regime_stats["mu_high"]
    sigma_high = regime_stats["sigma_high"]

    paths = np.zeros((simulations, days), dtype=float)

    for i in range(simulations):
        rate = float(current_rate)
        for d in range(days):
            if rng.random() < p_high:
                shock = rng.normal(mu_high * dt, sigma_high * np.sqrt(dt))
            else:
                shock = rng.normal(mu_low * dt, sigma_low * np.sqrt(dt))
            rate *= np.exp(shock)
            paths[i, d] = rate

    return paths

def run_fx_simulation(currency_id=3, days=90, simulations=10000):
    """
    Run Monte Carlo simulation for FX rate forecasting.
    
    Parameters:
    -----------
    currency_id : int
        Currency to simulate (default 3 for NGN)
    days : int
        Forecast horizon in days
    simulations : int
        Number of Monte Carlo paths
    """
    
    fx_query = f"""
    SELECT rate_date, rate_to_usd
    FROM fx_rates
    WHERE currency_id = {currency_id}
    ORDER BY rate_date
    """

    fx_df = pd.read_sql(fx_query, engine)

    if fx_df.empty:
        raise ValueError(f"No FX data available for currency_id={currency_id}")

    # Calculate log returns
    fx_df['log_return'] = np.log(
        fx_df['rate_to_usd'] / fx_df['rate_to_usd'].shift(1)
    )

    fx_df = fx_df.dropna()

    # Regime-specific drift and volatility
    regime_stats = detect_volatility_regimes(fx_df['log_return'])
    current_rate = fx_df['rate_to_usd'].iloc[-1]

    print(f"FX Simulation Parameters:")
    print(f"  Currency ID: {currency_id}")
    print(f"  Current Rate: {current_rate:.6f}")
    print(f"  Low-Vol Regime:  μ={regime_stats['mu_low']:.6f}, σ={regime_stats['sigma_low']:.6f}, p={regime_stats['p_low']:.2%}")
    print(f"  High-Vol Regime: μ={regime_stats['mu_high']:.6f}, σ={regime_stats['sigma_high']:.6f}, p={regime_stats['p_high']:.2%}")

    # Regime-weighted Monte Carlo simulation
    paths = simulate_regime_weighted_paths(
        current_rate=current_rate,
        days=days,
        simulations=simulations,
        regime_stats=regime_stats,
        seed=42,
    )
    final_rates = paths[:, -1]

    # Calculate percentiles
    p5, p50, p95 = np.percentile(final_rates, [5, 50, 95])

    print(f"\nForecast ({days} days ahead):")
    print(f"  5th Percentile (worst case): {p5:.6f}")
    print(f"  Median (50th percentile): {p50:.6f}")
    print(f"  95th Percentile (best case): {p95:.6f}")
    print(f"  Expected Change: {((p50 - current_rate) / current_rate * 100):.2f}%")

    # Prepare results
    result = pd.DataFrame({
        "simulation_date": [datetime.today().date()],
        "currency_id": [currency_id],
        "forecast_days": [days],
        "current_rate": [current_rate],
        "p5_rate": [p5],
        "median_rate": [p50],
        "p95_rate": [p95],
        "simulations_count": [simulations]
    })

    # Store results (append to keep history)
    result.to_sql(
        "fx_simulation_results",
        engine,
        if_exists="append",
        index=False
    )
    
    print(f"✓ Simulation results stored in fx_simulation_results table")

    return result


# =========================
# 3. COMPOSITE RISK SCORE
# =========================

def run_supplier_risk():
    """
    Calculate comprehensive supplier risk metrics.
    Writes all required columns to supplier_performance_metrics table.
    """
    
    print("\nCalculating Supplier Risk Metrics...")

    # Lead time metrics
    lead_query = """
    SELECT 
        supplier_id,
        AVG(DATEDIFF(delivery_date, order_date)) AS avg_lead_time,
        STDDEV(DATEDIFF(delivery_date, order_date)) AS lead_time_stddev
    FROM purchase_orders
    WHERE delivery_date IS NOT NULL
    GROUP BY supplier_id
    """

    lead_df = pd.read_sql(lead_query, engine)

    if lead_df.empty:
        print("⚠ No lead time data available")
        return

    # Quality metrics (defect rates)
    quality_query = """
    SELECT 
        supplier_id,
        AVG(defect_rate) * 100 AS avg_defect_rate
    FROM quality_incidents
    GROUP BY supplier_id
    """

    quality_df = pd.read_sql(quality_query, engine)

    # On-time delivery (actual lead time vs supplier's published lead time)
    otd_query = """
    SELECT 
        po.supplier_id,
        (SUM(CASE WHEN DATEDIFF(po.delivery_date, po.order_date) <= s.lead_time_days THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as on_time_delivery_pct
    FROM purchase_orders po
    JOIN suppliers s ON po.supplier_id = s.supplier_id
    WHERE po.delivery_date IS NOT NULL AND po.order_date IS NOT NULL
    GROUP BY po.supplier_id
    """

    otd_df = pd.read_sql(otd_query, engine)

    # Cost variance
    cost_query = """
    SELECT 
        po.supplier_id,
        (STDDEV(poi.unit_price) / AVG(poi.unit_price) * 100) as cost_variance_pct
    FROM purchase_orders po
    JOIN purchase_order_items poi ON po.po_id = poi.po_id
    GROUP BY po.supplier_id
    """

    cost_df = pd.read_sql(cost_query, engine)

    # FX exposure
    fx_query = """
    SELECT 
        po.supplier_id,
        (SUM(CASE WHEN cur.currency_code != 'USD' THEN poi.quantity * poi.unit_price ELSE 0 END) * 100.0 / 
         NULLIF(SUM(poi.quantity * poi.unit_price), 0)) as fx_exposure_pct
    FROM purchase_orders po
    JOIN purchase_order_items poi ON po.po_id = poi.po_id
    JOIN currencies cur ON po.currency_id = cur.currency_id
    GROUP BY po.supplier_id
    """

    fx_df = pd.read_sql(fx_query, engine)

    geo_query = """
    SELECT supplier_id, COALESCE(risk_index, 0) AS geographic_risk_index
    FROM suppliers
    """
    geo_df = pd.read_sql(geo_query, engine)

    # Merge all metrics
    df = lead_df.merge(quality_df, on='supplier_id', how='left')
    df = df.merge(otd_df, on='supplier_id', how='left')
    df = df.merge(cost_df, on='supplier_id', how='left')
    df = df.merge(fx_df, on='supplier_id', how='left')
    df = df.merge(geo_df, on='supplier_id', how='left')

    # Fill nulls with defaults
    df['avg_defect_rate'] = df['avg_defect_rate'].fillna(0)
    df['on_time_delivery_pct'] = df['on_time_delivery_pct'].fillna(100)
    df['cost_variance_pct'] = df['cost_variance_pct'].fillna(0)
    df['fx_exposure_pct'] = df['fx_exposure_pct'].fillna(0)
    df['lead_time_stddev'] = df['lead_time_stddev'].fillna(0)
    df['geographic_risk_index'] = df['geographic_risk_index'].fillna(0)

    # Normalize metrics for risk scoring
    df['norm_lead'] = (
        (df['avg_lead_time'] - df['avg_lead_time'].min()) /
        (df['avg_lead_time'].max() - df['avg_lead_time'].min() + 0.001)
    )

    df['norm_defect'] = df['avg_defect_rate'] / 100
    df['norm_otd'] = 1 - (df['on_time_delivery_pct'] / 100)
    df['norm_variance'] = df['cost_variance_pct'] / 100
    df['norm_fx'] = df['fx_exposure_pct'] / 100
    df['norm_geo'] = df['geographic_risk_index'] / 100

    # Composite risk score (weighted)
    df['composite_risk_score'] = (
        0.22 * df['norm_otd'] +       # On-time delivery
        0.20 * df['norm_defect'] +    # Quality defect rate
        0.18 * df['norm_variance'] +  # Cost variance
        0.18 * df['norm_fx'] +        # FX sensitivity
        0.12 * df['norm_lead'] +      # Lead time consistency
        0.10 * df['norm_geo']         # Geographic risk index
    ) * 100

    # Add timestamp
    df['last_updated'] = datetime.now()

    # Select columns matching schema
    final_df = df[[
        'supplier_id', 
        'avg_lead_time', 
        'lead_time_stddev',
        'avg_defect_rate', 
        'cost_variance_pct', 
        'on_time_delivery_pct',
        'fx_exposure_pct', 
        'composite_risk_score',
        'last_updated'
    ]]

    # Write to database (replace existing)
    final_df.to_sql(
        "supplier_performance_metrics",
        engine,
        if_exists="replace",
        index=False
    )

    print(f"✓ Updated {len(final_df)} supplier risk profiles")
    print(f"\nRisk Score Summary:")
    print(final_df[['supplier_id', 'composite_risk_score', 'avg_defect_rate', 'on_time_delivery_pct']].to_string(index=False))


# =========================
# MAIN PIPELINE
# =========================

if __name__ == "__main__":
    print("="*60)
    print("Advanced Analytics: FX Simulation & Supplier Risk")
    print("="*60)
    
    try:
        # Run FX Monte Carlo simulation (NGN = currency_id 3)
        run_fx_simulation(currency_id=3, days=90, simulations=10000)
        
        # Calculate supplier risk metrics
        run_supplier_risk()
        
        print("\n" + "="*60)
        print("✓ Analytics pipeline completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Analytics pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()
