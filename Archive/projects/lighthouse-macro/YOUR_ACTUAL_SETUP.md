# Your Actual Setup — Confirmed

Based on what you told me, here's your real configuration:

---

## ✅ API Keys You Have (Fully Automated)

```
✅ FRED Data              7f8e44038ee69c4f78cf71873e85db16
✅ Google/Gemini          AIzaSyDYD67P4y-bQcwP5TRuYgvmD3bB83ysLtM
✅ Claude (Anthropic)     sk-ant-api03-e8M3us7z...
✅ OpenAI (GPT-4)         sk-proj-yp7r9jrqolce7KrZ...
```

**These 4 are fully configured and ready to automate.**

---

## 📱 App Access Only (Semi-Automated)

```
📱 Grok (X Premium)       → No API (X Premium doesn't include API)
❓ Perplexity            → Not sure if you have Pro with API
```

### Grok Situation
**You said:** "I don't think Twitter Grok premium gets a key"
**You're right!** X Premium ($8-16/mo) does NOT include API access.

**Grok API requires:**
- Separate xAI API account at https://x.ai/
- Different pricing from X Premium
- Currently in beta/limited access

**Your options for Grok:**
1. **App-based workflow** (use the system's prompt helper) ← Recommended
2. Check if you can get xAI API access (separate from X Premium)

### Perplexity Situation
**You said:** "Simply not sure with respect to Perplexity"

**Quick check:**
1. Go to: https://www.perplexity.ai/settings/api
2. If you see "API" section → You have API access
3. If not → You have app-only access

**Perplexity API requires:**
- Perplexity Pro subscription ($20/mo)
- API access is included with Pro

**Your options:**
1. **Check now** → Visit link above, see if you have API section
2. **Use app workflow** → System helps with copy/paste (works great)
3. **Upgrade to Pro** → If you want full API automation ($20/mo)

---

## 🎯 Recommended Approach: Hybrid System

**Use what you have:**

### Fully Automated (4 Models)
```python
from src.ai import ClaudeClient, OpenAIClient, GeminiClient
from src.collectors import FREDCollector

# These work automatically
fred = FREDCollector()        # Economic data
gemini = GeminiClient()        # Charts, vision, multimodal
claude = ClaudeClient()        # Your voice, deep analysis
gpt = OpenAIClient()           # Fast extraction, fact-check
```

### Semi-Automated (2 Models)
```python
from src.ai.app_workflows import AppWorkflowHelper

# These use clipboard + prompt generation
helper = AppWorkflowHelper()

# Grok (X app)
helper.workflow("grok", "What's market sentiment on X about Fed policy?")

# Perplexity (web app)
helper.workflow("perplexity", "Latest economic data and Fed speeches")
```

---

## 🚀 What This Gives You

### Core Workflow (Fully Automated)

**Data → Analysis → Narrative → Verification**

```python
# 1. Collect data (FRED API)
fred = FREDCollector()
gdp = fred.fetch("GDP")
cpi = fred.fetch("CPIAUCSL")

# 2. Extract insights (GPT)
gpt = OpenAIClient()
data_summary = gpt.complete(f"Key insights: GDP={gdp}, CPI={cpi}")

# 3. Analyze charts (Gemini)
gemini = GeminiClient()
chart_analysis = gemini.analyze_chart("chart.png", "Patterns?")

# 4. Write article (Claude - your voice)
claude = ClaudeClient()
article = claude.complete(f"Write Beam: {data_summary} + {chart_analysis}")

# 5. Fact check (GPT)
verified = gpt.complete(f"Verify: {article}")
```

**100% automated. No manual switching.**

### Enhanced with App Workflows

When you need Perplexity research or Grok sentiment:

```python
from src.ai import ClaudeClient
from src.ai.app_workflows import perplexity_research

# Get current research (semi-automated)
# System: generates prompt, copies to clipboard
# You: paste in Perplexity, copy response back
research = perplexity_research(
    "Latest Fed policy changes and market implications"
)

# Continue automated
claude = ClaudeClient()
analysis = claude.complete(f"Analyze: {research}")
```

**90% automated. Only 2-3 copy/pastes for specialized research.**

---

## 💡 Practical Workflow Examples

### Example 1: Daily Macro Brief (100% Automated)

```python
from src.collectors import FREDCollector
from src.ai import OpenAIClient, ClaudeClient

# Collect data
fred = FREDCollector()
unrate = fred.load_latest("UNRATE")
cpi = fred.load_latest("CPIAUCSL")

# Extract insights
gpt = OpenAIClient()
insights = gpt.complete(f"Key insights: UNRATE={unrate}, CPI={cpi}")

# Write brief
claude = ClaudeClient()
brief = claude.complete(f"Daily brief (150 words): {insights}")

print(brief)
```

### Example 2: The Beam (Chart + Analysis)

```python
from src.ai import GeminiClient, ClaudeClient
from src.charting import LHMChart, set_lhm_style
from src.collectors import FREDCollector

# Get data and create chart
fred = FREDCollector()
gdp = fred.load_latest("GDP")

set_lhm_style()
chart = LHMChart()
chart.plot_line(gdp, color="ocean_blue")
chart.add_watermarks()
chart.save("gdp_beam.png")

# Analyze chart
gemini = GeminiClient()
analysis = gemini.analyze_chart("gdp_beam.png", "Analyze trends")

# Write Beam
claude = ClaudeClient()
beam = claude.complete(f"""
Write a Beam (150 words):
Chart: {analysis}
Style: Sharp, accessible, forward-thinking
""")

print(beam)
```

### Example 3: Research + Synthesis (90% Automated)

```python
from src.ai import ClaudeClient, OpenAIClient
from src.ai.app_workflows import perplexity_research

# Research latest (semi-automated: you paste in Perplexity app)
research = perplexity_research(
    "Latest inflation data and Federal Reserve response",
    focus="Policy implications for 2025"
)

# Extract key points (automated)
gpt = OpenAIClient()
key_points = gpt.complete(f"Extract key facts: {research}")

# Write analysis (automated)
claude = ClaudeClient()
analysis = claude.complete(f"""
Write macro analysis (300 words):
Research: {research}
Key facts: {key_points}
""")

# Fact check (automated)
verified = gpt.complete(f"Verify accuracy: {analysis}")

print("Final:", analysis)
print("\nVerification:", verified)
```

---

## 📥 Installation & First Test

### 1. Install System

```bash
cd ~/lighthouse-macro
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

This installs:
- `anthropic` (Claude)
- `openai` (GPT)
- `google-generativeai` (Gemini)
- `pyperclip` (clipboard for app workflows)
- All other dependencies

### 2. Verify What Works

```bash
python cli.py status
```

Expected:
```
✓ FRED API
✓ Google API
✓ Anthropic (Claude)
✓ OpenAI (GPT)
✓ Gemini (Google)
✗ Grok (xAI)            ← Expected (no API)
✗ Perplexity            ← Expected (unless you have Pro)
```

### 3. Test Automation

```bash
# Test data collection
python cli.py collect fred --series GDP

# Test chart
python cli.py chart create GDP --output test.png

# Test AI (example script)
python examples/hybrid_workflow_example.py
# Choose option 1 (fully automated with your 4 models)
```

---

## 🎓 What to Focus On

### Priority 1: Master Your 4 Automated Models

These give you 80% of the value:

**FRED** → All economic data
**Gemini** → Chart analysis, vision, long context
**Claude** → Your voice, deep reasoning, narrative
**GPT** → Fast extraction, fact-checking, summaries

**Build workflows with these first.**

### Priority 2: Decide on Perplexity

**Option A:** Check if you have API
- Visit: https://www.perplexity.ai/settings/api
- If you see API section → Add key to `configs/secrets.env`
- Full automation unlocked

**Option B:** Use app workflow
- Already built for you
- Copy/paste helper
- Still saves time

**Option C:** Get Perplexity Pro ($20/mo)
- Includes API access
- Worth it if you use it daily

### Priority 3: Grok Strategy

**For now:** Use app workflow helper
- X Premium doesn't include API
- App workflow works fine for checking sentiment
- System generates perfect prompts

**Future:** If xAI opens API access
- Watch for announcements
- Add key when available

---

## 💪 Bottom Line

**You have 4 powerful APIs ready now:**
1. FRED → Data
2. Gemini → Charts
3. Claude → Narrative
4. GPT → Extraction

**Plus 2 app helpers:**
5. Grok → X sentiment (app workflow)
6. Perplexity → Research (app workflow or check for API)

**This is enough to automate 80-90% of your workflow TODAY.**

---

## 🚀 Next Steps

### Right Now
```bash
cd ~/lighthouse-macro
python3 -m venv venv
source venv/bin/activate
pip install -e .
python cli.py status
```

### This Week
1. Test the 3 workflow examples above
2. Check Perplexity API status: https://www.perplexity.ai/settings/api
3. Collect your first data: `python cli.py collect fred --pillar macro_dynamics`
4. Generate your first chart: `python cli.py chart create GDP`
5. Try hybrid workflow: `python examples/hybrid_workflow_example.py`

### Optional
- Add Perplexity API key if you have it
- Practice app workflows for Grok/Perplexity
- Customize AI routing in `configs/ai_routing.yaml`

---

**You're ready to go with what you have. Focus on the 4 automated models, add others as needed.**

**LIGHTHOUSE MACRO**
MACRO, ILLUMINATED.
