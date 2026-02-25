-- PVIS Power BI Decision Layer (MySQL)
-- Build semantic views for Executive dashboard KPIs and scenario comparison

USE pro_intel_2;

DROP VIEW IF EXISTS v_pvis_procurement_volatility;
CREATE VIEW v_pvis_procurement_volatility AS
SELECT
    month,
    spend_usd,
    STDDEV(spend_usd) OVER () AS monthly_spend_std,
    AVG(spend_usd) OVER () AS monthly_spend_avg,
    (STDDEV(spend_usd) OVER () / NULLIF(AVG(spend_usd) OVER (), 0)) * 100 AS procurement_cost_volatility_index
FROM (
    SELECT DATE_FORMAT(d.full_date, '%Y-%m') AS month, SUM(f.total_usd_value) AS spend_usd
    FROM fact_procurement f
    JOIN dim_date d ON f.date_key = d.date_key
    GROUP BY DATE_FORMAT(d.full_date, '%Y-%m')
) m;

DROP VIEW IF EXISTS v_pvis_fx_exposure;
CREATE VIEW v_pvis_fx_exposure AS
SELECT
    (SUM(CASE WHEN c.currency_code <> 'USD' THEN poi.quantity * poi.unit_price ELSE 0 END)
      / NULLIF(SUM(poi.quantity * poi.unit_price), 0)) * 100 AS fx_exposure_pct_of_spend,
    SUM((poi.quantity * poi.unit_price) / COALESCE(fx.rate_to_usd, 1)) AS baseline_spend_usd,
    SUM(CASE WHEN c.currency_code <> 'USD' THEN (poi.quantity * poi.unit_price) / COALESCE(fx.rate_to_usd, 1) ELSE 0 END) AS non_usd_spend_usd
FROM purchase_orders po
JOIN purchase_order_items poi ON poi.po_id = po.po_id
JOIN currencies c ON c.currency_id = po.currency_id
LEFT JOIN fx_rates fx ON po.currency_id = fx.currency_id
 AND fx.rate_date = (
    SELECT MAX(f2.rate_date)
    FROM fx_rates f2
    WHERE f2.currency_id = po.currency_id
      AND f2.rate_date <= po.order_date
 );

DROP VIEW IF EXISTS v_pvis_supplier_risk;
CREATE VIEW v_pvis_supplier_risk AS
SELECT
    s.supplier_name,
    co.country_name,
    spm.composite_risk_score,
    spm.on_time_delivery_pct,
    spm.avg_defect_rate,
    spm.cost_variance_pct,
    spm.fx_exposure_pct,
    s.risk_index AS geographic_risk_index
FROM supplier_performance_metrics spm
JOIN suppliers s ON s.supplier_id = spm.supplier_id
JOIN countries co ON co.country_id = s.country_id;

DROP VIEW IF EXISTS v_pvis_working_capital;
CREATE VIEW v_pvis_working_capital AS
SELECT
    k.kpi_date,
    k.dio,
    k.dpo,
    (k.ccc - k.dio + k.dpo) AS dso,
    k.ccc,
    (COALESCE(sp.total_spend, 0) / 3) / NULLIF(inv.avg_inventory, 0) AS inventory_turnover
FROM financial_kpis k
LEFT JOIN (
    SELECT SUM(total_usd_value) AS total_spend FROM fact_procurement
) sp ON 1 = 1
LEFT JOIN (
    SELECT AVG(inventory_value_usd) AS avg_inventory FROM inventory_snapshots
) inv ON 1 = 1;

DROP VIEW IF EXISTS v_pvis_scenario_comparison;
CREATE VIEW v_pvis_scenario_comparison AS
SELECT 'Base' AS scenario, 0 AS shock_pct,
       baseline_spend_usd AS stressed_spend_usd,
       0 AS impact_usd
FROM v_pvis_fx_exposure
UNION ALL
SELECT 'Stress +10%' AS scenario, 10 AS shock_pct,
       (baseline_spend_usd - non_usd_spend_usd) + non_usd_spend_usd * 1.10,
       ((baseline_spend_usd - non_usd_spend_usd) + non_usd_spend_usd * 1.10) - baseline_spend_usd
FROM v_pvis_fx_exposure
UNION ALL
SELECT 'Stress +20%' AS scenario, 20 AS shock_pct,
       (baseline_spend_usd - non_usd_spend_usd) + non_usd_spend_usd * 1.20,
       ((baseline_spend_usd - non_usd_spend_usd) + non_usd_spend_usd * 1.20) - baseline_spend_usd
FROM v_pvis_fx_exposure;
