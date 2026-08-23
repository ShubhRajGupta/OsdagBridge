# =============================================================================
# Chapter 7: Material Take-off & Quantity Summary
# =============================================================================

from osdagbridge.core.reports.styles import make_longtable, embed_figure


def ch7_quantities(input_dict, fig_paths=None):
    # Prepare rows for Table 7.1 (BOM)
    rows = [
        r"1 & Structural Steel (IS 2062) for Girders & "
        + str(input_dict.get("steel_girders_vol_formula", "N.A."))
        + r" & "
        + str(input_dict.get("steel_girders_qty", "N.A."))
        + r" & "
        + str(input_dict.get("steel_girders_vol_total", "N.A."))
        + r" & "
        + str(input_dict.get("steel_girders_wt_single", "N.A."))
        + r" & "
        + str(input_dict.get("steel_girders_wt_total", "N.A."))
        + r" \\[6pt] \hline",
        r"2(a) & Cross Bracing --- Top Chord & "
        + str(input_dict.get("bracing_top_vol_formula", "N.A."))
        + r" & "
        + str(input_dict.get("bracing_top_qty", "N.A."))
        + r" & "
        + str(input_dict.get("bracing_top_vol_total", "N.A."))
        + r" & "
        + str(input_dict.get("bracing_top_wt_single", "N.A."))
        + r" & "
        + str(input_dict.get("bracing_top_wt_total", "N.A."))
        + r" \\[6pt] \hline",
        r"2(b) & Cross Bracing --- Bottom Chord & "
        + str(input_dict.get("bracing_bot_vol_formula", "N.A."))
        + r" & "
        + str(input_dict.get("bracing_bot_qty", "N.A."))
        + r" & "
        + str(input_dict.get("bracing_bot_vol_total", "N.A."))
        + r" & "
        + str(input_dict.get("bracing_bot_wt_single", "N.A."))
        + r" & "
        + str(input_dict.get("bracing_bot_wt_total", "N.A."))
        + r" \\[6pt] \hline",
        r"2(c) & Cross Bracing --- Diagonal Chord & "
        + str(input_dict.get("bracing_diag_vol_formula", "N.A."))
        + r" & "
        + str(input_dict.get("bracing_diag_qty", "N.A."))
        + r" & "
        + str(input_dict.get("bracing_diag_vol_total", "N.A."))
        + r" & "
        + str(input_dict.get("bracing_diag_wt_single", "N.A."))
        + r" & "
        + str(input_dict.get("bracing_diag_wt_total", "N.A."))
        + r" \\[6pt] \hline",
        r"3 & Concrete (M40) for Deck Slab & "
        + str(input_dict.get("concrete_deck_vol_formula", "N.A."))
        + r" & "
        + str(input_dict.get("concrete_deck_qty", "N.A."))
        + r" & "
        + str(input_dict.get("concrete_deck_vol_total", "N.A."))
        + r" & "
        + str(input_dict.get("concrete_deck_wt_single", "N.A."))
        + r" & "
        + str(input_dict.get("concrete_deck_wt_total", "N.A."))
        + r" \\[6pt] \hline",
        r"4 & Reinforcement Steel (Fe 500) & "
        + str(input_dict.get("rebar_deck_vol_formula", "N.A."))
        + r" & "
        + str(input_dict.get("rebar_deck_qty", "N.A."))
        + r" & "
        + str(input_dict.get("rebar_deck_vol_total", "N.A."))
        + r" & "
        + str(input_dict.get("rebar_deck_wt_single", "N.A."))
        + r" & "
        + str(input_dict.get("rebar_deck_wt_total", "N.A."))
        + r" \\[6pt] \hline",
        r"5 & Shear Stud Connectors & "
        + str(input_dict.get("shear_studs_vol_formula", "N.A."))
        + r" & "
        + str(input_dict.get("shear_studs_qty", "N.A."))
        + r" & "
        + str(input_dict.get("shear_studs_vol_total", "N.A."))
        + r" & "
        + str(input_dict.get("shear_studs_wt_single", "N.A."))
        + r" & "
        + str(input_dict.get("shear_studs_wt_total", "N.A."))
        + r" \\[6pt] \hline",
        r"6 & Crash Barrier & "
        + str(input_dict.get("crash_barrier_vol_formula", "N.A."))
        + r" & "
        + str(input_dict.get("crash_barrier_qty", "N.A."))
        + r" & "
        + str(input_dict.get("crash_barrier_vol_total", "N.A."))
        + r" & "
        + str(input_dict.get("crash_barrier_wt_single", "N.A."))
        + r" & "
        + str(input_dict.get("crash_barrier_wt_total", "N.A."))
        + r" \\[6pt] \hline",
    ]

    t71_tbl = make_longtable(
        col_spec=r"|C{1.0cm}|L{4.2cm}|C{2.6cm}|C{1.6cm}|C{1.8cm}|C{1.8cm}|C{1.8cm}|",
        caption="Bill of Materials (Steel, Concrete, and Reinforcement Quantities)",
        headers=[
            "S.N.",
            "Item Description",
            "Volume Formula",
            "Quantity",
            "Total Vol (m³)",
            "Unit Wt (MT)",
            "Total Wt (MT)",
        ],
        rows=rows,
        label="tab:bom",
        note="Quantities are calculated directly from bridge geometry, member schedules, and standard material densities.",
    )

    mat_fig_tex = ""
    if fig_paths and fig_paths.get("material_takeoff_summary"):
        mat_fig_tex = (
            embed_figure(
                fig_paths.get("material_takeoff_summary"),
                "Material Quantity Distribution: Structural Steel Breakdown (MT) and Concrete Volume vs Rebar Weight",
                width=r"0.92\textwidth",
                label="fig:mat-takeoff-summary-chart",
            )
            + "\n\\vspace{1em}\n"
        )
    elif fig_paths and fig_paths.get("material_summary"):
        mat_fig_tex = (
            embed_figure(
                fig_paths.get("material_summary"),
                "Material Quantity Distribution: Structural Steel Breakdown (MT) and Concrete Volume vs Rebar Weight",
                width=r"0.92\textwidth",
                label="fig:mat-takeoff-summary-chart",
            )
            + "\n\\vspace{1em}\n"
        )

    return rf"""
\chapter{{Material Take-off \& Quantity Summary}}
\label{{ch:material-takeoff}}

This chapter summarizes the bill of materials, estimated material quantities, and component weight distributions for the structural steel plate girders, cross bracing, concrete deck slab, and shear connectors.

\vspace{{0.8em}}
{t71_tbl}

\vspace{{0.8em}}
{mat_fig_tex}
"""
