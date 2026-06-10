"""Tuned predictor recipes for the BoC rate-decision experiment.

Use-case-specific predictors and recipes live here, paired with the
task-agnostic methods in :mod:`aieng.forecasting.methods`:

- :mod:`logistic_baseline` — the conventional baseline: a logistic
  regression on leak-safe macro features, fit at every forecast origin.
  Feature engineering is domain-specific, so the predictor lives in the use
  case (mirroring the placement of energy's Prophet model).
- :mod:`llmp_binary` — recipe wiring
  :class:`~aieng.forecasting.methods.BinaryProbabilityLLMPredictor` with a
  BoC-specific prompt context block.
"""

from .llmp_binary import build_llmp_binary
from .logistic_baseline import BoCLogisticPredictor


__all__ = ["BoCLogisticPredictor", "build_llmp_binary"]
