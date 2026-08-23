# =============================================================================
# Chapter 2: Input Parameters
# =============================================================================

from osdagbridge.core.reports.report_utils import (
    _render_value,
    _tex,
    get_girder_entries,
)
from osdagbridge.core.reports.styles import make_longtable
from osdagbridge.core.utils.common import (
    KEY_CARRIAGEWAY_WIDTH,
    KEY_CB_LOAD,
    KEY_CB_TYPE,
    KEY_CROSS_BRACING,
    KEY_DECK_CONCRETE_GRADE_BASIC,
    KEY_DESIGN_MODE,
    KEY_DO_GAMMA_C_BASIC,
    KEY_DO_GAMMA_FLT,
    KEY_DO_GAMMA_M0,
    KEY_DO_GAMMA_M1,
    KEY_DO_GAMMA_MF,
    KEY_DO_GAMMA_S,
    KEY_DO_GAMMA_V,
    KEY_END_DIAPHRAGM,
    KEY_FOOTPATH,
    KEY_GIRDER,
    KEY_INCLUDE_MEDIAN,
    KEY_MD_TYPE,
    KEY_MP_CB_BRACING_SECTION_DESIGNATION,
    KEY_MP_CB_MEMBER_ID,
    KEY_MP_CB_SELECT_GIRDERS,
    KEY_MP_CB_SPACING,
    KEY_MP_CB_TYPE,
    KEY_MP_ED_BRACING_SECTION_DESIGNATION,
    KEY_MP_ED_MEMBER_ID,
    KEY_MP_ED_SELECT_GIRDERS,
    KEY_MP_ED_TYPE,
    KEY_MP_GD_MEMBER_ID,
    KEY_MP_GD_SELECT_GIRDER,
    KEY_MP_GIRDER_BOTTOM_FLANGE_THICKNESS,
    KEY_MP_GIRDER_BOTTOM_FLANGE_WIDTH,
    KEY_MP_GIRDER_DEPTH,
    KEY_MP_GIRDER_SYMMETRY,
    KEY_MP_GIRDER_TOP_FLANGE_THICKNESS,
    KEY_MP_GIRDER_TOP_FLANGE_WIDTH,
    KEY_MP_GIRDER_TORSIONAL_RESTRAINT,
    KEY_MP_GIRDER_TYPE,
    KEY_MP_GIRDER_WARPING_RESTRAINT,
    KEY_MP_GIRDER_WEB_THICKNESS,
    KEY_MP_GIRDER_WEB_TYPE,
    KEY_MP_STIFFENER_BEARING_THICKNESS,
    KEY_MP_STIFFENER_INTERMEDIATE,
    KEY_MP_STIFFENER_INTERMEDIATE_SPACING,
    KEY_MP_STIFFENER_INTERMEDIATE_THICKNESS,
    KEY_MP_STIFFENER_LONGITUDINAL,
    KEY_MP_STIFFENER_NO_BEARING_STIFFENERS,
    KEY_MP_STIFFENER_SPACING,
    KEY_RL_LOAD_VALUE,
    KEY_RL_TYPE,
    KEY_SD_SHEAR_DIAMETER,
    KEY_SD_SHEAR_HEIGHT,
    KEY_SD_SHEAR_STUDS_PER_SECTION,
    KEY_SD_SHEAR_ULTIMATE_STRENGTH,
    KEY_SD_SHEAR_YIELD_STRENGTH,
    KEY_SKEW_ANGLE,
    KEY_SPAN,
    KEY_STRUCTURE_TYPE,
    KEY_TS_DECK_OVERHANG,
    KEY_TS_DECK_THICKNESS,
    KEY_TS_FOOTPATH_WIDTH,
    KEY_TS_GIRDER_SPACING,
    KEY_TS_NO_OF_GIRDERS,
    KEY_TS_OVERALL_WIDTH,
    KEY_WC_LD_LANE_TABLE_COUNT,
    KEY_WC_MATERIAL,
    KEY_WC_THICKNESS,
)


