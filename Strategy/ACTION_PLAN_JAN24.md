# Lighthouse Macro Action Plan
**Date:** January 24, 2026

---

## IMMEDIATE WINS (Today/This Weekend)

### 1. ✅ Adam Betancourt
**Status:** DONE - he responded, you're good
**Next:** Schedule actual catch-up call via IG

### 2. Cameron Dawson Outreach
**Status:** Pending - Adam can bridge
**Action:** Message Adam on IG asking if he can intro you to Cameron or if you should reach out direct
**Draft:**
> Yo quick q - should I reach out to Cameron directly or would an intro from you be better? Don't want to cold-email the CIO of the Year lol. Also she might still have my CMT book.

---

## LLC SETUP TASKS (This Week)

### Business Banking
- [ ] Open business checking account (Mercury, Relay, or traditional bank)
- [ ] Get business debit card
- [ ] Set up accounting software (QuickBooks, Wave, or similar)

### Substack Payment Migration
- [ ] Update Stripe Connect to Lighthouse Macro, LLC
- [ ] Update payout bank account to business account
- [ ] Update tax information (EIN instead of SSN)

### Other LLC Housekeeping
- [ ] Get business email properly configured (bob@lighthousemacro.com ✓ already have)
- [ ] Update any contracts/agreements to LLC name
- [ ] Set up basic bookkeeping system
- [ ] Understand quarterly tax obligations

---

## WEBSITE & PLATFORM ARCHITECTURE

### Current State
- lighthousemacro.com - needs new website
- Substack - current newsletter home
- Beehiiv - have account, not using

### Proposed Architecture

```
lighthousemacro.com (Main Site - NEW)
├── Home: Brand, positioning, "two beams" value prop
├── Research: Links to → research.lighthousemacro.com
├── Advisory: Links to → advisory.lighthousemacro.com
├── About: Bio, credentials, philosophy
├── Framework: High-level 12 Pillars overview (teaser)
└── Contact: Inquiry forms for both tracks

research.lighthousemacro.com (Substack OR Beehiiv)
├── Free content: Educational series, Beams
├── Paid content: Beacon, Horizon, positioning
└── Archive: All published work

advisory.lighthousemacro.com (Simple landing page)
├── Track 1: Institutional/HF/Family Office
├── Track 2: Economic Intelligence (SMB, regional institutions)
└── Contact/Inquiry form
```

### Platform Decision: Substack vs Beehiiv

| Factor | Substack | Beehiiv |
|--------|----------|---------|
| Current audience | ✅ Already there | ❌ Would need to migrate |
| Custom domain | ✅ Yes | ✅ Yes |
| Branding control | ⚠️ Limited | ✅ Full control |
| Referral program | ✅ Built-in | ✅ Better tools |
| Analytics | ⚠️ Basic | ✅ More robust |
| Cost | 10% of paid | Free up to 2,500, then $$ |
| Network effects | ✅ Substack network | ❌ None |

**Recommendation:** Stay on Substack for now, add custom domain (research.lighthousemacro.com). Revisit Beehiiv when/if you outgrow Substack's limitations.

### Website Build Options

1. **Framer** - Modern, fast, good for landing pages
2. **Webflow** - More complex, full CMS capabilities
3. **Carrd** - Super simple, cheap, limited
4. **Ghost** - If you want to self-host newsletter too
5. **Squarespace/Wix** - Easy but less cool

**Recommendation:** Framer for main site (lighthousemacro.com), Substack with custom domain for research.

---

## SENDA / TANIA FOLLOW-UP

### Current Status
- BCH analysis delivered Dec 22
- She said "Thanks! will take a look and revert"
- Jacky email exchange Jan 5-9 about data providers
- No formal retainer yet

### Open Items
- [ ] Await her response on BCH analysis (don't chase)
- [ ] Intro to her brother (she was sending email - follow up?)
- [ ] Schedule call with Jacky to continue data provider discussion
- [ ] Formalize scope/pricing when appropriate (~$20-25K/month given expanded scope)

### Engagement Rules
- Don't over-follow up
- Only re-engage if: she responds, BCH moves materially, she asks for more analysis, or liquidity regime changes
- Position as collaborative partner, not vendor

---

## CONTENT CALENDAR (20 Posts in 5 Weeks)

**See:** `/Users/bob/LHM/Strategy/CONTENT_CALENDAR.md` for full schedule

### Structure
- **14 FREE** educational posts (Intro + 12 Pillars + Wrap-up)
- **6 PAID** market posts (1 done, 5 remaining)
- **20 TOTAL** posts over 5 weeks (Jan 24 - Feb 28)

### Cadence
- **Mon/Tue/Wed:** Educational posts (FREE)
- **Friday:** Paid post (Beacon or Horizon)

### Key Dates
| Date | Content |
|------|---------|
| Jan 24 ✅ | Reflexive Bid (PAID) - DONE |
| Jan 27 | Post 0: Kickoff (FREE) |
| Jan 31 | Beacon (PAID) |
| Feb 7 | Beacon (PAID) |
| Feb 14 | Horizon (PAID) |
| Feb 21 | Beacon (PAID) |
| Feb 25 | Post 13: Pulling It Together (FREE) |
| Feb 28 | Beacon - Series Finale (PAID) |

### Notes
- Content 90-100% written already
- Use series to review/optimize framework as you publish
- Paid Fridays keep subscribers engaged while free content builds audience

---

## NEWSLETTER PARTNERSHIP OUTREACH

### Priority Target: Michael Nadeau (TheDefiReport)
**Why:** Perfect complement - he's crypto-domain with macro awareness, you're macro-domain with crypto awareness. Minimal overlap, maximum cross-pollination.

**Draft outreach:**
> Hey Michael,
>
> Been reading TheDefiReport for a while - your protocol-level fundamentals work is exactly what I wish more macro analysts understood. The rigor you bring from your TradFi background shows.
>
> I run Lighthouse Macro - institutional macro research with a focus on Fed plumbing, liquidity transmission, and how it flows through to crypto. Basically the inverse of your positioning.
>
> Would you be open to a newsletter swap? Our audiences seem complementary - your readers get macro context, mine get DeFi depth. Happy to discuss format.
>
> Bob

### Secondary Targets (Tier 2)
- Noelle Acheson (Crypto is Macro Now) - more overlap but good audience
- Willy Woo (if you can get his attention)
- BowTied Bull (scale play, 112K subscribers)

---

## FRAMEWORK REVIEW

### Scheduled Task
- Take 1 day to review all 12 pillars
- Ensure framework documentation is current
- Expand Monetary Mechanics (Pillars 8-10) given plumbing depth
- Update any thresholds based on recent data

### Not Urgent
- This can wait until after Post 0 publishes
- Do it before writing Pillars 8-10 in educational series

---

## PRIORITY STACK

### Today
1. ✅ Reflexive Bid post + thread (DONE)
2. Message Adam re: Cameron intro
3. Review this action plan

### This Weekend
1. LLC banking setup research
2. Website architecture decision
3. Draft Cameron email (pending Adam's response)
4. Nadeau outreach draft

### Next Week
1. Open business bank account
2. Migrate Substack payments to LLC
3. Post 0 final review and publish
4. Start website build (or hire someone)

---

## PARKING LOT (Not Now)

- TradFi portfolio tracking platform selection
- Track 2 (economic intelligence) packaging and pricing
- Beehiiv migration evaluation
- Framework deep review
- Chartbook revival decision

---

**END OF ACTION PLAN**
