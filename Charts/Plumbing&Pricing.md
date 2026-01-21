# 

# **Plumbing & Pricing**

# **Monetary Macro for Cross-Asset Signal Generation**

## **Introduction: From Opaque Pipes to Actionable Signals**

The global financial system is underpinned by a vast, intricate, and often opaque network of institutions and markets responsible for the daily movement of trillions of dollars in capital. This network, frequently referred to as "monetary plumbing," serves as a powerful metaphor for the critical, behind-the-scenes infrastructure—the institutional "pipes and valves"—that facilitates the essential flows of credit, capital, and financial risk.1 This framework, which includes money markets, payment systems, and clearinghouses, is the foundation upon which all modern financial transactions rest. While this infrastructure operates largely unseen during periods of market calm, its resilience and design become critically important during periods of stress, when it determines the scope for both risk-mitigating and harmful actions.1

The central thesis of this report is that the state of this plumbing is not merely a technical concern for operations specialists but is an active and potent source of high-frequency macroeconomic signals. Strains within these core funding markets—manifesting as liquidity shortages, funding rate volatility, or intermediary balance sheet constraints—propagate through the entire financial ecosystem, directly impacting the pricing and availability of leverage and collateral across all asset classes.1 By systematically monitoring a curated set of these plumbing indicators, it is possible to construct a quantifiable, data-driven framework that provides leading indicators for risk and opportunity.

The monetary plumbing network is composed of several key types of institutions, each playing a distinct and interdependent role. At the apex is the central bank, the Federal Reserve, which acts as the ultimate source of liquidity and the primary regulator.1 Forming the central hubs of the network are the Primary Dealer banks, which serve as the main counterparties for the Fed's operations and as the critical intermediaries connecting cash-rich institutions with those in need of funding or leverage.1 Major providers of cash include Money Market Mutual Funds (MMFs), which pool investments and are the largest net lenders into the short-term funding markets.1 The primary borrowers of both cash and specific securities are hedge funds and other leveraged investors, whose demand for leverage is a key driver of activity.1 Finally, Financial Market Infrastructures (FMIs) like clearinghouses and custodian banks form the operational backbone, providing the systems for clearing, settling, and managing collateral for trillions of dollars in daily transactions.1 The interactions between these participants, governed by their balance sheet constraints and economic incentives, generate the price and quantity signals that this report seeks to decode.

| Participant | Primary Role | Key Motivation | Market Impact |
| :---- | :---- | :---- | :---- |
| **Federal Reserve** | Monetary policy implementation; Lender/Borrower of last resort 1 | Achieve dual mandate (price stability, max employment) 1 | Sets the "rules of the game" via administered rates and facilities; provides/absorbs ultimate liquidity. |
| **Primary Dealers** | Market-maker; Intermediary; Fed counterparty 1 | Intermediation profit (bid-ask spread); Financing inventory 1 | Central nodes connecting cash and collateral. Their balance sheet capacity dictates market liquidity. |
| **Money Market Funds** | Major cash lender in repo market 1 | Earn a safe, liquid yield on cash balances 1 | Largest source of private funding for dealers. Their allocation decisions (repo vs. ON RRP) are a key signal. |
| **Hedge Funds / Leveraged Investors** | Cash borrower in repo; Security borrower in securities lending 1 | Finance long positions; Execute short sales & arbitrage 1 | Primary source of demand for leverage and specific securities, driving prices in both markets. |
| **Financial Market Infrastructures** | Clearing, settlement, collateral management 1 | Reduce risk; increase operational efficiency 1 | Mitigate counterparty risk; enable high-volume, standardized trading in markets like tri-party and GCF repo. |

## **Section I: The Monetary Policy & Funding Conditions Dashboard**

To begin extracting signals from the monetary plumbing, one must first establish a baseline understanding of its foundational price signals. This section visualizes the key money market interest rates relative to the Federal Reserve's intended policy stance. The Fed's operational framework has undergone a fundamental shift since the 2008 Global Financial Crisis. The pre-crisis "scarce reserves" system, where the Fed actively managed the daily supply of bank reserves, was rendered obsolete by the massive liquidity injections of Quantitative Easing (QE).1 The current "ample reserves" framework operates not by controlling the quantity of reserves, but by steering its key policy rate—the Effective Federal Funds Rate (EFFR)—into a target range by setting a corridor of administered rates that influence the incentives for financial institutions to lend and borrow.1 Deviations from this intended policy corridor are the clearest first-order signal of market stress.

The modern toolkit is best understood as a "floor and ceiling" system. The floor is established by two key rates: the Interest on Reserve Balances (IORB), which is the rate the Fed pays banks on their deposits, and the Overnight Reverse Repo (ON RRP) facility rate, which offers a risk-free investment for non-bank cash lenders like MMFs.1 The ceiling is formed by facilities that provide liquidity to prevent rates from spiking, chiefly the Standing Repo Facility (SRF) and the traditional Discount Window.1 The most potent signals of plumbing stress, therefore, emerge when market-determined rates deviate significantly from their intended positions within this corridor.

| Policy Tool | Purpose | Eligible Counterparties | Market Impact | Role in Policy Corridor |
| :---- | :---- | :---- | :---- | :---- |
| **Interest on Reserve Balances (IORB)** | Sets a reservation rate for banks, influencing their willingness to lend in private markets. | Depository Institutions | Acts as a soft ceiling for the EFFR. | Upper Bound |
| **Overnight Reverse Repo (ON RRP) Facility** | Provides a risk-free investment alternative for non-bank cash lenders. | Primary Dealers, MMFs, GSEs | Acts as a hard floor for overnight secured rates like SOFR. | Lower Bound / Floor |
| **Standing Repo Facility (SRF)** | Acts as a backstop source of liquidity for dealers against high-quality collateral. | Primary Dealers, Depository Institutions | Designed to cap upward spikes in repo rates during stress events. | Ceiling / Backstop |
| **Discount Window** | Serves as a lender-of-last-resort facility for depository institutions. | Depository Institutions | Provides liquidity against a broad range of collateral to mitigate funding stress. | Ultimate Ceiling / Backstop |

