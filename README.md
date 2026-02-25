<p align="center">
  <img src="https://img.icons8.com/fluency/128/combo-chart.png" alt="PVIS Logo" width="96"/>
</p>

<h1 align="center">PVIS: Procurement Volatility Intelligence System</h1>

<p align="center">
  <strong>A procurement analytics platform that combines Monte Carlo simulation, real-time FX monitoring, composite supplier risk scoring, and working capital optimization in a single executive dashboard.</strong>
</p>

<p align="center">
  <a href="https://github.com/DavidMaco/pvis/actions"><img src="https://github.com/DavidMaco/pvis/actions/workflows/python-app.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/python-3.13%2B-blue?logo=python&logoColor=white" alt="Python 3.13+">
  <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white" alt="MySQL 8.0">
  <img src="https://img.shields.io/badge/Streamlit-1.54-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <a href="https://davidmaco-pvis.streamlit.app"><img src="https://img.shields.io/badge/Live_Demo-Streamlit_Cloud-FF4B4B?logo=streamlit&logoColor=white" alt="Live Demo"></a>
</p>

<p align="center">
  <a href="#-live-demo">Live Demo</a> •
  <a href="#-key-features">Features</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-getting-started">Getting Started</a> •
  <a href="#-dashboard-pages">Dashboard</a> •
  <a href="#-import-your-company-data">Your Data</a> •
  <a href="#-deployment">Deploy</a> •
  <a href="#-data-model">Data Model</a> •
  <a href="#-contributing">Contributing</a>
</p>

---

## 🎯 Live Demo

