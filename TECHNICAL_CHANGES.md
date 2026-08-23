# OsdagBridge LaTeX Report Generator Refactoring & Technical Changes

## 1. Executive Summary

This document details the refactoring, architectural improvements, and visual enhancements implemented in the **OsdagBridge** LaTeX report generation module (`osdagbridge.core.reports`).

The refactoring addresses several critical formatting, layout, structural, and visual shortcomings present in the original report generator:
1. **Multi-Page Table Headers**: Replaced rigid tabular/longtable environments with a centralized, robust `make_longtable` builder that automatically injects `\endfirsthead`, `\endhead`, `\endfoot`, and `\endlastfoot` across all chapters. Tables spanning page breaks now repeat column headers and display continuation notices (`Table <N> (Continued)`).
2. **Footer Overlap and Vertical Margin Fixes**: Resolved the severe footer bleed on Page 30 and other pages caused by an erroneous `\vspace{-20pt}` inside `\footrule` and unconstrained page geometries. Standardized geometry options with `includehead`, `includefoot`, `headheight=22pt`, `headsep=12pt`, and `footskip=30pt`.
3. **Load and Geometry Table Refactoring**: Restructured Chapter 3 to distinctly separate Vehicle Live Loads (Table 3.3) and Footpath/Pedestrian Live Loads (Table 3.4), providing explicit unit columns and code references.
4. **Utilization Ratio (Demand/Capacity) Summary Visualizations**: Implemented programmatic generation of high-resolution bar charts in `plot_utils.py` displaying the Utilization Ratio ($UR = \text{Demand} / \text{Capacity}$) for all primary superstructure components (Plate Girders, Concrete Deck Slab, Cross Bracing, End Diaphragms) with a prominent red dashed reference line at the design limit ($UR = 1.0$), dynamically embedded into Section 5.5.
5. **Material Quantity Bar Charts**: Implemented programmatic generation and embedding of a 2-panel material quantity breakdown chart in Chapter 7 summarizing structural steel tonnage (Girders, Cross Bracing, End Diaphragms, Stiffeners/Splices) alongside concrete volume ($\text{m}^3$) versus reinforcement steel weight (MT).
6. **Centralized Style System (`styles.py`)**: Established a single source of truth for color palettes, geometry, table padding (`\arraystretch`, `\tabcolsep`), font sizing, and header/footer configurations.

---

## 2. Architecture & File Structure

```
src/osdagbridge/core/reports/
├── __init__.py               # Package exports (ReportMetadata, ReportOptions, ReportRequest)
├── styles.py                 # [NEW] Centralized design tokens, geometry, preamble & table generator
├── plot_utils.py             # [NEW] Programmatic chart generators for UR & Material Take-off
├── report_generator.py       # Main report orchestration & PyLaTeX compilation pipeline
├── report_utils.py           # Text escaping, unit formatting, and helper routines
├── executive_summary.py      # Executive Summary with multi-page table formatting
├── chap1.py                  # Chapter 1: Project Information & Design Team
├── chap2.py                  # Chapter 2: Input Parameters & Component Schedules
├── chap3.py                  # Chapter 3: Loads & Load Combinations (Refactored Live Loads)
├── chap4.py                  # Chapter 4: Analysis Results & Force Envelopes
├── chap5.py                  # Chapter 5: Design Checks & Embedded UR Summary Chart
├── chap6.py                  # Chapter 6: CAD Drawings & Superstructure Visualizations
├── chap7.py                  # Chapter 7: Material Take-off & Embedded Quantity Charts
├── chap8.py                  # Chapter 8: Standards, Assumptions & Engineering Log
└── chap9.py                  # Chapter 9: References
```

---

## 3. Detailed Component Refactoring

### 3.1. Centralized Formatting & Style System (`styles.py`)
- **Design Tokens**:
  - `COLOR_OSDAG_GREEN` (`#99B722`): Primary brand color for section rules and table accents.
  - `COLOR_HEADER_BG` (`#EEF5CB`): Soft tinted background for all table header rows.
  - `COLOR_PASS_GREEN` (`#2E7D32`) & `COLOR_FAIL_RED` (`#D32F2F`): High-contrast status indicators.
  - `COLOR_LIMIT_RED` (`#C62828`): Red dashed threshold line for $UR = 1.0$.
  - `COLOR_DARK_NAVY` (`#1A2B4C`): Deep navy for chapter titles and primary headings.
- **Unified Document Geometry**:
  ```latex
  \geometry{
    a4paper,
    top=25mm,
    bottom=28mm,
    left=20mm,
    right=20mm,
    headheight=22pt,
    headsep=12pt,
    footskip=30pt,
    includehead,
    includefoot
  }
  ```
- **Global Spacing & Paddings**:
  - `\renewcommand{\arraystretch}{1.15}`
  - `\setlength{\tabcolsep}{5pt}`
