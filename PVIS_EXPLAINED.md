# PVIS Explained: A Plain-English Guide to the Procurement Volatility Intelligence System

## What Is This Thing?

Imagine you run a factory. Every month, you buy raw materials from 8 different suppliers scattered across Nigeria, China, the UK, Europe, and the US. You place roughly 800 purchase orders per year. Some are paid in US dollars, some in euros, some in Nigerian naira.

Now here is the problem: you have no idea what any of this is really costing you in real terms. Not because you lack data, but because that data lives in spreadsheets, ERP export files, and tribal knowledge in the heads of your procurement managers.

PVIS (Procurement Volatility Intelligence System) is the tool that takes all of that raw information and turns it into a live dashboard that tells you exactly what is happening, why your costs are drifting, which suppliers are putting your production at risk, and what you should do about it. Right now, today, before the next board meeting.

---

## The Three Problems That Kill Manufacturing Companies Quietly

### Problem 1: Currency Movement Silently Erodes Your Margins

A manufacturing company that buys materials with foreign currency (say, naira, euros, or yuan) is constantly exposed to exchange rate risk. When the Nigerian naira weakens against the US dollar, the same shipment of raw materials that cost you $100,000 last quarter might effectively cost you $118,000 this quarter. No price change from your supplier, no renegotiation, no warning. The money just disappears.

Most procurement teams do not model this risk at all. They check the current rate, maybe glance at last month, and make a gut call. That is not analysis, that is guesswork with nicer spreadsheets.

**What PVIS does about it:** PVIS pulls the live exchange rate from the internet every time you open the dashboard. Then it runs 10,000 simulations of what that rate might do over the next 30 to 1,095 days, using a technique called Monte Carlo simulation. It asks: if the naira has behaved in a certain way for the past three years, what is the realistic range of outcomes for the next 90 days? The system shows you a worst-case band (the P5 line), a most-likely outcome (the P50 median), and a best-case band (the P95 line). You can see at a glance whether your next quarter looks expensive or manageable, and you get a number: "Under worst conditions, your FX exposure will cost you an extra $X."

### Problem 2: You Do Not Actually Know Which Suppliers Are Dangerous

Every company has that one supplier they have used forever. They feel reliable because nothing catastrophic has happened yet. But "nothing catastrophic yet" is not the same as "low risk."

A supplier might look fine on the surface while quietly exhibiting warning signs: delivery times that are slowly creeping longer, defect rates that tick up slightly each quarter, pricing that varies wildly depending on who is negotiating. Any one of those trends can stop your production line. The combination of them is especially dangerous.

**What PVIS does about it:** PVIS calculates a composite risk score for every supplier. It looks at six factors and puts a number between 0 and 100 on each supplier:

1. **On-time delivery rate** - What percentage of orders actually arrived when the supplier said they would?
2. **Defect rate** - How many quality incidents did this supplier cause?
3. **Cost variance** - Does this supplier's pricing stay consistent, or does it jump around?
4. **FX exposure** - What fraction of your spend with this supplier is in a foreign currency?
5. **Lead time consistency** - Even if they are mostly on time, do their delivery times vary wildly?
6. **Geographic risk index** - Is this supplier located in a country with political instability, infrastructure problems, or supply chain disruptions?

These six numbers are combined using a weighted formula. On-time delivery gets the most weight (22%) because a supplier who cannot deliver on schedule is the single fastest way to stop your factory. Defects get the second-most weight (20%) because quality failures are expensive to detect and fix. The result is a single score per supplier. Higher means more dangerous.

The system then ranks all your suppliers and generates a negotiation playbook for each high-risk one. Not just a score, but actual recommended actions: "This supplier's cost variance is in the top 30% of your panel. Recommend renegotiating fixed-price terms."

### Problem 3: Money Is Leaking Out of Your Procurement Budget and Nobody Notices

