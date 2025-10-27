## COPILOT / AI AGENT INSTRUCTIONS — LHM (Lighthouse Macro Monorepo)

Purpose: help an AI coding agent be immediately productive in this repo by surfacing structure, conventions, workflows, and exact examples found in the codebase.

- Languages & formats: Python (analysis + libraries) and Jupyter notebooks are primary. There are also Node/TypeScript client integrations in `src/data_clients/*` (see `docs/integration-implementation-guide.md`).

- Quick start (commands you can run or suggest):

  - Clone & install Python deps when `requirements.txt` exists: `pip install -r requirements.txt`.
  - Run the test suite: `pytest tests/ -v` (unit + integration under `tests/`).
  - Run notebook work: open Jupyter Lab/Notebook and use relative paths for data I/O (see `notebooks/README.md`).

- Project shape (key paths to reference):

  - `data/` — raw / external / interim / processed (large data not committed).
  - `src/` — reusable Python modules (type hints and docstrings required).
  - `notebooks/` — Jupyter analysis; use relative paths and export charts to `charts/`.
  - `configs/` — YAML/JSON configurations for data clients and charting.
  - `docs/` — integration & implementation guides (see `docs/integration-implementation-guide.md`).

- Important, discoverable conventions (do not invent):

  - Charting standards live in the root README and `configs/charting.yaml` examples: no gridlines, all four spines visible, specific color palette (Ocean Blue, Deep Sunset Orange, Neon Carolina Blue, Neon Magenta, Medium-Light Gray), line width ~3, watermark "MACRO, ILLUMINATED." bottom-right.
  - Notebooks must use relative paths and set random seeds for reproducibility (see `notebooks/README.md`).
  - Credentials and API keys: never commit; use environment variables and `.env` locally (configs/README.md and root README emphasize this).
  - Tests: use `pytest`, mock external API calls, include sample data for unit tests (see `tests/README.md`).

- Integration patterns and examples you can use directly:

  - To add or update external repositories as subtrees (examples from `docs/integration-implementation-guide.md`):
    - Add: `git subtree add --prefix=notebooks/daily_digest https://github.com/.../Daily_Digest.git main --squash`
    - Pull updates: `git subtree pull --prefix=src/data_clients/fred_mcp https://github.com/.../fred-mcp-server.git main --squash`
  - When integrating, update imports/paths after moving code; the guide shows `find` + `sed` example for path rewrites.

- CI / verification specifics:

  - The repo expects a GitHub Actions workflow which sets up Python and Node and runs `pytest` and `npm test` (see docs/examples in the integration guide). Use matrixed Python versions when creating CI changes.

- What to avoid / hard constraints (explicit from repo):

  - Do not add or commit raw data or secrets to `data/` or `configs/`.
  - Keep function signatures stable; prefer adding helpers rather than changing public APIs without tests.

- Files to consult when making edits or suggestions (examples to quote or patch):

  - `README.md` (root) — project overview, charting rules, data sources list.
  - `src/README.md` — source/module expectations (type hints, docstrings, PEP8).
  - `notebooks/README.md` — notebook I/O and reproducibility rules.
  - `docs/integration-implementation-guide.md` — exact git subtree commands and config templates.
  - `configs/` — config examples for FRED, SEC, and charting templates.

- Helpful short contract for any change you produce:

  1. Inputs: path(s) you modify (file names), environment assumptions (Python >=3.8), and whether external keys are required.
  2. Outputs: files created/modified, and commands/tests to verify behavior (e.g., `pytest tests/`).
  3. Error modes: missing config/env vars -> document required env var names and add defensive checks.

- If anything is ambiguous, ask these targeted questions before editing:
  1. Which environment (Python version) should I target for this change? (default: 3.8+)

2.  Do you want new integration added as subtree or submodule? (integration guide uses subtree by default)

Keep this file concise. After reviewing a proposed change, ask the human for missing secrets, target Python version, and whether to run full CI. When done, ask for feedback and iterate.

---

References: `README.md`, `src/README.md`, `notebooks/README.md`, `docs/integration-implementation-guide.md`, `configs/`.

# Copilot Instructions — LHM (Source of Truth Monorepo)

## Purpose

LHM is the internal, single source of truth for Lighthouse Macro. It contains code, datasets, notebooks, and reusable modules powering reproducible macro research.

## Operating Mode

- Task-first, agent-style. Concise and technical.
- Never fabricate or approximate data. If inputs are missing, stop and request the exact source (FRED, TreasuryDirect, OFR, TIC, NY Fed, etc.).
- Python by default (pandas, numpy, matplotlib; statsmodels/pyarrow optional).
- Deliver runnable code first; add minimal context after.

## Charting Standards

- No gridlines. All four spines visible. Right axis is primary.
- Color palette: Ocean Blue, Deep Sunset Orange, Neon Carolina Blue, Neon Magenta, Medium-Light Gray.
- Line thickness ~3; longest history available.
- Axes matched at zero; independently scaled (linear/log/stdev ranges) for clarity.
- Labels clear, no overlaps. Watermark "MACRO, ILLUMINATED." bottom-right (never overlap data).

## Project Structure (recommended)

- `/data/` (raw, external, interim, processed) — never commit proprietary client data.
- `/src/` (reusable modules)
- `/notebooks/` (analysis notebooks; keep I/O paths relative)
- `/charts/` (exported figures, auto-watermarked)
- `/reports/` (draft outputs for Lighthouse Macro repo)
- `/configs/` (YAML/JSON configs, credentials via env vars only)
- `/tests/`

##
