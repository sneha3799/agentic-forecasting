# AGENTS.md

## How to use this file

Instructions here are **general when possible, specific when needed.** Prefer patterns and principles over static lists — static lists go stale. When something is specific (a command, a maintenance contract, a non-obvious convention), it is specific for a reason.

---

## Project documentation

### planning-docs/

`./planning-docs/roadmap.md` captures the architecture principles worth preserving and the catalog of extension ideas. It is the place for cross-cutting design notes, not per-task tracking.

The older planning log, backlog, project charter, and technical-design files under `planning-docs/` (and `planning-docs/archive/`) are retired and kept only for continuity — do not add new decisions to them. When a change affects architecture, datasets, repo layout, or the set of reference implementations, update `planning-docs/roadmap.md` (for an architectural principle or a new extension idea) and the relevant README files in the same session.

Project shape to keep in mind:

- The core library `aieng.forecasting` owns stable infrastructure; reusable predictors live in `aieng.forecasting.methods`; use-case material lives in `implementations/<use-case>/`.
- YAML specs are co-located under `implementations/<use-case>/specs/`.
- Reference implementations: Getting Started, Food Price Forecasting, Energy/Oil (stateless capability track plus an adaptive learning agent), BoC Rate Decisions (quantitative path, cutoff-aware press-release ingestion, and a reasoning-alignment evaluator), and S&P 500 (in active development).
- Energy/oil's older information-session notebooks are archived under `playground/energy_case_study/`.
- Continuous and discrete-event forecasts are output modalities; numerical methods, LLM Processes, and agentic forecasters are method families that apply to either.

### README files

Search the repo for `README.md` files (excluding `.venv/`) to find all current READMEs. Check them for needed updates whenever a design change is made — datasets, architecture, repo layout, new methods or implementations. READMEs are the primary user surface and the first thing a new contributor reads; keep them accurate and production-quality (no internal program/ownership framing).

---

## Development conventions

### Data cache

Historical data is stored in `data/` at the repo root (gitignored). Before running notebooks or scripts that depend on live data, populate the cache by running the relevant script in `scripts/` (e.g. `uv run python scripts/fetch_cpi.py`). Never commit data files.

### Model selection

The project standardizes on **two** Vector-proxy models so examples stay consistent: `gemini-3.1-flash-lite-preview` (the **lite / default** model) and `gemini-3.5-flash` (the **advanced** model, used for the adaptive-agent path and curriculum runs). Both are defined once in `aieng.forecasting.models` as `LITE_MODEL` / `ADVANCED_MODEL` (`DEFAULT_MODEL = LITE_MODEL`). Reference these constants in code rather than hardcoding model strings; notebooks pick one of the two literals with the other shown as a commented alternative. See `planning-docs/vector-llm-proxy.md` for the full convention.

### Code quality (not on commit)

Git commits **do not** run automated hooks locally. Run **`make lint`** (ruff format + ruff check + mypy on `aieng`) before pushing — a passing `make lint` means CI will be happy with the code. To fully mirror CI (yaml checks, uv-lock, etc.) run **`uv run pre-commit run --all-files`**. CI on `main` runs the same `pre-commit` config.

Notebook outputs **are** committed at the author's discretion — `nbstripout` is not in the pre-commit config. Strip outputs manually before committing if you don't want them in the repo.

### Test philosophy

Tests should justify their existence. Write tests for: non-obvious logic that is easy to get wrong, defensive contracts (e.g. copy-on-return), and error paths where the message matters. Do not write tests for: Pydantic model construction (Pydantic already validates this), trivial Python behaviour (sorted lists, empty dicts), or mock-interaction assertions that test implementation rather than behaviour. When in doubt, fewer focused tests are better than many shallow ones.
