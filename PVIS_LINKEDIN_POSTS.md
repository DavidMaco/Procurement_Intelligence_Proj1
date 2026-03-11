# PVIS LinkedIn Posts

---

## Post 1: The Problem (Hook)

Your procurement team places 800 purchase orders this year.

778 of them are in multiple currencies. 8 suppliers across 4 continents. 1,952 individual line items.

And at the end of the quarter, someone opens a spreadsheet and tries to figure out why costs are up 12%.

That spreadsheet will not find it. Not because the data is wrong, but because the real answer is distributed across currency movements, supplier reliability trends, and unit-price variances that nobody is comparing against a standard cost catalog.

This is not a data problem. It is a visibility problem.

Three things are silently killing procurement margins in manufacturing companies right now:

1. FX volatility that nobody is modeling forward
2. Supplier risk that is measured by gut feel instead of data
3. Cost leakage against standard costs that goes undetected for quarters

I spent months building PVIS (Procurement Volatility Intelligence System) specifically because I wanted to see what it would look like if you actually solved all three at the same time, in a single dashboard, backed by real math.

Here is what I found: the analysis that takes a team a week to assemble manually can be made available in real time, continuously updated, with no analyst intervention. You just have to build it right.

Over the next few posts I am going to break down exactly how each part works, what decisions it enables, and why the approach matters. Starting with the problem that companies feel most acutely right now.

Currency volatility.

What does your procurement team currently use to forecast FX exposure 90 days out?

#Procurement #SupplyChain #DataAnalytics #FXRisk #Manufacturing

---

## Post 2: FX Volatility and Monte Carlo Simulation

Most manufacturing procurement teams forecast FX exposure in one of two ways.

They either use today's rate and assume it stays flat. Or they use an average of the past 12 months and assume mean reversion.

Both are wrong, and for the same reason: they describe the center of the distribution without saying anything about the tails.

In currency markets, the tails are where the disasters happen.

A 15% NGN devaluation is not a black swan. It happens. It happened multiple times in recent years. When it happens, a company that budgeted procurement spend at the average rate suddenly faces a cost overrun that cannot be offset by operational savings anywhere in the business.

The technical solution to this is Monte Carlo simulation with regime detection.

Here is what that means in plain English:

You look at three years of daily exchange rates and calculate how the rate changed day by day. You notice that there are two distinct patterns: periods when the currency moves gently (low volatility regime) and periods when it moves sharply (high volatility regime). You fit separate statistical models to each regime. Then you run 10,000 simulations, each of which makes 90 daily decisions: is today a calm day or a volatile day? Based on that, a random shock is applied.

After 10,000 runs, you have 10,000 possible futures. The 5th percentile of those futures is your worst-case scenario. The 50th is your central estimate. The 95th is your upside.

This gives you a number. Not a vague sense of "the naira is risky," but: "under the 5% worst-case scenario, your FX-exposed procurement costs will be $X million higher than today's rate implies."

That is a sentence you can take to a CFO. It can support a hedging decision. It tells you whether the cost of a forward contract is worth paying.

PVIS does this in real time, for any currency, for any horizon between 30 and 1,095 days, with user-configurable simulation count up to 50,000 paths. The live rate is fetched automatically from a dual-API failover system.

The dashboard shows you the fan chart, the terminal distribution histogram, VaR, CVaR, and FX shock sensitivity at fixed intervals.

The question this answers: should we hedge, and if so, by how much?

That is a decision PVIS makes possible in minutes instead of weeks.

#MonteCarlo #FXRisk #Procurement #QuantitativeFinance #DataScience

---

## Post 3: Supplier Risk Scoring

Here is a question very few procurement managers can answer quickly:

Which of your suppliers is most likely to stop your production line in the next six months?

Not which one you are most nervous about. Which one the data says is the most dangerous.

There is a difference, and it matters.

Gut feel about suppliers is shaped by relationships, by recent incidents, by whoever complains the loudest. Data tells a different story. A supplier you trust because they have never caused a crisis might be showing warning signs in their cost variance, their defect rate trend, or their delivery consistency. A newer supplier might actually be performing better on every measurable dimension.

PVIS calculates a composite risk score for every supplier using six factors:

**On-time delivery rate (22% weight):** What fraction of orders actually arrived when the supplier committed to delivering them? This gets the highest weight because late delivery is the most direct path to a production stoppage.

**Defect rate (20% weight):** Quality incidents as a percentage of orders. Second-highest weight because defects mean line stoppages, rework, and warranty liability.

**Cost variance (18% weight):** How much does this supplier's unit pricing fluctuate? A supplier who charges different prices on different orders with no clear reason is a budget management problem and a negotiation problem.

**FX exposure (18% weight):** What fraction of your spend with this supplier is in a foreign currency? Higher FX exposure means higher volatility in real cost, independent of the supplier's own performance.

