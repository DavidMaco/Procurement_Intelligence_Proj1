# PVIS X (Twitter) Posts / Threads

---

## Thread 1: The Three Invisible Drains on Procurement Margins

**Tweet 1 (hook):**
Your factory buys from 8 suppliers across 4 countries in 5 currencies.

You think you know what everything costs.

You do not.

Here are the 3 invisible drains that are quietly destroying procurement margins in manufacturing. Thread.

---

**Tweet 2:**
1/ Currency volatility.

When the NGN drops 15% against the dollar, your procurement costs just went up 15% on all naira-denominated orders.

No price change from the supplier. No renegotiation. The money just disappears.

Most teams do not model this forward. They budget a flat rate and absorb the variance in the P&L.

---

**Tweet 3:**
2/ Supplier risk you cannot see yet.

"We have used them for 6 years" is not a risk assessment.

"Their defect rate went from 1.2% to 3.8% in 18 months" is.

By the time the gut feeling catches up to the data, you already have a production stoppage.

---

**Tweet 4:**
3/ Cost leakage against standard costs.

You have agreed prices (standard costs). You have what you actually paid (unit prices on POs).

The gap is cost leakage. At 1,952 line items across 50 materials, even 2% average overpayment is $100k/year nobody is looking for.

---

**Tweet 5:**
I built PVIS to surface all three in real time.

Monte Carlo FX simulation. Composite supplier risk scores. Automated cost leakage detection.

Live demo: davidmaco-pvis.streamlit.app
Open source on GitHub.

What does your team currently use to model FX exposure?

---

## Thread 2: Monte Carlo FX Simulation Explained Simply

**Tweet 1 (hook):**
"What will the exchange rate be in 90 days?"

Wrong question.

The right question: "What is the full distribution of possible rates in 90 days, and what is the worst 5% of them going to cost me?"

Here is how Monte Carlo simulation answers that. Simple version.

---

**Tweet 2:**
You take 3 years of daily FX data.

Calculate the daily % change (log return) for each day.

Now you have a history of how this currency actually moves day to day.

That history is your model.

---

**Tweet 3:**
Now simulate.

Start at today's rate. Make 90 random daily moves drawn from that history. Record the final rate after 90 days.

That is 1 simulation.

Run it 10,000 times.

You now have 10,000 possible futures.

---

**Tweet 4:**
Take the 5th percentile of all those futures.

That is your worst-case planning scenario. 95% of simulations ended better than this.

Take the 50th percentile: your central estimate.

Take the 95th: your optimistic case.

The spread is your uncertainty band.

---

**Tweet 5:**
The extra step PVIS adds: regime detection.

Currencies are not always equally volatile. There are calm periods and crisis periods.

Fitting one model to both gives you parameters that describe neither accurately.

PVIS fits separate models to each regime, then weights them by historical frequency.

---

**Tweet 6:**
The result: a number you can act on.

"There is a 5% chance FX exposure costs us $X more than today's rate implies in the next 90 days."

That sentence supports a hedging decision.

An average forecast cannot tell you that.

Live demo: davidmaco-pvis.streamlit.app

---

## Thread 3: How to Score Supplier Risk With Actual Data

**Tweet 1 (hook):**
If I ask you which of your suppliers is most likely to stop your production line in the next 6 months, what do you say?

If the answer is based on a relationship, a gut feel, or a recent incident, you are missing something.

Here is how to do it with data.

---

**Tweet 2:**
6 factors. Each scored 0 to 1. Combined with weights.

1. On-time delivery rate (22%)
2. Defect rate (20%)
3. Cost variance (18%)
4. FX exposure % (18%)
5. Lead time consistency (12%)
6. Geographic risk index (10%)

---

**Tweet 3:**
Why OTD at 22%?

Because late delivery is the fastest path to a production stoppage. It is the most direct, most immediate, most operationally painful failure mode.

Defect rate at 20% for similar reasons: quality failures mean line holds and rework.

---

**Tweet 4:**
Why cost variance at 18%?

A supplier whose prices bounce around is a budget management problem AND a negotiation signal.

Inconsistent pricing usually means one thing: there is room to lock in fixed terms. High variance = start that conversation.