Every material you buy has a standard cost: the agreed-upon or budgeted price per unit. In a well-run procurement operation, what you actually pay should match the standard cost closely. When it does not, that gap is called cost leakage, and it adds up fast across 1,952 line items and 778 purchase orders.

The problem is that nobody is sitting down every month to compare every unit price on every PO against the standard cost catalog. That is hundreds of rows to check manually.

**What PVIS does about it:** PVIS calculates cost leakage automatically. For every purchase order line item, it checks: did we pay more than standard cost? By how much? Multiplied by how many units? It adds up all instances where actual price exceeded standard cost, groups them by material category, and shows you a waterfall chart of where your money is leaking. You can see at a glance that, for example, steel components cost you $47,000 more than standard last year because three suppliers raised prices mid-contract and nobody flagged it.

---

## How the Whole System Works (Step by Step)

### Step 1: Data Goes In

The system works with three types of data. The first is your own procurement records: suppliers, materials, purchase orders, and line items. You upload these as spreadsheet files using a drag-and-drop uploader in the dashboard, or you connect it directly to your database.

The second type is quality incident records: every time a delivery arrived with defects, that gets logged. The system uses this to calculate defect rates per supplier.

The third type is exchange rate data. PVIS fetches live rates from a public financial API every time the dashboard loads. For historical rates going back three years, it either builds them from the API or uses a realistic synthetic backcast if the API has limits. This means the currency analysis is always based on how the market has actually behaved recently, not on five-year-old assumptions.

### Step 2: The Database Organizes Everything

All of this data is stored in a structured MySQL database with 19 tables. Think of it like a very well-organized filing system. There is a table for suppliers, a table for materials, a table for purchase orders, a table for the individual line items within each order, a table for daily exchange rates, a table for quality incidents, and so on.

The relationships between tables are carefully designed. A purchase order links to a supplier, to a currency, and to individual line items, and each line item links to a material. This means the system can always answer questions like: "For all orders from Nigerian suppliers denominated in naira, what was the average defect rate last year?"

### Step 3: The Warehouse Transforms Raw Data Into Analysis-Ready Form

Raw transactional data is great for recording what happened. It is not ideal for analytics. To make analysis fast and reliable, PVIS runs an ETL (Extract, Transform, Load) pipeline that takes the raw data and reorganizes it into a star-schema data warehouse. Think of this as creating pre-prepared summaries that can be read instantly.

The warehouse has:
- A dimension table for dates (every date from 2023 to 2026, with fields for month, quarter, year, and day of week)
- A dimension table for suppliers (with their country and surrogate keys)
- A dimension table for materials (with category and cost)
- A central fact table that joins all of these together at the level of individual purchase order line items, converted to USD using the closest matching exchange rate

On top of that, pre-aggregated summary tables live in the warehouse: supplier spend totals by year, supplier risk scores, and financial KPIs.

### Step 4: The Analytics Engine Does the Math

This is where the intelligence lives. Two main calculations run here.

**The Monte Carlo FX Simulation:** The engine takes three years of daily exchange rates for a currency (say, NGN/USD) and calculates the daily percentage change (called the log return) for each day. It then checks: are there periods where the currency was relatively calm, and other periods where it was moving wildly? This is called regime detection, and it is a more sophisticated approach than assuming the currency always behaves the same way.

With those patterns detected, it runs 10,000 separate simulations. Each simulation starts at today's rate and makes 90 daily decisions: is today a calm day or a volatile day? Based on that, it applies a random shock drawn from the appropriate statistical distribution. After 90 days of simulated shocks, you have one possible future for the exchange rate. Do this 10,000 times and you have a full picture of the space of possibilities. The middle 90% of all those outcomes is your confidence band.

**The Composite Risk Score:** The engine queries the database for lead times, defect rates, on-time delivery records, cost variance, FX exposure, and geographic risk for every supplier. It normalizes all of those to a common 0-to-1 scale (so that, for example, a 15-day average lead time and a 5% defect rate can be added together meaningfully). Then it applies the weighted formula and produces a score out of 100 for each supplier.