def ch2_input_parameters(m, input_dict, output_dict=None):
    girder_entries = get_girder_entries(input_dict)
    n_girders = len(girder_entries)

    # ── Table 2.1: Project Location ──
    t21_rows = [
        r"Project Location & " + _tex(m.project_location) + r" \\[6pt] \hline",
        r"Latitude / Longitude & "
        + _render_value(input_dict, "latitude")
        + ", "
        + _render_value(input_dict, "longitude")
        + r" \\[6pt] \hline",
        r"Seismic Zone (IRC 6) & "
        + _render_value(input_dict, "seismic_zone")
        + r" \\[6pt] \hline",
        r"Basic Wind Speed, $V_b$ & "
        + _render_value(input_dict, "wind_speed", " m/s")
        + r" \\[6pt] \hline",
        r"Shade Temperature (Max / Min) & "
        + _render_value(input_dict, "shade_temp_max", "")
        + r" $^\circ$C / "
        + _render_value(input_dict, "shade_temp_min", "")
        + r" $^\circ$C \\[6pt] \hline",
    ]
    t21 = make_longtable(
        col_spec=r"|L{5.5cm}|L{9.5cm}|",
        caption="Project Location and Environmental Parameters",
        headers=["Parameter", "Design Input Value"],
        rows=t21_rows,
        label="tab:project-location",
    )

    # ── Table 2.2: Bridge Geometry ──
    t22_rows = [
        r"Type of Structure & "
        + _render_value(input_dict, KEY_STRUCTURE_TYPE)
        + r" \\[6pt] \hline",
        r"Effective Span & "
        + _render_value(input_dict, KEY_SPAN, " m")
        + r" \\[6pt] \hline",
        r"Carriageway Width & "
        + _render_value(input_dict, KEY_CARRIAGEWAY_WIDTH, " m")
        + r" \\[6pt] \hline",
        r"Include Median & "
        + _render_value(input_dict, KEY_INCLUDE_MEDIAN)
        + r" \\[6pt] \hline",
        r"Footpath Provision & "
        + _render_value(input_dict, KEY_FOOTPATH)
        + r" \\[6pt] \hline",
        r"Skew Angle & "
        + _render_value(input_dict, KEY_SKEW_ANGLE, "°")
        + r" (IRC 24 limit: $\pm 15^\circ$) \\[6pt] \hline",
    ]
    t22 = make_longtable(
        col_spec=r"|L{5.5cm}|L{9.5cm}|",
        caption="Basic Bridge Geometry (User Defined)",
        headers=["Parameter", "Design Input Value"],
        rows=t22_rows,
        label="tab:bridge-geometry",
    )

    # ── Table 2.3: Material Selection ──
    t23_rows = [
        r"Plate Girder Steel Grade (IS 2062) & "
        + _render_value(input_dict, KEY_GIRDER)
        + r" \\[6pt] \hline",
        r"Cross Bracing Steel Grade & "
        + _render_value(input_dict, KEY_CROSS_BRACING)
        + r" \\[6pt] \hline",
        r"End Diaphragm Steel Grade & "
        + _render_value(input_dict, KEY_END_DIAPHRAGM)
        + r" \\[6pt] \hline",
        r"Concrete Deck Grade (IRC 112) & "
        + _render_value(input_dict, KEY_DECK_CONCRETE_GRADE_BASIC)
        + r" \\[6pt] \hline",
    ]
    t23 = make_longtable(
        col_spec=r"|L{5.5cm}|L{9.5cm}|",
        caption="Material Selection",
        headers=["Parameter", "Design Input Value"],
        rows=t23_rows,
        label="tab:material-selection",
    )

    # ── Table 2.4: Typical Section Details ──
    t24_rows = [
        r"Overall Bridge Width & "
        + _render_value(input_dict, KEY_TS_OVERALL_WIDTH, " m")
        + r" \\[6pt] \hline",
        r"Number of Girders & "
        + _render_value(input_dict, KEY_TS_NO_OF_GIRDERS)
        + r" \\[6pt] \hline",
        r"Girder Spacing (c/c) & "
        + _render_value(input_dict, KEY_TS_GIRDER_SPACING, " m")
        + r" \\[6pt] \hline",
        r"Deck Overhang Width & "
        + _render_value(input_dict, KEY_TS_DECK_OVERHANG, " m")
        + r" \\[6pt] \hline",
        r"Deck Slab Thickness & "
        + _render_value(input_dict, KEY_TS_DECK_THICKNESS, " mm")
        + r" \\[6pt] \hline",
        r"Footpath Width & "
        + _render_value(input_dict, KEY_TS_FOOTPATH_WIDTH, " m")
        + r" (IRC 5 min: 1.5 m) \\[6pt] \hline",
        r"Number of Traffic Lanes & "
        + _render_value(input_dict, KEY_WC_LD_LANE_TABLE_COUNT)
        + r" (per IRC 5 Cl. 104.3.1) \\[6pt] \hline",
    ]
    t24 = make_longtable(
        col_spec=r"|L{5.5cm}|L{9.5cm}|",
        caption="Typical Section Geometry Details",
        headers=["Parameter", "Design Input Value"],
        rows=t24_rows,
        label="tab:typical-section",
    )

    # ── Table 2.5: Components & Appurtenances ──
    median_val = (
        _render_value(input_dict, KEY_MD_TYPE)
        if str(input_dict.get(KEY_INCLUDE_MEDIAN, "")).strip().lower()
        in ("yes", "true", "1")
        else "None"
    )
    t25_rows = [
        r"Crash Barrier Type & "
        + _render_value(input_dict, KEY_CB_TYPE)
        + r" \\[6pt] \hline",
        r"Crash Barrier Load & "
        + _render_value(input_dict, KEY_CB_LOAD, " kN/m")
        + r" \\[6pt] \hline",
        r"Median Configuration & " + median_val + r" \\[6pt] \hline",
        r"Railing Type & "
        + _render_value(input_dict, KEY_RL_TYPE)
        + r" \\[6pt] \hline",
        r"Railing Load & "
        + _render_value(input_dict, KEY_RL_LOAD_VALUE, " kN/m")
        + r"\sdstar{} \\[6pt] \hline",
        r"Wearing Course Material & "
        + _render_value(input_dict, KEY_WC_MATERIAL)
        + r" \\[6pt] \hline",
        r"Wearing Course Thickness & "
        + _render_value(input_dict, KEY_WC_THICKNESS, " mm")
        + r" \\[6pt] \hline",
    ]
    t25 = make_longtable(
        col_spec=r"|L{5.5cm}|L{9.5cm}|",
        caption="Bridge Superstructure Component Details",
        headers=["Parameter", "Design Input Value"],
        rows=t25_rows,
        label="tab:component-details",
    )

    return rf"""
\chapter{{Input Parameters}}

This section documents all structural and geometric inputs provided to OsdagBridge. User-provided inputs are clearly distinguished from software-assumed defaults. Where the user did not supply a value, the software has applied the IRC/IS code default or an empirical guideline; these are annotated with an asterisk (\sdstar{{}}).

\section{{Basic Inputs (User-Defined)}}
\label{{sec:basic-inputs}}

\vspace{{0.4em}}
{t21}

\vspace{{0.4em}}
{t22}

\vspace{{0.4em}}
{t23}

\section{{Additional Inputs}}
\label{{sec:additional-inputs}}

\vspace{{0.4em}}
{t24}

\vspace{{0.4em}}
{t25}

{_girder_tables(input_dict, n_girders)}

{_bracing_tables(input_dict, n_girders)}

{_shear_connector_table(input_dict, output_dict)}

{_safety_factors_table(input_dict)}
"""