---

**Tweet 5:**
Why geographic risk at only 10%?

It is a background probability, not an operational measurement.

A country with elevated political risk might never affect your specific supplier. The other 5 factors are continuously updated from actual transaction data.

---

**Tweet 6:**
The output is not just a rank.

PVIS generates per-supplier negotiation playbooks.

Cost variance high: "Consider fixed-price contract terms."
FX exposure high: "Explore USD-denominated invoicing."
OTD low: "Request delivery performance clause."

Data to decision.

---

## Thread 4: The Cash Conversion Cycle Is a Procurement Problem

**Tweet 1 (hook):**
Most procurement managers know how to negotiate price.

Far fewer think about payment terms as a working capital lever.

That is leaving real money on the table. Let me show you how much.

---

**Tweet 2:**
The Cash Conversion Cycle (CCC):

CCC = DIO - DPO

DIO: how many days of inventory you hold on average.
DPO: how many days before you pay suppliers after receiving goods.

Lower CCC means less of your cash is frozen in the supply chain.

---

**Tweet 3:**
Procurement controls DPO directly.

If you currently pay suppliers in 30 days and renegotiate to 45 days, you have delayed two weeks of outgoing cash per payment cycle.

At $5M annual procurement spend: ~$208,000 in working capital freed.

From one conversation. Per supplier.

---

**Tweet 4:**
Procurement also influences DIO indirectly.

Unreliable suppliers with high lead time variance force you to hold more safety stock.

More safety stock = higher DIO = larger CCC.

A supplier who cuts their lead time variability by 60% lets you reduce buffer inventory.

---

**Tweet 5:**
PVIS models this live.

Working capital page shows current DIO, DPO, and CCC.

Scenario modeler: "What if we extend payment terms from 30 to 45 days with our top 3 suppliers?" Instant calculation.

The math is done before the negotiation meeting. You walk in knowing exactly what to ask for.

---

## Thread 5: Why Your Procurement Spreadsheet Cannot Find Cost Leakage

**Tweet 1 (hook):**
You have agreed prices for every material you buy.

You have what you actually paid on every PO.

The gap is cost leakage.

At $5M annual procurement spend, 3% average overpayment is $150,000/year leaving the business silently.

Nobody is looking for it. Here is why.

---

**Tweet 2:**
Manual comparison of unit prices against standard costs means opening the PO export, pulling the standard cost catalog, writing VLOOKUP formulas across 1,952 rows, checking for matches, flagging variances.

At best, this happens quarterly.

Three months of leakage before anyone notices.

---

**Tweet 3:**
PVIS calculates this automatically on every pipeline run.

For every line item: (actual unit price - standard cost) x quantity.

If positive: leakage.

Aggregated by material category. Sorted by total leakage. Displayed as a waterfall chart.

---

**Tweet 4:**
The output changes the conversation.

Not "do we have a cost leakage problem?" (no one knows)

But: "packaging materials: $47K over standard. Steel and metals: $22K over standard. Electronics: within tolerance."

Now you have an audit target and a supplier conversation with a specific number.

---

**Tweet 5:**
This is what automation is actually for.

Not replacing analysts.

Removing the manual work that prevents analysts from doing the analysis that matters.

PVIS is open source: github.com/DavidMaco/pvis

---

## Thread 6: Star Schema vs Raw Tables (Why It Matters for Analytics Speed)

**Tweet 1 (hook):**
"Our dashboards are too slow."

99% of the time, the real problem is not the visualization library or the server size.

It is the data architecture.

Here is the difference between analyzing raw transactional data and a star schema, in plain English.

---

**Tweet 2:**
Raw normalized tables are great for recording transactions accurately.

Answering "total USD spend by supplier country by quarter for 3 years" requires joining 5 tables: orders, line items, suppliers, countries, currencies.

Plus a lookup of exchange rates by date to convert.

---

**Tweet 3:**
A star schema pre-computes those joins.

One fact table with one row per PO line item, already converted to USD.

Joined to dim_date, dim_supplier, dim_material.

The question that needed 5 joins now needs 2.

At 1M rows: seconds vs milliseconds.

