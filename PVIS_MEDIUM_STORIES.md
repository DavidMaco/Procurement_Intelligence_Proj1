# PVIS Medium Stories

---

## Story 1: The Hidden Costs Destroying Manufacturing Procurement Margins (And How to Find Them)

*A plain-English explanation of the three invisible drains on procurement profitability, and the system built to expose all of them.*

---

Walk into any mid-size manufacturing company and ask the head of procurement: "Where is your biggest cost risk right now?" You will get an answer. It will be confident. And it will almost certainly be incomplete.

Not because they are not good at their job. Because the data is not organized in a way that makes the real answer visible.

This is the story of what those hidden costs actually are, why traditional tools miss them, and how a system called PVIS was built to find them automatically.

### The Spreadsheet Problem

Most procurement data lives in some combination of an ERP system, export spreadsheets, email threads, and institutional memory. Each of those sources captures a slice of the picture. None of them connect.

The ERP knows what you paid. The spreadsheet someone built three years ago tracks supplier performance. The email thread from last quarter is where someone flagged a defect issue with a Nigerian supplier. The institutional memory is in the head of a manager who has been there twelve years.

When someone asks "how much did currency movement cost us last year?", the honest answer in most organizations is: "We would need a few days to pull that together." And when it does get pulled together, it is a backward-looking number. It tells you what happened. It does not tell you what is about to happen.

PVIS was built to change that from reactive to real-time.

### Hidden Cost 1: Currency Volatility

If you manufacture in one country and source from another, you have FX exposure. Unless every contract is denominated in your home currency (and most are not), you are taking on exchange rate risk on every single purchase order.

For a company with significant NGN-denominated procurement spend, a 15% devaluation of the naira against the dollar is not a theoretical scenario. It is something that has happened, and the effect on procurement costs is immediate and precise. The unit price does not change. The currency rate changes. And the company pays more in real terms with no renegotiation, no warning, no escape valve.

The problem is that most procurement teams do not model this forward. They take the current rate, maybe anchor to a budget rate set at the beginning of the fiscal year, and absorb the variance when it appears. That variance shows up as an unexplained cost overrun in the monthly P&L. The root cause is obvious in hindsight but invisible in advance.

A sophisticated approach is to use simulation. Specifically, Monte Carlo simulation with regime detection, which we will explain in detail in a later story. The key insight is that instead of asking "what rate will we get in 90 days?", you ask "what is the full distribution of possible rates in 90 days, and what are the financial implications at the worst end of that distribution?"

The answer to that question supports a concrete business decision: whether to hedge, how much, and at what cost.

### Hidden Cost 2: Supplier Risk You Cannot See Yet

Every supplier has a story. The problem is that the story is told in aggregates and vibes, not in data.

"We have used them for six years" is not a risk assessment. "Their defect rate has trended from 1.2% to 3.8% over 18 months" is a risk assessment. The first is a comfort statement. The second is an early warning signal.

PVIS computes a composite risk score for every supplier based on six measurable factors: on-time delivery rate, defect rate, cost price variance, FX exposure percentage, lead time consistency, and geographic risk index. Each factor is normalized to a common scale. Each is weighted by how directly it translates to operational damage if it deteriorates.

The output is a ranked list. A score of 78 out of 100 means this supplier is in the high-risk tier. A score of 12 means they are performing reliably across all dimensions. The score is recomputed every time the analytics pipeline runs, so it reflects recent data, not a snapshot from the last annual supplier review.

The next step beyond the score is the question it enables: now that you know who is risky and why, what exactly should you do about it? PVIS generates per-supplier action playbooks. If cost variance is driving a supplier's score, the recommendation is to move toward fixed-price contracts and request quarterly price reviews. If FX exposure is the primary driver, the recommendation is to renegotiate to USD invoicing.

These are specific, actionable items derived from data. Not general procurement best practices pasted from a textbook.

### Hidden Cost 3: Cost Leakage at the Line Item Level

The least glamorous of the three problems is also the most consistently under-monitored.

Every material in your catalog has a standard cost: the approved price per unit derived from your most recent negotiation or market benchmark. When you actually pay more than that per unit on a purchase order, the difference is cost leakage. It is money that left your business without a corresponding benefit.

At scale, this adds up fast. Across 1,952 line items and 50 materials, even a 2% average overpayment represents tens of thousands of dollars per year. It does not appear as a line item on a P&L. It hides inside the aggregate cost of goods sold, indistinguishable from legitimate price increases unless someone does the comparison explicitly.

PVIS does this comparison automatically. For every line item, it calculates the variance from standard cost and stores it. The spend analysis page shows a waterfall chart breaking down leakage by material category. This takes the question from "do we have cost leakage?" (nobody knows) to "here is the packaging category, with $47,000 in leakage last year, which came primarily from three specific suppliers."

That is an audit target. That is a meeting with a supplier that has a specific number on the table.

### The Compounding Effect

