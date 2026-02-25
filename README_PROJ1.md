<p align="center">
  <img src="https://img.icons8.com/fluency/96/prototype.png" alt="Prototype" width="72"/>
</p>

<h1 align="center">Procurement Intelligence Engine: Prototype</h1>

<p align="center">
  <em>Rapid prototyping repository for <a href="https://github.com/DavidMaco/pvis"><strong>PVIS</strong></a> (Procurement Volatility Intelligence System)</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-prototype-orange" alt="Status: Prototype">
  <img src="https://img.shields.io/badge/python-3.13%2B-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white" alt="MySQL">
  <a href="https://github.com/DavidMaco/pvis"><img src="https://img.shields.io/badge/Production_Repo-PVIS-1d4f91?logo=github" alt="Production Repo"></a>
</p>

---

## ⚠️ This Is the Prototype

This repository served as the **initial proof-of-concept** for the PVIS project. It was used to:

- Validate the core architecture (MySQL → SQLAlchemy → Streamlit)
- Prototype the Monte Carlo FX simulation engine
- Test supplier risk scoring algorithms
- Iterate on the star-schema data warehouse design
- Prove the external data import pipeline concept

**For the production-ready system with all features, go to → [DavidMaco/pvis](https://github.com/DavidMaco/pvis)**

---

## 🔀 Prototype → Production

| Aspect | This Prototype | [PVIS (Production)](https://github.com/DavidMaco/pvis) |
|:-------|:---------------|:-------|
| **Status** | Archived for reference only | Active development |
| **Dashboard** | 7 pages | 8 pages (+ Company Data Upload) |
| **Demo Mode** | Not available | Full synthetic data fallback |
| **Cloud Deploy** | Not supported | Streamlit Cloud + Aiven MySQL |
| **Data Import** | CLI only | CLI + interactive file upload |
| **FX Horizon** | 90 days | Up to 1,095 days (3 years) |
| **Documentation** | Basic | Production-grade README + guides |
| **Live Demo** | Not available | [▶ Launch Dashboard](https://davidmaco-pvis.streamlit.app) |

---

## 📐 What Was Prototyped Here

### Phase 1: Data Foundation
- MySQL schema design (19 tables: transactional + warehouse)
- Realistic 3-year data generator with live FX rate integration
- Star-schema ETL pipeline (dim_date, dim_supplier, dim_material → fact_procurement)

### Phase 2: Analytics Engine
- Monte Carlo FX simulation (Geometric Brownian Motion, 10K paths)
- Composite supplier risk scoring (5 weighted factors)
- Cash Conversion Cycle computation (DIO, DPO, CCC)

### Phase 3: Dashboard
- 7-page Streamlit executive dashboard with Plotly visualizations
- Live FX rate integration (dual-API failover)
- Interactive scenario planning and stress testing

### Phase 4: Data Import
- CSV-based external data loader with schema validation
- Template files for suppliers, materials, purchase orders, PO items

### Phase 5: Deployment
- Docker + docker-compose containerization
- GitHub Actions CI pipeline
- Windows PowerShell launcher script

---

## 🏃 Quick Run (For Reference)

```powershell
git clone https://github.com/DavidMaco/Procurement_Intelligence_Proj1.git
cd Procurement_Intelligence_Proj1
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Configure DB
Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml

# Seed → ETL → Analytics → Dashboard
python data_ingestion\seed_realistic_data.py
python data_ingestion\populate_warehouse.py
python analytics\advanced_analytics.py
.\RUN_STREAMLIT.ps1
```

---

## 📁 Structure

```
├── streamlit_app.py              # 7-page dashboard (prototype)
├── demo_data.py                  # Demo mode synthetic data
├── config.py                     # DB connection
├── analytics/
│   └── advanced_analytics.py     # Monte Carlo + risk scoring
├── data_ingestion/
│   ├── seed_realistic_data.py    # Data generator
│   ├── external_data_loader.py   # CSV import
│   └── populate_warehouse.py     # Star-schema ETL
├── external_data_samples/        # Template CSVs
├── tests/                        # pytest suite
└── requirements.txt              # Dependencies
```

---

## ➡️ Go to Production

**All future development happens in the PVIS repository:**

<p align="center">
  <a href="https://github.com/DavidMaco/pvis">
    <img src="https://img.shields.io/badge/▶_PVIS_Production_Repo-1d4f91?style=for-the-badge&logo=github&logoColor=white" alt="PVIS Repo">
  </a>
</p>

---

<p align="center">
  <sub>Prototype by <a href="https://github.com/DavidMaco">David Maco</a></sub>
</p>