### **Chart 1: The Federal Reserve's Policy Corridor**

\!(placeholder\_chart\_1.png)

#### **WHAT IT IS**

This chart provides a visualization of the primary overnight funding rates relative to the Federal Reserve's target range and its key administered rates, which form a policy "corridor".1 The rates plotted are the Effective Federal Funds Rate (EFFR), the primary unsecured policy rate targeted by the FOMC 1; the Overnight Bank Funding Rate (OBFR), a broader measure of unsecured bank funding costs 1; and the Secured Overnight Financing Rate (SOFR), the broadest measure of the cost of borrowing cash overnight collateralized by U.S. Treasury securities.1 The corridor is defined by the ON RRP offering rate as the floor and the Standing Repo Facility (SRF) rate as the ceiling.1

#### **WHY IT MATTERS**

This chart offers an immediate, high-level assessment of the Federal Reserve's control over short-term interest rates. In the current "ample reserves" framework, the Fed's ability to keep market rates within this corridor is the primary mechanism for implementing monetary policy.1 A breakdown in this relationship, where market rates either fall through the floor or breach the ceiling, is a clear indication of a significant mismatch between policy intent and market reality, signaling dysfunction within the financial plumbing.1 The stability of this corridor is the bedrock upon which global dollar funding markets are built.

#### **HOW TO INTERPRET THE CHART**

* **Normal Conditions:** In a well-functioning market, the unsecured EFFR should trade very close to the IORB rate, as banks have little incentive to lend reserves to each other for less than they can earn risk-free from the Fed. The secured SOFR should trade slightly below EFFR (reflecting its lower risk) but comfortably above the ON RRP rate, which acts as a floor for MMFs. All rates should remain well-contained within the shaded corridor.1  
* **Stress Signal (Scarcity of Cash):** A sustained upward drift of market rates, especially SOFR, away from the ON RRP floor and toward the IORB and SRF ceiling is a powerful signal of tightening liquidity. It indicates a shortage of cash relative to the amount of collateral needing to be financed, forcing borrowers to bid up rates aggressively. This dynamic was a key leading indicator of mounting pressure in the months before the September 2019 repo market spike.1  
* **Stress Signal (Glut of Cash / Clogged Pipes):** Market rates, particularly SOFR, becoming "pinned" to or even trading below the ON RRP floor indicates an excess of cash that the private dealer community is unable or unwilling to absorb. This is often not a sign of a healthy market but rather a symptom of dealer balance sheet constraints, which prevent them from intermediating the excess liquidity.1

#### **THE CURRENT READING**

As of August 8, 2025, the key rates are as follows: the EFFR is 4.33% 7, the OBFR is 4.33% 8, and SOFR is 4.35%.4 The policy corridor is defined by the ON RRP offering rate of 4.25% 9 and the SRF minimum bid rate of 4.50%.6 The current configuration shows all key funding rates trading in a tight cluster, well within the bounds of the Fed's policy corridor. SOFR, at 4.35%, is positioned above the ON RRP floor and below the SRF ceiling, indicating a balanced state of liquidity where private markets are functioning without undue stress. The unusual reading is that the secured rate (SOFR) is trading slightly above the unsecured rates (EFFR/OBFR). While this deviates from the typical risk premium hierarchy, it does not suggest broad systemic stress and is likely due to idiosyncratic, technical factors related to the composition of each rate's underlying transactions.

#### **THE GLOBAL MACROECONOMIC & CROSS-ASSET TRADING IMPLICATIONS**

The current stability within the policy corridor is a positive signal for global markets, indicating that the Fed has firm control over the front end of the U.S. yield curve. This anchors global dollar funding costs and reduces the risk of unexpected liquidity shocks, providing a supportive backdrop for risk assets such as equities and corporate credit. Traders should monitor for any sustained upward drift of SOFR toward the SRF rate. Such a move would be a leading indicator of tightening liquidity conditions, which could precede a sell-off in equities and a widening of credit spreads, as the cost of leverage for the entire financial system would be rising. Conversely, should SOFR become pinned to the ON RRP rate for a prolonged period, especially along with high ON RRP facility usage, it would imply that dealer balance sheets are clogged. This could lead to underperformance in assets that rely heavily on dealer intermediation, such as complex derivatives and less-liquid corporate bonds, as market-making capacity would be impaired.

### **Chart 2: The Systemic Risk Barometer: Secured vs. Unsecured Funding Spreads**

\!(placeholder\_chart\_2.png)

#### **WHAT IT IS**

This chart displays the spread, measured in basis points, between the average rate at which banks lend to each other on an *unsecured* basis (the Overnight Bank Funding Rate, OBFR) and the average rate for loans *secured* by U.S. Treasury collateral (the Secured Overnight Financing Rate, SOFR).1 The calculation is simply

OBFR−SOFR.

#### **WHY IT MATTERS**

This spread is a direct, real-time measure of perceived counterparty credit risk and systemic stress within the core of the banking system. Because SOFR transactions are collateralized by U.S. Treasury securities, they are considered nearly risk-free.1 Therefore, any premium that lenders demand to provide funding on an unsecured basis in the OBFR market represents direct compensation for the risk that the borrowing bank might default. In essence, this spread is the market's "fever chart" for interbank credit risk and is a powerful barometer of financial stability.1

