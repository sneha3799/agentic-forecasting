# Agentic Forecasting — Technical Design

## Purpose

This document is the **technical source of truth** for the agentic forecasting repository. It captures all significant architectural decisions, library selections, interface designs, and build plans.

> **Maintenance contract:** This document MUST be kept up to date. Whenever an architectural decision is made, revised, or reversed — in a coding session, a planning conversation, or a commit — this document should be updated in the same session. Do not let decisions live only in chat logs or planning notes. Planning notes are for exploration and quick logging; this document is for what we have decided and are building toward.

---

## Library & Tooling Decisions

### Forecasting: Darts (over sktime)

**Decision date:** Mar 31, 2026

**Darts** is the primary numerical forecasting library.

Key reasons:
- Consistent `fit()`/`predict()` API across all model types — one mental model to debug
- Better developer experience for a mixed-skill bootcamp audience
- Built-in `historical_forecasts()` and `backtest()` utilities are first-class
- Modular install (`pip install darts` vs `darts[torch]`) lets us stage complexity incrementally
- Lower support burden for the bootcamp instructor

sktime remains a valid reference for specific use cases (AutoARIMA, panel forecasting) but is not the primary interface we support or teach.

### Agent Framework: Google ADK

**Google ADK** is the default framework for building forecasting agents. Additional dependencies are introduced only when blocked by ADK's native capabilities.

### Tracing & Logging: Langfuse

**Langfuse** is selected for tracing. The integration point is at the **Predictor level** — reasoning traces are linked to prediction outcomes via `predictor_id` + `question_id`. This is separate from the evaluation harness's own prediction/resolution/score logging. Implementation details are deferred.

### Structured Outputs: Pydantic

All prediction payloads and data interfaces use **Pydantic** models with mypy-compatible typing throughout.

---

## Evaluation Architecture

### Core Insight

Backtesting and live evaluation are the same loop — they differ only in whether ground truth is already known. A single unified architecture handles both.

### Unified Loop

```
Predictor → Prediction → Resolution → Score
```

- **Predictor** — model-agnostic; produces a `Prediction` given a question/task and an as-of date
- **Prediction** — paradigm-specific payload, but shares common metadata: `question_id`, `predictor_id`, `issued_at`, `horizon`
- **ResolutionStore** — pre-populated in backtest mode; fills in asynchronously in live mode
- **Scorer** — swappable: CRPS for continuous forecasts, Brier score for discrete event

### Prediction Payload Types

Two concrete payload types:

- **`ContinuousForecast`** — point values + quantiles, for economic/time series tasks
- **`BinaryForecast`** — probability estimate, for Metaculus-style discrete event questions

We follow existing standards rather than inventing new ones. For discrete event forecasting, we follow Metaculus conventions.

---

## Data Service

### Design Philosophy

Two categories of data are treated very differently:

| Category | Examples | How it's delivered | Live calls during sessions? |
| :--- | :--- | :--- | :--- |
| **Deterministic** | historical series, resolution targets | local data service, pre-populated | No |
| **Stochastic context** | news, web search, live indicators | live API calls, agentic tools | Yes — logged via Langfuse |

No outbound calls for historical or resolution data occur during bootcamp sessions or backtests. Adapters are run offline to populate the local store ahead of time.

### Architecture

```
DataService
├── SeriesStore          # historical time series, indexed by series_id + as_of
├── ResolutionStore      # ground truth values at resolution timestamps
├── CutoffEnforcer       # enforces information cutoff discipline (see below)
└── ProviderAdapters
    ├── StatCanAdapter
    ├── FREDAdapter
    └── yfinanceAdapter
```

### Information Cutoff Discipline

The `CutoffEnforcer` enforces a critical principle: **no model or agent may access data that would not have been available at the time the forecast was issued**. This is the unifying concept across both time series backtesting and discrete event evaluation, and is a core teaching objective of the bootcamp.

### Open Questions

- **Data service update pipeline**: How are updates handled as new data releases come in (e.g., monthly StatCan drops)? This needs to be resolved before live evaluation infrastructure is built, and is important for the live benchmark extension.

---

## Build Plan

### Principle: Two Concrete Passes Before Abstracting

Shared abstractions are extracted after both passes are working — not designed in advance.

1. **Pass 1 — Economic forecasting** (StatCan, continuous series, `ContinuousForecast` payloads)
2. **Pass 2 — Metaculus predictions** (binary/categorical, discrete event, `BinaryForecast` payloads)

### Connection to Project Charter Deliverables

- The **evaluation harness + data service** together constitute the *forecast resolution service* in Phase 2 of the project proposal.
- The **live experiment leaderboard** is the data service update pipeline made visible.
- The **information cutoff discipline** is the unifying teaching concept across both forecasting paradigms.
