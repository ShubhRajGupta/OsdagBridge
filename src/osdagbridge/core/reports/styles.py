"""
styles.py
---------
Centralized Styling and Formatting Configuration for OsdagBridge LaTeX Reports.
Acts as the single source of truth for:
  - Document geometry, margins, and page layout
  - Color palettes (Osdag green, header background, pass/fail status, neutral accents)
  - Typography, line spacing, and paragraph styling
  - Table formatting tokens (padding, row height, rule thickness, multi-page repeated headers)
  - Header and footer styling (with clean footrules, page numbering, and default notes)
  - Reusable PyLaTeX / LaTeX table builders (make_longtable)
"""

from __future__ import annotations
import re
from typing import List, Optional, Sequence, Union

# ==============================================================================
# 1. COLOR PALETTE CONSTANTS (Hex strings for Python/matplotlib & LaTeX HTML)
# ==============================================================================

COLOR_OSDAG_GREEN = "91B014"       # Primary Osdag brand green
COLOR_DARK_GREEN  = "6D850E"       # Darker shade for borders and accents
COLOR_HEADER_BG   = "EBF3CE"       # Soft pastel green for table headers
COLOR_ALT_ROW     = "F9FAF5"       # Alternating row background
COLOR_DARK_NAVY   = "1A2B4C"       # Primary heading & dark text accent
COLOR_PASS_GREEN  = "2E7D32"       # Passing checks / success
COLOR_FAIL_RED    = "C62828"       # Failing checks / warnings
COLOR_LIMIT_RED   = "D32F2F"       # Threshold line on charts
COLOR_LIGHT_GRAY  = "F4F5F7"       # Secondary container background
COLOR_BORDER_GRAY = "CCCCCC"       # Subtle table borders
COLOR_ACCENT_BLUE = "1976D2"       # Diagram / auxiliary elements

# Hex codes with '#' for matplotlib / HTML
HEX_OSDAG_GREEN = f"#{COLOR_OSDAG_GREEN}"
HEX_HEADER_BG   = f"#{COLOR_HEADER_BG}"
HEX_PASS_GREEN  = f"#{COLOR_PASS_GREEN}"
HEX_FAIL_RED    = f"#{COLOR_FAIL_RED}"
HEX_LIMIT_RED   = f"#{COLOR_LIMIT_RED}"
HEX_DARK_NAVY   = f"#{COLOR_DARK_NAVY}"
HEX_LIGHT_GRAY  = f"#{COLOR_LIGHT_GRAY}"

# ==============================================================================
# 2. DOCUMENT GEOMETRY & LAYOUT SETTINGS
# ==============================================================================

GEOMETRY_OPTIONS = (
    "a4paper, "
    "top=25mm, "
    "bottom=28mm, "
    "left=20mm, "
    "right=20mm, "
    "headheight=22pt, "
    "headsep=12pt, "
    "footskip=30pt, "
    "includehead, "
    "includefoot"
)

# Table layout tokens
TABCOLSEP = "5pt"              # Column horizontal separation
ARRAYSTRETCH = "1.15"          # Row height multiplier
ARRAYRULEWIDTH = "0.5pt"       # Grid rule thickness
EXTRAROWHEIGHT = "0.8pt"       # Vertical text padding per row
LTPRE = "4pt"                  # Space before longtable
LTPOST = "6pt"                 # Space after longtable

# ==============================================================================
# 3. LATEX PREAMBLE GENERATOR
# ==============================================================================

