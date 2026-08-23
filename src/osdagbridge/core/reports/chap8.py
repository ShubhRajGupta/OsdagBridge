# =============================================================================
# Chapter 8: Design Standards & Assumptions
# =============================================================================

from typing import List
from osdagbridge.core.utils.common import KEY_DESIGN_MODE
from osdagbridge.core.reports.styles import make_longtable


def ch8_design_log(log_entries: List[str], input_dict: dict) -> str:
    mode = str(input_dict.get(KEY_DESIGN_MODE, "Optimized")).strip().lower()
    is_custom = mode in {"custom", "customized"}
    return _ch8_assumptions(is_custom)


def _ch8_assumptions(is_custom: bool) -> str:
    irc_rows = [
        r"IRC 5 & 2015 & General Features of Design --- Carriageway widths, kerb, footpath, clearance dimensions \\[6pt] \hline",
        r"IRC 6 & 2017 & Loads and Load Combinations --- Dead load, vehicle live load, impact, wind, seismic, thermal \\[6pt] \hline",
        r"IRC 22 & 2015 & Composite Construction (Limit State) --- Effective slab width, composite section properties, ULS/SLS design, shear studs \\[6pt] \hline",
        r"IRC 24 & 2010 & Steel Road Bridges (Limit State) --- Plate girder detailing, stiffener design, skew limits, lateral bracing \\[6pt] \hline",
        r"IRC 112 & 2020 & Concrete Road Bridges --- Reinforced concrete deck slab flexure, beam shear, punching shear, crack control \\[6pt] \hline",
        r"IRC SP 114 & 2018 & Guidelines for Seismic Design of Road Bridges \\[6pt] \hline",
    ]

    t_irc = make_longtable(
        col_spec=r"|C{2.5cm}|C{2.0cm}|L{10.5cm}|",
        caption="Indian Roads Congress (IRC) Design Standards",
        headers=["Standard Code", "Year", "Scope and Application in OsdagBridge"],
        rows=irc_rows,
        label="tab:irc-standards",
    )

    is_rows = [
        r"IS 800 & 2007 & General Construction in Steel --- Tension, compression, bending, shear, LTB, stiffeners, connection checks \\[6pt] \hline",
        r"IS 456 & 2000 & Plain and Reinforced Concrete --- Stress block parameters for deck slab ultimate moment capacity \\[6pt] \hline",
        r"IS 1786 & 2008 & High Strength Deformed Steel Bars and Wires for Concrete Reinforcement \\[6pt] \hline",
        r"IS 1893 (Part 3) & 2014 & Criteria for Earthquake Resistant Design of Structures (Bridges and Retaining Walls) \\[6pt] \hline",
        r"IS 2062 & 2011 & Hot Rolled Medium and High Tensile Structural Steel Specification \\[6pt] \hline",
    ]

    t_is = make_longtable(
        col_spec=r"|C{2.8cm}|C{2.0cm}|L{10.2cm}|",
        caption="Bureau of Indian Standards (IS) Design Standards",
        headers=["Standard Code", "Year", "Scope and Application in OsdagBridge"],
        rows=is_rows,
        label="tab:is-standards",
    )

    return rf"""
\chapter{{Standards \& Assumptions}}
\label{{ch:Design-Standards}}

This chapter lists the governing design codes, standards, and engineering assumptions incorporated into OsdagBridge calculation routines.

\section{{Design Standards}}
\label{{sec:design_standards}}

\vspace{{0.4em}}
{t_irc}

\vspace{{0.6em}}
{t_is}

\section{{Design Assumptions and Implementation Scope}}
\label{{sec:scope_assumptions}}

\begin{{enumerate}}
\item \textbf{{Structural Superstructure}}: The bridge superstructure is analyzed as simply supported composite steel plate girders with an in-situ reinforced concrete deck slab.
\item \textbf{{Analysis Method}}: 3D grillage analysis is performed using OpenSees (via OSPGrillage). Wheel load dispersal through wearing course and deck slab is calculated per IRC 6:2017.
\item \textbf{{Effective Flange Width}}: Effective slab width for composite girder action is evaluated in accordance with IRC 22:2015 Cl. 602.
\item \textbf{{Buckling \& Stability}}: Lateral torsional buckling of girders during construction and in service is assessed per IS 800:2007 Cl. 8.2.2.
\item \textbf{{Substructure \& Bearings}}: Design of piers, abutments, foundations, bearings, and expansion joints are omitted from this superstructure report.
\end{{enumerate}}
"""