#### **HOW TO INTERPRET THE CHART**

* **Low & Stable Spread:** A narrow and stable spread, typically a few positive basis points, indicates a healthy, high-trust environment. It signals that banks are confident in each other's solvency and are willing to lend to one another on an unsecured basis for a minimal premium over the risk-free collateralized rate. This is the hallmark of normal market functioning.1  
* **Widening Spread:** A sharp and sustained increase in the spread is a classic "flight to quality" signal and a major red flag for systemic risk. It indicates that lenders are becoming fearful of counterparty defaults and are consequently withdrawing from the unsecured market in favor of the safety of the collateralized repo market. This dynamic causes unsecured rates to spike while secured rates remain stable or even fall, blowing out the spread. This was a key feature of the 2008 financial crisis and the March 2020 "dash for cash".1

#### **THE CURRENT READING**

As of August 8, 2025, the latest OBFR is 4.33% 8 and the latest SOFR is 4.35%.4 This results in a current OBFR-SOFR spread of \-2 basis points (

4.33%−4.35%). A negative spread is atypical but definitively indicates the absence of any systemic credit risk premium being priced into the interbank market. The market is not demanding extra compensation for lending unsecured to banks. In fact, technical factors are making secured funding slightly more expensive than unsecured funding at the margin. From a systemic risk perspective, the signal is "all clear."

#### **THE GLOBAL MACROECONOMIC & CROSS-ASSET TRADING IMPLICATIONS**

This spread is one of the most potent risk-off indicators available to macro and cross-asset traders. A significant widening is a powerful signal to implement defensive portfolio strategies.

* **Fixed Income:** A widening spread is a strong signal to reduce credit risk by selling corporate bonds (particularly high-yield and financials) and increasing allocations to safe-haven government bonds. It often precedes a general widening of all credit default swap indices, such as CDX and iTraxx.  
* **Equities:** A widening OBFR-SOFR spread is a clear signal to reduce equity exposure, especially in cyclical sectors and financial stocks, which are most sensitive to banking system stress. Capital would be expected to rotate into defensive sectors like consumer staples and utilities, or into cash.  
* **Currencies:** A widening spread signals a surge in global demand for U.S. dollar liquidity as a safe haven. This typically leads to broad-based USD strength against most other G10 and emerging market currencies. The spread can be viewed as a real-time proxy for the "dollar smile" theory, where the dollar strengthens in both risk-on environments (driven by U.S. economic outperformance) and severe risk-off environments (driven by a flight to safety).

### **Chart 3: Private Market Funding Pressure: SOFR vs. The ON RRP Floor**

\!(placeholder\_chart\_3.png)

#### **WHAT IT IS**

This chart measures the premium, in basis points, that cash lenders (primarily Money Market Funds) can earn by lending into the private repurchase agreement (repo) market versus parking their cash in the Federal Reserve's risk-free Overnight Reverse Repo (ON RRP) facility.1 The spread is calculated as the Secured Overnight Financing Rate (SOFR) minus the ON RRP Award Rate (

SOFR−RRPONTSYAWARD).4

#### **WHY IT MATTERS**

The ON RRP rate acts as a hard floor for the money market system because it is available to a wide range of non-bank participants who are ineligible to earn the IORB rate.1 An MMF has no economic incentive to lend cash to a private dealer in the repo market for a rate lower than what it can receive from the Federal Reserve with zero counterparty risk.1 Therefore, this spread is a pure, market-driven measure of the supply and demand balance for cash versus collateral in the private market. It quantifies how much dealers and other private borrowers must bid up their funding rates to attract cash away from the Fed's perfectly safe alternative.

#### **HOW TO INTERPRET THE CHART**

* **Spread Near Zero:** A very narrow or even negative spread indicates a glut of cash chasing scarce high-quality collateral, or a lack of dealer balance sheet capacity to intermediate more funds. When the spread is near zero, it signals that cash lenders have few attractive private market options, so they are content to use the Fed's facility, which effectively "pins" private market rates to the policy floor.1  
* **Positive & Widening Spread:** A rising spread is a clear signal that funding conditions are tightening. It means that dealers are competing more aggressively for cash to finance their securities inventories, forcing them to offer higher rates to entice MMFs away from the risk-free ON RRP. A sustained rise in this spread is an unambiguous signal that liquidity in the private market is becoming scarcer relative to demand.1

#### **THE CURRENT READING**

As of August 8, 2025, the latest SOFR is 4.35% 4, and the latest ON RRP Award Rate is 4.25%.9 The resulting spread is a healthy \+10 basis points (

4.35%−4.25%). This positive spread indicates that the private repo market is functioning effectively, offering a sufficient premium over the Fed's floor to attract the necessary cash for funding activities. The market is in a balanced state, neither exhibiting signs of a cash glut (which would compress the spread to zero) nor acute funding stress (which would cause the spread to widen dramatically).

#### **THE GLOBAL MACROECONOMIC & CROSS-ASSET TRADING IMPLICATIONS**

This spread serves as a subtle but powerful leading indicator of underlying market health. A persistent compression of the spread toward zero, especially when ON RRP balances are high, suggests the plumbing is becoming "clogged." This indicates that dealer balance sheet capacity is constrained, which could impair their ability to provide liquidity and make markets during even minor stress events. This is a negative signal for market depth across all asset classes and could lead to higher transaction costs and increased "gap risk."

Conversely, a sharp and sustained widening of this spread is a more immediate warning sign of funding stress. It implies that the marginal cost of leverage is rising for the financial system's most important market makers. This would be a catalyst for leveraged players to reduce risk, trim positions in less-liquid assets (such as off-the-run corporate bonds or emerging market debt), and anticipate higher volatility across the board. For those monitoring the Fed's balance sheet policy, a sustained rise in the SOFR-RRP spread is a key signal that Quantitative Tightening (QT) is beginning to "bite" by draining meaningful reserves from the banking system.