### Step 5: The Dashboard Makes Everything Visible and Actionable

The eight-page Streamlit dashboard is the final output. You do not need to be a data analyst to use it. Here is what each page does:

**Executive Summary:** One page with all the key numbers. Total spend this period, live exchange rate, average supplier risk score, how many days your working capital cycle takes, and a heatmap of supplier risk.

**FX Volatility and Monte Carlo:** Select a currency and a forecast horizon. Watch the simulation fan chart update in real time. See your worst-case scenario (P5), the median outcome (P50), and the optimistic outcome (P95).

**Supplier Risk Analysis:** A ranked table of all your suppliers with their risk scores, color-coded. Click into any supplier for a breakdown of which factors are driving their score.

**Spend and Cost Analysis:** Donut charts of spend by supplier and by material category. The cost leakage waterfall showing where money leaked relative to standard costs.

**Working Capital:** How many days of inventory are you holding (DIO)? How long before you pay your suppliers (DPO)? Subtract DPO from DIO and you get the Cash Conversion Cycle. This page models that and shows you what happens if you adjusted payment terms.

**Scenario Planning:** An interactive slider where you can ask "what happens to my total procurement costs if the naira weakens by 20%?" The system immediately recalculates landed costs for all affected suppliers and shows the dollar impact.

**Company Data Upload:** The page where you drag in your own CSV files. The system validates them, imports them, runs the whole pipeline, and refreshes the dashboard with your real data.

**Pipeline Runner:** A control panel for rerunning the data pipeline (seed data, ETL, FX simulation, risk scoring) directly from the browser, one click at a time.

---

## What Decisions Can You Make With PVIS?

This section is the most important one. Data is only valuable if it drives decisions.

### Decision 1: Which suppliers should you renegotiate contracts with, and on what terms?

The risk score ranking tells you directly. If Supplier A has a composite risk score of 78 out of 100, driven primarily by a 35% FX exposure and a cost variance in the top quartile, the negotiation playbook might say: "Consider fixed-price contracts for the next 6 months to eliminate cost variance. Explore USD-denominated invoicing to reduce FX exposure."

Without PVIS, this analysis would take a procurement analyst a week to assemble. With PVIS, it is on the screen when you walk into the meeting.

### Decision 2: Should you lock in a forward contract or hedge your FX exposure?

The Monte Carlo output gives you a quantified answer. If the P5 (worst case, 5th percentile) outcome for the naira says your costs will be $X million higher than today, and a forward contract costs $Y million to acquire, and X is significantly larger than Y, then hedging is justified. You now have the numbers to take that decision to a CFO without hand-waving.

### Decision 3: Which material categories are bleeding money versus standard cost?

The cost leakage analysis answers this. If the waterfall shows that packaging materials are leaking $22,000 per quarter while electronics and metals are within tolerance, you know where to focus the audit. That is a procurement category manager conversation, not a blind search.

### Decision 4: How much cash is tied up unnecessarily in your supply chain?

The CCC (Cash Conversion Cycle) analysis on the Working Capital page answers this. If your DIO is 45 days (you hold 45 days of inventory on average) and your DPO is 32 days (you pay suppliers in 32 days on average), then your CCC is 13 days. The scenario tool lets you ask: if we extend supplier payment terms from 32 to 45 days, how much working capital is freed up? This is a direct input into treasury management.

### Decision 5: Which markets or geographies carry too much supply chain concentration risk?

The geographic risk index in the supplier risk score, combined with the supplier country exposure map, shows you how concentrated your sourcing is. If five of your eight suppliers are in one region and that region has an elevated risk index, you can see the aggregate exposure and make a supply base diversification plan.

---

## The Logic Behind the Key Calculations, In Plain English

### Why Monte Carlo and not just an average forecast?