**Lead time consistency (12% weight):** Even suppliers who are mostly on time can have terrible variance. A supplier who sometimes delivers in 5 days and sometimes in 30 days is hard to plan around.

**Geographic risk index (10% weight):** Country-level risk: political stability, infrastructure reliability, logistics quality. Gets the lowest weight because it is a background probability, not an immediate operational signal.

All six factors are normalized to a common 0-to-1 scale and combined into a score from 0 to 100. Higher means more risk.

The output is a ranked list of all your suppliers, color-coded by risk level, with a per-supplier negotiation playbook generated automatically: specific recommended actions based on which factors are driving the score.

This turns "we should probably have a conversation with that supplier" into "here is exactly what to renegotiate and why."

#SupplierRisk #Procurement #SupplyChain #Analytics #Manufacturing

---

## Post 4: Cost Leakage and Spend Analysis

Every material you buy has a standard cost: the agreed-upon, budgeted price per unit.

In a healthy procurement operation, what you actually pay is close to that number. When you pay more, the difference is called cost leakage, and it should be zero. It is almost never zero.

Across 1,952 purchase order line items and 50 materials, a 3% variance on average does not sound like much. It is. At $5 million in annual procurement spend, 3% is $150,000 per year leaving the business with no corresponding value received, for no reason other than price drift that nobody caught.

The problem is catching it. Manually comparing every line item's unit price against the standard cost catalog takes an analyst days. It is not something that gets done monthly. So the leakage accumulates for quarters before someone notices.

PVIS automates this completely.

For every line item on every purchase order, the system calculates: actual unit price minus standard cost, multiplied by quantity. If the result is positive (you paid more than standard), it is leakage. The system aggregates this by material category and visualizes it as a waterfall chart. You can see at a glance:

"Packaging materials: $47,000 over standard. Electronic components: within tolerance. Steel and metals: $22,000 over standard."

Now you know exactly where to send the audit. And you know before a quarter has gone by.

The spend analysis layer goes further: it shows total spend by supplier, by category, by year, with year-over-year comparison. This tells you not just where money is leaking against standard cost, but where spend concentration is building. If 60% of your procurement spend is with two suppliers, that is a concentration risk that looks fine until it is not.

Both of these analyses are live on the dashboard. No export to Excel. No waiting for the monthly report.

#CostManagement #Procurement #SpendAnalysis #Manufacturing #DataAnalytics

---

## Post 5: Working Capital and the Cash Conversion Cycle

There is a number that treasury teams care about deeply that procurement managers often treat as someone else's problem.

It is called the Cash Conversion Cycle, and the procurement function owns a large part of it.

Here is the simple version: you buy materials (cash goes out), you turn them into products (inventory), you sell the products (cash comes back in). The CCC measures how many days elapse between writing a check to your supplier and collecting from your customer. A shorter CCC means cash flows back to you faster. A longer CCC means more of your own money is tied up in the supply chain at any given time.

Two factors that procurement directly controls:

**DIO (Days Inventory Outstanding):** On average, how many days of production do you keep in your warehouses? This is a function of supplier lead times and safety stock decisions. Longer lead times from unreliable suppliers force higher safety stock, which means more days of inventory, which means more cash tied up.

**DPO (Days Payable Outstanding):** How many days does it take you to pay suppliers after receiving goods? If you pay immediately, you are extending an interest-free loan to your supplier at your own expense. If you can negotiate 45-day payment terms instead of 30-day, you effectively free up cash that was previously sitting in accounts payable.

The relationship is: CCC = DIO minus DPO. You want this number to be as small as possible, ideally zero or negative for companies with strong negotiating power.

PVIS models this directly. The Working Capital dashboard page shows current DIO and DPO, the resulting CCC, and a scenario modeler. You can ask: if we extend payment terms with our top three suppliers from 30 to 45 days, how much working capital is freed? The system calculates the answer immediately.

This is not abstract treasury theory. It is a concrete, achievable decision that procurement managers can act on in the next contract negotiation cycle.

#WorkingCapital #CashConversionCycle #Procurement #SupplyChain #Finance

---

## Post 6: The Technical Architecture

Building a useful analytics platform requires solving a less visible problem that users never see: the data needs to be organized in a way that makes fast, accurate querying possible.

PVIS has a two-layer data architecture, and the distinction matters.

**The transactional layer** is a normalized MySQL database with 19 tables. This is designed for accuracy and data integrity. Every purchase order links to a supplier, a currency, and a set of line items. Every quality incident links to a specific order. Every exchange rate is stamped to a specific date and currency. Foreign key constraints and check constraints ensure that bad data cannot enter the system. This layer is optimized for writing correct data.