def _girder_tables(input_dict, n_girders):
    n = n_girders if n_girders >= 1 else 1
    girder_entries = get_girder_entries(input_dict)
    if not girder_entries:
        girder_entries = [(f"Girder {i}", f"M1") for i in range(1, n + 1)]

    entries_for_table = [
        (lbl, mid, i)
        for i, (lbl, mid) in enumerate(girder_entries, start=1)
    ]

    def _gen_row(g_lbl, m_id, i):
        return (
            g_lbl
            + r" & "
            + m_id
            + r" & "
            + (_render_value(input_dict, KEY_DESIGN_MODE))
            + r" & "
            + (_render_value(input_dict, f"{KEY_MP_GIRDER_TYPE}.G{i}.M1"))
            + r" & "
            + (_render_value(input_dict, f"{KEY_MP_GIRDER_SYMMETRY}.G{i}.M1"))
            + r" \\[6pt] \hline"
        )

    def _dim_row(g_lbl, i):
        return (
            g_lbl
            + r" & "
            + (_render_value(input_dict, f"{KEY_MP_GIRDER_DEPTH}.G{i}.M1", " mm"))
            + r" & "
            + (_render_value(input_dict, f"{KEY_MP_GIRDER_WEB_THICKNESS}.G{i}.M1", " mm"))
            + r" & "
            + (_render_value(input_dict, f"{KEY_MP_GIRDER_TOP_FLANGE_WIDTH}.G{i}.M1", " mm"))
            + ", "
            + (_render_value(input_dict, f"{KEY_MP_GIRDER_TOP_FLANGE_THICKNESS}.G{i}.M1", " mm"))
            + r" & "
            + (_render_value(input_dict, f"{KEY_MP_GIRDER_BOTTOM_FLANGE_WIDTH}.G{i}.M1", " mm"))
            + ", "
            + (_render_value(input_dict, f"{KEY_MP_GIRDER_BOTTOM_FLANGE_THICKNESS}.G{i}.M1", " mm"))
            + r" \\[6pt] \hline"
        )

    def _rst_row(g_lbl, i):
        return (
            g_lbl
            + r" & "
            + (_render_value(input_dict, f"{KEY_MP_GIRDER_TORSIONAL_RESTRAINT}.G{i}.M1"))
            + ", "
            + (_render_value(input_dict, f"{KEY_MP_GIRDER_WARPING_RESTRAINT}.G{i}.M1"))
            + r" & "
            + (_render_value(input_dict, f"{KEY_MP_GIRDER_WEB_TYPE}.G{i}.M1"))
            + r" & "
            + (_render_value(input_dict, f"{KEY_MP_STIFFENER_INTERMEDIATE}.G{i}.M1"))
            + "; Spacing: "
            + (_render_value(input_dict, f"{KEY_MP_STIFFENER_INTERMEDIATE_SPACING}.G{i}.M1", " mm"))
            + "; $t_s$: "
            + (_render_value(input_dict, f"{KEY_MP_STIFFENER_INTERMEDIATE_THICKNESS}.G{i}.M1", " mm"))
            + r" & "
            + (_render_value(input_dict, f"{KEY_MP_STIFFENER_LONGITUDINAL}.G{i}.M1"))
            + r" & No: "
            + (_render_value(input_dict, f"{KEY_MP_STIFFENER_NO_BEARING_STIFFENERS}.G{i}.M1"))
            + "; Spacing: "
            + (_render_value(input_dict, f"{KEY_MP_STIFFENER_SPACING}.G{i}.M1", " mm"))
            + "; $t_b$: "
            + (_render_value(input_dict, f"{KEY_MP_STIFFENER_BEARING_THICKNESS}.G{i}.M1", " mm"))
            + r" \\[6pt] \hline"
        )

    gen_rows = [_gen_row(g_lbl, m_id, i) for g_lbl, m_id, i in entries_for_table]
    dim_rows = [_dim_row(g_lbl, i) for g_lbl, _, i in entries_for_table]
    rst_rows = [_rst_row(g_lbl, i) for g_lbl, _, i in entries_for_table]

    t_gen = make_longtable(
        col_spec=r"|L{2.2cm}|L{2.0cm}|C{2.8cm}|C{3.8cm}|C{3.8cm}|",
        caption="Girder General Information",
        headers=["Girder", "Member ID", "Design Mode", "Girder Type", "Girder Symmetry"],
        rows=gen_rows,
        label="tab:girder-gen-info",
    )

    t_dim = make_longtable(
        col_spec=r"|L{2.0cm}|C{2.6cm}|C{2.2cm}|C{3.8cm}|C{3.8cm}|",
        caption="Girder Section Dimensions",
        headers=["Girder", "Total Depth $D$ (mm)", "Web $t_w$ (mm)", "Top Flange ($b_{tf}, t_{tf}$)", "Bottom Flange ($b_{bf}, t_{bf}$)"],
        rows=dim_rows,
        label="tab:girder-dim-info",
    )

    t_rst = make_longtable(
        col_spec=r"|L{1.8cm}|p{2.6cm}|p{2.2cm}|p{3.2cm}|p{2.2cm}|p{2.6cm}|",
        caption="Girder Restraint and Stiffener Details",
        headers=["Girder", "Torsional/Warping Restraint", "Web Philosophy", "Intermediate Stiffeners", "Longitudinal Stiffeners", "Bearing Stiffener"],
        rows=rst_rows,
        label="tab:girder-stiffener-details",
    )

    return f"{t_gen}\n\\vspace{{0.6em}}\n{t_dim}\n\\vspace{{0.6em}}\n{t_rst}"