> **[▶ Launch PVIS Dashboard](https://davidmaco-pvis.streamlit.app)**
>
> The live demo runs on Streamlit Cloud with Aiven MySQL. All 8 pages are fully interactive. Explore FX simulations, supplier risk heatmaps, spend analysis, and more.

---

## 🧠 What Problem Does PVIS Solve?

Manufacturing procurement teams face three critical blind spots:

| Blind Spot | Business Impact | PVIS Solution |
|:---|:---|:---|
| **FX Volatility** | A 15% NGN devaluation can wipe out ₦180M+ in margin on a single quarter | Monte Carlo simulation (10K-50K paths) with live API rates, P5/P50/P95 forecast bands |
| **Supplier Risk** | Late deliveries and defects cascade into production stoppages | Composite risk scoring (5 weighted factors) with automated negotiation playbooks |
| **Cash Leakage** | Cost variances against standard costs go undetected across 1,000+ PO lines | Spend decomposition by supplier × category × year with leakage attribution |

PVIS turns raw procurement data into **actionable intelligence**. It provides specific recommendations on which contracts to renegotiate, where to hedge FX exposure, and how to optimize the cash conversion cycle.

---

## ✨ Key Features

### Analytics Engine
- **Monte Carlo FX Simulation:** Geometric Brownian Motion with 10K-50K paths over up to 1,095 trading days (3 years), seeded from live exchange rates
- **Composite Supplier Risk Scoring:** Weighted model: 30% lead time volatility + 35% defect rate + 25% on-time delivery + 10% FX exposure
- **Cash Conversion Cycle Optimization:** DIO/DPO modeling with target scenario recommendations
- **Cost Leakage Detection:** Automated identification of unit-price vs. standard-cost variances by category
- **FX Stress Testing:** Interactive scenario planner for landed-cost impact across -30% to +50% shock spectrum

### Data Platform
- **Live Exchange Rates:** Dual-API failover (open.er-api.com to frankfurter.dev), 150+ currencies including NGN
- **Star-Schema Data Warehouse:** Dimensional model (3 dimensions, 1 fact table) with ETL pipeline
- **3-Year Historical Backcast:** Realistic procurement data generator with configurable parameters
- **External Data Import:** CSV-based ingestion with validation for company data (suppliers, materials, POs)
- **Company Data Upload:** Interactive file uploader in the dashboard to run simulations on your own data

### Dashboard
- **8 Interactive Pages:** Executive Summary, FX Volatility & Monte Carlo, Supplier Risk Analysis, Spend & Cost Analysis, Working Capital, Scenario Planning, Company Data Upload, Pipeline Runner
- **Real-Time KPIs:** Live USD/NGN rate, total spend, FX exposure %, average risk score, CCC days
- **Auto-Negotiation Playbooks:** Per-supplier action items generated from risk metrics
- **Demo Mode:** Full dashboard functionality with synthetic data when no database is connected

---

## 🏗 Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           DATA SOURCES                                       │
│                                                                              │
│   📡 Live FX APIs              📁 Company CSV Upload        🏭 Seed Generator│
│   (open.er-api.com)            (st.file_uploader)           (synthetic 3yr)  │
│   (frankfurter.dev)                                                          │
└─────────┬──────────────────────────┬──────────────────────────┬──────────────┘
          │                          │                          │
          ▼                          ▼                          ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        INGESTION LAYER                                       │
│                                                                              │
│   external_data_loader.py    ◄── CSV validation + schema enforcement         │
│   seed_realistic_data.py     ◄── 3-year realistic data with live FX          │
│   rebuild_fx_historical.py   ◄── FX backfill from APIs                       │
│                                                                              │
│                  MySQL 8.0 with 19 transactional tables                      │
└─────────────────────────────────┬────────────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        WAREHOUSE LAYER                                       │
│                                                                              │
│   populate_warehouse.py      ◄── Star-schema ETL                             │
│                                                                              │
│   ┌──────────┐  ┌──────────────┐  ┌──────────────┐                          │
│   │ dim_date  │  │ dim_supplier │  │ dim_material │                          │
│   └─────┬────┘  └──────┬───────┘  └──────┬───────┘                          │
│         └──────────────┼──────────────────┘                                  │
│                        ▼                                                     │
│              ┌──────────────────┐                                            │
│              │ fact_procurement │  + supplier_spend_summary                   │
│              └──────────────────┘  + supplier_performance_metrics             │
│                                    + financial_kpis                           │
└─────────────────────────────────┬────────────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                       ANALYTICS ENGINE                                       │
│                                                                              │
│   advanced_analytics.py                                                      │
│   ├── Monte Carlo FX Simulation  (GBM, configurable paths & horizon)         │
│   ├── Composite Supplier Risk    (5-factor weighted scoring model)            │
│   ├── Spend Aggregation          (supplier × category × year)                │
│   └── Working Capital KPIs       (DIO, DPO, CCC optimization)               │
└─────────────────────────────────┬────────────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                       PRESENTATION LAYER                                     │
│                                                                              │
│   streamlit_app.py: 8-page executive dashboard                               │
│                                                                              │
│   🏠 Executive Summary    📈 FX Monte Carlo      🏭 Supplier Risk            │
│   💰 Spend Analysis       🏦 Working Capital      🔄 Scenario Planning       │
│   📂 Company Data Upload  ⚙️ Pipeline Runner                                 │
│                                                                              │
│   Plotly charts • Live KPIs • Interactive sliders • File upload              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|:------|:-----------|:--------|
| **Database** | MySQL 8.0 | 19-table transactional store + star-schema warehouse |
| **Cloud DB** | Aiven MySQL | Streamlit Cloud connectivity (free tier) |
| **ORM** | SQLAlchemy + PyMySQL | Connection pooling, parameterized queries |
| **Processing** | pandas · NumPy | DataFrame operations, statistical computation |
| **Simulation** | NumPy (GBM) | Geometric Brownian Motion Monte Carlo engine |
| **FX Data** | open.er-api.com · frankfurter.dev | Live rates for 150+ currencies, dual-API failover |
| **Dashboard** | Streamlit 1.54 + Plotly | Interactive visualizations, file upload, 8-page app |
| **CI/CD** | GitHub Actions | Automated testing on push/PR |
| **Containerization** | Docker + docker-compose | One-command full-stack deployment |
| **Language** | Python 3.13+ | Type hints, modern stdlib (tomllib, pathlib) |

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Version | Check |
|:---|:---|:---|
| Python | 3.13+ | `python --version` |
| MySQL | 8.0+ | `mysql --version` |
| Git | Any | `git --version` |

### One-Command Setup (Windows/PowerShell)

```powershell
# Clone
git clone https://github.com/DavidMaco/pvis.git
cd pvis

# Environment
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Configure database credentials
Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml
# Edit .streamlit\secrets.toml with your MySQL credentials

# Seed data → ETL → Analytics (one pipeline)
python data_ingestion\seed_realistic_data.py
python data_ingestion\populate_warehouse.py
python analytics\advanced_analytics.py

# Launch
.\RUN_STREAMLIT.ps1
```

> **No MySQL?** The dashboard detects the absence of a database and runs in **Demo Mode** with synthetic data.

### macOS / Linux

```bash
git clone https://github.com/DavidMaco/pvis.git && cd pvis
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml, then:
python data_ingestion/seed_realistic_data.py
python data_ingestion/populate_warehouse.py
python analytics/advanced_analytics.py
streamlit run streamlit_app.py
```

### Run Tests

```powershell
pip install pytest
python -m pytest tests/ -v
```

---

## 📊 Dashboard Pages

### 1. 🏠 Executive Summary
Real-time KPI cards (total spend, FX exposure %, avg risk score, CCC days, live USD/NGN rate) with supplier risk ranking bar chart and monthly procurement trend area chart.

### 2. 📈 FX Volatility & Monte Carlo
Select any currency, configure horizon (30-1,095 days) and simulations (1K-50K paths). Renders historical rate chart with live rate marker, P5/P50/P95 forecast fan chart, and terminal rate distribution histogram.

### 3. 🏭 Supplier Risk Analysis
Normalized risk heatmap across 7 metrics, detailed performance table with conditional formatting, and lead-time volatility dual-axis chart.

### 4. 💰 Spend & Cost Analysis
Spend donut charts by supplier and category, cost leakage waterfall by material category, annual spend grouped bar chart with year-over-year comparison.

### 5. 🏦 Working Capital
Inventory value trend, payables/receivables dual timeline, CCC breakdown (DIO/DPO) with optimization targets and projected savings.

### 6. 🔄 Scenario Planning
Interactive FX stress test slider (-30% to +50%), multi-scenario comparison table, and per-supplier negotiation action playbooks.

### 7. 📂 Company Data Upload
Drag-and-drop file uploader for company CSV or ZIP data. It validates, processes, and runs the full analytics pipeline on your own procurement data from the browser.

### 8. ⚙️ Pipeline Runner
One-click buttons to regenerate seed data, run ETL, execute Monte Carlo simulation, and refresh supplier risk scores. Includes database health check with row counts for all 11 key tables.

---

## 📂 Import Your Company Data

PVIS supports two methods for using your own procurement data:

### Method A: Dashboard Upload (Recommended)
Navigate to the **📂 Company Data Upload** page in the dashboard and drag-and-drop your CSV files or a ZIP archive. The system validates, imports, runs ETL + analytics, and refreshes all dashboard pages automatically.

### Method B: Command-Line Import
```powershell
# Prepare CSVs (use external_data_samples/ as templates)
mkdir .\company_data

# Import → ETL → Analytics
python data_ingestion\external_data_loader.py --input-dir .\company_data
python data_ingestion\populate_warehouse.py
python analytics\advanced_analytics.py
```

### Required CSV Files

| File | Key Columns | Description |
|:-----|:------------|:------------|
| `suppliers.csv` | supplier_name, country, lead_time, defect_rate | Supplier master data |
| `materials.csv` | material_name, category, standard_cost | Material catalog |
| `purchase_orders.csv` | po_date, supplier, total_amount, currency | PO headers |
| `purchase_order_items.csv` | po_id, material, quantity, unit_price | PO line items |
| `fx_rates.csv` *(optional)* | rate_date, currency_code, rate_to_usd | Auto-generated if omitted |

See [EXTERNAL_DATA_GUIDE.md](EXTERNAL_DATA_GUIDE.md) and `external_data_samples/` for complete specs and templates.

---

## 🐳 Deployment

### Docker (One Command)

```powershell
docker-compose up --build
# Dashboard → http://localhost:8501
# MySQL → localhost:3306
```

### Streamlit Cloud

1. Fork/push to GitHub
2. Connect at [share.streamlit.io](https://share.streamlit.io)
3. Set **Secrets** (Settings → Secrets):
   ```toml
   [database]
   host = "your-cloud-mysql-host"
   port = 3306
   user = "your_user"
   password = "your_password"
   name = "your_database"
   ```
4. Deploy, or skip secrets to run in Demo Mode

---

## 🗄 Data Model

### Transactional Layer (19 Tables)

```
countries ─┐
            ├── suppliers ──── purchase_orders ──── purchase_order_items
currencies ─┘                        │
                                     ├── fx_rates
                                     ├── quality_incidents
materials ───────────────────────────┘
                              
inventory_snapshots    payables_summary    receivables_summary
```

### Warehouse Layer (Star Schema)

```
           dim_date
              │
dim_supplier ─┼── fact_procurement
              │
         dim_material

+ supplier_spend_summary
+ supplier_performance_metrics
+ financial_kpis
+ fx_simulation_results
```

### Key Metrics

| Metric | Formula / Method |
|:-------|:-----------------|
| **Composite Risk Score** | 0.30 × lead_time_vol + 0.35 × defect_rate + 0.25 × (1 − OTD%) + 0.10 × fx_exposure |
| **Monte Carlo FX** | GBM: S(t+1) = S(t) × exp((μ − σ²/2)Δt + σ√Δt × Z), Z ~ N(0,1) |
| **Cash Conversion Cycle** | CCC = DIO − DPO (days inventory outstanding − days payable outstanding) |
| **On-Time Delivery** | `COUNT(actual_lead ≤ published_lead) / COUNT(*)` |
| **Cost Leakage** | `Σ (unit_price − standard_cost) × quantity` where unit_price > standard_cost |

---

## 📁 Repository Structure

```
pvis/
├── streamlit_app.py                  # 8-page Streamlit executive dashboard
├── demo_data.py                      # Synthetic data engine for demo mode
├── config.py                         # DB connection (secrets / env fallback)
├── RUN_STREAMLIT.ps1                 # Windows quick-launcher script
├── requirements.txt                  # Python dependencies (pinned)
├── Dockerfile                        # Streamlit container image
├── docker-compose.yml                # Full stack (app + MySQL)
│
├── analytics/
│   └── advanced_analytics.py         # Monte Carlo FX + supplier risk scoring
│
├── data_ingestion/
│   ├── seed_realistic_data.py        # 3-year data generator (live FX rates)
│   ├── external_data_loader.py       # CSV import with validation
│   ├── populate_warehouse.py         # Star-schema ETL pipeline
│   └── rebuild_fx_historical.py      # FX backfill utility
│
├── external_data_samples/            # Template CSVs for external import
│   ├── suppliers.csv
│   ├── materials.csv
│   ├── purchase_orders.csv
│   └── purchase_order_items.csv
│
├── database/
│   └── add_constraints_migration.sql # FK/CHECK constraints + indexes
│
├── tests/                            # pytest suite
│
├── .streamlit/
│   ├── config.toml                   # Theme & server settings
│   └── secrets.toml.example          # Credentials template
│
├── .github/workflows/
│   └── python-app.yml                # CI pipeline
│
├── EXTERNAL_DATA_GUIDE.md            # CSV import specifications
├── WINDOWS_SETUP_GUIDE.md            # Windows/PowerShell guide
├── FX_DATA_INTEGRITY.md              # FX data rebuild documentation
└── PROJECT_WALKTHROUGH.md            # Technical walkthrough
```

---

## 🔮 Roadmap

- [ ] Anomaly detection on supplier performance trends
- [ ] Multi-currency portfolio hedge optimizer
- [ ] Automated PDF report generation with executive summaries
- [ ] REST API layer for ERP integration (SAP, Oracle)
- [ ] Role-based access control (RBAC) for enterprise deployment
- [ ] Real-time alerting via Slack/Teams webhooks

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**David Maco**

- GitHub: [@DavidMaco](https://github.com/DavidMaco)

---

<p align="center">
  <sub>Built with ❤️ for procurement intelligence</sub>
</p>