## **Section II: The Anatomy of System-Wide Liquidity**

Moving beyond the price signals of interest rates, this section analyzes the underlying quantity drivers of liquidity within the financial plumbing. To achieve a comprehensive understanding, one must dissect the Federal Reserve's balance sheet, which provides a transparent record of its interventions and their impact on the money supply. A single actor does not determine the level of bank reserves—the ultimate measure of liquidity within the core banking system— but is the residual outcome of the interaction between Federal Reserve asset holdings, Treasury fiscal operations, and money market fund investment decisions. This relationship can be summarized in a simple but powerful "liquidity equation" 1:

$$ \\Delta \\text{Bank Reserves} \\approx \\Delta \\text{Fed Assets} \- \\Delta \\text{ON RRP} \- \\Delta \\text{TGA} \- \\Delta \\text{Currency} $$

This equation demonstrates that the level of bank reserves is determined by the interplay of Fed policy (changes in assets via QE or QT), money market fund behavior (changes in ON RRP usage), and fiscal operations (changes in the Treasury General Account, or TGA). By tracking these key components, an analyst can construct a real-time model of the net injection or withdrawal of liquidity from the banking system, providing a forward-looking view of funding conditions.1

### **Chart 4: The Liquidity Equation in Practice: Drivers of Bank Reserves**

\!(placeholder\_chart\_4.png)

#### **WHAT IT IS**

This chart provides a visual representation of the major liabilities on the Federal Reserve's balance sheet that directly impact private sector liquidity. It illustrates the core accounting identity that the Fed's assets (such as bonds purchased during QE, tracked by FRED ticker WALCL) must be financed by its liabilities.1 The key non-reserve liabilities are physical currency in circulation, the U.S. Treasury's checking account (Treasury General Account or TGA, FRED: WDTGAL), and deposits from money market funds via the ON RRP facility (FRED: RRPONTSYD).1 The residual balancing item is commercial bank reserves (Reserve Balances with Federal Reserve Banks, FRED: WRBWFRBL).1

#### **WHY IT MATTERS**

This chart provides a holistic, dynamic view of the sources and uses of system-wide liquidity. It is critically important because it shows that the level of bank reserves—the ultimate high-powered money for the banking system—is not a direct policy choice but the *residual outcome* of other, often volatile, factors.1 This framework allows an analyst to decompose any change in banking system liquidity and attribute it to its root cause: intentional Fed policy (a change in assets), fiscal policy and debt management (changes in the TGA), or shifts in private market risk appetite and intermediation capacity (changes in ON RRP usage).1

#### **HOW TO INTERPRET THE CHART**

* **Rising TGA or ON RRP Balances:** A rise in either of these components acts as a direct drain on liquidity from the private banking system. When the Treasury collects taxes or sells bonds, cash moves from commercial bank accounts to the TGA, causing a corresponding drop in bank reserves. Similarly, when MMFs place cash in the ON RRP, that liquidity is removed from the private market, also reducing bank reserves.1  
* **Falling TGA or ON RRP Balances:** Conversely, a fall in these balances represents a direct injection of liquidity into the banking system. When the Treasury spends money, the TGA falls and bank reserves rise. When MMFs pull cash from the ON RRP to invest in the private market, bank reserves also tend to rise.  
* **Quantitative Tightening (QT) Dynamics:** During a QT program, the Fed's total assets decline. This chart is essential for diagnosing *how* this liquidity drain is being absorbed. In the initial stages of QT, the drain is often absorbed by a decrease in the ON RRP balance, which acts as a buffer. Once this buffer is depleted, any further decline in Fed assets will cause a direct, one-for-one drop in bank reserves, representing a much more potent and potentially disruptive phase of monetary tightening.1

#### **THE CURRENT READING**

Based on the latest available weekly data from early August 2025, the Treasury General Account (WDTGAL) stands at approximately $464.3 billion.14 The most recent monthly data for Total Reserves (TOTRESNS) for June 2025 was $3,355.7 billion, though the weekly series (WRBWFRBL) is more appropriate for this high-frequency analysis.16 The ON RRP facility (RRPONTSYD) balance is currently low, cited in examples as being under $100 billion, a significant decline from its multi-trillion dollar peak.17 The analysis of the chart would focus on the week-over-week changes. A rise in the TGA, for instance, would be identified as a primary driver of any concurrent fall in bank reserves, independent of Fed asset sales. The system remains in an "ample reserves" regime, but the depletion of the ON RRP buffer means that future liquidity drains from QT or TGA growth will now have a more direct impact on bank reserve levels.

#### **THE GLOBAL MACROECONOMIC & CROSS-ASSET TRADING IMPLICATIONS**

This chart provides a forward-looking view on financial conditions that is independent of Fed rate policy. A rapid, unexpected rise in the TGA—such as what occurs after a debt ceiling resolution triggers a flood of T-bill issuance—acts as a de facto monetary tightening that can catch markets off guard and is broadly negative for risk assets.1 Monitoring the decline in the ON RRP balance during a QT cycle is crucial for asset allocators. As the ON RRP approaches zero, it signals that the most benign phase of QT is over. The subsequent direct drain on bank reserves is likely to put more significant and sustained upward pressure on funding rates like SOFR, leading to higher market volatility, a stronger dollar, and underperformance of assets most sensitive to liquidity conditions, such as emerging market equities and high-yield credit. This framework allows traders to anticipate when QT will begin to "bite," potentially front-running the market's reaction to tightening liquidity.