Here is the thing that makes these three problems worse together than separately: they interact.

A supplier that is high-risk on defect rate and FX exposure at the same time is not just doubly risky. They are a supplier where your cost is volatile for two independent reasons simultaneously. A currency devaluation hits at the same time as a defect-driven line stoppage, and your procurement team is trying to solve both problems with the same limited bandwidth.

PVIS surfaces the interactions. The risk score incorporates FX exposure. The scenario planning page lets you ask how a 20% currency shock would hit your spend by supplier, which means you immediately see which high-risk suppliers are also high-FX-exposure suppliers, which are the ones most likely to cause compounding damage.

This is what it means to have visibility. Not a chart that shows one dimension. A system where the relationships between dimensions are visible and quantified.

### Where to Go From Here

The remaining stories in this series cover each component of PVIS in depth: how the Monte Carlo simulation works, how the risk scoring model was designed and calibrated, how the star-schema data warehouse was built, how the scenario planning layer enables executive decision-making, how the system handles real company data, what the architecture looks like under the hood, and what the build process actually taught about building production-grade analytics tools.

PVIS is open source and has a live demo on Streamlit Cloud. If you work in procurement analytics, manufacturing finance, or supply chain data engineering, something in this series will likely be directly relevant to a problem you are working on.

---

## Story 2: How Monte Carlo Simulation Makes FX Risk Quantifiable (Not Just Scary)

*The step-by-step explanation of why 10,000 simulations tell you more than any single forecast, and what regime detection adds to the picture.*

---

If you have heard the term "Monte Carlo simulation" in a finance context and nodded along without being sure exactly what it means, you are in good company. The name sounds impressive and the math underneath can get complex. But the core idea is actually intuitive, and understanding it changes how you think about FX risk in procurement.

This story walks through exactly how PVIS implements Monte Carlo FX simulation, starting from the basic concept and ending with the specific numbers the dashboard shows.

### Why One Forecast Is Not Enough

Start with a simple question: what will the USD/NGN exchange rate be in 90 days?

Every bank, every trader, every economist has an answer to this question. Every single answer is wrong. Not because the analysis is bad, but because exchange rates are genuinely uncertain. The future state of a currency is determined by oil prices, central bank policy decisions, trade flows, inflation differentials, sentiment, and dozens of other variables that interact unpredictably when stacked 90 days into the future.

A single forecast number, no matter how sophisticated the model that produced it, is presenting false precision. The honest answer is not a number. It is a range, with probabilities attached to different parts of that range.

That range is what Monte Carlo gives you.

### The Basic Idea

Monte Carlo simulation works like this: instead of asking "what will happen?", you ask "if I ran this situation ten thousand times, what would the distribution of outcomes look like?"

For FX rates, the process goes like this. You start with today's rate. You make a random step that is consistent with how this currency has historically moved day to day. You apply that step to get tomorrow's rate. You make another random step. After 90 steps, you have one possible future path for the exchange rate over 90 days.

Now you run that entire process 10,000 times, each time with different random steps drawn from the same historical distribution. You end up with 10,000 complete 90-day paths. All of them are plausible futures. The collection of their endpoints (the rate after 90 days across all 10,000 simulations) is the distribution you care about.

Take the 5th percentile of that distribution. That is the rate that 95% of your simulations beat, meaning that only 1 in 20 scenarios ends worse than this number. That is your worst-case planning scenario, call it P5.

Take the 50th percentile. That is the median outcome, the rate that half the simulations end above and half end below. That is your central estimate.

Take the 95th percentile. That is your optimistic scenario.

The spread between P5 and P95 is your uncertainty band. A wide band means high uncertainty. A narrow band means the currency has historically been relatively stable.

### What Makes the Random Steps Realistic

The specific mathematical model PVIS uses for the random steps is called Geometric Brownian Motion, abbreviated GBM. This is the same model used in the famous Black-Scholes options pricing formula. It treats percentage changes in the exchange rate as random draws from a normal distribution, with a mean drift (the average direction the rate has been moving) and a standard deviation (how much it typically moves per day).

In equation form: the rate tomorrow equals the rate today, multiplied by the exponential of the drift plus a random component. The random component is a standard normal random variable multiplied by the daily volatility and the square root of the time increment.

In plain English: the rate tomorrow is the rate today, adjusted by an amount that is mostly centered around zero but can be much larger or smaller on any given day, with the distribution of how large or small calibrated to match what this specific currency has historically done.

### Regime Detection: Why Not Just One Set of Parameters?

Here is the insight that takes the simulation from realistic to much more accurate.

Currencies do not behave the same way all the time. There are calm periods when the rate moves by 0.1% or 0.2% a day and the trend is stable. There are crisis periods when the rate moves by 1% to 2% a day and the direction is hard to predict.

If you estimate a single drift and volatility parameter by averaging over your entire historical dataset, you get a number that describes neither regime accurately. You are averaging a calm period with a crisis period and getting a parameter that resembles neither.