def _bracing_tables(input_dict, n_girders):
    n = n_girders if n_girders >= 2 else 2
    panels = [
        (
            _render_value(input_dict, f"{KEY_MP_CB_SELECT_GIRDERS}.G{i}G{i+1}.B{i}M1"),
            _render_value(input_dict, f"{KEY_MP_CB_MEMBER_ID}.G{i}G{i+1}.B{i}M1"),
            _render_value(input_dict, f"{KEY_MP_ED_SELECT_GIRDERS}.G{i}G{i+1}.E{i}M1"),
            _render_value(input_dict, f"{KEY_MP_ED_MEMBER_ID}.G{i}G{i+1}.E{i}M1"),
            i,
        )
        for i in range(1, n)
    ]

    def _cb_row(location, member_ids, i):
        return (
            location
            + r" & "
            + member_ids
            + r" & "
            + (_render_value(input_dict, f"{KEY_MP_CB_TYPE}.G{i}G{i+1}.B{i}M1"))
            + r" & "
            + (_render_value(input_dict, f"{KEY_MP_CB_BRACING_SECTION_DESIGNATION}.G{i}G{i+1}.B{i}M1"))
            + r" & "
            + (_render_value(input_dict, f"{KEY_MP_CB_SPACING}.G{i}G{i+1}.B{i}M1", " m"))
            + r" \\[6pt] \hline"
        )

    def _ed_row(location, member_ids, i):
        return (
            location
            + r" & "
            + member_ids
            + r" & "
            + (_render_value(input_dict, f"{KEY_MP_ED_TYPE}.G{i}G{i+1}.E{i}M1"))
            + r" & "
            + (_render_value(input_dict, f"{KEY_MP_ED_BRACING_SECTION_DESIGNATION}.G{i}G{i+1}.E{i}M1"))
            + r" \\[6pt] \hline"
        )

    cb_rows = [_cb_row(cb_loc, cb_ids, i) for cb_loc, cb_ids, _, _, i in panels]
    ed_rows = [_ed_row(ed_loc, ed_ids, i) for _, _, ed_loc, ed_ids, i in panels]

    t_cb = make_longtable(
        col_spec=r"|L{2.2cm}|L{2.2cm}|L{3.5cm}|L{4.2cm}|C{2.5cm}|",
        caption="Member Properties: Cross Bracing Details",
        headers=["Location", "Member IDs", "Type of Bracing", "Bracing Section", "Spacing (m)"],
        rows=cb_rows,
        label="tab:cb-details",
    )

    t_ed = make_longtable(
        col_spec=r"|L{2.2cm}|L{2.2cm}|L{4.5cm}|L{5.5cm}|",
        caption="Member Properties: End Diaphragm Details",
        headers=["Location", "Member IDs", "Type of Diaphragm", "Diaphragm Section"],
        rows=ed_rows,
        label="tab:ed-details",
    )

    return f"{t_cb}\n\\vspace{{0.6em}}\n{t_ed}"


