# PVIS Power BI Decision Layer

This folder contains the semantic SQL layer and report design spec for the PVIS executive dashboard.

## 1) Build semantic layer
Run [pvis_decision_layer.sql](pvis_decision_layer.sql) against the `pro_intel_2` database.

Views created:
- `v_pvis_procurement_volatility`
- `v_pvis_fx_exposure`
- `v_pvis_supplier_risk`
- `v_pvis_working_capital`
- `v_pvis_scenario_comparison`

## 2) Power BI model tables
Import all views above as DirectQuery or Import tables.

## 3) Executive view requirements mapping
- Procurement Cost Volatility Index: `v_pvis_procurement_volatility.procurement_cost_volatility_index`
- FX Exposure % of Spend: `v_pvis_fx_exposure.fx_exposure_pct_of_spend`
- Supplier Risk Heatmap: `v_pvis_supplier_risk`
- Working Capital Forecast: `v_pvis_working_capital` (`dio`, `dpo`, `dso`, `ccc`, `inventory_turnover`)
- Scenario Comparison (Base vs Stress): `v_pvis_scenario_comparison`

## 4) Recommended visuals
- KPI cards: volatility index, FX exposure %, latest CCC, inventory turnover
- Matrix heatmap: supplier vs risk factors
- Filled map: country + geographic risk index + spend exposure
- Column chart: scenario impact USD
- Line chart: monthly spend volatility trend

## 5) DAX starter measures
```DAX
Latest CCC = MAX(v_pvis_working_capital[ccc])

FX Exposure % = MAX(v_pvis_fx_exposure[fx_exposure_pct_of_spend])

Volatility Index % = MAX(v_pvis_procurement_volatility[procurement_cost_volatility_index])

Stress Impact USD =
CALCULATE(
    MAX(v_pvis_scenario_comparison[impact_usd]),
    v_pvis_scenario_comparison[scenario] = "Stress +20%"
)
```