Because a single average forecast is almost always wrong, and being wrong in one direction is very different from being wrong in the other. If you just say "the naira has averaged 0.1% depreciation per day, so in 90 days it will be X," you have no idea how confident to be in that number, and you have no sense of tail risk.

Monte Carlo gives you a distribution of outcomes. You can say: "There is a 5% chance the naira weakens by more than 18%. If that happens, here is the dollar impact." That is a sentence you can act on. An average cannot tell you that.

### Why regime detection instead of a single drift-and-volatility estimate?

Currency markets change character. The naira in a stable period behaves differently from the naira during an import restriction policy change or an oil price shock. If you estimate a single volatility number, you are averaging the calm periods and the crisis periods together, which gives you a number that describes neither accurately.

By detecting two regimes (low volatility and high volatility) and estimating separate drift and sigma values for each, the simulation is much more realistic. It knows that on most days the rate moves gently, but on a fraction of days it moves sharply, and it simulates that asymmetry correctly.

### Why are on-time delivery and defect rate weighted more heavily in the risk score?

Because the consequences of those failures are immediate and production-stopping. If a supplier delivers 10 days late, your factory may idle. If a shipment arrives with a 15% defect rate, you have a line stoppage and a quality investigation. These are direct, hard costs. Geographic risk, by contrast, is a background probability. It matters but it rarely materializes immediately, which is why it gets a lower weight (10%).

### Why a star schema for the data warehouse?

Because analytical queries run dramatically faster against a star schema than against the raw normalized transactional tables. When you want to answer "what was total spend in USD for Nigerian suppliers in Q4 2024?", a star schema can answer that with a single join between `dim_supplier` and `fact_procurement`, filtered by `dim_date`. On the raw 19-table transactional schema, the same query would require multiple joins across orders, line items, currencies, suppliers, and exchange rates. The warehouse pre-computes those joins.

### Why does the cost leakage calculation matter at scale?

At 1,952 line items across 778 purchase orders, small unit-price deviations from standard cost accumulate silently. A 3% overpayment on a $500,000 line of raw materials is $15,000 you never intended to spend. Multiply that across dozens of categories and several years, and cost leakage can easily represent 2 to 5% of total procurement spend. PVIS finds this automatically so that manual review can focus on the biggest deviations rather than searching through every row.

---

## The Technology, In Everyday Terms

| Component | What It Is in Plain English |
| :--- | :--- |
| **MySQL 8.0** | The filing cabinet. All data lives here in structured tables. |
| **Python** | The language everything is written in. It reads data, does calculations, and runs the dashboard. |
| **SQLAlchemy** | The translator between Python code and the database. It turns Python commands into SQL queries safely. |
| **pandas** | A Python library for working with table-shaped data, like an extremely capable spreadsheet that runs in code. |
| **NumPy** | A Python library for fast numerical calculations. The Monte Carlo simulation uses this to generate 10,000 random paths efficiently. |
| **Streamlit** | The framework that turns Python code into an interactive web dashboard without needing frontend development skills. |
| **Plotly** | The charting library. Makes the interactive fan charts, donut charts, heatmaps, and waterfall plots. |
| **Docker** | A standardized box that packages the whole application so it runs identically on any computer. |
| **GitHub Actions** | Runs automated tests every time code is changed, to catch bugs immediately. |

---

## Summary: What PVIS Is, In One Paragraph

PVIS is a procurement intelligence platform for manufacturing companies that buy materials across multiple currencies and multiple suppliers. It takes raw procurement records, connects to live exchange rate feeds, and produces a real-time dashboard that answers three questions that otherwise take analysts weeks to answer: how much is currency volatility going to cost us, which suppliers are genuinely risky, and where is money leaking against our standard costs. Every number is backed by a specific calculation with a documented formula, and every insight links directly to a decision: renegotiate this contract, hedge this exposure, audit this category, diversify this supply source.