def _shear_connector_table(input_dict, output_dict=None):
    od = output_dict or {}
    rows = [
        r"Stud Diameter & " + (_render_value(od, KEY_SD_SHEAR_DIAMETER, " mm")) + r" \\[6pt] \hline",
        r"Stud Height & " + (_render_value(od, KEY_SD_SHEAR_HEIGHT, " mm")) + r" \\[6pt] \hline",
        r"Stud Yield Strength, $f_y$ & " + (_render_value(od, KEY_SD_SHEAR_YIELD_STRENGTH, " MPa")) + r" \\[6pt] \hline",
        r"Stud Ultimate Tensile Strength, $f_u$ & " + (_render_value(od, KEY_SD_SHEAR_ULTIMATE_STRENGTH, " MPa")) + r" \\[6pt] \hline",
        r"Number of Studs per Section & " + (_render_value(od, KEY_SD_SHEAR_STUDS_PER_SECTION)) + r" \\[6pt] \hline",
    ]
    return make_longtable(
        col_spec=r"|L{5.5cm}|L{9.5cm}|",
        caption="Shear Connector Specification Details",
        headers=["Parameter", "Design Specification Value"],
        rows=rows,
        label="tab:shear-connector-details",
    )


def _safety_factors_table(input_dict):
    rows = [
        r"$\gamma_{M0}$ (Yielding / Buckling Resistance) & " + (_render_value(input_dict, KEY_DO_GAMMA_M0)) + r" \\[6pt] \hline",
        r"$\gamma_{M1}$ (Ultimate Tensile Resistance) & " + (_render_value(input_dict, KEY_DO_GAMMA_M1)) + r" \\[6pt] \hline",
        r"$\gamma_C$ (Concrete in Compression, Basic) & " + (_render_value(input_dict, KEY_DO_GAMMA_C_BASIC)) + r" \\[6pt] \hline",
        r"$\gamma_s$ (Reinforcement Steel) & " + (_render_value(input_dict, KEY_DO_GAMMA_S)) + r" \\[6pt] \hline",
        r"$\gamma_v$ (Shear Stud Connectors) & " + (_render_value(input_dict, KEY_DO_GAMMA_V)) + r" \\[6pt] \hline",
        r"$\gamma_{Fft}$ (Fatigue Load Factor) & " + (_render_value(input_dict, KEY_DO_GAMMA_FLT)) + r" \\[6pt] \hline",
        r"$\gamma_{Mft}$ (Fatigue Material Strength Factor) & " + (_render_value(input_dict, KEY_DO_GAMMA_MF)) + r" \\[6pt] \hline",
    ]
    return make_longtable(
        col_spec=r"|L{5.5cm}|L{9.5cm}|",
        caption="Partial Safety Factors for Materials and Loads (IS 800 / IRC 22)",
        headers=["Safety Factor", "Design Multiplier Value"],
        rows=rows,
        label="tab:partial-safety-factors",
        note="All partial safety factors conform to IRC 22:2015 Table 1 and IS 800:2007 Table 5.",
    )