def get_report_preamble(
    project_name: str,
    job_number: str,
    report_date: str,
    report_version: str = "Rev 0",
) -> str:
    """Generate the standardized LaTeX preamble with centralized geometry,
    colors, headers, footers, and packages."""
    from osdagbridge.core.reports.report_utils import _tex

    pn = _tex(project_name)
    jn = _tex(job_number)
    rd = _tex(report_date)
    rv = _tex(report_version)

    return rf"""
\documentclass[12pt,a4paper]{{report}}

% ── Geometry & Margins (Single Source of Truth) ──
\usepackage[{GEOMETRY_OPTIONS}]{{geometry}}

% ── Essential Packages ──
\usepackage{{graphicx}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{booktabs}}
\usepackage{{array}}
\usepackage{{tabularx}}
\usepackage{{float}}
\usepackage{{fancyhdr}}
\usepackage[hidelinks]{{hyperref}}
\usepackage{{xcolor}}
\usepackage{{setspace}}
\usepackage{{enumitem}}
\usepackage{{caption}}
\usepackage{{subcaption}}
\usepackage{{multirow}}
\usepackage{{colortbl}}
\usepackage{{longtable}}
\usepackage{{titlesec}}
\usepackage{{titletoc}}
\usepackage{{lastpage}}
\usepackage{{makecell}}
\usepackage{{etoolbox}}
\usepackage{{needspace}}

% ── Color Definitions ──
\definecolor{{osdagGreen}}{{HTML}}{{{COLOR_OSDAG_GREEN}}}
\definecolor{{darkGreen}}{{HTML}}{{{COLOR_DARK_GREEN}}}
\definecolor{{tableHeaderBg}}{{HTML}}{{{COLOR_HEADER_BG}}}
\definecolor{{altRowBg}}{{HTML}}{{{COLOR_ALT_ROW}}}
\definecolor{{passGreen}}{{HTML}}{{{COLOR_PASS_GREEN}}}
\definecolor{{failRed}}{{HTML}}{{{COLOR_FAIL_RED}}}
\definecolor{{darkNavy}}{{HTML}}{{{COLOR_DARK_NAVY}}}
\definecolor{{lightGray}}{{HTML}}{{{COLOR_LIGHT_GRAY}}}

% ── Caption Styling ──
\captionsetup{{
    labelfont=bf,
    justification=raggedright,
    singlelinecheck=false,
    format=plain
}}

% ── Numbering Within Chapters ──
\numberwithin{{table}}{{chapter}}
\numberwithin{{figure}}{{chapter}}

% ── Table Layout and Spacing System ──
\setlength{{\tabcolsep}}{{{TABCOLSEP}}}
\renewcommand{{\arraystretch}}{{{ARRAYSTRETCH}}}
\setlength{{\arrayrulewidth}}{{{ARRAYRULEWIDTH}}}
\setlength{{\extrarowheight}}{{{EXTRAROWHEIGHT}}}
\setlength{{\LTpre}}{{{LTPRE}}}
\setlength{{\LTpost}}{{{LTPOST}}}
\setlength{{\LTleft}}{{0pt}}
\setlength{{\LTright}}{{\fill}}

% ── Page Break Protection Before Tables ──
\BeforeBeginEnvironment{{table}}{{\needspace{{4\baselineskip}}}}
\BeforeBeginEnvironment{{longtable}}{{\needspace{{4\baselineskip}}}}

% ── Software Default Boolean Flag ──
\newbool{{hasSDonPage}}
\boolfalse{{hasSDonPage}}
\newcommand{{\sdstar}}{{\booltrue{{hasSDonPage}}\ensuremath{{^*}}}}

% ── Header and Footer Configuration ──
\fancypagestyle{{main}}{{
  \fancyhf{{}}
  \fancyhead[L]{{\small {pn} $|$ {jn}}}
  \fancyhead[R]{{\small {rd} $|$ {rv}}}
  \fancyfoot[L]{{\footnotesize\textcolor{{black!70}}{{Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}}}}
  \fancyfoot[R]{{\footnotesize\textcolor{{black!70}}{{Page \thepage\ of \pageref*{{LastPage}}}}}}
  \renewcommand{{\headrule}}{{\color{{osdagGreen}}\hrule width\headwidth height 1pt \vspace{{2pt}}}}
  \renewcommand{{\footrule}}{{%
    \ifbool{{hasSDonPage}}{{%
      \hbox to \headwidth{{\footnotesize\textit{{* Software default value}}\hfil}}%
      \vspace{{2pt}}%
    }}{{%
      \vspace{{0pt}}%
    }}%
    \color{{osdagGreen}}\hrule width\headwidth height 1pt \vspace{{4pt}}%
  }}
}}

\fancypagestyle{{plain}}{{
  \fancyhf{{}}
  \fancyhead[L]{{\small {pn} $|$ {jn}}}
  \fancyhead[R]{{\small {rd} $|$ {rv}}}
  \fancyfoot[L]{{\footnotesize\textcolor{{black!70}}{{Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}}}}
  \fancyfoot[R]{{\footnotesize\textcolor{{black!70}}{{Page \thepage\ of \pageref*{{LastPage}}}}}}
  \renewcommand{{\headrule}}{{\color{{osdagGreen}}\hrule width\headwidth height 1pt \vspace{{2pt}}}}
  \renewcommand{{\footrule}}{{%
    \ifbool{{hasSDonPage}}{{%
      \hbox to \headwidth{{\footnotesize\textit{{* Software default value}}\hfil}}%
      \vspace{{2pt}}%
    }}{{%
      \vspace{{0pt}}%
    }}%
    \color{{osdagGreen}}\hrule width\headwidth height 1pt \vspace{{4pt}}%
  }}
}}

\fancypagestyle{{firstpage}}{{
  \fancyhf{{}}
  \renewcommand{{\headrulewidth}}{{0pt}}
  \fancyfoot[L]{{\footnotesize\textcolor{{black!70}}{{Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}}}}
  \fancyfoot[R]{{\footnotesize\textcolor{{black!70}}{{Page \thepage\ of \pageref*{{LastPage}}}}}}
  \renewcommand{{\footrule}}{{\color{{osdagGreen}}\hrule width\headwidth height 1pt \vspace{{4pt}}}}
}}

\pagestyle{{main}}
\setstretch{{1.15}}

% ── Column Types ──
\newcolumntype{{L}}[1]{{>{{\raggedright\arraybackslash}}p{{#1}}}}
\newcolumntype{{C}}[1]{{>{{\centering\arraybackslash}}p{{#1}}}}
\newcolumntype{{R}}[1]{{>{{\raggedleft\arraybackslash}}p{{#1}}}}
\newcolumntype{{Y}}{{>{{\centering\arraybackslash}}X}}

% ── Helper Macros ──
\newcommand{{\placeholder}}[1]{{\textit{{\textless #1\textgreater}}}}
\newcommand{{\todo}}[1]{{\colorbox{{yellow}}{{TODO: #1}}}}

% ── Section Heading Format & Colors ──
\titleformat{{\chapter}}[hang]{{\normalfont\huge\bfseries\color{{darkNavy}}}}{{\thechapter.}}{{12pt}}{{\huge}}
\titleformat{{\section}}[hang]{{\normalfont\Large\bfseries\color{{darkNavy}}}}{{\thesection}}{{10pt}}{{\Large}}
\titleformat{{\subsection}}[hang]{{\normalfont\large\bfseries\color{{darkNavy}}}}{{\thesubsection}}{{8pt}}{{\large}}

% ── Chapter Spacing ──
\titlespacing*{{\chapter}}{{0pt}}{{0pt}}{{12pt}}
\titlespacing*{{\section}}{{0pt}}{{12pt}}{{6pt}}
\titlespacing*{{\subsection}}{{0pt}}{{8pt}}{{4pt}}

\title{{\Large\textbf{{OsdagBridge}} \\ \normalsize Open Source Software for Steel Girder Bridge Design \\ \vspace{{2cm}} \large Design Report}}
\author{{}}
\date{{}}

\begin{{document}}
"""

