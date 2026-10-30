"""
Shared Figure Style

Styling shared by the compound figures in the paper, so that they all match
the original PowerPoint charts and the paper's typography.

The paper uses the IEEEtran class, which typesets text in Times at a 3.5 in
column width; figures are drawn at that width with 8 pt text (caption size)
and included at width=\\columnwidth, so no text is scaled.
"""

import matplotlib.pyplot as plt

FIGURE_WIDTH = 3.5
FONT_SIZE = 8

# Bars, as they print in the paper: ~7.2 pt thick including the outline
BAR_THICKNESS_PT = 6.4
BAR_EDGE_COLOR = 'black'
BAR_EDGE_WIDTH = 0.8

GRID_COLOR = '#D9D9D9'
PLOT_BACKGROUND = '#F2F2F2'

# Bar fills used by the original PowerPoint charts
BLUE = '#46B1E1'
LIGHT_BLUE = '#61CBF4'
GREEN = '#8ED973'
ORANGE = '#F2AA84'


def apply_paper_style():
    """Use the paper's font (Times) for all text, with embedded fonts."""
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'Times', 'Nimbus Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'stix',
        'font.size': FONT_SIZE,
        'pdf.fonttype': 42,  # embed TrueType fonts (required by IEEE PDF eXpress)
    })


def style_axes(ax, value_axis):
    """
    Apply the shared look to one panel.

    value_axis is 'x' for horizontal bars or 'y' for vertical bars; gridlines
    run along it, and the category baseline gets the black axis line.
    """
    ax.set_facecolor(PLOT_BACKGROUND)
    ax.grid(axis=value_axis, color=GRID_COLOR, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)

    for spine in ('top', 'right'):
        ax.spines[spine].set_visible(False)
    # Horizontal bars keep a light category axis on the left; vertical bars
    # rely on the gridlines instead
    if value_axis == 'x':
        ax.spines['left'].set_color(GRID_COLOR)
    else:
        ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0, pad=2)

    # Black axis line along the bottom, with outward ticks
    ax.spines['bottom'].set_color(BAR_EDGE_COLOR)
    ax.spines['bottom'].set_linewidth(BAR_EDGE_WIDTH)
    ax.tick_params(axis='x', length=2.5, width=BAR_EDGE_WIDTH, pad=1.5,
                   color=BAR_EDGE_COLOR)
