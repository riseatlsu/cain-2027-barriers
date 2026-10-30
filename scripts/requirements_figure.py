"""
Requirements Compound Figure

This script regenerates the requirement completion figure directly from the
per-participant program analysis in program_analysis.xlsx:

    (a) how many participants completed each requirement (R1-R9), and
    (b) how many participants completed each total number of requirements.

Both panels count participants, so they are drawn side by side as one
compound figure at the IEEE single-column width (3.5 in). The panels keep
their own y-scales (up to 35 vs. up to 8 participants), and each panel's width
is proportional to its number of bars, so all bars have the same thickness and
spacing.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from figure_style import (FIGURE_WIDTH, FONT_SIZE, BAR_THICKNESS_PT,
                          BAR_EDGE_COLOR, BAR_EDGE_WIDTH, GREEN, LIGHT_BLUE,
                          apply_paper_style, style_axes)

PROGRAM_ANALYSIS_PATH = 'program_analysis.xlsx'
SHEET_NAME = 'Requirements'
OUTPUT_DIR = 'images'
OUTPUT_NAME = 'requirements_completion'

REQUIREMENTS = [f'R{i}' for i in range(1, 10)]

# Layout in inches: room for the y label and tick labels on the left, the
# second panel's tick labels between panels, and the x labels below
LEFT_MARGIN = 0.34
PANEL_GAP = 0.20
RIGHT_MARGIN = 0.03
TOP_MARGIN = 0.31
BOTTOM_MARGIN = 0.33
PLOT_HEIGHT = 1.0


def load_requirements():
    """Load one row per participant with a 0/1 column per requirement."""
    df = pd.read_excel(PROGRAM_ANALYSIS_PATH, sheet_name=SHEET_NAME)
    df = df[df['Participant'].astype(str).str.match(r'p\d+')]
    assert df[REQUIREMENTS].isin([0, 1]).all().all(), 'Requirements must be 0 or 1'
    return df


def count_completion(df):
    """Count participants per requirement and per total requirements completed."""
    per_requirement = df[REQUIREMENTS].sum().astype(int)

    totals = df[REQUIREMENTS].sum(axis=1).astype(int)
    per_participant = totals.value_counts().reindex(
        range(totals.min(), totals.max() + 1), fill_value=0)
    return per_requirement, per_participant


def plot_requirements(per_requirement, per_participant):
    """Draw both completion panels side by side."""
    apply_paper_style()

    # Two-line titles so the descriptions fit within each panel's width
    panels = [
        (per_requirement,
         '(a) Participants who completed\neach requirement',
         'Requirement', GREEN, 10),
        (per_participant,
         '(b) Participants by total\nrequirements completed',
         '# Requirements', LIGHT_BLUE, 2),
    ]

    # Same bar pitch in both panels: split the plot width by number of bars
    n_bars = sum(len(counts) for counts, *_ in panels)
    pitch = (FIGURE_WIDTH - LEFT_MARGIN - PANEL_GAP - RIGHT_MARGIN) / n_bars
    figure_height = PLOT_HEIGHT + TOP_MARGIN + BOTTOM_MARGIN
    fig = plt.figure(figsize=(FIGURE_WIDTH, figure_height))

    axes = []
    left = LEFT_MARGIN
    for counts, title, x_label, color, y_tick_step in panels:
        width = len(counts) * pitch
        ax = fig.add_axes([left / FIGURE_WIDTH, BOTTOM_MARGIN / figure_height,
                           width / FIGURE_WIDTH, PLOT_HEIGHT / figure_height])
        axes.append(ax)
        left += width + PANEL_GAP

        # Skip zero counts so they don't leave an outline stub on the x-axis
        values = counts.values
        drawn = values > 0
        ax.bar(np.arange(len(counts))[drawn], values[drawn],
               width=BAR_THICKNESS_PT / (pitch * 72), color=color,
               edgecolor=BAR_EDGE_COLOR, linewidth=BAR_EDGE_WIDTH, zorder=3)
        ax.set_xticks(range(len(counts)), [str(label) for label in counts.index])
        ax.set_xlim(-0.5, len(counts) - 0.5)
        ax.set_xlabel(x_label, fontsize=FONT_SIZE, labelpad=2)
        ax.set_title(title, fontsize=FONT_SIZE, pad=3)

        # The y-axis ends one participant past the tallest bar
        y_max = int(values.max()) + 1
        ax.set_ylim(0, y_max)
        ax.set_yticks(range(0, y_max + 1, y_tick_step))
        style_axes(ax, value_axis='y')

    # Both panels count participants; label the y-axis once, on the left
    axes[0].set_ylabel('# Participants', fontsize=FONT_SIZE, labelpad=2)
    return fig


def main():
    df = load_requirements()
    per_requirement, per_participant = count_completion(df)
    totals = df[REQUIREMENTS].sum(axis=1)
    print(f'Participants: {len(df)}')
    print('Participants completing each requirement:')
    print(per_requirement.to_string())
    print('Participants by number of requirements completed:')
    print(per_participant.to_string())
    print(f'Requirements completed: mean {totals.mean():.1f}, sd {totals.std():.1f}, '
          f'min {totals.min():.0f}, max {totals.max():.0f}')

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    per_requirement.rename('Participants').to_csv(
        os.path.join('data', 'requirements_per_requirement.csv'),
        index_label='Requirement')
    per_participant.rename('Participants').to_csv(
        os.path.join('data', 'requirements_per_participant.csv'),
        index_label='Requirements completed')

    fig = plot_requirements(per_requirement, per_participant)
    for extension in ('pdf', 'png'):
        path = os.path.join(OUTPUT_DIR, f'{OUTPUT_NAME}.{extension}')
        fig.savefig(path, dpi=300)
        print(f'Saved {path}')
    plt.close(fig)


if __name__ == '__main__':
    main()
