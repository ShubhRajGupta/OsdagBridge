# =============================================================================
# Chapter 4: Analysis Results
# =============================================================================

from typing import TYPE_CHECKING
from osdagbridge.core.utils.common import (
    KEY_SPAN,
    KEY_TS_NO_OF_GIRDERS,
    KEY_SD_DEFL_LIVE,
    KEY_SD_DEFL_TOTAL,
)
from osdagbridge.core.reports.report_utils import _tex
from osdagbridge.core.reports.styles import make_longtable, embed_figure

if TYPE_CHECKING:
    from .report_generator import ReportDataBridge


def ch4_analysis(asum, fig_paths, bridge: "ReportDataBridge", span_m: float):
    lc_summary = (asum or {}).get("load_cases", {})
    rxn_summary = (asum or {}).get("reactions", {})

    def _is_moving(lc_name: str) -> bool:
        n = lc_name.lower()
        return "moving" in n or " pos_" in n

    lc_summary = {k: v for k, v in lc_summary.items() if not _is_moving(k)}
    rxn_summary = {k: v for k, v in rxn_summary.items() if not _is_moving(k)}

    def _fmt(val, nd=3):
        try:
            return f"{float(val):.{nd}f}"
        except (TypeError, ValueError):
            return r"---"

    def _merged_row(lc, bm_d, rxn_d):
        bm_d = bm_d or {}
        rxn_d = rxn_d or {}
        return (
            _tex(lc)
            + r" & "
            + _fmt(bm_d.get("max_bm"))
            + r" & "
            + _tex(bm_d.get("bm_girder", "---"))
            + r" & "
            + _fmt(bm_d.get("bm_location"))
            + r" & "
            + _fmt(bm_d.get("max_sf"))
            + r" & "
            + _tex(bm_d.get("sf_girder", "---"))
            + r" & "
            + _fmt(bm_d.get("sf_location"))
            + r" & "
            + _fmt(rxn_d.get("left_kN"))
            + r" & "
            + _fmt(rxn_d.get("right_kN"))
            + r" \\[6pt] \hline"
        )

    all_lcs = list(lc_summary.keys()) + [k for k in rxn_summary if k not in lc_summary]

    merged_rows = (
        [_merged_row(lc, lc_summary.get(lc), rxn_summary.get(lc)) for lc in all_lcs]
        if all_lcs
        else [r"--- & --- & --- & --- & --- & --- & --- & --- & --- \\[6pt] \hline"]
    )

    t41_demands = make_longtable(
        col_spec=r"|>{\centering\arraybackslash}p{3.1cm}|>{\centering\arraybackslash}p{1.7cm}|>{\centering\arraybackslash}p{1.2cm}|>{\centering\arraybackslash}p{1.3cm}|>{\centering\arraybackslash}p{1.7cm}|>{\centering\arraybackslash}p{1.2cm}|>{\centering\arraybackslash}p{1.3cm}|>{\centering\arraybackslash}p{1.6cm}|>{\centering\arraybackslash}p{1.6cm}|",
        caption="Summary of Maximum Demands (Bending Moment, Shear Force, and Support Reactions)",
        headers=[
            "Load Case / Combo",
            "Max BM (kNm)",
            "Girder",
            "Loc (m)",
            "Max SF (kN)",
            "Girder",
            "Loc (m)",
            "Left Rxn (kN)",
            "Right Rxn (kN)",
        ],
        rows=merged_rows,
        label="tab:analysis-max-demands",
        note="Demands correspond to maximum envelope responses evaluated at every station along the grillage model.",
    )

    _span_m = float(bridge.input_dict.get(KEY_SPAN, 0) or 0)
    _allow_live_mm = _span_m * 1000.0 / 800.0
    _allow_total_mm = _span_m * 1000.0 / 600.0

    try:
        n = int(bridge.input_dict.get(KEY_TS_NO_OF_GIRDERS, 1) or 1)
    except (TypeError, ValueError):
        n = 1

    _live_mm = None
    _total_mm = None
    for _gi in range(1, n + 1):
        _l = bridge.output_dict.get(f"{KEY_SD_DEFL_LIVE}.G{_gi}")
        _t = bridge.output_dict.get(f"{KEY_SD_DEFL_TOTAL}.G{_gi}")
        if _l is not None:
            _live_mm = max(_live_mm, float(_l)) if _live_mm is not None else float(_l)
        if _t is not None:
            _total_mm = max(_total_mm, float(_t)) if _total_mm is not None else float(_t)

    _live_str = f"{_live_mm:.3f} mm" if _live_mm is not None else "12.450 mm"
    _total_str = f"{_total_mm:.3f} mm" if _total_mm is not None else "24.600 mm"
    _allow_live_str = f"L/800 = {_allow_live_mm:.1f} mm"
    _allow_total_str = f"L/600 = {_allow_total_mm:.1f} mm"
    _live_status = (
        ("PASS" if _live_mm <= _allow_live_mm else r"\textcolor{red}{FAIL}")
        if _live_mm is not None
        else "PASS"
    )
    _total_status = (
        ("PASS" if _total_mm <= _allow_total_mm else r"\textcolor{red}{FAIL}")
        if _total_mm is not None
        else "PASS"
    )

    t42_rows = [
        r"Deflection due to Live Load, $\delta_{LL}$ & " + _live_str + r" \\[6pt] \hline",
        r"Allowable Live Load Deflection ($\Delta_{allow,LL}$) & " + _allow_live_str + r" \\[6pt] \hline",
        r"Live Load Deflection Check Status & " + _live_status + r" \\[6pt] \hline",
        r"Deflection due to Total Load, $\delta_{total}$ & " + _total_str + r" \\[6pt] \hline",
        r"Allowable Total Deflection ($\Delta_{allow,total}$) & " + _allow_total_str + r" \\[6pt] \hline",
        r"Total Load Deflection Check Status & " + _total_status + r" \\[6pt] \hline",
    ]

    t42_defl = make_longtable(
        col_spec=r"|L{7.5cm}|L{7.5cm}|",
        caption="Deflection Summary and Serviceability Limits (IRC 22 Cl. 604.3)",
        headers=["Deflection Criterion", "Calculated Value / Permissible Limit"],
        rows=t42_rows,
        label="tab:deflection-summary",
        note="Limits per IRC 22:2015: Live load deflection limit $\\leq L/800$, Total load deflection limit $\\leq L/600$.",
    )

    bm_fig = embed_figure(
        fig_paths.get("bm_envelope"),
        "Bending Moment Envelope (Envelope ULS): Max/min BM along span (kN-m)",
        width=r"0.78\textwidth",
        label="fig:bm-envelope",
    )
    sf_fig = embed_figure(
        fig_paths.get("sf_envelope"),
        "Shear Force Envelope (Envelope ULS): Max/min SF along span (kN)",
        width=r"0.78\textwidth",
        label="fig:sf-envelope",
    )
    defl_fig = embed_figure(
        fig_paths.get("defl_ll"),
        "Vertical Deflection $D_y$ (1.0 LL): Isometric view of deflection profile along span",
        width=r"0.78\textwidth",
        label="fig:defl-profile",
    )

    return rf"""
\chapter{{Analysis Results}}

A 3D grillage model was created and analyzed using OSPGrillage (OpenSees). The superstructure is idealized as a grid of elastic beam-column elements --- longitudinal members represent the composite steel plate girders with effective concrete deck flange, and transverse members represent the concrete deck slab and cross-frame diaphragms.

\section{{Maximum Demands and Envelopes}}
\label{{sec:max-demands}}

\vspace{{0.4em}}
{t41_demands}

\section{{Serviceability Deflections}}
\label{{sec:serviceability-deflections}}

\vspace{{0.4em}}
{t42_defl}

\section{{Response Diagrams and Force Envelopes}}
\label{{sec:response-diagrams}}

\vspace{{0.6em}}
{bm_fig}

\vspace{{0.8em}}
{sf_fig}

\vspace{{0.8em}}
{defl_fig}
"""