---

**Tweet 4:**
PVIS runs an ETL pipeline between the two layers.

Raw data lives in 19 normalized transactional tables (accuracy optimized).

The warehouse layer has the star schema + pre-aggregated summary tables (speed optimized).

ETL runs on demand. Takes under 30 seconds on 3 years of data.

---

**Tweet 5:**
The lesson: analytical speed is a design decision, not a hardware problem.

If your dashboards are slow, look at the query layer before looking at the server specs.

Nine times out of ten, the fix is architecture, not more compute.

---

## Thread 7: Building a Production Analytics Tool: What Nobody Tells You

**Tweet 1 (hook):**
I spent months building a procurement analytics platform from scratch.

Here are the things that bit me that nobody told me about upfront.

Thread.

---

**Tweet 2:**
1. Data validation is 3x harder than the analysis.

The Monte Carlo simulation took me two days to write.

The data import validation pipeline took me two weeks.

Bad input data does not fail loudly. It produces plausible-looking wrong answers. That is much worse than a crash.

---

**Tweet 3:**
2. Build for the decision, not the chart.

I built several very impressive visualizations early on that went into the final version.

I also built several impressive visualizations that got cut because nobody could name a decision they would support.

If you cannot name the decision, cut the chart.

---

**Tweet 4:**
3. SQL injection is still a thing in Python.

Several early queries used f-string interpolation for parameter insertion.

That is a SQL injection vulnerability in a financial analytics system.

All of them got refactored to parameterized queries. Start with parameterized queries. Always.

---

**Tweet 5:**
4. Demo mode is not an afterthought.

I built demo mode (synthetic data when no DB is connected) as a practical necessity.

It became the main way people explore the app.

Zero-setup exploration dramatically lowers the barrier to evaluation.

---

**Tweet 6:**
5. The architecture decision that matters most is the one you make week 1.

Separating the analytics module from the dashboard code was the right call.

It made testing possible, made the Power BI integration easy, and made the codebase maintainable.

Structure early. Refactoring later is expensive.

---

## Thread 8: 8 Pages, 8 Decisions

**Tweet 1 (hook):**
PVIS has 8 dashboard pages.

Each one exists because it enables a specific decision.

Here is the decision each page was built for.

Thread.

---

**Tweet 2:**
Page 1: Executive Summary

Decision: Is our procurement health acceptable right now and what needs my attention today?

Live KPIs, risk heatmap, top risk suppliers, monthly spend trend. Everything on one screen. Opens the meeting.

---

**Tweet 3:**
Page 2: FX Volatility and Monte Carlo

Decision: Should we hedge our FX exposure, and if so how much?

P5/P50/P95 fan chart, VaR, CVaR. Live rate. Configurable horizon and simulation count. The number that belongs in a CFO conversation.

---

**Tweet 4:**
Page 3: Supplier Risk Analysis

Decision: Which supplier needs a contract renegotiation conversation, and what specifically should we change?

Ranked risk scores with factor decomposition. Per-supplier action playbooks. Brings the analysis into the negotiation.

---

**Tweet 5:**
Page 4: Spend and Cost Analysis

Decision: Where is money leaking against standard cost, and where is spend concentration building?

Cost leakage waterfall. Spend concentration by supplier and category. Year-over-year comparison. Points the audit team at the right target.

---

**Tweet 6:**
Page 5: Working Capital

Decision: How much working capital can we free by extending payment terms, and which suppliers to prioritize?

DIO, DPO, CCC live calculation. Scenario modeler for payment term changes. Connects the procurement negotiation to the treasury goal.

---

**Tweet 7:**
Page 6: Scenario Planning

Decision: What is the dollar impact of a specific FX shock on our procurement costs by supplier?

-30% to +50% slider. Landed cost model breakdown. Multi-scenario comparison table. Answers "what if" in real time.

---

**Tweet 8:**
Pages 7 and 8: Company Data Upload and Pipeline Runner

Decision: Can I run this on my actual data, not synthetic data?

Drag-and-drop CSV upload with validation. One-click pipeline re-run. The answer is yes.

Live demo: davidmaco-pvis.streamlit.app

---