### **Chart 5: A Proxy for Dealer Balance Sheet Constraint: Money Market Fund Cash Allocation**

\!(placeholder\_chart\_5.png)

#### **WHAT IT IS**

This chart tracks the critical allocation decisions of Money Market Funds, which represent the single largest pool of cash in the U.S. funding markets.1 It displays the daily volume of cash that MMFs and other eligible counterparties are placing in the Federal Reserve's Overnight Reverse Repo (ON RRP) facility (FRED: RRPONTSYD).1 This is contextualized by plotting it against the total assets under management (AUM) of government MMFs, the primary users of the facility.20

#### **WHY IT MATTERS**

The ON RRP usage level has become the single best high-frequency, inverse proxy for primary dealer balance sheet capacity and private market intermediation health.1 When dealers are constrained by regulations like the Supplementary Leverage Ratio (SLR), they are unable or unwilling to take on more low-spread repo financing from MMFs because it expands their total assets.1 With their primary private-market investment outlet unavailable, the cash from MMFs has nowhere else to go and flows into the Fed's ON RRP facility by default. Therefore, a high and persistent ON RRP balance is a direct, quantifiable signal that the private financial plumbing is "clogged," with diminished capacity for intermediation.1

#### **HOW TO INTERPRET THE CHART**

* **High & Persistent ON RRP Balance:** An elevated level of ON RRP usage, particularly as a high percentage of total MMF AUM, indicates that dealer balance sheets are constrained. The system is flush with cash, but the "pipes" to move that cash through private markets are narrow. This suggests a fragile market structure that is vulnerable to shocks.  
* **Rapidly Falling ON RRP Balance:** A sharp decline in the facility's balance indicates that cash is being pushed out of the Fed's facility and back into the private market. This typically occurs for two reasons: either the Treasury is issuing a large volume of T-bills (which MMFs buy as an alternative to the RRP), or dealer balance sheet capacity has improved, allowing them to take on more repo financing. This dynamic puts downward pressure on short-term bill yields and signals a normalization of funding markets.1

#### **THE CURRENT READING**

As of the week ending August 6, 2025, total MMF assets stood at $7.15 trillion, with government MMFs accounting for $5.83 trillion.20 Daily ON RRP usage has been cited in recent examples at levels below $100 billion (e.g., $80.3 billion or $91.97 billion).18 This represents a dramatic decline from the facility's peak usage of nearly $2.7 trillion in late 2022\.19 The current ON RRP balance represents a very small fraction of total government MMF assets. This implies that dealer balance sheet constraints are not a primary concern at this moment. The vast majority of MMF cash is finding a home in private market instruments, likely a combination of private repo and short-term Treasury bills. The "clog" that led to the massive run-up in the facility's use appears to have been cleared.

#### **THE GLOBAL MACROECONOMIC & CROSS-ASSET TRADING IMPLICATIONS**

A low ON RRP balance is generally a positive sign for market liquidity and functioning. It suggests that primary dealers have ample capacity to make markets, provide leverage, and intermediate flows, which is a supportive environment for risk assets globally. A sudden, sharp increase in the ON RRP balance, especially outside of predictable month-end or quarter-end periods, would be a major red flag for traders. It would signal a rapid tightening of dealer balance sheet capacity and could be a precursor to a "risk-off" event, as dealers would likely pull back on providing liquidity to all but their most important clients. This indicator is particularly relevant for arbitrage and relative value strategies. When dealer balance sheets are constrained (signaled by a high ON RRP balance), arbitrage opportunities, such as the spread between Treasury futures and cash bonds, may widen and persist because the entities that would normally correct them lack the balance sheet capacity to put on the required trades.

## **Section III: Intermediary Positioning and Market Expectations**

Having examined the system's core price signals and liquidity quantities, the analysis now turns to the key intermediaries and forward-looking indicators. The positioning of primary dealers, who stand at the nexus of funding flows, provides crucial information about the market's ability to absorb collateral. Simultaneously, derivatives markets offer a real-time gauge of the market's collective expectations for future monetary policy, which heavily influences current behavior and asset pricing.

### **Chart 6: The Collateral Shock Absorber: Primary Dealer Net Treasury Positions**

\!(placeholder\_chart\_6.png)

#### **WHAT IT IS**

This chart displays the weekly net outright inventory of U.S. Treasury securities held by primary dealers, as reported in the Federal Reserve Bank of New York's (FRBNY) Primary Dealer Statistics.1 This figure represents the stock of collateral on dealer balance sheets that they must finance on a daily basis, primarily through the repurchase agreement (repo) market.1

#### **WHY IT MATTERS**

Primary dealers are the system's shock absorbers. They are obligated to bid in all Treasury auctions and serve as the primary market makers, absorbing new government debt issuance and warehousing it before distributing it to end investors like pension funds and foreign central banks.1 A high or rapidly increasing level of dealer inventory signifies a large, latent demand for repo funding. If this build-up in collateral coincides with a scarcity of cash in the system, it creates the perfect conditions for a funding squeeze. This exact dynamic—dealers holding near-record inventories of Treasuries financed by a shrinking pool of reserves—was a primary cause of the September 2019 repo market spike.1

#### **HOW TO INTERPRET THE CHART**

* **Rising Trend:** A sustained increase in net positions indicates that dealers are absorbing more government debt than they are successfully distributing to end-users. This inflates their balance sheets, increases their daily need for cash from the repo market, and makes the entire financial system more vulnerable to funding shocks.  
* **Sharp Spike:** Spikes often occur around large Treasury auctions. A failure of this inventory to decline in the subsequent weeks suggests weak demand from end-investors and a potential "indigestion" problem for the market, signaling that the current level of yields may be too low to attract buyers.  
* **Falling Trend:** A declining inventory level suggests strong demand from end-investors, allowing dealers to offload their positions and reduce their financing needs. This is indicative of a healthy and well-functioning market.

