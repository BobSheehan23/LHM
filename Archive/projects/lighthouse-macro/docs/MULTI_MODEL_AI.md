# Lighthouse Macro — Multi-Model AI Orchestration

**Your system now supports 6 AI models with intelligent routing**

---

## Overview

Instead of manually switching between ChatGPT, Claude, Grok, Perplexity, and Gemini, your Lighthouse Macro system **automatically routes tasks** to the optimal model based on the task type.

## Configured Models

### 1. **Claude Sonnet 4** (Anthropic) ✅
**Best for:** Deep reasoning, narrative writing, code generation
**Use cases:**
- Writing Beacon articles in your voice
- Complex cross-pillar analysis
- Code generation for custom transformations
- Multi-stage research workflows

**Why:** Superior reasoning depth, maintains voice consistency, excellent at synthesis

### 2. **GPT-4 Turbo** (OpenAI) ✅
**Best for:** Fast extraction, fact-checking, batch processing
**Use cases:**
- Extracting data from FOMC statements
- Fact-checking drafts
- Quick summaries
- Batch chart annotations (Chartbook)

**Why:** Speed, cost-efficiency, structured output

### 3. **Grok** (xAI) 🔜 *Add your key*
**Best for:** Real-time X/Twitter analysis, current events, sentiment
**Use cases:**
- Analyzing market sentiment from X/Twitter
- Real-time event monitoring
- Fast inference on breaking news
- Social media trend analysis

**Why:** X integration, real-time data, fast responses

### 4. **Perplexity** (Sonar) 🔜 *Add your key*
**Best for:** Web research, cited sources, current data
**Use cases:**
- Researching recent economic policy changes
- Finding latest Fed speeches with citations
- Gathering current market conditions
- Verifying data with sources

**Why:** Real-time web access, automatic citations, research-optimized

### 5. **Gemini 2.0 Flash** (Google) 🔜 *Add your key*
**Best for:** Multimodal analysis, vision + text, long context
**Use cases:**
- Analyzing complex charts with multiple series
- Processing PDFs and documents
- Long-context analysis (128k tokens)
- Fast multimodal inference

**Why:** Excellent vision capabilities, fast, long context window

---

## Smart Routing Logic

Your system **automatically** selects the best model for each task:

| Task | Model | Why |
|------|-------|-----|
| **Write Beacon article** | Claude Sonnet 4 | Deep reasoning, your voice |
| **Extract FOMC data** | GPT-4 Turbo | Fast, structured output |
| **Research recent policy** | Perplexity | Web access, citations |
| **Analyze X sentiment** | Grok | Real-time social data |
| **Analyze complex chart** | Gemini | Vision + text analysis |
| **Generate code** | Claude Sonnet 4 | Superior code quality |
| **Quick summary** | GPT-4 Turbo | Speed, cost-efficiency |
| **Fact check** | GPT-4 Turbo | Structured verification |

---

## How to Add Your Keys

### 1. Grok (xAI)
Get your key at: https://x.ai/

Add to `configs/secrets.env`:
```bash
GROK_API_KEY=your_key_here
```

### 2. Perplexity
Get your key at: https://www.perplexity.ai/settings/api

Add to `configs/secrets.env`:
```bash
PERPLEXITY_API_KEY=your_key_here
```

### 3. Gemini
Use your existing Google API key, or get one at: https://aistudio.google.com/app/apikey

Add to `configs/secrets.env`:
```bash
GEMINI_API_KEY=your_google_api_key
```

---

## Usage Examples

### Automatic Routing (Recommended)

The system routes automatically based on task type:

```python
from src.ai import AIRouter, TaskType

router = AIRouter()

# This uses Perplexity (web research)
config = router.get_model_for_task(TaskType.WEB_RESEARCH)
print(config['reason'])
# Output: "Real-time web access, cited sources, current events"

# This uses Grok (real-time analysis)
config = router.get_model_for_task(TaskType.REAL_TIME_ANALYSIS)
print(config['reason'])
# Output: "X/Twitter integration, real-time sentiment, fast inference"
```

### Direct Model Usage

Or use specific models directly:

```python
from src.ai import PerplexityClient, GrokClient, GeminiClient

# Perplexity for web research
perplexity = PerplexityClient()
research = perplexity.research_topic(
    topic="Latest Federal Reserve policy changes in 2025",
    context="Focus on rate decisions and balance sheet policy"
)
print(research)  # Includes citations to sources

# Grok for X sentiment
grok = GrokClient()
sentiment = grok.complete(
    prompt="Analyze current market sentiment on X regarding Fed policy",
    temperature=0.5
)

# Gemini for chart analysis
gemini = GeminiClient()
analysis = gemini.analyze_chart(
    chart_path="charts/yield_curve.png",
    prompt="Analyze this yield curve chart and identify key patterns"
)
```

### Enhanced Research Workflows

Combine multiple models for comprehensive research:

```python
from src.ai import PerplexityClient, ClaudeClient, OpenAIClient

# Step 1: Web research (Perplexity)
perplexity = PerplexityClient()
web_research = perplexity.research_topic(
    topic="Current state of US labor market",
    context="Focus on participation rate, wage growth, job openings"
)

# Step 2: Deep analysis (Claude)
claude = ClaudeClient()
analysis = claude.complete(
    prompt=f"Analyze this research and synthesize key insights:\n\n{web_research}",
    temperature=0.7
)

# Step 3: Fact check (GPT)
gpt = OpenAIClient()
verified = gpt.extract_structured(
    prompt=f"Extract and verify key data points from this analysis:\n\n{analysis}"
)

print("Multi-model research complete!")
```

---

## Model Comparison

| Feature | Claude | GPT | Grok | Perplexity | Gemini |
|---------|--------|-----|------|------------|--------|
| **Reasoning depth** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Speed** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Voice consistency** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Web access** | ❌ | ❌ | ✅ | ✅✅ | ❌ |
| **Vision** | ✅ | ✅ | ❌ | ❌ | ✅✅ |
| **Citations** | ❌ | ❌ | ❌ | ✅✅ | ❌ |
| **Code quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Cost** | $$ | $$ | $ | $ | $ |

---

## Recommended Workflows

### Daily Macro Brief

```python
from src.ai import PerplexityClient, ClaudeClient

# Get latest news (Perplexity)
perplexity = PerplexityClient()
news = perplexity.search_and_summarize(
    "Latest economic data releases and Fed commentary today"
)

# Synthesize brief (Claude)
claude = ClaudeClient()
brief = claude.complete(
    prompt=f"Write a concise daily macro brief based on:\n\n{news}",
    temperature=0.6
)
```

### Market Sentiment Analysis

```python
from src.ai import GrokClient, ClaudeClient

# Get X sentiment (Grok)
grok = GrokClient()
sentiment = grok.complete(
    "Analyze current market sentiment on X regarding interest rates and equity markets"
)

# Deep analysis (Claude)
claude = ClaudeClient()
analysis = claude.complete(
    prompt=f"Analyze this sentiment data in context of recent macro developments:\n\n{sentiment}",
    temperature=0.7
)
```

### Chart Analysis + Research

```python
from src.ai import GeminiClient, PerplexityClient, ClaudeClient

# Analyze chart (Gemini)
gemini = GeminiClient()
chart_insights = gemini.analyze_chart(
    "charts/inflation_trends.png",
    "Identify key patterns and turning points in this inflation chart"
)

# Research context (Perplexity)
perplexity = PerplexityClient()
context = perplexity.research_topic(
    "Recent inflation trends and Fed policy response",
    context=chart_insights
)

# Synthesize (Claude)
claude = ClaudeClient()
final = claude.complete(
    prompt=f"Synthesize chart analysis and research:\n\nChart: {chart_insights}\n\nContext: {context}",
    temperature=0.7
)
```

---

## Configuration

Customize routing in `configs/ai_routing.yaml`:

```yaml
routing:
  web_research:
    model: llama-3.1-sonar-large-128k-online
    provider: perplexity
    reason: "Real-time web access, cited sources"
    temperature: 0.3

  real_time_analysis:
    model: grok-beta
    provider: grok
    reason: "X/Twitter integration, real-time sentiment"
    temperature: 0.5

  multimodal_analysis:
    model: gemini-2.0-flash-exp
    provider: gemini
    reason: "Fast multimodal processing"
    temperature: 0.4
```

---

## Best Practices

### 1. **Use the Right Model for the Job**
- **Research** → Perplexity (citations)
- **Narrative** → Claude (voice)
- **Speed** → GPT or Gemini (fast)
- **Sentiment** → Grok (X data)
- **Vision** → Gemini or Claude (charts)

### 2. **Chain Models for Complex Tasks**
- Start with Perplexity for current data
- Use Claude for synthesis
- Verify with GPT

### 3. **Monitor Costs**
- Claude: Most expensive, use for high-value narrative
- GPT: Mid-range, good for extraction
- Grok/Perplexity/Gemini: Cost-effective for specific tasks

### 4. **Leverage Unique Capabilities**
- **Perplexity**: Only model with real-time web + citations
- **Grok**: Only model with X/Twitter integration
- **Gemini**: Fastest for vision + long context
- **Claude**: Best for your voice and deep reasoning

---

## Next Steps

1. **Add your API keys** to `configs/secrets.env`
2. **Test each model** with sample prompts
3. **Customize routing** in `configs/ai_routing.yaml`
4. **Build workflows** combining multiple models

## Status Check

After adding keys, verify:

```bash
python cli.py status
```

Expected output:
```
✓ FRED API
✓ Google API
✓ Anthropic (Claude)
✓ OpenAI (GPT)
✓ Grok (xAI)
✓ Perplexity
✓ Gemini (Google)
```

---

**You now have the most advanced AI orchestration system for macro research. Six models, intelligent routing, one unified interface.**

**LIGHTHOUSE MACRO**
MACRO, ILLUMINATED.
