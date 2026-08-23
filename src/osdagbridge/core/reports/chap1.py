# =============================================================================
# Chapter 1: Project Information
# =============================================================================

from osdagbridge.core.reports.report_utils import _tex
from osdagbridge.core.reports.styles import make_longtable


def ch1_project_info(m):
    rows = [
        r"Project Name & " + _tex(m.project_name) + r" \\[6pt] \hline",
        r"Project Location & " + _tex(m.project_location) + r" \\[6pt] \hline",
        r"Lead Structural Designer & " + _tex(m.designer) + r" \\[6pt] \hline",
        r"Design Reviewer / Approver & " + _tex(m.reviewer) + r" \\[6pt] \hline",
        r"Engineering Organization & " + _tex(m.company) + r" \\[6pt] \hline",
        r"Client / Authority & " + _tex(m.client) + r" \\[6pt] \hline",
        r"Design Software & OsdagBridge (FOSSEE, IIT Bombay) \\[6pt] \hline",
    ]

    table_proj = make_longtable(
        col_spec=r"|L{5.5cm}|L{9.5cm}|",
        caption="Project and Design Team Details",
        headers=["Parameter", "Details"],
        rows=rows,
        label="tab:project-details",
    )

    return rf"""
\chapter{{Project Information}}

This section records all project metadata, design team credentials, and governing design standard references.

\section{{Project and Design Team Details}}
\label{{sec:project-details}}

\vspace{{0.4em}}
{table_proj}

\section{{Applicable Codes and Standards}}
\label{{sec:codes}}

\begin{{itemize}}
\item \textbf{{IRC 5:2015}}: \textit{{Standard Specifications and Code of Practice for Road Bridges, Section I: General Features of Design.}}
\item \textbf{{IRC 6:2017}}: \textit{{Standard Specifications and Code of Practice for Road Bridges, Section II: Loads and Load Combinations (Incorporating all amendments).}}
\item \textbf{{IRC 22:2015}}: \textit{{Standard Specifications and Code of Practice for Road Bridges, Section VI: Composite Construction (Limit State Design).}}
\item \textbf{{IRC 24:2010}}: \textit{{Standard Specifications and Code of Practice for Road Bridges, Section V: Steel Road Bridges (Limit State Method).}}
\item \textbf{{IRC 112:2020}}: \textit{{Code of Practice for Concrete Road Bridges (Limit State Method).}}
\item \textbf{{IRC SP 114:2018}}: \textit{{Guidelines for Seismic Design of Road Bridges.}}
\item \textbf{{IS 800:2007}}: \textit{{General Construction in Steel --- Code of Practice (Third Revision).}}
\item \textbf{{IS 2062:2011}}: \textit{{Hot Rolled Medium and High Tensile Structural Steel --- Specification.}}
\item \textbf{{IS 456:2000}}: \textit{{Plain and Reinforced Concrete --- Code of Practice.}}
\end{{itemize}}
"""
