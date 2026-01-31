import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors


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

palette = {
    "ProteinSage": "#F7C98B",
    "ESM-2": "#9FBAD5",
}
EDGE_TOTAL = "#3A3A3A"


def lighten_color(hex_color, amount=0.62):
    rgb = np.array(mcolors.to_rgb(hex_color))
    white = np.array([1, 1, 1])
    return mcolors.to_hex(rgb + (white - rgb) * amount)


thresholds = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 0.95])
total_a = np.array([4202, 3389, 2916, 2646, 2401, 2210])
struct_a = np.array([2343, 2322, 2297, 2261, 2151, 2029])
total_b = np.array([6382, 4712, 3932, 3178, 2832, 2509])
struct_b = np.array([2984, 2804, 2711, 2539, 2318, 2194])

ratio_a = struct_a / total_a
ratio_b = struct_b / total_b
delta_model = ratio_a - ratio_b

c_a_struct = palette["ProteinSage"]
c_b_struct = palette["ESM-2"]
c_a_total = lighten_color(c_a_struct)
c_b_total = lighten_color(c_b_struct)

fig = plt.figure(figsize=(170 / 25.4, 120 / 25.4))
gs = fig.add_gridspec(1, 2, width_ratios=[0.72, 0.28], wspace=0.10)
ax_e = fig.add_subplot(gs[0, 0])
ax_r = fig.add_subplot(gs[0, 1], sharey=ax_e)

pair_sep, group_gap = 0.34, 0.55
bar_h_total, bar_h_struct = 0.30, 0.18
ypos, meta, y = [], [], 0.0
for i in range(len(thresholds)):
    ypos += [y, y + pair_sep]
    meta += [(i, "A"), (i, "B")]
    y += pair_sep + group_gap
ypos = np.array(ypos)
ax_e.set_ylim(-0.45, ypos.max() + bar_h_total)


def draw_row(yy, total, struct, c_total, c_struct):
    ax_e.barh(yy, total, height=bar_h_total, color=c_total,
              edgecolor=EDGE_TOTAL, linewidth=0.7, zorder=1, clip_on=False)
    ax_e.barh(yy, struct, height=bar_h_struct, color=c_struct,
              edgecolor="white", linewidth=0.9, zorder=2, clip_on=False)


for yy, (i, m) in zip(ypos, meta):
    if m == "A":
        draw_row(yy, total_a[i], struct_a[i], c_a_total, c_a_struct)
    else:
        draw_row(yy, total_b[i], struct_b[i], c_b_total, c_b_struct)

max_w = max(total_a.max(), total_b.max())
ax_e.set_xlim(0, max_w * 1.06)
ax_e.set_xlabel("Predicted count")
ax_e.set_ylabel("Prediction threshold")
ax_e.spines["top"].set_visible(False)
ax_e.spines["right"].set_visible(False)
yticks = [(ypos[2 * i] + ypos[2 * i + 1]) / 2 for i in range(len(thresholds))]
ax_e.set_yticks(yticks, [f"{t:g}" for t in thresholds])

ax_r.set_xlabel("Delta structure ratio\n(ProteinSage - ESM-2)", fontsize=SMALL_FONTSIZE)
ax_r.xaxis.labelpad = 3.0
ax_r.spines["top"].set_visible(False)
ax_r.spines["right"].set_visible(False)
ax_r.spines["left"].set_visible(False)
ax_r.tick_params(left=False, labelleft=False)
max_abs = float(np.max(np.abs(delta_model)))
pad = max_abs * 0.35 + 1e-6
ax_r.set_xlim(-max_abs - pad, max_abs + pad)
tick_max = max_abs if max_abs > 1e-6 else 0.05
ax_r.set_xticks([-tick_max, 0.0, tick_max])
ax_r.set_xticklabels([f"{-tick_max:.2f}", "0", f"{tick_max:.2f}"], fontsize=8.6)
ax_r.axvline(0.0, color="#555555", linewidth=0.8, linestyle="--", zorder=1)
colors_delta = np.where(delta_model >= 0, c_a_struct, c_b_struct)
ax_r.scatter(delta_model, yticks, s=5.6 ** 2, c=colors_delta,
             edgecolors="white", linewidths=0.9, zorder=5)

out = "fig5_e_threshold_comparison.png"
fig.savefig(out, dpi=600, transparent=True)
print(f"Saved {out}")
