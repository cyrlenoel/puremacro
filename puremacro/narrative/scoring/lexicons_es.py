"""Bilingual Spanish macroeconomic and central bank monetary policy lexicons.

Provides specialized Spanish dictionaries for:
- Monetary Policy Stance: Hawkish vs. Dovish tone in Central Bank minutes (Banxico, BCCh, BanRep).
- Inflation Risk: Upward vs. Downward balance of risks.
- Economic Activity: Expansion vs. Contraction / Slowdown.
- Financial Stability: Vulnerabilities, credit risk, exchange rate stress.
"""

from __future__ import annotations

import functools
import re
from dataclasses import dataclass

# Domain-specific Spanish monetary policy and macro lexicon
SPANISH_MACRO_LEXICON = {
    "hawkish": [
        "postura restrictiva",
        "postura contractiva",
        "alza de tasas",
        "aumento de tasas",
        "incremento en la tasa",
        "presiones inflacionarias",
        "presiones de costos",
        "balance de riesgos sesgado al alza",
        "sobrecalentamiento",
        "anclar las expectativas",
        "desanclaje de expectativas",
        "endurecimiento monetario",
        "restringir la liquidez",
        "contener la inflacion",
        "contener la inflación",
        "riesgos inflacionarios",
        "inflacion subyacente elevada",
        "inflación subyacente elevada",
        "choque inflacionario",
        "segundo orden",
        "efectos de segundo orden",
        "resistencia a la baja",
        "rigidez de precios",
        "demanda agregada sobrecalentada",
        "apretamiento cuantitativo",
        "mantener la cautela",
    ],
    "dovish": [
        "postura acomodaticia",
        "recorte de tasas",
        "disminución de tasas",
        "reducción de tasas",
        "baja en la tasa",
        "holgura económica",
        "brecha del producto negativa",
        "balance de riesgos sesgado a la baja",
        "desaceleración económica",
        "debilitamiento de la demanda",
        "estímulo monetario",
        "relajamiento monetario",
        "flexibilización monetaria",
        "convergencia de la inflación",
        "trayectoria descendente",
        "alivio en costos",
        "menores presiones",
        "atenuación de presiones",
        "enfriamiento del mercado laboral",
        "espacio para recortar",
        "ciclo de recortes",
        "facilitar el crédito",
    ],
    "inflation_uncertainty": [
        "incertidumbre sobre precios",
        "volatilidad cambiaria",
        "depreciación del peso",
        "traspaso cambiario",
        "pass-through",
        "choque de oferta",
        "disrupciones en cadenas",
        "precios de energéticos",
        "precios agropecuarios",
        "persistencia inflacionaria",
        "anomalías en precios",
        "volatilidad en materias primas",
    ],
    "financial_stress": [
        "estrés financiero",
        "volatilidad en mercados",
        "aversión al riesgo",
        "salida de capitales",
        "riesgo soberano",
        "ampliación de diferenciales",
        "riesgo crediticio",
        "morosidad",
        "vulnerabilidad bancaria",
        "tensión de liquidez",
    ],
}


@functools.lru_cache(maxsize=32)
def _compile_lexicon(
    lex_tuple: tuple[tuple[str, tuple[str, ...]], ...],
) -> dict[str, re.Pattern[str]]:
    """Helper to compile a combined regex pattern per category and cache it."""
    compiled = {}
    for key, terms in lex_tuple:
        if terms:
            # Sort terms by length descending to match longer phrases first if they overlap,
            # though findall won't overlap, it's good practice for alternations.
            sorted_terms = sorted(terms, key=len, reverse=True)
            escaped = [re.escape(t) for t in sorted_terms]
            pattern = re.compile(r"\b(?:" + "|".join(escaped) + r")\b")
            compiled[key] = pattern
    return compiled


def _to_hashable(
    lexicon: dict[str, list[str]],
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    return tuple(sorted((k, tuple(v)) for k, v in lexicon.items()))


@dataclass(frozen=True)
class SpanishSentimentResult:
    """Detailed score from Spanish macroeconomic text scoring."""

    net_stance: float
    hawkish_count: int
    dovish_count: int
    uncertainty_count: int
    stress_count: int
    matched_hawkish: list[str]
    matched_dovish: list[str]
    matched_uncertainty: list[str]
    matched_stress: list[str]


def score_spanish_macro_sentiment(
    text: str,
    lexicon: dict[str, list[str]] | None = None,
) -> SpanishSentimentResult:
    """Score Spanish central bank or macro text for monetary policy stance and risks.

    Parameters
    ----------
    text : str
        Input Spanish text (e.g. Banxico minutas paragraph).
    lexicon : dict, optional
        Custom dictionary with keys 'hawkish', 'dovish', 'inflation_uncertainty', 'financial_stress'.
        Defaults to `SPANISH_MACRO_LEXICON`.

    Returns
    -------
    SpanishSentimentResult
        Net stance score in [-1.0, +1.0] (+1 = strongly hawkish, -1 = strongly dovish),
        counts, and lists of matched keywords.
    """
    if lexicon is None:
        lexicon = SPANISH_MACRO_LEXICON

    # ⚡ Bolt: Compile a combined regex pattern per category and cache it.
    compiled_lex = _compile_lexicon(_to_hashable(lexicon))

    text_lower = text.lower()

    matched_hawk = (
        compiled_lex["hawkish"].findall(text_lower) if "hawkish" in compiled_lex else []
    )
    matched_dove = (
        compiled_lex["dovish"].findall(text_lower) if "dovish" in compiled_lex else []
    )
    matched_unc = (
        compiled_lex["inflation_uncertainty"].findall(text_lower)
        if "inflation_uncertainty" in compiled_lex
        else []
    )
    matched_str = (
        compiled_lex["financial_stress"].findall(text_lower)
        if "financial_stress" in compiled_lex
        else []
    )

    h_count = len(matched_hawk)
    d_count = len(matched_dove)
    total = h_count + d_count

    if total == 0:
        net_stance = 0.0
    else:
        net_stance = float((h_count - d_count) / total)

    return SpanishSentimentResult(
        net_stance=net_stance,
        hawkish_count=h_count,
        dovish_count=d_count,
        uncertainty_count=len(matched_unc),
        stress_count=len(matched_str),
        matched_hawkish=matched_hawk,
        matched_dovish=matched_dove,
        matched_uncertainty=matched_unc,
        matched_stress=matched_str,
    )


__all__ = [
    "SPANISH_MACRO_LEXICON",
    "SpanishSentimentResult",
    "score_spanish_macro_sentiment",
]