PVIS implements a two-regime model. It calculates the 20-day rolling volatility of log returns across the entire history. Any period where volatility was above the median rolling volatility is classified as the high-volatility regime. Any period below is the low-volatility regime.

Separate drift and volatility parameters are estimated for each regime. The proportion of historical days spent in each regime gives the probability of being in each regime on any given day.

During simulation, each day, the model first draws a random number to decide: are we in the low-volatility regime today (with probability equal to the historical proportion) or the high-volatility regime? Then it draws the random shock from the appropriate regime's distribution.

The result is a simulation that correctly reproduces the fat-tailed behavior of FX rates: mostly small moves, but with occasional large moves that make the P5 worse than a pure normal distribution would suggest.

### What the Dashboard Shows You

The FX Volatility page in PVIS has several outputs from this simulation.

The fan chart shows the historical rate as a solid line, with today's rate marked clearly, and then a forward-looking fan in three bands: P5 (worst case), P50 (median), and P95 (best case). This visual immediately communicates two things: the direction the rate has been moving, and the uncertainty about where it is going.

The terminal distribution histogram shows the shape of the distribution of final rates across all 10,000 simulations. If this histogram is centered close to today's rate, the rate is expected to be stable. If it is skewed strongly in one direction, there is historical momentum pushing it there.

VaR (Value at Risk) tells you: "at the 5th percentile, the FX rate will cost you approximately $X more per unit of NGN-denominated spend than today's rate implies." This is the procurement-relevant number. It translates the abstract exchange rate distribution into a direct cost impact.

CVaR (Conditional Value at Risk, also called Expected Shortfall) tells you: "in the worst 5% of scenarios, the average cost impact is $Y." This is the number that matters for stress testing. It tells you not just where the bad outcomes start, but how bad they are on average when they occur.

### What Decision This Supports

The output of this analysis is not "the exchange rate will be X." It is: "given historical behavior, there is a 5% chance your FX-exposed procurement costs will increase by more than $X in the next 90 days."

That sentence tells you whether hedging is worth exploring. If $X is small relative to the cost of a forward contract, hedge. If $X is larger than the cost, you have quantified risk that exceeds your hedging cost, which is a clear signal to explore protection.

PVIS makes this calculation available in real time, for any currency, for any horizon. The simulation rebuilds every time you change the parameters. There is no analyst handoff, no waiting for a model to be run, no report to request. The answer is there when you need it.

---

## Story 3: Designing a Supplier Risk Score That Actually Predicts Problems

*How six weighted factors, a composite formula, and per-supplier action playbooks turn raw supplier data into procurement decisions.*

---

A supplier risk score sounds simple in concept. You pick some metrics, you combine them into a number, you rank your suppliers. In practice, the design choices matter enormously and wrong choices produce scores that are mathematically valid but behaviorally useless.

This story covers the design decisions behind the PVIS composite risk model: which factors were chosen, why they are weighted the way they are, how the normalization works, and why the output is structured around decisions rather than just rankings.

### What Makes a Risk Score Useful Versus Decorative

The test of a risk score is not "does it feel reasonable?" It is "does it predict operational problems, and does it produce specific recommendations?"

A score that accurately ranks suppliers from most to least risky but produces no actionable output is interesting as a measurement but not useful as a management tool. The score needs to be decomposable: you need to be able to say not just "Supplier A scored 73" but "Supplier A scored 73 primarily because of high cost variance (contributing 22 points) and high FX exposure (contributing 18 points), and here is what to do about each of those specifically."

The PVIS score was designed with this in mind from the beginning.

### The Six Factors and Their Weights

**On-Time Delivery Rate: 22% weight**

This is the fraction of purchase orders where the actual delivery date was on or before the supplier's published lead time promise. It is calculated precisely: for each order, did the number of days from order date to actual delivery date equal or exceed the supplier's stated lead time in days? The binary yes/no across all orders gives a percentage.

This factor gets the highest weight because late delivery is the most direct translation to production disruption. A supplier who delivers late consistently is one planning crisis away from stopping your factory.

**Defect Rate: 20% weight**

Calculated from quality incident records. The average defect rate percentage across all incidents attributed to this supplier. Second-highest weight because defects are costly in multiple directions: rework labor, scrapped materials, quality hold delays, potential customer warranty implications.

**Cost Variance: 18% weight**

The coefficient of variation on unit price: the standard deviation of unit prices across all purchase order line items for this supplier, divided by the average unit price, expressed as a percentage. A supplier with consistent pricing scores low on this factor. A supplier whose prices bounce significantly is flagged.

High cost variance is both a budgeting problem (hard to forecast) and a negotiation signal (inconsistent pricing usually means there is room to negotiate fixed terms).

**FX Exposure: 18% weight**

The fraction of total spend with this supplier denominated in a foreign currency. If 100% of a supplier's invoices are in NGN and your reporting currency is USD, the entire spend with them is FX-exposed, meaning the real cost in USD fluctuates with the exchange rate regardless of the negotiated local price.

