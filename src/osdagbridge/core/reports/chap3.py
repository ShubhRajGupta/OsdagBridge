# =============================================================================
# Chapter 3: Loads and Load Combinations
# =============================================================================

from osdagbridge.core.utils.common import (
    KEY_CB_LOAD,
    KEY_FOOTPATH,
    KEY_LL_CUSTOM_VEHICLES,
    KEY_LL_FOOTPATH_PRESSURE_MODE,
    KEY_LL_FOOTPATH_PRESSURE_VALUE,
    KEY_LL_IRC_70R_BOGIE,
    KEY_LL_IRC_70R_TRACKED,
    KEY_LL_IRC_70R_WHEELED,
    KEY_LL_IRC_AA_TRACKED,
    KEY_LL_IRC_AA_WHEELED,
    KEY_LL_IRC_CLASS_A,
    KEY_LL_IRC_CLASS_FATIGUE,
    KEY_LL_IRC_CLASS_SV,
    KEY_MATERIAL_DECK_DENSITY,
    KEY_MATERIAL_GIRDER_DENSITY,
    KEY_PL_SELF_WEIGHT_FACTOR,
    KEY_RL_LOAD_VALUE,
    KEY_SL_DAMPING,
    KEY_SL_DEAD_LOAD_MODE,
    KEY_SL_DEAD_LOAD_VALUE,
    KEY_SL_HORIZONTAL_COEFF,
    KEY_SL_IMPORTANCE_FACTOR,
    KEY_SL_LIVE_LOAD_MODE,
    KEY_SL_LIVE_LOAD_VALUE,
    KEY_SL_SEISMIC_ZONE,
    KEY_SL_SOIL_TYPE,
    KEY_SL_SPECTRAL_COEFF,
    KEY_SL_TIME_PERIOD,
    KEY_SL_VERTICAL_COEFF,
    KEY_SL_ZONE_FACTOR,
    KEY_SPAN,
    KEY_TL_BRIDGE_TEMP_MAX,
    KEY_TL_BRIDGE_TEMP_MIN,
    KEY_TL_HIGHEST_MAX_TEMP,
    KEY_TL_LOWEST_MIN_TEMP,
    KEY_TL_TEMP_FALL,
    KEY_TL_TEMP_RISE,
    KEY_WC_LD_LANE_TABLE_COUNT,
    KEY_WC_MATERIAL,
    KEY_WC_THICKNESS,
    KEY_WL_AVG_EXPOSED_HEIGHT,
    KEY_WL_BASIC_WIND_SPEED,
    KEY_WL_HOURLY_MEAN_WIND,
    KEY_WL_HOURLY_WIND_PRESSURE,
    KEY_WL_LONGITUDINAL_WIND_FORCE,
    KEY_WL_TERRAIN_TYPE,
    KEY_WL_TRANSVERSE_WIND_FORCE,
    KEY_WL_VERTICAL_WIND_FORCE,
)

from osdagbridge.core.reports.report_utils import _tex, _render_value
from osdagbridge.core.reports.styles import make_longtable