#### **THE CURRENT READING**

The FRBNY releases this data weekly on Thursdays at approximately 4:15 p.m..22 While a specific, up-to-the-minute data point is not available in the provided materials, the analysis would focus on the latest release relative to historical context. For example, research notes that dealer inventories reached all-time highs in the run-up to the September 2019 event, creating a vulnerable backdrop.1 An analyst would assess the current level against that historical peak and other periods of stress. The key question is whether the recent trend shows inventory building (a warning sign) or declining (a healthy sign).

#### **THE GLOBAL MACROECONOMIC & CROSS-ASSET TRADING IMPLICATIONS**

This chart is a crucial indicator for the health of the U.S. Treasury market, the benchmark for all global finance. Persistently elevated dealer inventories signal that the market may struggle to absorb future government issuance, which could lead to higher bond yields (lower prices) and increased volatility. This has a direct spillover effect on risk assets. If dealers are burdened with financing large, unwanted bond inventories, their capacity and willingness to finance other, riskier assets—such as equities via prime brokerage or corporate bonds—diminishes significantly. This can lead to a general tightening of financial conditions, even without any change in official policy rates. A sharp, sustained increase in dealer inventory can be a powerful leading indicator of a "risk-off" environment, as it suggests a breakdown in the distribution chain of the world's most important financial asset.

### **Chart 7: The Market's Monetary Policy Forecast: The SOFR Futures Curve**

\!(placeholder\_chart\_7.png)

#### **WHAT IT IS**

The SOFR futures curve reflects the market's collective, real-time expectation for the future path of the 3-month Secured Overnight Financing Rate, which is tightly linked to the Federal Reserve's policy rate.1 Each point on the curve is derived from the price of a 3-month SOFR futures contract traded on the CME Group exchange and represents the market's consensus forecast for where short-term rates will be at that future date.24 The implied interest rate is calculated as

100−Futures Price.26

#### **WHY IT MATTERS**

This chart provides a transparent, forward-looking view of market expectations for monetary policy, which is a primary driver of all asset prices. It reveals whether the market finds the Fed's own guidance (communicated through speeches and the "dot plot") credible. Discrepancies between the market's pricing and the Fed's projections are a key source of market tension, volatility, and trading opportunities.1 It allows investors to see what is "priced in" to the market regarding future Fed actions.

#### **HOW TO INTERPRET THE CHART**

* **Upward Sloping Curve (Contango):** The market is pricing in future interest rate hikes. The steeper the slope, the more aggressive the expected tightening cycle.  
* **Downward Sloping Curve (Backwardation/Inversion):** The market is pricing in future interest rate cuts. This is often a signal that the market anticipates an economic slowdown or recession that will force the Fed to ease policy.  
* **Curve Shape vs. Fed "Dot Plot":** The most valuable analysis comes from comparing the futures curve to the Fed's own projections. If the futures curve is significantly above the dot plot, it means the market believes the Fed is "behind the curve" on inflation and will be forced to tighten more than it currently expects. If the curve is below the dot plot, the market is "calling the Fed's bluff," believing that economic weakness will force it to cut rates sooner or more deeply than planned.

#### **THE CURRENT READING**

As of August 8, 2025, data from the CME Group shows the following prices for 3-Month SOFR futures: June 2025 at 95.635, September 2025 at 95.925, December 2025 at 96.255, and March 2026 at 96.475.27 This translates to the following implied 3-month rates:

* June 2025: 100−95.635=4.365%  
* September 2025: 100−95.925=4.075%  
* December 2025: 100−96.255=3.745%  
* March 2026: 100−96.475=3.525%  
  The curve is clearly downward sloping (in backwardation), indicating that the market is aggressively pricing in a series of interest rate cuts beginning in mid-2025 and continuing into 2026\. This implies that the market's central expectation is for a significant economic slowdown that will necessitate a shift to an accommodative monetary policy stance from the Federal Reserve.

#### **THE GLOBAL MACROECONOMIC & CROSS-ASSET TRADING IMPLICATIONS**

The shape of the SOFR futures curve is a primary driver of the entire Treasury yield curve and has profound implications for all asset classes.

* **Fixed Income:** A dovish futures curve (pricing in cuts) puts downward pressure on short- to medium-term Treasury yields (e.g., 2-year and 5-year notes), often leading to a "bull steepening" of the yield curve, where short-term yields fall more than long-term yields.  
* **Equities:** An aggressively inverted curve pricing in rate cuts is often interpreted as a recessionary signal, which can be a headwind for economically sensitive cyclical stocks. However, the prospect of lower discount rates can be a powerful tailwind for long-duration growth stocks (e.g., technology), whose valuations are highly sensitive to changes in long-term interest rates.  
* **Currencies:** A dovish shift in the SOFR futures curve—where the market prices in more or faster rate cuts—typically weakens the U.S. dollar. This is because it lowers the expected future interest rate differential between the U.S. and other major economies, making the dollar less attractive to hold. This is a key input for foreign exchange carry trades and directional bets against the dollar.

## **Section IV: Synthesis and Transmission to Securities Finance**

This section bridges the gap between the high-level macroeconomic analysis of the monetary plumbing and the specific domain of securities finance. The objective is to establish the clear transmission mechanisms through which systemic funding conditions propagate into the markets for borrowing and lending individual securities. The critical nexus is the balance sheet of the dealer-bank, which acts as a major intermediary in both the repo market (a "cash-driven" market for funding) and the securities lending market (a "security-driven" market for sourcing specific assets).1 Stress in the former market directly dictates behavior and pricing in the latter.