This factor gets equal weight to cost variance because FX exposure is, in effect, a form of cost variance imposed by the currency market rather than by the supplier's own pricing behavior.

**Lead Time Consistency: 12% weight**

The standard deviation of actual lead times (days from order to delivery) across all orders. A supplier might have an acceptable average lead time but terrible consistency: sometimes delivering in 5 days, sometimes in 45. This is hard to plan around and forces higher safety stock, which ties up working capital.

The standard deviation divided by the mean (another coefficient of variation) is what gets normalized and included. High variance in lead times scores high on this factor.

**Geographic Risk Index: 10% weight**

A country-level score, 0 to 100, capturing political stability, infrastructure reliability, and logistics quality for the country the supplier is based in. This data comes from the supplier master record and is maintained as a static field that can be updated when country conditions change.

Geographic risk gets the lowest weight because it is a background probability rather than an ongoing operational measurement. A country can have elevated risk without it manifesting in any specific order. The other five factors are continuously updated from actual transaction data; this one represents potential rather than observed behavior.

### The Normalization Step

The six factors are measured in different units with different scales. On-time delivery is a percentage. Lead time standard deviation is in days. Cost variance is a ratio. Geographic risk is a raw index score.

Before combining them, each factor is normalized to a 0-to-1 scale using min-max normalization: the observed value minus the minimum across all suppliers, divided by the range. The result is always between 0 and 1, where 0 is the best-performing supplier in the dataset and 1 is the worst.

One subtlety: on-time delivery rate is measured as a "good" percentage (higher is better). In the risk score, we want 0 to mean low risk and 1 to mean high risk. So on-time delivery is inverted: the factor that enters the formula is 1 minus the normalized OTD rate, which means a supplier with perfect on-time delivery contributes 0 to their risk score from this factor.

### The Composite Formula

After normalization, the weighted sum:

Risk Score = 100 × (0.22 × OTD risk + 0.20 × defect norm + 0.18 × cost variance norm + 0.18 × FX exposure norm + 0.12 × lead time consistency norm + 0.10 × geo risk norm)

Multiplying by 100 brings the result into a 0-to-100 scale. The weights sum to 1.0, so the maximum possible score is 100 and the minimum is 0.

In practice, the distribution of scores across a typical supplier panel tends to cluster between 20 and 70, with high-risk suppliers above 60 and excellent suppliers below 25.

### The Negotiation Playbook Output

The score is a means to an end, not the end itself. The end is a specific recommended action for each high-risk supplier.

PVIS generates these automatically by examining which factors are driving each supplier's score. The logic is threshold-based: if cost variance norm is above 0.5 (meaning this supplier is in the worse half of your panel on cost variance), the playbook includes a fixed-price contract recommendation. If FX exposure norm is above 0.6, it includes a currency denomination recommendation. If OTD risk is above 0.5 and lead time consistency is above 0.4, it includes a delivery performance clause recommendation.

These recommendations are displayed per supplier on the Supplier Risk Analysis page, giving procurement managers a ready-made negotiation brief for their next supplier meeting.

---

## Story 4: What Is a Star Schema and Why Does It Make Your Analytics 10x Faster

*The data architecture behind PVIS, and why organizing data correctly is more important than any algorithm.*

---

Imagine you want to answer this question: "What was our total procurement spend in USD, broken down by supplier country, for every quarter of the last three years?"

If your data is stored as a set of normalized transactional tables, answering this question means joining several tables: purchase orders to line items, line items to materials, orders to suppliers, suppliers to countries, orders to currencies, and then looking up exchange rates by date to convert everything to USD. Depending on your data volume, this could take seconds or minutes. More importantly, if analysts are running dozens of variations of this question constantly through a live dashboard, the database gets hammered.

The star schema solves this. This story explains what it is, why it exists, and how PVIS implements it.

### The Two-Layer Data Architecture

PVIS deliberately separates its data into two layers with different purposes.

The transactional layer (19 normalized tables) is designed for correctness. Every fact is stored once. Changes propagate correctly. Constraints prevent bad data from entering. This layer is optimized for writing accurate data and for operational queries like "show me the status of purchase order 4412."

The warehouse layer (star schema) is designed for analytics. It is optimized for reading aggregated data quickly. It has some redundancy, which is fine: its goal is not to be maximally efficient for storage but to make analytical queries as fast as possible with minimal join overhead.

The ETL pipeline is the bridge between the two layers. It runs on demand and transforms normalized transactional data into the denormalized, aggregated warehouse format.

### The Star Schema Structure

In a star schema, one central table (the fact table) contains the primary measurements you care about. Surrounding it are dimension tables that describe the context of each measurement.

In PVIS:

The **fact_procurement** table is the center of the star. Each row represents one purchase order line item. It contains: the quantity, the unit price, the total value in local currency, and the total value converted to USD using the closest matching exchange rate. Each row also contains foreign keys pointing to the date dimension, the supplier dimension, and the material dimension.