**The warehouse layer** is a star schema sitting on top of the transactional tables. An ETL pipeline runs and transforms the raw data into a fact table (individual procurement line items in USD, with surrogate keys) surrounded by dimension tables for dates, suppliers, and materials. Pre-aggregated summary tables are computed: supplier spend by year, supplier risk metrics, financial KPIs. This layer is optimized for fast reading and analytical queries.

Why does this split matter? Because analytical questions like "what was total USD spend for Nigerian suppliers in Q4 2024, broken down by material category?" require joining five transactional tables together. Against the warehouse, the same question is a single indexed lookup. The difference is seconds versus milliseconds at production scale.

The analytics engine (written in NumPy and pandas) reads from the warehouse layer, runs the Monte Carlo simulation and composite risk scoring, and writes the results back to the database. The Streamlit dashboard reads from both layers depending on context.

The whole stack is containerized with Docker. One command starts the application and the database together, with the correct versions, environment variables, and network configuration. This eliminates the "it works on my machine" problem entirely.

The CI/CD pipeline runs automated tests on every commit. This is not optional in a system where financial decisions depend on the calculations. If a code change breaks the risk score formula, the tests catch it before it reaches production.

This architecture was built to be maintainable by one person, deployable by a non-engineer, and accurate enough to trust with real procurement decisions.

#DataEngineering #StarSchema #Python #MySQL #Streamlit

---

## Post 7: The Scenario Planning Layer

The most common question in a procurement planning meeting is some version of: "what if."

What if the naira weakens by 20% next quarter?
What if we shift 30% of our NGN spend to USD-denominated suppliers?
What if we renegotiate payment terms with our top three suppliers?

In most organizations, answering these questions requires a financial analyst, a spreadsheet build, several assumptions that get debated for 20 minutes, and a result that arrives three days after the meeting when it is no longer relevant.

PVIS has a dedicated Scenario Planning page that makes these questions answerable in real time.

The FX stress test slider lets you input a rate change percentage (from -30% to +50%) and immediately see the recalculated total procurement costs for all FX-affected suppliers. The number is broken into a landed cost model: base materials cost, freight and insurance, import duties, FX impact, and payment delay carrying cost. You can see the component breakdown, not just a total.

The multi-scenario comparison table shows Base, Stress, and Optimized scenarios side by side, with the delta between each. You can walk into a meeting, open the dashboard, and say: "If NGN weakens 20%, here is the specific dollar impact per supplier, here is the total exposure, and here is what it would cost to hedge it." All with live data.

The per-supplier negotiation playbooks are generated directly from the risk scoring. A supplier with high cost variance gets a recommendation about fixed-price contracts. A supplier with high FX exposure gets a recommendation about currency denomination. A supplier with a high defect rate gets a recommendation about quality escrow provisions.

These are not generic suggestions. They are derived from each supplier's specific score profile.

The result is that procurement planning meetings shift from debating data to making decisions. The preparation that used to take a week happens in the background, continuously, so that the meeting time goes to judgment and action.

#ScenarioPlanning #Procurement #SupplyChainFinance #DataAnalytics #Manufacturing

---

## Post 8: Lessons From Building This

Ten months ago I started building a procurement analytics platform because I wanted to answer a question:

Is it possible to take all the analytical work that a procurement team does manually across spreadsheets and ERP export files, and automate it into a system that gives real-time answers instead of week-old reports?

The answer is yes. Here is what the process taught me.

**The hardest problem was data quality, not analysis.** The algorithms for Monte Carlo simulation and composite risk scoring are not trivial, but they are solvable with known techniques. The much harder challenge was designing the data pipeline so that any input, even a messy CSV from an ERP export, gets validated, normalized, and inserted correctly. A single row with a missing currency code can corrupt an entire FX exposure analysis. Data contracts and schema enforcement are not optional extras.

**The decision layer is more valuable than the visualization layer.** Pretty charts are easy to build. The hard thing is deciding what the chart should cause someone to do. Every visualization in PVIS was built backward from a specific decision. The Monte Carlo fan chart exists to support a hedging decision. The cost leakage waterfall exists to direct an audit. If you cannot name the decision an analysis supports, it is not analysis, it is decoration.

**Production-grade means making failure visible.** The system has a live FX rate that comes from an external API. That API can fail. There is a failover to a second API. That can also fail. In that case, the system degrades gracefully and shows the last known rate with a clear warning, rather than crashing the dashboard. Designing for failure modes is what separates a production system from a prototype.

**Simplicity is a feature.** The dashboard has no login, no role management, no complex configuration. You open it and it works. You can connect your own data via file upload directly from the browser. The entire stack runs with one Docker command. Making a complex system feel simple is one of the hardest engineering problems, and it is also one of the most valuable outcomes for the people who actually use the tool.

PVIS is open source and live on Streamlit Cloud. If you work in procurement analytics or supply chain finance and want to explore it, the link is in my profile.

#OpenSource #Procurement #DataScience #Python #LessonsLearned

---