While economically similar to forms of collateralized finance, the different primary motivations behind repo and securities lending are the key to understanding the transmission of signals. The general collateral repo rate reflects the systemic, market-wide cost of secured funding. In contrast, the securities lending fee for a specific stock or bond reflects the idiosyncratic demand for that particular piece of collateral.1 A dealer's ability to offer securities lending services is directly dependent on its ability to fund its overall balance sheet in the broader repo market. Therefore, a systemic shock that raises the cost of funding in the repo market will inevitably increase the dealer's cost base and constrain its capacity for all forms of financing, including securities lending.1

| Feature | Repurchase Agreement (Repo) | Securities Lending |
| :---- | :---- | :---- |
| **Primary Motivation** | Cash-Driven: Borrowing/lending cash 1 | Security-Driven: Borrowing a specific security 1 |
| **Economic Function** | Secured money market instrument | Collateral rental market |
| **Typical Participants** | Cash Lenders: MMFs, Central Banks 1 Cash Borrowers: Securities Dealers 1 | Security Lenders: Pension Funds, Asset Managers 1 Security Borrowers: Hedge Funds, Market Makers 1 |
| **Typical Collateral** | From Borrower to Lender: High-Quality Liquid Assets (HQLA) like U.S. Treasuries 1 | From Borrower to Lender: Cash, other securities, or Letter of Credit 1 |
| **Pricing Metric** | Repo Rate: An interest rate paid by the cash borrower 1 | Lending Fee: A fee paid by the security borrower 1 |

### **Chart 8: The Composite Plumbing Liquidity Index (PLI)**

#### **WHAT IT IS**

This chart displays a proprietary, composite Plumbing Liquidity Index (PLI) designed to provide a single, comprehensive measure of overall funding market stress and liquidity conditions.1 It is constructed as a weighted average of several normalized indicators discussed previously, including: (1) the OBFR-SOFR spread to capture credit risk; (2) ON RRP facility usage as a percentage of MMF AUM to measure dealer balance sheet constraint; (3) SOFR's absolute deviation from the policy corridor midpoint to measure implementation stress; and (4) repo market volatility, measured as the daily range between the 99th and 1st percentiles of SOFR transactions, to capture market fragmentation.1

#### **WHY IT MATTERS**

Individual plumbing indicators can sometimes be noisy or provide conflicting signals. For instance, the credit spread might be stable while ON RRP usage is surging, pointing to a nuanced state of balance sheet constraint rather than credit fear.1 The PLI synthesizes these multiple data points into a single, robust "fever chart" for the funding markets. This process filters out idiosyncratic noise and provides a clearer, more holistic picture of the underlying state of the system, making it a more reliable input for risk management models and a tool for quick assessment by senior decision-makers.1

#### **HOW TO INTERPRET THE CHART**

* **Low & Stable Level (Green Regime):** Indicates calm, liquid, and well-functioning funding markets. Systemic risk is low, and dealer intermediation capacity is high.  
* **Rising Index (Yellow Regime):** A rising PLI indicates tightening liquidity, increasing dealer balance sheet constraints, and rising systemic stress. This serves as a warning signal to reduce risk.  
* **Spike in Index (Red Regime):** A sharp spike signals an acute market dislocation, such as the events of September 2019 or March 2020\. By decomposing the index's components, an analyst can diagnose whether the stress is being driven primarily by credit risk, a liquidity shortage, or balance sheet constraints.

#### **THE CURRENT READING**

This is a proprietary index to be constructed based on the methodology outlined. However, based on the current readings of its underlying components—a low OBFR-SOFR spread, very low ON RRP usage, and key rates trading well within the policy corridor—the PLI would currently be in the 'Calm' (Green) regime. The analysis indicates that the monetary plumbing is functioning smoothly, with low perceived credit risk and ample dealer capacity for intermediation. There are no immediate signs of systemic funding stress.

#### **THE GLOBAL MACROECONOMIC & CROSS-ASSET TRADING IMPLICATIONS**

The PLI serves as a master risk indicator for a cross-asset portfolio. A low and stable PLI is effectively a green light for risk-taking and the use of leverage across asset classes, as the risk of a sudden funding shock is minimal. A sustained rise in the PLI would be a powerful signal to reduce overall portfolio risk, decrease leverage, increase cash holdings, and rotate into defensive assets. Such a rise would suggest a broad-based tightening of financial conditions that would negatively impact equities, corporate credit, and emerging markets. For volatility traders, a rising PLI could be a signal to buy protection (e.g., VIX futures, put options) in anticipation of a market shock, as funding stress is a primary catalyst for an expansion in market-wide volatility.

### **Chart 9: The Transmission Mechanism: Plumbing Stress vs. Securities Finance Costs**

#### **WHAT IT IS**

This chart directly visualizes the relationship between macro-plumbing stress, as measured by the composite Plumbing Liquidity Index (PLI), and the cost of borrowing specific securities.1 The left axis plots the PLI from Chart 8\. The right axis plots a key securities finance metric, such as a publicly available index like the S\&P Securities Lending Index or a proprietary, custom-built index of borrowing fees for a specific collateral class (e.g., "hard-to-borrow" equities or high-yield corporate bonds).1

#### **WHY IT MATTERS**

This is the capstone chart that operationalizes the entire framework. It moves from abstract concepts of liquidity and risk to a concrete, observable impact on the securities finance market. It provides visual and quantitative evidence of the transmission channels—namely, the Funding Cost Channel and the Balance Sheet Capacity Channel—through which dealers pass on higher systemic funding costs and balance sheet constraints to their securities finance clients.1 It demonstrates the core thesis of the report: that conditions in the core plumbing directly impact the price and availability of collateral across the entire securities finance landscape.