- **Automated Multi-Page Table Generator (`make_longtable`)**:
  - Automatically wraps headers in `\rowcolor{tableHeaderBg}` and bold typography.
  - Configures `\endfirsthead`, continued header with `\small\textbf{<Caption> (Continued)}` and `\endhead`.
  - Injects `\footnotesize\textit{Continued on next page}` with `\endfoot`.
  - Closes with `\endlastfoot` and optional sanitized footnotes (`\noindent\textit{Note: ...}`).

### 3.2. Footer Overlap & Vertical Spacing Resolution
- **Root Cause**: The original `report_generator.py` defined `\renewcommand{\footrule}{\vspace{-20pt}\textcolor{osdagGreen}{\rule{\linewidth}{1.0pt}}}`, which shifted the footer rule upward by 20 points directly into the text body. In addition, the lack of `includehead, includefoot` and inadequate `footskip` allowed table rows (such as "G4" on Page 30) to bleed into the footer margin.
- **Solution**: Removed negative vertical spacing from `\footrule`, calibrated `footskip=30pt`, and set standard top/bottom margins with `includehead, includefoot`.

### 3.3. Load & Geometry Table Refactoring (`chap3.py`)
- **Table 3.3 (Vehicle Live Loads)**:
  - Lists vehicle classes per IRC 6:2017 Cl. 204 (Class A, Class 70R, Class AA, Class SV, Fatigue).
  - Explicit columns for `Parameter`, `Standard Reference`, `Design Value`, and `Unit`.
  - Details Impact Factors (Cl. 208), Longitudinal Braking Force (Cl. 211), and Centrifugal Force (Cl. 212).
- **Table 3.4 (Pedestrian and Footpath Live Loads)**:
  - Distinct table detailing Footpath Provision, Footway Live Load Intensity (IRC 6 Cl. 206.1), Footway Live Load Reduction (Cl. 206.1.1), and Pedestrian Railing Transverse Load (Cl. 209.7).

### 3.4. Utilization Ratio Summary Visualizations (`plot_utils.py` & `chap5.py`)
- **Function**: `generate_ur_summary_chart(output_dict, output_path)`
- **Features**:
  - Evaluates Demand-to-Capacity Ratios ($UR = \text{Demand} / \text{Capacity}$) across all key structural elements:
    - Plate Girders (Moment, Shear, Lateral-Torsional Buckling, Deflection, Fatigue)
    - Concrete Deck Slab (Sagging Flexure, Hogging Flexure, Cantilever Flexure, Punching Shear, One-Way Shear)
    - Cross Bracing (Compression, Tension, Slenderness)
    - End Diaphragms (Moment, Shear)
  - Color codes bars: Forest Green for safe passing members ($UR \leq 1.0$), Crimson Red for overstressed members ($UR > 1.0$).
  - Renders a bold red dashed reference line at $UR = 1.0$ labeled `Limit (UR = 1.0)`.
  - Dynamically embedded into Section 5.5 (*Overall Design Check Summary*) as `Figure 5.1`.

### 3.5. Material Quantity Take-Off Bar Charts (`plot_utils.py` & `chap7.py`)
- **Function**: `generate_material_quantity_charts(output_dict, input_dict, output_path)`
- **Features**:
  - 2-panel chart summarizing Bill of Materials quantities:
    - **Panel 1 (Structural Steel Breakdown)**: Plate Girders (MT), Cross Bracing (MT), End Diaphragms (MT), Stiffeners & Splices (MT).
    - **Panel 2 (Deck Slab Materials)**: Concrete Volume ($\text{m}^3$) vs Reinforcement Steel Weight (MT).
  - Dynamically embedded into Chapter 7 as `Figure 7.1`.

---

## 4. Verification & Output Comparison

| Metric / Aspect | Report_Before.pdf (Baseline) | Report_After.pdf (Enhanced) |
| :--- | :--- | :--- |
| **Total Pages** | 51 pages | 62 pages (complete, untruncated schedules) |
| **File Size** | 469,046 bytes | 883,135 bytes (high-res vector graphics & charts) |
| **Multi-page Tables** | Headers lost after page breaks | Headers repeated cleanly with `(Continued)` |
| **Table Header Style** | Plain unshaded text | Tinted background (`#EEF5CB`) with bold headers |
| **Page 30 Footer** | G4 row and text colliding with footer line | Clean separation with 30pt footskip & green rule |
| **Live Load Tables** | Merged / incomplete layout | Distinct Table 3.3 (Vehicle LL) & Table 3.4 (Footpath LL) |
| **Section 5.5 Visuals** | None (only tabular data) | Embedded Utilization Ratio bar chart ($UR=1.0$ limit line) |
| **Chapter 7 Visuals** | None (only tabular BOM) | Embedded 2-panel Material Quantity Take-off chart |
| **Styling Architecture** | Hardcoded LaTeX scattered across files | Centralized `styles.py` single source of truth |

---

## 5. Deliverables

1. **`Report_Before.pdf`**: Baseline design verification report generated prior to refactoring.
2. **`Report_After.pdf`**: Enhanced design report incorporating all PyLaTeX refactoring and visualizations.
3. **`TECHNICAL_CHANGES.md`**: Comprehensive technical documentation of all architecture and code changes.
4. **Git Repository**: All source modifications committed to the `dev` branch.
