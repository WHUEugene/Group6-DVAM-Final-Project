import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors
from matplotlib_venn import venn3, venn3_circles


BASE_FONTSIZE = 12.0
SMALL_FONTSIZE = 10.0

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
    "font.size": BASE_FONTSIZE,
    "axes.labelsize": BASE_FONTSIZE,
    "axes.titlesize": BASE_FONTSIZE,
    "legend.fontsize": SMALL_FONTSIZE,
    "xtick.labelsize": SMALL_FONTSIZE,
    "ytick.labelsize": SMALL_FONTSIZE,
    "axes.linewidth": 0.6,
    "lines.linewidth": 1.0,
    "patch.linewidth": 0.6,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.major.size": 3.0,
    "ytick.major.size": 3.0,
    "grid.linestyle": "--",
    "grid.linewidth": 0.5,
    "grid.alpha": 0.25,
    "savefig.dpi": 600,
    "figure.dpi": 200,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.unicode_minus": False,
})


def lighten_color(hex_color, amount=0.62):
    rgb = np.array(mcolors.to_rgb(hex_color))
    white = np.array([1, 1, 1])
    return mcolors.to_hex(rgb + (white - rgb) * amount)


def style_venn_common(v, circle_artists=None):
    if getattr(v, "subset_labels", None) is not None:
        for t in v.subset_labels:
            if t is None:
                continue
            t.set_fontsize(9.6)
            t.set_color("#222222")
    if getattr(v, "set_labels", None) is not None:
        for t in v.set_labels:
            if t is None:
                continue
            t.set_fontsize(9.6)
            t.set_color("#222222")
            t.set_fontweight("normal")
    if circle_artists is not None:
        for c in circle_artists:
            if c is None:
                continue
            c.set_lw(1.1)
            c.set_ls("-")
            c.set_edgecolor("#444444")
            c.set_alpha(0.85)


venn_ps = dict(onlyA=124, onlyB=0, AB=19, onlyC=538, AC=119, BC=20, ABC=1539)

fig, ax = plt.subplots(figsize=(90 / 25.4, 80 / 25.4))

v = venn3(
    subsets=(venn_ps["onlyA"], venn_ps["onlyB"], venn_ps["AB"],
             venn_ps["onlyC"], venn_ps["AC"], venn_ps["BC"], venn_ps["ABC"]),
    set_labels=("BLAST", "MMseqs2", "ProteinSage"),
    ax=ax,
)

colors = (
    lighten_color("#BFBFBF", 0.10),
    lighten_color("#C9D7E6", 0.10),
    lighten_color("#F7C98B", 0.10),
)

for pid, col in zip(["100", "010", "001"], colors):
    p = v.get_patch_by_id(pid)
    if p:
        p.set_color(col)
        p.set_alpha(0.35)
        p.set_edgecolor("none")
for pid in ["110", "101", "011", "111"]:
    p = v.get_patch_by_id(pid)
    if p:
        p.set_alpha(0.22)
        p.set_edgecolor("none")

circles = venn3_circles(
    subsets=(venn_ps["onlyA"], venn_ps["onlyB"], venn_ps["AB"],
             venn_ps["onlyC"], venn_ps["AC"], venn_ps["BC"], venn_ps["ABC"]),
    ax=ax,
)
style_venn_common(v, circles)
ax.set_axis_off()

plt.tight_layout()
out = "fig5_j_venn_proteinsage.png"
fig.savefig(out, dpi=600, transparent=True)
print(f"Saved {out}")