def ch3_loads(input_dict):
    # ── Live load vehicle mapping ──
    vehicles = []
    if input_dict.get(KEY_LL_IRC_CLASS_A):
        vehicles.append("Class A")
    if input_dict.get(KEY_LL_IRC_70R_WHEELED):
        vehicles.append("Class 70R (Wheeled)")
    if input_dict.get(KEY_LL_IRC_70R_TRACKED):
        vehicles.append("Class 70R (Tracked)")
    if input_dict.get(KEY_LL_IRC_AA_WHEELED):
        vehicles.append("Class AA (Wheeled)")
    if input_dict.get(KEY_LL_IRC_AA_TRACKED):
        vehicles.append("Class AA (Tracked)")
    if input_dict.get(KEY_LL_IRC_CLASS_SV):
        vehicles.append("Class SV")
    if input_dict.get(KEY_LL_IRC_70R_BOGIE):
        vehicles.append("Class 70R (Bogie)")
    if input_dict.get(KEY_LL_IRC_CLASS_FATIGUE):
        vehicles.append("Class Fatigue")

    custom = input_dict.get(KEY_LL_CUSTOM_VEHICLES)
    if custom and isinstance(custom, list):
        for c in custom:
            if isinstance(c, dict) and c.get("name"):
                vehicles.append(c["name"])
            elif isinstance(c, str):
                vehicles.append(c)

    vehicles_str = ", ".join(vehicles) if vehicles else "IRC Class A"

    from osdagbridge.core.utils.codes.irc6_2017 import IRC6_2017
    span = input_dict.get(KEY_SPAN)
    impact_factor_str = ""
    if span not in (None, ""):
        try:
            span_m = float(span)
            factors = []
            if input_dict.get(KEY_LL_IRC_CLASS_A, True):
                im_a = IRC6_2017.cl_208_2_impact_factor(span_m)
                factors.append(f"Class A: {1.0 + im_a:.3f}")
            is_wheeled_heavy = (
                input_dict.get(KEY_LL_IRC_70R_WHEELED)
                or input_dict.get(KEY_LL_IRC_AA_WHEELED)
                or input_dict.get(KEY_LL_IRC_70R_BOGIE)
            )
            is_tracked_heavy = (
                input_dict.get(KEY_LL_IRC_70R_TRACKED)
                or input_dict.get(KEY_LL_IRC_AA_TRACKED)
            )
            if is_wheeled_heavy or is_tracked_heavy:
                im_aa = IRC6_2017.cl_208_3_impact_factor(span_m)
                factors.append(f"Class AA/70R: {1.0 + im_aa:.3f}")

            impact_factor_str = ", ".join(factors) if factors else f"Class A: {1.0 + IRC6_2017.cl_208_2_impact_factor(span_m):.3f}"
        except Exception:
            impact_factor_str = "1.188 (Class A)"
    else:
        impact_factor_str = "1.188 (Class A)"

    lanes = input_dict.get(KEY_WC_LD_LANE_TABLE_COUNT)
    braking_force_str = ""
    if lanes not in (None, ""):
        try:
            lanes_int = int(lanes)
            braking_force_t = IRC6_2017.cl_211_2_braking_force(lanes_int)
            braking_force_kN = braking_force_t * 9.81
            braking_force_str = f"{braking_force_kN:.2f} kN ({braking_force_t:.2f} tonnes)"
        except Exception:
            braking_force_str = "200.00 kN (20.39 tonnes)"
    else:
        braking_force_str = "200.00 kN (20.39 tonnes)"

    # Footpath live loads
    fp_mode = input_dict.get(KEY_LL_FOOTPATH_PRESSURE_MODE, "")
    fp_value = input_dict.get(KEY_LL_FOOTPATH_PRESSURE_VALUE, "")
    fp_config = input_dict.get(KEY_FOOTPATH, "None")
    if str(fp_mode).strip().lower() in ("as per irc 6", "as per irc6", "automatic"):
        try:
            fp_intensity = f"{IRC6_2017.cl_206_1_footway_load():.3f}"
        except Exception:
            fp_intensity = "5.000"
    elif fp_value not in (None, ""):
        fp_intensity = f"{float(fp_value):.3f}"
    else:
        fp_intensity = "5.000" if str(fp_config).strip().lower() not in ("none", "") else "N/A"

    # Wind Loads (WL)
    vz_val = input_dict.get(KEY_WL_HOURLY_MEAN_WIND)
    pz_val = input_dict.get(KEY_WL_HOURLY_WIND_PRESSURE)
    if not vz_val or not pz_val:
        try:
            _vb = input_dict.get(KEY_WL_BASIC_WIND_SPEED) or input_dict.get("wind_speed", 39.0)
            _h = input_dict.get(KEY_WL_AVG_EXPOSED_HEIGHT, 10.0)
            _ter = {
                "Plain Terrain": "plain",
                "Terrain with Obstructions": "obstructed",
            }.get(str(input_dict.get(KEY_WL_TERRAIN_TYPE, "")).strip(), "plain")
            _res = IRC6_2017.table_12(float(_h), _ter, float(_vb))
            if not vz_val:
                vz_val = _res.get("Vz")
            if not pz_val:
                pz_val = _res.get("Pz")
        except Exception:
            pass
    vz_str = f"{float(vz_val):.2f}" if vz_val not in (None, "") else "29.80"
    pz_str = f"{float(pz_val):.2f}" if pz_val not in (None, "") else "532.82"

    # Seismic Loads (EL)
    sl_zone_factor = input_dict.get(KEY_SL_ZONE_FACTOR)
    sl_spectral = input_dict.get(KEY_SL_SPECTRAL_COEFF)
    sl_ah = input_dict.get(KEY_SL_HORIZONTAL_COEFF)
    sl_av = input_dict.get(KEY_SL_VERTICAL_COEFF)
    if not sl_ah or not sl_zone_factor:
        try:
            _zone = input_dict.get(KEY_SL_SEISMIC_ZONE) or input_dict.get("seismic_zone", "III")
            _zmap = {"1": "I", "2": "II", "3": "III", "4": "IV", "5": "V"}
            _z = str(_zone).strip().upper()
            if _z.isdigit():
                _z = _zmap.get(_z, "III")
            _smap = {"Type I – Rocky or Hard": 1, "Type II – Medium Soil": 2, "Type III – Soft Soil": 3}
            _st = _smap.get(str(input_dict.get(KEY_SL_SOIL_TYPE, "")), 2)
            _tp = input_dict.get(KEY_SL_TIME_PERIOD)
            _damp = input_dict.get(KEY_SL_DAMPING) or "5"
            _dl_v = input_dict.get(KEY_SL_DEAD_LOAD_VALUE)
            _ll_v = input_dict.get(KEY_SL_LIVE_LOAD_VALUE)
            _dead = float(_dl_v) if str(input_dict.get(KEY_SL_DEAD_LOAD_MODE, "")) == "Custom" and _dl_v else 0.0
            _live = float(_ll_v) if str(input_dict.get(KEY_SL_LIVE_LOAD_MODE, "")) == "Custom" and _ll_v else 0.0
            _res = IRC6_2017.cl_218_5_1(
                zone=f"Zone {_z}",
                soil_type=_st,
                dead_load_kN=_dead,
                live_load_kN=_live,
                period_T=float(_tp) if _tp else None,
                damping_percent=float(_damp),
            )
            if not sl_zone_factor:
                sl_zone_factor = _res.get("Z", 0.16)
            if not sl_spectral:
                sl_spectral = _res.get("Sa_g_adjusted", 2.50)
            if not sl_ah:
                sl_ah = _res.get("Ah", 0.067)
            if not sl_av:
                sl_av = round(float(sl_ah or 0.067) * 2 / 3, 4)
        except Exception:
            sl_zone_factor = sl_zone_factor or "0.16"
            sl_spectral = sl_spectral or "2.50"
            sl_ah = sl_ah or "0.067"
            sl_av = sl_av or "0.045"

    def _sl(v, unit=""):
        return f"{float(v):.4f}{unit}" if v not in (None, "") else "N/A"

    # Temperature Loads (TL)
    tl_temp_min = tl_temp_max = tl_rise = tl_fall = "N/A"
    try:
        _tmax = input_dict.get(KEY_TL_HIGHEST_MAX_TEMP) or input_dict.get("shade_temp_max", 42.0)
        _tmin = input_dict.get(KEY_TL_LOWEST_MIN_TEMP) or input_dict.get("shade_temp_min", 4.0)
        if _tmax and _tmin:
            _res = IRC6_2017.cl_215_2_effective_bridge_temperature(
                float(_tmax), float(_tmin), "metallic", False
            )
            _bt_min = _res.get("T_min", 0)
            _bt_max = _res.get("T_max", 0)
            _mean = (_bt_max + _bt_min) / 2.0
            tl_temp_min = f"{_bt_min:.2f}"
            tl_temp_max = f"{_bt_max:.2f}"
            tl_rise = f"{_bt_max - _mean:.2f}"
            tl_fall = f"{_mean - _bt_min:.2f}"
    except Exception:
        tl_temp_min = "-2.00"
        tl_temp_max = "48.00"
        tl_rise = "25.00"
        tl_fall = "25.00"

    # ── Table 3.1: Dead Load -- Self Weight ──
    t31_rows = [
        r"Steel Superstructure Density & IS 800:2007 Cl. 3.2.1 & " + (_render_value(input_dict, KEY_MATERIAL_GIRDER_DENSITY, '')) + r" & kN/m\textsuperscript{3} \\[6pt] \hline",
        r"Concrete Deck Slab Density & IRC 112:2020 Cl. 3.2 & " + (_render_value(input_dict, KEY_MATERIAL_DECK_DENSITY, '')) + r" & kN/m\textsuperscript{3} \\[6pt] \hline",
        r"Self-Weight Factor Multiplier & Analysis Input & " + (_render_value(input_dict, KEY_PL_SELF_WEIGHT_FACTOR, '')) + r" & --- \\[6pt] \hline",
    ]
    t31_table = make_longtable(
        col_spec=r"|L{6.0cm}|C{3.8cm}|C{3.0cm}|C{2.5cm}|",
        caption="Dead Load --- Self Weight (DL)",
        headers=["Parameter", "Standard Reference", "Design Value", "Unit"],
        rows=t31_rows,
        label="tab:dead-loads",
    )

    # ── Table 3.2: Dead Load for Surfacing (DW) ──
    t32_rows = [
        r"Wearing Course Material & IRC 6:2017 Cl. 202.2 & " + (_render_value(input_dict, KEY_WC_MATERIAL)) + r" & --- \\[6pt] \hline",
        r"Wearing Course Thickness & Cross Section & " + (_render_value(input_dict, KEY_WC_THICKNESS)) + r" & mm \\[6pt] \hline",
        r"Crash Barrier SIDL & IRC 5:2015 & " + (_render_value(input_dict, KEY_CB_LOAD)) + r" & kN/m per barrier \\[6pt] \hline",
        r"Railing Load & IRC 5:2015 & " + (_render_value(input_dict, KEY_RL_LOAD_VALUE)) + r"\sdstar{} & kN/m \\[6pt] \hline",
    ]
    t32_table = make_longtable(
        col_spec=r"|L{6.0cm}|C{3.8cm}|C{3.0cm}|C{2.5cm}|",
        caption="Dead Load for Surfacing and Superimposed Dead Load (DW / SIDL)",
        headers=["Parameter", "Standard Reference", "Design Value", "Unit"],
        rows=t32_rows,
        label="tab:sidl-loads",
    )

    # ── Table 3.3: Vehicle Live Loads (LL) ──
    t33_rows = [
        r"Vehicle Classes Considered & IRC 6:2017 Cl. 204 & " + _tex(vehicles_str) + r" & --- \\[6pt] \hline",
        r"Impact Factor (Dynamic Amplification) & IRC 6:2017 Cl. 208 & " + _tex(impact_factor_str) + r" & --- \\[6pt] \hline",
        r"Longitudinal Braking Force & IRC 6:2017 Cl. 211 & " + _tex(braking_force_str) + r" & kN \\[6pt] \hline",
        r"Centrifugal Force & IRC 6:2017 Cl. 212 & 0.00 (Straight Span) & kN \\[6pt] \hline",
    ]
    t33_table = make_longtable(
        col_spec=r"|L{6.0cm}|C{3.8cm}|C{3.0cm}|C{2.5cm}|",
        caption="Vehicle Live Loads (LL) per IRC 6:2017",
        headers=["Parameter", "Standard Reference", "Design Value", "Unit"],
        rows=t33_rows,
        label="tab:vehicle-live-loads",
        note="Impact factors and braking forces are computed automatically in accordance with IRC 6:2017 based on span and lane count.",
    )

    # ── Table 3.4: Pedestrian & Footpath Live Loads ──
    t34_rows = [
        r"Footpath Provision & General Arrangement & " + _tex(str(fp_config)) + r" & --- \\[6pt] \hline",
        r"Footway Live Load Intensity & IRC 6:2017 Cl. 206.1 & " + _tex(fp_intensity) + r" & kN/m\textsuperscript{2} \\[6pt] \hline",
        r"Footway Live Load Reduction & IRC 6:2017 Cl. 206.1.1 & Function of Span ($L \geq 7.5\text{ m}$) & --- \\[6pt] \hline",
        r"Pedestrian Railing Transverse Load & IRC 6:2017 Cl. 209.7 & 1.50 & kN/m \\[6pt] \hline",
    ]
    t34_table = make_longtable(
        col_spec=r"|L{6.0cm}|C{3.8cm}|C{3.0cm}|C{2.5cm}|",
        caption="Pedestrian and Footpath Live Loads per IRC 6:2017 Cl. 206",
        headers=["Parameter", "Standard Reference", "Design Value", "Unit"],
        rows=t34_rows,
        label="tab:footpath-live-loads",
        note="Footway live load intensity is reduced for longer spans according to IRC 6:2017 Clause 206.1.1.",
    )

    # ── Table 3.5: Wind Load (WL) ──
    t35_rows = [
        r"Basic Wind Speed, $V_b$ & IRC 6:2017 Table 11 & " + (_render_value(input_dict, 'wind_speed', '')) + r" & m/s \\[6pt] \hline",
        r"Terrain Type & IRC 6:2017 Table 12 & " + (_render_value(input_dict, KEY_WL_TERRAIN_TYPE)) + r" & --- \\[6pt] \hline",
        r"Average Exposed Bridge Height, $H$ & Bridge Geometry & " + (_render_value(input_dict, KEY_WL_AVG_EXPOSED_HEIGHT, '')) + r" & m \\[6pt] \hline",
        r"Hourly Mean Wind Speed, $V_z$ & IRC 6:2017 Table 12 & " + _tex(vz_str) + r" & m/s \\[6pt] \hline",
        r"Hourly Wind Pressure, $P_z$ & IRC 6:2017 Cl. 209.3 & " + _tex(pz_str) + r" & N/m\textsuperscript{2} \\[6pt] \hline",
        r"Transverse Wind Force on Superstructure & IRC 6:2017 Cl. 209.4 & " + (_render_value(input_dict, KEY_WL_TRANSVERSE_WIND_FORCE, '')) + r" & kN \\[6pt] \hline",
        r"Longitudinal Wind Force on Superstructure & IRC 6:2017 Cl. 209.4 & " + (_render_value(input_dict, KEY_WL_LONGITUDINAL_WIND_FORCE, '')) + r" & kN \\[6pt] \hline",
        r"Vertical Wind Force (Aerodynamic Lift) & IRC 6:2017 Cl. 209.5 & " + (_render_value(input_dict, KEY_WL_VERTICAL_WIND_FORCE, '')) + r" & kN \\[6pt] \hline",
    ]
    t35_table = make_longtable(
        col_spec=r"|L{6.0cm}|C{3.8cm}|C{3.0cm}|C{2.5cm}|",
        caption="Wind Load (WL) Parameters per IRC 6:2017 Table 12",
        headers=["Parameter", "Standard Reference", "Design Value", "Unit"],
        rows=t35_rows,
        label="tab:wind-loads",
    )

    # ── Table 3.6: Earthquake Load (EL) ──
    t36_rows = [
        r"Seismic Zone & IRC 6:2017 Fig. 15 & " + (_render_value(input_dict, 'seismic_zone')) + r" & --- \\[6pt] \hline",
        r"Zone Factor, $Z$ & IRC 6:2017 Table 13 & " + _tex(str(sl_zone_factor)) + r" & --- \\[6pt] \hline",
        r"Importance Factor, $I$ & IRC 6:2017 Table 14 & " + (_render_value(input_dict, KEY_SL_IMPORTANCE_FACTOR, '1.20')) + r" & --- \\[6pt] \hline",
        r"Subsoil Foundation Category & IRC 6:2017 Cl. 218.4 & " + (_render_value(input_dict, KEY_SL_SOIL_TYPE)) + r" & --- \\[6pt] \hline",
        r"Spectral Acceleration Coefficient, $S_a/g$ & IRC 6:2017 Fig. 16 & " + _tex(str(sl_spectral)) + r" & --- \\[6pt] \hline",
        r"Horizontal Seismic Coefficient, $A_h$ & IRC 6:2017 Cl. 218.5.1 & " + _tex(str(sl_ah)) + r" & --- \\[6pt] \hline",
        r"Vertical Seismic Coefficient, $A_v$ & IRC 6:2017 Cl. 218.5.2 & " + _tex(str(sl_av)) + r" & --- \\[6pt] \hline",
    ]
    t36_table = make_longtable(
        col_spec=r"|L{6.0cm}|C{3.8cm}|C{3.0cm}|C{2.5cm}|",
        caption="Seismic Load (EL) Parameters per IRC 6:2017 Cl. 218",
        headers=["Parameter", "Standard Reference", "Design Value", "Unit"],
        rows=t36_rows,
        label="tab:seismic-loads",
    )

    # ── Table 3.7: Temperature Load (TL) ──
    t37_rows = [
        r"Maximum Shade Temperature & IRC 6:2017 Fig. 13 & " + (_render_value(input_dict, 'shade_temp_max')) + r" & $^\circ$C \\[6pt] \hline",
        r"Minimum Shade Temperature & IRC 6:2017 Fig. 14 & " + (_render_value(input_dict, 'shade_temp_min')) + r" & $^\circ$C \\[6pt] \hline",
        r"Effective Bridge Temperature Range & IRC 6:2017 Cl. 215.2 & " + _tex(f"{tl_temp_min} to {tl_temp_max}") + r" & $^\circ$C \\[6pt] \hline",
        r"Design Temperature Rise ($\Delta T_{rise}$) & IRC 6:2017 Cl. 215.3 & +" + _tex(tl_rise) + r" & $^\circ$C \\[6pt] \hline",
        r"Design Temperature Fall ($\Delta T_{fall}$) & IRC 6:2017 Cl. 215.3 & \textminus{}" + _tex(tl_fall) + r" & $^\circ$C \\[6pt] \hline",
    ]
    t37_table = make_longtable(
        col_spec=r"|L{6.0cm}|C{3.8cm}|C{3.0cm}|C{2.5cm}|",
        caption="Temperature Load (TL) Parameters per IRC 6:2017 Cl. 215",
        headers=["Parameter", "Standard Reference", "Design Value", "Unit"],
        rows=t37_rows,
        label="tab:temp-loads",
    )

    # ── Table 3.8: Load Combinations ──
    _LOAD_LABEL_MAP = {
        "dead_load": "DL",
        "surfacing": "SIDL",
        "live_load": "LL",
        "wind_load": "WL",
        "thermal_load": "TL",
        "vehicle_collision": "VC",
        "barge_impact": "BI",
        "floating_bodies": "FB",
        "seismic": "EQ",
    }

    def _fmt_factors(factors):
        parts = []
        for load, val in factors.items():
            label = _LOAD_LABEL_MAP.get(load, load.upper())
            if isinstance(val, dict):
                add = val.get("adding")
                rel = val.get("relieving")
                add_s = f"{add:.2f}" if add is not None else "--"
                rel_s = f"{rel:.2f}" if rel is not None else "--"
                parts.append(f"{label}({add_s}/{rel_s})")
            else:
                if val is None:
                    continue
                parts.append(f"{label}({val:.2f})")
        return " + ".join(parts)

    uls_combos = IRC6_2017.uls_load_combinations()
    sls_combos = IRC6_2017.sls_load_combinations()
    lc_rows = []
    for i, combo in enumerate(uls_combos, start=1):
        cases = _fmt_factors(combo["factors"])
        lc_rows.append(f"ULS-{i:02d} & {cases} \\\\[6pt] \\hline")
    for i, combo in enumerate(sls_combos, start=1):
        cases = _fmt_factors(combo["factors"])
        lc_rows.append(f"SLS-{i:02d} & {cases} \\\\[6pt] \\hline")

    t38_table = make_longtable(
        col_spec=r"|C{3.2cm}|p{12.2cm}|",
        caption="Design Load Combinations (ULS and SLS) per IRC 6:2017 Table B.1 to B.4",
        headers=["Combination ID", r"Governing Load Cases \& Combination Factors"],
        rows=lc_rows,
        label="tab:load-combos",
        note="All IRC 6:2017 load combinations are evaluated automatically across the grillage model envelope.",
    )

    return rf"""
\chapter{{Loads and Load Combinations}}

This chapter provides a complete specification of all structural loads applied to the bridge and the load combinations considered for analysis and design in accordance with IRC 6:2017, IRC 112:2020, and IS 800:2007.

\vspace{{0.8em}}
{t31_table}

\vspace{{0.8em}}
{t32_table}

\vspace{{0.8em}}
{t33_table}

\vspace{{0.8em}}
{t34_table}

\vspace{{0.8em}}
{t35_table}

\vspace{{0.8em}}
{t36_table}

\vspace{{0.8em}}
{t37_table}

\vspace{{0.8em}}
{t38_table}
"""