#### **HOW TO INTERPRET THE CHART**

* **Correlation and Lead-Lag:** The primary method of interpretation is to look for a strong positive correlation between the two series. Critically, one must analyze the lead-lag relationship. A dynamic where spikes in the PLI consistently *precede* spikes in securities lending fees by several days would validate the PLI as a powerful leading indicator for borrowing costs.  
* **Regime-Dependent Behavior:** The relationship may be state-dependent. The correlation might be weak or non-existent during 'Calm' market regimes (low PLI), when idiosyncratic factors dominate borrowing costs. However, the correlation could become extremely strong during 'Stressed' or 'Crisis' regimes (high PLI), as systemic funding costs become the overriding determinant of all financing rates. This is an actionable insight in itself.

#### **THE CURRENT READING**

With the Plumbing Liquidity Index currently in a 'Calm' regime, the chart would be expected to show a low and stable PLI. In this environment, securities lending fees for general collateral would also be expected to be low and stable. The borrowing costs for specific "hard-to-borrow" stocks will be driven by idiosyncratic factors such as high short interest or M\&A activity, but the *general* cost of dealer balance sheet usage for financing should be minimal.30 The analysis would conclude that in the current environment, macro funding conditions are not a significant driver of securities lending costs. Any observed high fees are likely due to security-specific demand rather than systemic stress.

#### **THE GLOBAL MACROECONOMIC & CROSS-ASSET TRADING IMPLICATIONS**

This framework provides a powerful tool for developing quantitative trading strategies. By modeling securities lending fees as a function of the PLI (and its components) alongside traditional factors like short interest and implied volatility, one could build a predictive model for borrowing costs, potentially identifying mispricings or forecasting changes in the cost to short specific securities. For risk management, a rising PLI is a clear signal that the cost of carry for short positions is likely to increase across the board. This could prompt a portfolio manager to proactively reduce the size of their short book or focus on shorts with lower expected borrowing costs to avoid a sudden, adverse spike in financing expenses. The framework also has implications for long-only investors participating in securities lending programs. A rising PLI suggests that lending revenue is likely to increase, providing a small but potentially meaningful offset to falling portfolio values during a risk-off period.

## **Conclusion: Integrating Plumbing Analysis into the Investment Process**

The central thesis of this report is that the "plumbing" of the financial system is not a passive utility but an active and potent source of macroeconomic signals. The intricate network of money markets, intermediary balance sheets, and central bank facilities that constitute this plumbing serves as the primary transmission mechanism for monetary policy and systemic risk. By moving beyond a superficial view of interest rates and embracing a deeper, more mechanistic understanding of these markets, sophisticated financial firms can uncover quantifiable, leading indicators for risk and opportunity in their securities finance and broader cross-asset operations.

The analysis has demonstrated that stress is transmitted from the core funding markets—primarily the U.S. Treasury repo market—through the balance sheets of primary dealers directly to the pricing and availability of all forms of collateral. A constraint in one part of the system, whether driven by regulatory friction, a temporary liquidity shortage, or a systemic crisis, creates ripples that affect the entire collateral landscape. The framework presented provides a structured, data-driven approach to monitoring these dynamics, constructing robust composite signals like the Plumbing Liquidity Index (PLI), and ultimately connecting the esoteric world of monetary plumbing to the practical realities of asset pricing and risk management.

| Macroeconomic Signal | Primary Indicator(s) | Data Source(s) | Interpretation & Implication for Securities Finance |
| :---- | :---- | :---- | :---- |
| **Systemic Funding Stress** | Widening SOFR-EFFR/OBFR Spread | NY Fed | Indicates flight to quality and rising interbank credit risk. Implies higher dealer funding costs, leading to wider bid-ask spreads on securities loans and potentially reduced market-making capacity. |
| **Specific Collateral Scarcity** | GC-Special Repo Spread | OFR, Market Data Vendors | Measures intense demand to borrow a specific security. A direct, high-frequency leading indicator for higher securities lending fees on that specific security. |
| **Dealer Balance Sheet Constraint** | Quarter-end spikes in repo rates; High ON RRP Balance | NY Fed, Fed H.4.1 | Signals reduced dealer capacity for intermediation due to regulatory costs. Predicts higher average fees for general collateral loans and lower market liquidity. |
| **Monetary Policy Stance** | Fed Funds / SOFR Futures Curve | CME Group | Indicates the expected path of interest rates. Tightening policy suggests increased demand to borrow fixed-income assets for hedging/shorting, impacting relative lending fees across asset classes. |

Looking ahead, this analytical framework provides a valuable lens for assessing the potential impacts of future structural changes to the financial system. The potential introduction of a Central Bank Digital Currency (CBDC), for instance, could fundamentally alter the financial landscape.1 A widely available retail CBDC could trigger disintermediation from commercial bank deposits, potentially shrinking bank balance sheets and reducing their capacity for market-making in securities financing markets. A wholesale CBDC, however, could revolutionize settlement by enabling "atomic" delivery-versus-payment, virtually eliminating settlement risk and increasing the velocity of collateral.1 The tools and indicators developed in this report would be essential for monitoring the real-time impact of such innovations on bank reserves, funding rates, and dealer behavior. The key takeaway for the financial professional is that the conditions in their specific market are not determined in a vacuum. They are deeply and inextricably linked to the broader flows of cash and collateral coursing through the financial plumbing. By adopting the data-driven, systematic approach outlined in this report, it is possible to move from being a passive observer of these powerful forces to an informed practitioner capable of anticipating their impact and making more strategic, data-driven decisions.