# ==============================================================================
# 4. STANDARDIZED LONGTABLE BUILDER (Repeated Headers Across Page Breaks)
# ==============================================================================

def make_longtable(
    col_spec: str,
    caption: str,
    headers: Sequence[str],
    rows: Union[Sequence[str], str],
    label: Optional[str] = None,
    note: Optional[str] = None,
    col_widths: Optional[Sequence[str]] = None,
) -> str:
    """Build a standardized PyLaTeX/LaTeX longtable with repeated headers
    across page transitions, tinted header row, and continued notices.

    Parameters
    ----------
    col_spec : str
        Column specification (e.g. '|C{2.0cm}|L{4.0cm}|C{2.5cm}|').
    caption : str
        Main table caption.
    headers : Sequence[str]
        List of header cell strings (e.g. ['Girder', 'Check', 'UR', 'Status']).
    rows : Sequence[str] or str
        Either a list of LaTeX row strings (each ending with '\\\\ \\hline')
        or a single multiline string of formatted rows.
    label : Optional[str]
        LaTeX \\label for the table.
    note : Optional[str]
        Footnote / description displayed below the table.
    """
    # Count number of columns from col_spec or headers
    num_cols = len(headers)

    import re
    # Format header row safely
    formatted_headers = []
    for h in headers:
        h_str = str(h).strip()
        h_str = re.sub(r'(?<!\\)&', r'\\&', h_str)
        if not h_str.startswith(r"\textbf{") and not h_str.startswith(r"\makecell{") and not h_str.startswith(r"\multicolumn{"):
            formatted_headers.append(f"\\textbf{{{h_str}}}")
        else:
            formatted_headers.append(h_str)

    header_cells = " & ".join(formatted_headers)
    header_row = f"\\rowcolor{{tableHeaderBg}} {header_cells} \\\\[6pt]\n\\hline"

    caption_clean = re.sub(r'(?<!\\)&', r'\\&', caption)
    # Caption and label line
    label_str = f"\\label{{{label}}}" if label else ""
    caption_line = f"\\caption{{\\textbf{{{caption_clean}}}}}{label_str} \\\\"

    # Multi-page repeated header
    continued_header = (
        f"\\multicolumn{{{num_cols}}}{{c}}{{\\small\\textbf{{{caption_clean} (Continued)}}}} \\\\[6pt]\n"
        f"\\hline\n"
        f"{header_row}"
    )

    # Continuation footer
    continuation_footer = (
        f"\\hline\n"
        f"\\multicolumn{{{num_cols}}}{{r}}{{\\footnotesize\\textit{{Continued on next page}}}} \\\\"
    )

    # Body content formatting
    if isinstance(rows, (list, tuple)):
        body_content = "\n".join(r.rstrip() for r in rows if r.strip())
    else:
        body_content = rows.strip()

    # Note below table
    if note:
        note_clean = re.sub(r'(?<!\\)%', r'\\%', str(note).strip())
        note_clean = re.sub(r'(?<!\\)&', r'\\&', note_clean)
        if not note_clean.lower().startswith("note:"):
            note_clean = f"Note: {note_clean}"
        note_block = f"\n\\noindent\\textit{{{note_clean}}}"
    else:
        note_block = ""

    return (
        f"\\begin{{longtable}}{{{col_spec}}}\n"
        f"{caption_line}\n"
        f"\\hline\n"
        f"{header_row}\n"
        f"\\endfirsthead\n"
        f"\n"
        f"{continued_header}\n"
        f"\\endhead\n"
        f"\n"
        f"{continuation_footer}\n"
        f"\\endfoot\n"
        f"\n"
        f"\\hline\n"
        f"\\endlastfoot\n"
        f"\n"
        f"{body_content}\n"
        f"\\end{{longtable}}{note_block}\n"
    )

# ==============================================================================
# 5. FIGURE EMBEDDING HELPER
# ==============================================================================

def embed_figure(
    path: Optional[str],
    caption: str,
    width: str = r"0.92\textwidth",
    label: Optional[str] = None,
) -> str:
    """Embed a high-resolution figure or a structured placeholder box."""
    label_tex = f"\\label{{{label}}}\n" if label else ""
    if path:
        p = path.replace("\\", "/")
        return (
            r"\begin{figure}[H]" + "\n"
            r"\centering" + "\n"
            r"\includegraphics[width=" + width + r"]{" + p + r"}" + "\n"
            r"\caption{\textbf{" + caption + r"}}" + "\n"
            + label_tex +
            r"\end{figure}"
        )
    return (
        r"\begin{figure}[H]" + "\n"
        r"\centering" + "\n"
        r"\fbox{\parbox{0.92\textwidth}{" + "\n"
        r"\centering\vspace{1.5em}" + "\n"
        r"\textit{[ Figure: " + caption + r" ]}" + "\n"
        r"\vspace{1.5em}" + "\n"
        r"}}" + "\n"
        r"\caption{\textbf{" + caption + r"}}" + "\n"
        + label_tex +
        r"\end{figure}"
    )
