# FRED Series Catalog Outline

The following table captures the ten macroeconomic categories requested
by the stakeholder. Each category will contain 50-100 vetted FRED series
selected via the automated tag-based catalog generator.

| Category  | Description | Status | Next Actions |
| --------- | ----------- | ------ | ------------ |
| GDP       | Aggregate output measures such as GDP, GDI, and potential GDP. | Tag recipe defined; generator fetches top series under the `gdp` tag. | Review generated catalog and pin any mandatory inclusions/exclusions. |
| Labor     | Employment, unemployment, hours worked, participation rates. | Tag recipe defined (`employment` + `unemployment`). | Validate coverage of BLS headline indicators; refine tags if needed. |
| Prices    | Inflation, price indices, producer prices, deflators. | Tag recipe defined (`inflation`). | Evaluate inclusion of survey expectations; adjust generator filters. |
| Health    | Healthcare expenditure, insurance coverage, health outcomes. | Tag recipe defined (`health`). | Augment with priority health expenditure series if missing. |
| Money     | Monetary aggregates, interest rates, credit measures. | Tag recipe defined (`money`, `monetary`). | Ensure inclusion of Fed balance sheet aggregates; tweak tags as required. |
| Trade     | Exports, imports, balance of trade, exchange rates. | Tag recipe defined (`trade`). | Review for key bilateral balances and trade-weighted indexes. |
| Government| Fiscal revenue/expenditure, debt, budget balances. | Tag recipe defined (`government`). | Confirm Treasury receipts/outlays presence; expand tags if gaps remain. |
| Business  | Business sentiment, production, investment, inventories. | Tag recipe defined (`business`). | Incorporate targeted survey series (e.g., ISM) via supplemental tags. |
| Consumer  | Spending, confidence, credit, income distribution metrics. | Tag recipe defined (`consumer`). | Verify consumption, income, credit coverage; refine as necessary. |
| Housing   | Construction, sales, prices, mortgage data. | Tag recipe defined (`housing`). | Add explicit mortgage rate series if excluded. |
| Taxes     | Federal, state, and local tax receipts and rates. | Tag recipe defined (`taxes`). | Review generated list for revenue vs. rate balance; adjust accordingly. |

After reviewing the automatically generated catalog, update
`configs/fred_catalog_sources.yaml` with additional tags or overrides to
lock in the final 50-100 indicators per category.
