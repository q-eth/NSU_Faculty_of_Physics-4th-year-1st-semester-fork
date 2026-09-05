"""
python-style/colors.py

Цвета и минимальный Matplotlib-стиль под dog-blood LaTeX theme.

Идея:
    1--10  — красные оттенки из ChemNotes2.tex
    11--20 — голубая/синяя палитра p1--p9 из Physics Updated.tex + фиолетовый добивочный цвет

Графики по умолчанию делаются без фона:
    figure.facecolor = "none"
    axes.facecolor   = "none"

Для LaTeX с тёмной страницей это удобно:
    plt.savefig("image/plot.pdf", transparent=True, bbox_inches="tight")
"""

from __future__ import annotations

from cycler import cycler
import matplotlib.pyplot as plt


# ============================================================
# 1. Базовые цвета документа
# ============================================================

PAG = "#293133"       # фон страницы из исходника
PAG_TWO = "#3E4547"   # дополнительный тёмный фон из ChemNotes2
WHITE = "#FFFFFF"


# ============================================================
# 2. Красная палитра 1--10 из ChemNotes2.tex
# ============================================================

RED_1 = "#ffccd5"
RED_2 = "#ffb3c1"
RED_3 = "#ff8fa3"
RED_4 = "#ff758f"
RED_5 = "#ff4d6d"
RED_6 = "#c9184a"
RED_7 = "#a4133c"
RED_8 = "#800f2f"
RED_9 = "#590d22"
RED_10 = "#c9181e"

REDS = [
    RED_1,
    RED_2,
    RED_3,
    RED_4,
    RED_5,
    RED_6,
    RED_7,
    RED_8,
    RED_9,
    RED_10,
]


# ============================================================
# 3. Голубая / синяя палитра 11--19 из Physics Updated.tex
# ============================================================

P_1 = "#caf0f8"
P_2 = "#ade8f4"
P_3 = "#90e0ef"
P_4 = "#48cae4"
P_5 = "#00b4d8"
P_6 = "#0096c7"
P_7 = "#0077b6"
P_8 = "#023e8a"
P_9 = "#03045e"

# Добивочный 20-й цвет: фиолетовый из material-like палитры исходника
PURPLE_20 = "#9c27b0"

BLUES = [
    P_1,
    P_2,
    P_3,
    P_4,
    P_5,
    P_6,
    P_7,
    P_8,
    P_9,
    PURPLE_20,
]


# ============================================================
# 4. Общая палитра 1--20
# ============================================================

DOG_COLORS = {
    1: RED_1,
    2: RED_2,
    3: RED_3,
    4: RED_4,
    5: RED_5,
    6: RED_6,
    7: RED_7,
    8: RED_8,
    9: RED_9,
    10: RED_10,
    11: P_1,
    12: P_2,
    13: P_3,
    14: P_4,
    15: P_5,
    16: P_6,
    17: P_7,
    18: P_8,
    19: P_9,
    20: PURPLE_20,
}

DOG_COLORS_LIST = [DOG_COLORS[i] for i in range(1, 21)]


def dog_color(n: int) -> str:
    """
    Вернуть цвет по номеру 1--20.

    Пример:
        ax.plot(x, y, color=dog_color(15))
    """
    if n not in DOG_COLORS:
        raise ValueError("dog_color(n): n должен быть целым числом от 1 до 20.")
    return DOG_COLORS[n]


def dog_cycle(indices=range(1, 21)):
    """
    Вернуть matplotlib cycler по выбранным номерам цветов.

    Пример:
        ax.set_prop_cycle(dog_cycle([11, 13, 15, 17]))
    """
    return cycler(color=[dog_color(i) for i in indices])


# ============================================================
# 5. Matplotlib-стиль под тёмный LaTeX-документ
# ============================================================

def use_dog_style(
    *,
    transparent: bool = True,
    text_color: str = WHITE,
    grid_alpha: float = 0.18,
    linewidth: float = 2.0,
    fontsize: int = 12,
) -> None:
    """
    Включить стиль графиков.

    transparent=True:
        фон figure и axes отсутствует.
        Это удобно для вставки на тёмную страницу LaTeX.

    transparent=False:
        фон figure и axes будет PAG.
        Это удобно для просмотра графика отдельно вне LaTeX.
    """
    face = "none" if transparent else PAG

    plt.rcParams.update({
        "figure.facecolor": face,
        "axes.facecolor": face,
        "savefig.facecolor": face,
        "savefig.edgecolor": face,

        "text.color": text_color,
        "axes.labelcolor": text_color,
        "axes.titlecolor": text_color,
        "xtick.color": text_color,
        "ytick.color": text_color,

        "axes.edgecolor": text_color,
        "axes.linewidth": 0.8,

        "grid.color": text_color,
        "grid.alpha": grid_alpha,
        "grid.linewidth": 0.5,

        "lines.linewidth": linewidth,
        "patch.edgecolor": text_color,

        "font.size": fontsize,
        "axes.titlesize": fontsize + 2,
        "axes.labelsize": fontsize,
        "xtick.labelsize": fontsize - 1,
        "ytick.labelsize": fontsize - 1,
        "legend.fontsize": fontsize - 1,

        "legend.facecolor": face,
        "legend.edgecolor": text_color,
        "legend.framealpha": 0.0,

        "axes.prop_cycle": dog_cycle([15, 5, 13, 7, 17, 3, 20, 11]),
    })


def style_axis(ax, *, grid: bool = True) -> None:
    """
    Доточить конкретные оси под стиль.

    Пример:
        fig, ax = plt.subplots()
        style_axis(ax)
    """
    ax.set_facecolor("none")

    for spine in ax.spines.values():
        spine.set_color(WHITE)
        spine.set_linewidth(0.8)

    ax.tick_params(colors=WHITE, which="both")
    ax.xaxis.label.set_color(WHITE)
    ax.yaxis.label.set_color(WHITE)
    ax.title.set_color(WHITE)

    if grid:
        ax.grid(True, alpha=0.18)
    else:
        ax.grid(False)


def save_dogfig(fig, path: str, *, transparent: bool = True, dpi: int = 300) -> None:
    """
    Сохранить график для LaTeX.

    Для векторных графиков лучше:
        save_dogfig(fig, "image/plot.pdf")

    Для растровых:
        save_dogfig(fig, "image/plot.png")
    """
    fig.savefig(
        path,
        bbox_inches="tight",
        transparent=transparent,
        dpi=dpi,
    )
