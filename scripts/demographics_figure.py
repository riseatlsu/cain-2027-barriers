"""
Demographics Compound Figure

This script regenerates the participant demographics figure (computer,
block-based, and robot programming experience) directly from the
post-experiment questionnaire in survey_data.xlsx.

The three panels share the same experience categories, so they are drawn as
one compound figure with a single shared y-axis. The figure is sized to the
IEEE single-column width (3.5 in) and uses 8 pt text, so it can be included
at width=\\columnwidth without any scaling of the text.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from figure_style import (FIGURE_WIDTH, FONT_SIZE, BAR_THICKNESS_PT,
                          BAR_EDGE_COLOR, BAR_EDGE_WIDTH, BLUE, GREEN, ORANGE,
                          apply_paper_style, style_axes)

SURVEY_PATH = 'survey_data.xlsx'
SHEET_NAME = 'Former Programming Experience'
OUTPUT_DIR = 'images'
OUTPUT_NAME = 'demographics_programming_exp'

# Space above and below the plot area for the panel titles and x tick labels (in)
TOP_MARGIN = 0.18
BOTTOM_MARGIN = 0.15

# Bar spacing in printed points, matching the original requirements figure as
# it appeared in the paper (one bar every ~10.7 pt). The figure height follows.
BAR_PITCH_PT = 10.7

# A tick every 10 participants; the x-axis ends one past the longest bar
X_TICK_STEP = 10

# Survey question column -> (panel title, bar color)
PANELS = [
    ('How many years of experience do you have in computer programming?',
     '(a) Computer', BLUE),
    ('How many years of experience do you have with block-based programming languages?',
     '(b) Block-based', GREEN),
    ('How many years of experience do you have with robot programming languages?',
     '(c) Robot', ORANGE),
]

# Survey answer -> short axis label, in display order (top to bottom)
CATEGORIES = [
    ('No experience', 'None'),
    ('< 1 Year', '< 1 yr'),
    ('1 - 3 years', '1–3 yrs'),
    ('4 - 5 years', '4–5 yrs'),
    ('> 5 Years', '> 5 yrs'),
]


def categorize_experience(answer):
    """
    Map a survey answer to its canonical experience category.

    Matching is case- and whitespace-insensitive, mirroring the wildcard
    COUNTIF formulas originally used in the spreadsheet.
    """
    normalized = ' '.join(str(answer).lower().split())
    for category, _ in CATEGORIES:
        if ' '.join(category.lower().split()) in normalized:
            return category
    raise ValueError(f'Unrecognized experience answer: {answer!r}')


def load_survey_data():
    """Load one row per participant from the questionnaire sheet."""
    df = pd.read_excel(SURVEY_PATH, sheet_name=SHEET_NAME)
    return df[df['Participant'].notna()]


def count_experience(df):
    """Count participants per experience category for each panel."""
    counts = {}
    for column, title, _ in PANELS:
        categories = df[column].map(categorize_experience)
        counts[title] = categories.value_counts().reindex(
            [category for category, _ in CATEGORIES], fill_value=0)
        assert counts[title].sum() == len(df), f'{title}: counts do not sum to N'
    return pd.DataFrame(counts)


def plot_demographics(counts):
    """Draw the three experience panels side by side with a shared y-axis."""
    apply_paper_style()

    plot_height = len(CATEGORIES) * BAR_PITCH_PT / 72
    figure_height = plot_height + TOP_MARGIN + BOTTOM_MARGIN
    fig, axes = plt.subplots(1, len(PANELS), sharex=True, sharey=True,
                             figsize=(FIGURE_WIDTH, figure_height))
    labels = [label for _, label in CATEGORIES]
    x_max = int(counts.values.max()) + 1

    for ax, (_, title, color) in zip(axes, PANELS):
        # Skip zero counts so they don't leave an outline stub on the y-axis,
        # and draw bars above the spines so short bars keep their left outline
        values = counts[title].values
        drawn = values > 0
        ax.barh(np.arange(len(labels))[drawn], values[drawn],
                height=BAR_THICKNESS_PT / BAR_PITCH_PT, color=color,
                edgecolor=BAR_EDGE_COLOR, linewidth=BAR_EDGE_WIDTH, zorder=3)
        ax.set_yticks(range(len(labels)), labels)
        ax.set_title(title, fontsize=FONT_SIZE, pad=3)
        ax.set_xlim(0, x_max)
        ax.set_xticks(range(0, x_max + 1, X_TICK_STEP))
        style_axes(ax, value_axis='x')

    # Exactly one pitch per category, first category at the top
    axes[0].set_ylim(len(CATEGORIES) - 0.5, -0.5)
    fig.subplots_adjust(left=0.135, right=0.98, wspace=0.12,
                        top=1 - TOP_MARGIN / figure_height,
                        bottom=BOTTOM_MARGIN / figure_height)
    return fig


def main():
    df = load_survey_data()
    counts = count_experience(df)
    print(f'Participants: {len(df)}')
    print(counts.to_string())

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    counts.to_csv(os.path.join('data', 'demographics_programming_exp.csv'),
                  index_label='Experience')

    fig = plot_demographics(counts)
    for extension in ('pdf', 'png'):
        path = os.path.join(OUTPUT_DIR, f'{OUTPUT_NAME}.{extension}')
        fig.savefig(path, dpi=300)
        print(f'Saved {path}')
    plt.close(fig)


if __name__ == '__main__':
    main()
