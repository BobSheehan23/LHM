# # 📘 LIGHTHOUSE MACRO — FRIDAY CHARTBOOK  
**Macro, Illuminated.**

**Date:** {{YYYY-MM-DD}}  
**Edition:** Week {{#}}  
**Prepared by:** Lighthouse Macro Research  
**Lead:** Bob Sheehan, CFA, CMT  

---

## 🔍 Lead Summary (3 Bullets)

1. {{Macro theme headline — e.g., Growth plateau, fiscal pulse softens}}
2. {{Monetary lens — e.g., RRP bleed moderates, bill issuance up}}
3. {{Market takeaway — e.g., equity vol regime coiling; correlation map shifting}}

---

## 🌍 Thematic Arc 1 — Macro Dynamics (15–20 charts)

**Narrative:** {{Two-sentence summary of growth/inflation/labor/fiscal mix.}}  
*Focus:* GDP | Inflation | Labor | Fiscal | Trade | Commodities

| Chart | Title | Description / Takeaway | File |
|-------|--------|------------------------|------|
| 1 | Real GDP vs Final Sales (3M ann.) | {{Growth pulse stabilizing?}} | `macro_gdp_01.png` |
| 2 | Core PCE vs Supercore | {{Services inflation stickiness persists}} | `infl_supercore_02.png` |
| 3 | Goods vs Services Inflation Spread | {{Converging disinflation path}} | `infl_goods_services_spread_03.png` |
| 4 | Payrolls vs Diffusion Index | {{Breadth softening beneath headline}} | `labor_diffusion_04.png` |
| 5 | ISM Mfg vs New Orders–Inventories | {{Mfg contraction lengthens}} | `ism_no_inv_05.png` |
| … | {{Add up to 20}} | {{Summary per chart}} | `macro_XX.png` |

---

## 💧 Thematic Arc 2 — Monetary Mechanics (15–20 charts)

**Narrative:** {{Describe funding, collateral, reserves, RRP, term premia context.}}  
*Focus:* Fed balance sheet | Bills/Coupons | Auctions | SOFR/GC | FX basis

| Chart | Title | Description / Takeaway | File |
|-------|--------|------------------------|------|
| 21 | Fed Balance Sheet: RRP & Reserves | {{Reserve drift continues}} | `plumbing_fed_21.png` |
| 22 | Treasury Cash Ladder (TGA vs Issuance) | {{Bill-heavy QRA supports reserves}} | `treasury_tga_22.png` |
| 23 | ON RRP vs Bills Yield Spread | {{MMF preference turning?}} | `rrp_bills_spread_23.png` |
| 24 | SOFR – GC – IORB (bps) | {{Collateral scarcity proxy}} | `repo_basis_24.png` |
| 25 | Term Premia (ACM 10y) | {{Repricing of real term risk}} | `term_premia_25.png` |
| … | {{Continue to ~40}} |  |  |

---

## 📈 Thematic Arc 3 — Market Technicals (15–20 charts)

**Narrative:** {{Describe breadth, vol, and positioning regime.}}  
*Focus:* Equities | Rates vol | Credit | CTA | Cross-asset correlation

| Chart | Title | Description / Takeaway | File |
|-------|--------|------------------------|------|
| 41 | SPX vs Breadth Z-score | {{Concentration risk remains high}} | `eq_spx_breadth_41.png` |
| 42 | Equal vs Cap Weight SPX | {{Rotation faint but broadening}} | `eq_eqw_capw_42.png` |
| 43 | MOVE vs VIX | {{Vol cross-market decoupling}} | `move_vix_43.png` |
| 44 | CFTC Specs: TY/US | {{Net longs rebuilding in TY}} | `cftc_ty_44.png` |
| 45 | Cross-Asset Corr Matrix | {{Regime shift watch}} | `corr_matrix_45.png` |

---

## 💹 Thematic Arc 4 — Asset Class Dash (8–12 charts)

**Narrative:** {{Rates, credit, FX, commodities — summary sentence.}}

| Chart | Title | Takeaway | File |
|-------|--------|-----------|------|
| 51 | 2s10s/3m10y Yield Curves | {{Inversion duration}} | `curve_inversion_51.png` |
| 52 | IG & HY OAS vs Defaults | {{Credit spreads contained}} | `credit_oas_52.png` |
| 53 | DXY vs EM FX Basket | {{USD resilience continues}} | `dxy_emfx_53.png` |
| 54 | Gold vs Real Yields | {{Inverse relationship intact}} | `gold_real_54.png` |
| 55 | BTC vs USD Liquidity Proxy | {{Crypto = marginal liquidity gauge}} | `btc_liquidity_55.png` |

---

## 🧭 Thematic Arc 5 — Single-Name Diagnostics (~10–15)

**Narrative:** {{Earnings, positioning, and macro-beta lens for flagship equities.}}

| Chart | Ticker | Key Variable | Takeaway | File |
|-------|--------|---------------|-----------|------|
| 61 | AAPL | EPS vs Real Yields | {{Defensiveness holding}} | `sn_aapl_61.png` |
| 62 | NVDA | CapEx Proxy vs Price | {{Data center cycle peak watch}} | `sn_nvda_62.png` |
| 63 | JPM | 2s10s vs NIM Proxy | {{Curve compression → margin risk}} | `sn_jpm_63.png` |
| 64 | META | Ad Spend vs Price | {{Ad recovery plateau}} | `sn_meta_64.png` |
| … | {{Add through 75}} |  |  |

---

## 🧩 Proprietary Indicators (optional overlay)

| Indicator | Definition | State | Implication |
|------------|-------------|--------|--------------|
| Liquidity Plumbing Index | Composite of reserves, RRP, TGA, GC–SOFR | {{Tightening / Easing}} | {{Liquidity bias}} |
| Collateral Fragility Score | Bills–IORB basis, fails, tails | {{Stable / Worsening}} | {{Collateral pressure risk}} |
| Positioning Heatmap | Z-scores of CFTC + ETF flows | {{Neutral / Long / Short}} | {{Crowding or unwind risk}} |

---

## 📄 Summary Strip (one-page executive view)

> Include 3–5 proprietary indices + 5 macro/market dashboards.  
> This page becomes the PDF cover summary.

---

## 🧱 Reproducibility

**Sources:**  
BLS, BEA, Fed (H.4.1, H.8, G.17), Treasury (QRA, auctions, TGA), ISM, NY Fed (SOFR, GSCPI), CME, Refinitiv/Bloomberg, index providers.  

**Transforms:**  
YoY, 3M/6M ann., index=100, rolling z-scores (12m/24m), spreads, contributions, log diffs, rolling correlations, percentile bands.  

**File conventions:**  
- `theme_shortname_##.png`  
- Full-page, standalone; no grids; 4 spines; right axis primary.  
- Palette: Ocean Blue #0077FF | Dusk Orange #FF4500 | Carolina Blue #00BFFF | Neon Magenta #FF00FF | Gray #8A8F98  
- Title (Ocean Blue, centered), white value labels on-axis, bottom-left citation:  
  *Source: [Data] | Analysis: Lighthouse Macro*  
- Watermarks: top-left **LIGHTHOUSE MACRO**, bottom-right **MACRO, ILLUMINATED.**

---

## ⚙️ Workflow Checklist

1. [ ] Update data via pipelines / FRED API / Bloomberg pulls.  
2. [ ] Generate charts (Python, standardized style template).  
3. [ ] QA (revision anomalies, label alignment).  
4. [ ] Insert summaries + takeaways.  
5. [ ] Export as PDF (landscape A4, sequential numbering).  
6. [ ] Upload to Substack post — headline summary + download link.

---

## 🪶 Notes

- Avoid posting all 50+ charts inline — Substack compresses images.  
- Teaser post = 3–5 charts, one narrative arc, and link to full PDF.  
- Keep narrative tight; charts do the heavy lifting.  
- Reuse 1–2 lead visuals in *The Beacon* Sunday note.

---

**© Lighthouse Macro 2025**  
*“Less noise, more signal.”*