# FRED Series Catalog Outline

The following table captures the ten macroeconomic categories requested
by the stakeholder. Each category will eventually contain 50-100 vetted
FRED series. The present outline documents the curation status and notes
open questions that will be resolved prior to implementation of the
fetching logic.

| Category  | Description | Current Status | Next Actions |
| --------- | ----------- | -------------- | ------------ |
| GDP       | Aggregate output measures such as GDP, GDI, and potential GDP. | Placeholder entry created in `configs/fred_series_catalog.template.yaml`. | Compile full list of national accounts series and confirm seasonal adjustment preferences. |
| Labor     | Employment, unemployment, hours worked, participation rates. | Pending. | Identify BLS-based series (e.g., payrolls, unemployment rate) and ensure availability in FRED. |
| Prices    | Inflation, price indices, producer prices, deflators. | Pending. | Gather CPI, PCE, PPI, GDP deflators, and survey-based inflation expectations. |
| Health    | Healthcare expenditure, insurance coverage, health outcomes. | Pending. | Source data from CMS, BEA health satellite accounts, CDC series present in FRED. |
| Money     | Monetary aggregates, interest rates, credit measures. | Pending. | Confirm coverage of M1/M2, monetary base, bank credit, interest rates. |
| Trade     | Exports, imports, balance of trade, exchange rates. | Pending. | Assemble goods/services trade series and trade-weighted exchange rates. |
| Government| Fiscal revenue/expenditure, debt, budget balances. | Pending. | Collect Treasury statement series and NIPA government spending metrics. |
| Business  | Business sentiment, production, investment, inventories. | Pending. | Include ISM indices, industrial production components, capital goods orders. |
| Consumer  | Spending, confidence, credit, income distribution metrics. | Pending. | Combine retail sales, personal income/outlays, consumer credit series. |
| Housing   | Construction, sales, prices, mortgage data. | Pending. | Combine housing starts, permits, sales, price indices, mortgage rates. |
| Taxes     | Federal, state, and local tax receipts and rates. | Pending. | Identify FRED series sourced from BEA, Treasury, and IRS. |

The next iteration will expand this outline with the concrete list of
series identifiers, including validation that each FRED series is active
and up to date.