**dim_date** contains one row for every date from 2023 to 2026 with fields for year, quarter, month number, month name, week number, and day of week. Adding new date attributes (like "is this a fiscal quarter end?") is cheap: just add a column to this table.

**dim_supplier** contains one row per supplier with their name, country, surrogate key, and any other attributes you want to filter or group by.

**dim_material** contains one row per material with the category, standard cost, and surrogate key.

The "star" in star schema comes from the visual: if you draw the fact table in the center with the dimension tables surrounding it, the connections radiate outward like the points of a star.

### Why Queries Are Faster

The procurement spend question from before: "total USD spend by supplier country by quarter" now requires exactly one join from fact_procurement to dim_supplier (for country) and one join to dim_date (for quarter). The exchange rate conversion has already been applied when the ETL populated fact_procurement. There is no need to do the multi-table join at query time.

On a table with 1,952 rows (our dataset), this difference is not dramatic. But at 1,000,000 rows (a larger company's annual procurement volume), the difference between a query that needs four joins and one that needs one join can be the difference between a one-second dashboard load and a twenty-second one.

Pre-aggregated summary tables sit alongside the star schema. The `supplier_spend_summary` table pre-computes annual USD spend per supplier. The `supplier_performance_metrics` table stores the pre-computed risk scores. The `financial_kpis` table stores pre-computed DIO, DPO, and CCC values. These tables are the fastest possible reads: no computation at query time, just a lookup.

### The ETL Pipeline

The ETL (Extract, Transform, Load) pipeline in `populate_warehouse.py` runs seven steps in sequence:

1. Populate dim_date with one row per date in the 2023-2026 window
2. Populate dim_material from the materials transactional table
3. Populate dim_supplier by joining the suppliers table with countries
4. Populate fact_procurement by joining PO line items, finding the closest exchange rate date per currency for each order, converting to USD, and inserting with surrogate keys
5. Populate supplier_spend_summary by aggregating fact_procurement by supplier and year
6. Calculate supplier_performance_metrics by running the risk score queries against the transactional layer
7. Calculate financial_kpis from payables, receivables, and inventory snapshots

Each step is idempotent: it truncates the table before repopulating, so running the pipeline multiple times produces the same result without duplicates.

The pipeline runs in under 30 seconds on the full 3-year dataset. For larger datasets, each step could be partitioned to insert incrementally rather than replacing the full table.

---

## Story 5: The Cash Conversion Cycle Explained for Procurement Professionals

*How DIO, DPO, and the CCC connect procurement decisions to working capital, and how PVIS makes the math visible in real time.*

---

Most conversations about procurement focus on price: what did we pay per unit, are we getting the best rate, can we negotiate lower. Price is important. But there is a dimension of procurement cost that is invisible if you only look at unit price: the cost of time.

Time is money in procurement because of the cash conversion cycle. This story explains what the CCC is, why procurement managers should care about it, and how PVIS makes CCC optimization a live, interactive decision.

### The Basic Concept

A manufacturing company's cash goes through a cycle. It starts as cash. It becomes raw materials (inventory). It gets transformed into finished goods (still inventory). It gets shipped to customers, creating a receivable. The receivable gets collected, becoming cash again.

At any given moment, a slice of your cash is frozen inside this cycle. It cannot be invested, cannot be used to pay down debt, cannot be returned to shareholders. The longer the cycle, the more cash is frozen.

The Cash Conversion Cycle (CCC) measures this in days: CCC = DIO minus DPO.

**DIO (Days Inventory Outstanding)** measures how many days of production value is tied up in your warehouses on average. Calculated as: average inventory value divided by daily cost of goods sold.

**DPO (Days Payable Outstanding)** measures how long, on average, you wait before paying your suppliers after receiving goods. Calculated as: average accounts payable balance divided by daily procurement spend.

A shorter DIO means you are not holding excess inventory. A longer DPO means you are holding onto cash longer before paying suppliers. Both shrink the CCC. A smaller CCC means less of your cash is frozen inside the supply chain at any given time.

### Why This Is a Procurement Decision

DPO is directly controlled by procurement in contract negotiations. When you agree to payment terms with a supplier, you are setting DPO for that supplier relationship.

If your current payment terms average 30 days and you successfully negotiate to 45 days with your top five suppliers, you have effectively delayed roughly two weeks of outgoing cash per payment cycle. At $5 million in annual procurement spend ($417,000 per month), extending from 30 to 45 days frees up approximately $208,000 in working capital that was previously sitting in accounts payable.

This is real money that procurement directly controls. It is also something that almost never gets modeled explicitly, because the analysis requires the right data in the right place at the right time.

DIO is also influenced by procurement, specifically through supplier reliability. If suppliers have long and unpredictable lead times, you have to hold more safety stock to avoid stockouts. More safety stock means higher DIO. A supplier whose lead time standard deviation drops from 10 days to 3 days allows you to reduce safety stock, which reduces DIO, which shortens the CCC.

### How PVIS Models This

The Working Capital page in PVIS shows three things: current DIO, current DPO, and the resulting CCC, visualized as gauge charts with historical trend lines.

The scenario modeler on this page lets you adjust the DPO by inputting different payment term assumptions. If you move DPO from 30 to 45 days for all suppliers, the CCC calculation updates immediately. The working capital freed is calculated and displayed.

The payables and receivables timeline charts show month-by-month trends, so you can see if DPO has been drifting (perhaps suppliers have been pushing for earlier payment without it being a formal term change) and if DIO has been inflating (perhaps safety stock accumulation is quietly happening).

The inventory value trend shows whether inventory is growing or shrinking in dollar terms over time. A growing inventory trend combined with stable sales is a signal that DIO is increasing, which is a signal that either demand forecasting is off or lead times have lengthened.

### The Scenario That Matters Most

The most valuable scenario to model is this one: "if we renegotiate our top three suppliers to 45-day payment terms (from current 30-day terms), what is the working capital impact?"

The three suppliers with the highest spend drive a disproportionate share of total payables. Extending terms with them has the largest CCC impact. PVIS makes it possible to identify which three those are (via the spend analysis page), estimate the dollar impact of extending their terms (via the working capital scenario), and walk into the negotiation with a specific goal and a specific financial justification.

The suppliers are unlikely to offer better terms unless asked. Most payment term negotiations start with the buyer requesting a change and the supplier agreeing, disagreeing, or proposing an alternative. Having the working capital math done before the meeting means the ask is grounded in a specific number rather than a vague preference.

---

## Story 6: How PVIS Handles Real Company Data (The Import Architecture)

*A technical walkthrough of the CSV validation pipeline, schema enforcement, and data normalization that make external data uploads reliable.*

---

Building a clean analytics platform on synthetic data is straightforward. The data is generated to be exactly the right format, with exactly the right relationships, with no missing values and no schema violations. The real world is different.

Real company data has inconsistent date formats. It has supplier names spelled three different ways. It has missing currency codes, duplicate rows, negative quantities, and price fields that occasionally contain dollar signs or commas. Any production analytics system that accepts external data must handle all of this gracefully, or it will produce wrong answers silently, which is worse than producing no answer at all.

This story covers how PVIS handles real company data through its CSV import pipeline.

### The Import Methods

PVIS supports two paths for external data.

The first is the dashboard uploader. On the Company Data Upload page, a drag-and-drop file uploader accepts CSV files or a ZIP archive containing multiple CSVs. The upload is processed in the browser session: validation runs immediately, errors are surfaced to the user with specific row numbers and field names, and if validation passes, the data is imported, the ETL pipeline runs, and the dashboard refreshes with the new data. No command line required.

The second is the command-line import. The `external_data_loader.py` script accepts a directory of CSV files, validates them against the defined schema, normalizes values, and inserts them into the transactional database tables. This path is designed for bulk loads and automated pipelines.

### The Five Required Files

PVIS requires five CSV files with specific schemas:

**suppliers.csv**: supplier name, country, lead time in days, and historical defect rate percentage. The country field is validated against the known country list. Lead time must be a positive integer. Defect rate must be between 0 and 1.

**materials.csv**: material name, category (must be one of the valid category codes), and standard cost in USD. Standard cost must be positive.

**purchase_orders.csv**: purchase order date (in ISO format), supplier name (matched against imported suppliers by name), total amount, and currency code. Currency code is validated against the known currency list.

**purchase_order_items.csv**: PO identifier, material name (matched against imported materials), quantity (positive integer), and unit price. The combination of quantity times unit price must be consistent with the PO total within tolerance.

**fx_rates.csv** (optional): rate date, currency code, and daily rate to USD. If omitted, the system auto-generates FX history using the live API and backcast logic.

### The Validation Layer

Before any data touches the database, it passes through a validation layer that checks every row.

For each file, the validator checks:

- Required columns are present with the correct names
- No rows have null values in required fields
- Numeric fields contain valid numeric values (not strings, not blanks)
- Date fields parse correctly as dates
- Code fields (currency, country, category) match the valid value list
- Numeric ranges are plausible (quantities positive, costs positive, defect rates between 0 and 1)
- Foreign key relationships resolve (every supplier name in purchase_orders.csv matches a name in suppliers.csv)

If any check fails, validation stops and returns a structured error report: file name, row number, field name, observed value, and what was expected. The user sees this on the dashboard immediately and can fix the specific rows before re-uploading.

This approach prevents silent corruption. A row that fails validation is not silently dropped or imputed. It is explicitly reported so the user knows exactly what needs to be corrected.

### The Normalization Step

After validation, normalization handles the inconsistencies that are valid but not yet in the right format.

Supplier names are stripped of extra whitespace and normalized to title case. Date strings are parsed using multiple format patterns (ISO, US format, European format) and converted to a consistent datetime64 format. Currency codes are uppercased. All amounts are stored as numeric types, not strings.

The normalization step also deduplicates. If a CSV file contains two rows for the same supplier with slightly different names (perhaps "Apex Metals Ltd" and "Apex Metals Limited"), the validator flags this as a potential duplicate and asks the user to confirm or consolidate before proceeding.

### The Complete Pipeline After Import

Once the data is validated and normalized, the following sequence runs automatically:

1. Data is inserted into the transactional layer tables (suppliers, materials, purchase_orders, purchase_order_items)
2. If fx_rates.csv was not provided, the FX rebuild script runs to generate historical rate data for each currency in the uploaded data
3. The warehouse ETL pipeline runs to rebuild the star schema from the new transactional data
4. The analytics engine runs to recalculate supplier risk scores and financial KPIs from the new data
5. The dashboard refreshes to show results based on the uploaded data

This full pipeline runs in under two minutes on a typical company dataset. The user sees a progress indicator during each step, and the dashboard automatically switches to show the imported data instead of the synthetic demo data.

---

## Story 7: Building PVIS: Architecture Decisions and What I Would Do Differently

*A technical retrospective on the system design decisions behind PVIS and the lessons that only became visible in production.*

---

PVIS is a production-grade procurement analytics platform built in Python, MySQL, and Streamlit. It has about 3,000 lines of application code (not counting tests), a two-layer database architecture with 23 tables total, an eight-page interactive dashboard, and a CI/CD pipeline that runs on every push.

This story is a retrospective on the build: what decisions were made, why, what worked, and what I would do differently.

### Decision 1: Streamlit Over Flask (Right Call)

Early in the project, I built a prototype using Flask with a templated HTML frontend. The UI was functional but required significant effort to make interactive: every chart update required a form submission or a JavaScript fetch, session management was manual, and adding a new widget meant modifying HTML templates, CSS, route handlers, and client-side JavaScript simultaneously.

Switching to Streamlit was the right decision for this type of analytical application. Streamlit's reactivity model (re-run the entire script on any user input change) makes interactive dashboards easy to reason about. Adding a slider that changes a Monte Carlo parameter and immediately updates a chart requires exactly two lines of code. The tradeoff is that Streamlit is not great for highly customized UI or for applications that need fine-grained client-side state. For a data analytics dashboard, the trade is completely worth it.

### Decision 2: MySQL Over SQLite (Right Call for Different Reasons Than Expected)

I considered SQLite initially because the deployment story is simpler: no server to manage, the database is a file. For a single-user analytical tool, SQLite is often the right choice.

The reason MySQL became the right choice was deployability, not performance. The Streamlit Cloud deployment (the live demo everyone can access) needs a hosted database that the Streamlit Cloud container can connect to. SQLite on disk does not work because the Streamlit Cloud filesystem is ephemeral. Aiven provides a free-tier hosted MySQL instance that the deployed application connects to reliably.

The secondary benefit of MySQL was the ability to use `ONLY_FULL_GROUP_BY` enforcement and proper constraint checking, which caught several data modeling errors early that would have been silent bugs in SQLite.

### Decision 3: Separate Analytics Module (Right Call)

Putting the Monte Carlo simulation and supplier risk scoring into a separate `analytics/advanced_analytics.py` module instead of embedding them in the Streamlit app was one of the best structural decisions. It means the analytics can be run independently from the command line, tested in isolation, and reused by the Power BI semantic layer without any Streamlit dependency.

The alternative (embedding calculations directly in the dashboard code) is tempting because it is faster to write. It leads to large, untestable functions mixed with UI code that become impossible to maintain.

### Decision 4: The Demo Mode Architecture (Surprising Value)

PVIS detects at startup whether a database connection is available. If it is not, the app serves synthetic data generated by `demo_data.py` and clearly labels every page as "Demo Mode."

This was originally a practical necessity: people exploring the app on Streamlit Cloud without configuring their own database should still see a working, useful product. It turned out to be much more valuable than expected. The demo mode means the app is instantly explorable for anyone. There is no setup barrier to seeing what the platform looks like and how the analysis works.

### What I Would Do Differently

**I would add parameterized queries from day one.** Several early database queries were built using f-string interpolation to insert query parameters. This pattern is a SQL injection risk and was refactored to use SQLAlchemy parameterized queries in a later pass. Starting with parameterized queries removes that risk completely and is no more complex to write.

**I would design the test suite alongside the application, not after it.** The test coverage for the analytics module is good because it was built with testing in mind from an early stage. The test coverage for the dashboard page logic is thinner because the dashboard was prototyped first and tests added later. The result is that refactoring dashboard code carries more risk than refactoring analytics code.

**I would separate configuration more aggressively.** Several magic numbers (regime detection window, risk score weights, simulation count defaults) live in the code rather than in a configuration file. Moving them to a TOML config file would make them easy to tune without touching source code.

The overall architecture holds up well. The two-layer data model, the separation between analytics and dashboard, and the Docker containerization have all made the system easier to maintain, extend, and deploy than a simpler flat structure would have.

---

## Story 8: What Procurement Analytics Gets Wrong (And How to Do It Right)

*A critical look at the common failures in procurement analytics implementations and the design principles that produce genuinely useful systems.*

---

Procurement analytics has a credibility problem.

Not because the tools are bad or the data is unavailable. Because the implementations tend to optimize for impressiveness rather than usefulness. Dashboards get built. Charts get made. Nobody changes a decision because of them. The dashboard becomes ignored six weeks after launch.

This story is about why that happens and what the design principles are that make analytics actually drive decisions.

### Failure Mode 1: Answering Questions Nobody Is Asking

The most common procurement analytics failure is building a system that answers the analyst's questions, not the decision-maker's questions.

An analyst wants to see spend trends, detailed breakdowns, drill-down capability at every level. A chief procurement officer wants to walk into a meeting and answer three questions: where are our costs going, who is our biggest risk, and what should we do about it?

These are not the same requirements. A dashboard optimized for analyst exploration will have dozens of filters, hundreds of combinations, and no clear hierarchy of importance. The CPO will open it, feel overwhelmed, and close it.

PVIS was built by asking the decision question first and then building the analysis to answer it. The Executive Summary exists because the first question is "what is the state of our procurement health right now?" The Scenario Planning page exists because the second question is "what happens if the currency moves?" Every page maps to a specific decision, not to a data exploration opportunity.

### Failure Mode 2: Building on Stale Data

A report that takes three days to produce tells you what happened three days ago. In a static environment, that is acceptable. In procurement, it is often useless.

A supplier risk situation that deteriorated two weeks ago and was not visible in the latest monthly report is a situation where you are reacting instead of acting. By the time the report surfaces the problem, the production impact may have already happened.

Real-time or near-real-time data is not a luxury in procurement analytics. It is the feature that makes the difference between a reporting tool and an intelligence tool. PVIS fetches live exchange rates on every dashboard load. The analytics pipeline can be triggered from the dashboard at any time. The risk scores reflect the most recent data in the database.

The tradeoff is data pipeline design: you have to build the ingestion, transformation, and analytics layers so they can run quickly and reliably on demand, not just on a nightly batch schedule.

### Failure Mode 3: Metrics That Do Not Connect to Actions

A metric without an action is noise.

"Average lead time is 28 days." What should I do with that? Nothing. It is interesting, but it is not actionable.

"Supplier A's average lead time has increased from 18 days to 31 days over the past six months, placing them in the high-risk tier for on-time delivery consistency." That is actionable. It leads directly to a supplier meeting, a contract review, and possibly a source diversification decision.

PVIS displays derived conclusions, not just raw metrics. The composite risk score is not just a number; it comes with a decomposition of which factors are driving it and a set of recommended actions. The cost leakage analysis does not just show variance; it ranks the categories by leakage magnitude and flags the specific supplier relationships contributing the most.

The design principle is: every metric shown should have a corresponding decision it enables. If you cannot name the decision, cut the metric.

### Failure Mode 4: Ignoring Uncertainty

Single-point estimates are seductive because they are clean and easy to communicate. "FX will add $500,000 to procurement costs next quarter." Clear, specific, quotable.

Also potentially very wrong, with no indication of how wrong.

The honest version of that statement is: "Under our Monte Carlo simulation, there is a 5% chance FX adds more than $1.2 million to procurement costs next quarter, a 50% chance it adds between $200,000 and $600,000, and a 5% chance it actually reduces costs." That is more complex to communicate, but it is also more useful: it tells you the range of outcomes you should plan for and gives you a basis for deciding whether to hedge.

PVIS consistently presents uncertainty alongside central estimates. The fan chart shows P5, P50, and P95 explicitly. The VaR and CVaR metrics quantify the tail risk explicitly. The scenario comparison table shows Base, Stress, and Optimized side by side rather than a single projected number.

This makes the analysis more honest and, ultimately, more trustworthy. Decision-makers who have been burned by overconfident single-point forecasts tend to distrust analytics systems that present everything as certain. Showing uncertainty explicitly, with the right framing, builds credibility.

### The Design Principle That Ties All of This Together

Every design decision in PVIS comes back to one principle: does this make it easier or harder for a procurement professional to take a better decision in the next meeting?

If it makes it easier, it belongs. If it adds complexity without enabling a better decision, it does not.

This sounds obvious. It is consistently violated in analytics implementations because the people building the system tend to be excited about the analytics, not about the decisions. Keeping the decision front and center requires actively resisting the temptation to make the system more sophisticated than the decision requires.

Procurement analytics done well is not about impressive algorithms or beautiful visualizations. It is about getting the right number to the right person at the right moment so they can take a better action. Everything else is in service of that.

---
