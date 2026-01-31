import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Patch
import matplotlib.colors as mcolors
from matplotlib_venn import venn3, venn2, venn3_circles, venn2_circles

# =========================
# 全局样式设置
# =========================
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
    "cnn": "#F5B8B5",
    "transformer": "#B7D5C0",
    "attention": "#C7DCA7",
    "LSTM": "#9C73A7",
}
EDGE_TOTAL = "#3A3A3A"

def lighten_color(hex_color, amount=0.62):
    rgb = np.array(mcolors.to_rgb(hex_color))
    white = np.array([1, 1, 1])
    return mcolors.to_hex(rgb + (white - rgb) * amount)

C_A_STRUCT = palette["ProteinSage"]
C_B_STRUCT = palette["ESM-2"]

# =========================
# 数据定义
# =========================
models = ["ProteinSage", "ESM-2", "cnn", "transformer", "attention", "LSTM"]
data = {
    "ProteinSage": dict(test_accuracy=0.9725841639087245,
                        test_f1=0.9286473510926831,
                        test_precision=0.9814592763058942,
                        test_recall=0.9063728541973658),
    "ESM-2":       dict(test_accuracy=0.9481726539084715,
                        test_f1=0.9635827410956382,
                        test_precision=0.8957463218095724,
                        test_recall=0.9518274639081572),
    "cnn":         dict(test_accuracy=0.9862735419086523,
                        test_f1=0.9172654390874615,
                        test_precision=0.9381726549083726,
                        test_recall=0.9627354190876532),
    "transformer": dict(test_accuracy=0.9058274639081725,
                        test_f1=0.9736541829076543,
                        test_precision=0.9263541829075638,
                        test_recall=0.8972654390817265),
    "attention":   dict(test_accuracy=0.9572654390876523,
                        test_f1=0.9481726539084715,
                        test_precision=0.9827354190865234,
                        test_recall=0.9163541829076543),
    "LSTM":        dict(test_accuracy=0.9273541829076532,
                        test_f1=0.9681726539084715,
                        test_precision=0.9072654390817265,
                        test_recall=0.9718274639081572),
}
metrics = ["test_accuracy", "test_f1", "test_precision", "test_recall"]
titles  = ["Accuracy", "F1-score", "Precision", "Recall"]

# 数据e
thresholds = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 0.95])
total_A  = np.array([4202, 3389, 2916, 2646, 2401, 2210])
struct_A = np.array([2343, 2322, 2297, 2261, 2151, 2029])
total_B  = np.array([6382, 4712, 3932, 3178, 2832, 2509])
struct_B = np.array([2984, 2804, 2711, 2539, 2318, 2194])
ratio_A = struct_A / total_A
ratio_B = struct_B / total_B
delta_model = ratio_A - ratio_B

# 数据f,g
thr_line = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 0.95])
esm_col1 = np.array([0.7124725, 0.8026315, 0.8761440, 0.9018250, 0.9269060, 0.9465920])
esm_col2 = np.array([0.4675650, 0.5950760, 0.6894710, 0.7989300, 0.8185020, 0.8744510])
ps_col1  = np.array([0.6358880, 0.7789910, 0.8916320, 0.9561600, 0.9870890, 0.9945700])
ps_col2  = np.array([0.5575920, 0.6851580, 0.7877230, 0.8544970, 0.8958770, 0.9181000])

# 数据h,i
pie_h = {"BR": 2343 - 8 - 119, "Other": 119, "Unknown": 8}
pie_i = {
    "BR": 2984 - (79 + 258 + 71 + 83 + 102 + 443 + 152),
    "AU": 79, "BaxI_1": 258, "NrfD": 71, "Rcel-like": 83,
    "HeR": 102, "Other": 443, "Unknown": 152,
}

# 数据j,k,l
venn_PS = dict(onlyA=124, onlyB=0, AB=19, onlyC=538, AC=119, BC=20, ABC=1539)
venn_ESM = dict(onlyA=39, onlyB=15, AB=131, onlyC=160, AC=204, BC=5, ABC=1427)
PS_total = 2216
ESM_total = 1796
PS_ESM_inter = 1513
PS_only = PS_total - PS_ESM_inter
ESM_only = ESM_total - PS_ESM_inter

# =========================
# 辅助函数
# =========================
def soft_grid(ax):
    ax.yaxis.grid(True, linestyle="--", linewidth=0.6, alpha=0.28)
    ax.set_axisbelow(True)

def set_adaptive_ylim(ax, values):
    vmin, vmax = min(values), max(values)
    span = vmax - vmin if vmax > vmin else 0.01
    ax.set_ylim(max(0.88, vmin - span*0.15), 1.00)

def add_bar_labels(ax, xs, heights, fontsize=7.1):
    for x, v in zip(xs, heights):
        ax.text(x, v + 0.002, f"{v:.4f}",
                ha="center", va="bottom",
                fontsize=fontsize, clip_on=False)

def _style_venn_common(v, circle_artists=None):
    if getattr(v, "subset_labels", None) is not None:
        for t in v.subset_labels:
            if t is None: continue
            t.set_fontsize(9.6)
            t.set_color("#222222")
    if getattr(v, "set_labels", None) is not None:
        for t in v.set_labels:
            if t is None: continue
            t.set_fontsize(9.6)
            t.set_color("#222222")
            t.set_fontweight("normal")
    if circle_artists is not None:
        for c in circle_artists:
            if c is None: continue
            c.set_lw(1.1)
            c.set_ls("-")
            c.set_edgecolor("#444444")
            c.set_alpha(0.85)

# =========================
# 子图 (a) - Accuracy
# =========================
fig_a, ax_a = plt.subplots(figsize=(80/25.4, 60/25.4))
xs = np.arange(len(models))
colors = [palette[m] for m in models]
vals = [data[m]["test_accuracy"] for m in models]
ax_a.bar(xs, vals, width=0.72, color=colors, edgecolor="black", linewidth=0.9)
set_adaptive_ylim(ax_a, vals)
add_bar_labels(ax_a, xs, vals)
ax_a.set_xticks(xs, models, rotation=35, ha="right")
ax_a.set_title("Accuracy")
ax_a.set_ylabel("Accuracy")
soft_grid(ax_a)
plt.tight_layout()
fig_a.savefig("fig5_a_accuracy.png", dpi=600, transparent=True)
plt.close()

# =========================
# 子图 (b) - F1-score
# =========================
fig_b, ax_b = plt.subplots(figsize=(80/25.4, 60/25.4))
vals = [data[m]["test_f1"] for m in models]
ax_b.bar(xs, vals, width=0.72, color=colors, edgecolor="black", linewidth=0.9)
set_adaptive_ylim(ax_b, vals)
add_bar_labels(ax_b, xs, vals)
ax_b.set_xticks(xs, models, rotation=35, ha="right")
ax_b.set_title("F1-score")
ax_b.set_ylabel("F1-score")
soft_grid(ax_b)
plt.tight_layout()
fig_b.savefig("fig5_b_f1score.png", dpi=600, transparent=True)
plt.close()

# =========================
# 子图 (c) - Precision
# =========================
fig_c, ax_c = plt.subplots(figsize=(80/25.4, 60/25.4))
vals = [data[m]["test_precision"] for m in models]
ax_c.bar(xs, vals, width=0.72, color=colors, edgecolor="black", linewidth=0.9)
set_adaptive_ylim(ax_c, vals)
add_bar_labels(ax_c, xs, vals)
ax_c.set_xticks(xs, models, rotation=35, ha="right")
ax_c.set_title("Precision")
ax_c.set_ylabel("Precision")
soft_grid(ax_c)
plt.tight_layout()
fig_c.savefig("fig5_c_precision.png", dpi=600, transparent=True)
plt.close()

# =========================
# 子图 (d) - Recall
# =========================
fig_d, ax_d = plt.subplots(figsize=(80/25.4, 60/25.4))
vals = [data[m]["test_recall"] for m in models]
ax_d.bar(xs, vals, width=0.72, color=colors, edgecolor="black", linewidth=0.9)
set_adaptive_ylim(ax_d, vals)
add_bar_labels(ax_d, xs, vals)
ax_d.set_xticks(xs, models, rotation=35, ha="right")
ax_d.set_title("Recall")
ax_d.set_ylabel("Recall")
soft_grid(ax_d)
plt.tight_layout()
fig_d.savefig("fig5_d_recall.png", dpi=600, transparent=True)
plt.close()

# =========================
# 子图 (e) - 水平条形图+差异散点
# =========================
fig_e = plt.figure(figsize=(170/25.4, 120/25.4))
gs = fig_e.add_gridspec(1, 2, width_ratios=[0.72, 0.28], wspace=0.10)
ax_e = fig_e.add_subplot(gs[0, 0])
ax_r = fig_e.add_subplot(gs[0, 1], sharey=ax_e)

C_A_TOTAL = lighten_color(C_A_STRUCT)
C_B_TOTAL = lighten_color(C_B_STRUCT)

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
        draw_row(yy, total_A[i], struct_A[i], C_A_TOTAL, C_A_STRUCT)
    else:
        draw_row(yy, total_B[i], struct_B[i], C_B_TOTAL, C_B_STRUCT)

max_w = max(total_A.max(), total_B.max())
ax_e.set_xlim(0, max_w * 1.06)
ax_e.set_xlabel("Predicted count")
ax_e.set_ylabel("Prediction threshold")
ax_e.spines["top"].set_visible(False)
ax_e.spines["right"].set_visible(False)
yticks = [(ypos[2*i] + ypos[2*i+1]) / 2 for i in range(len(thresholds))]
ax_e.set_yticks(yticks, [f"{t:g}" for t in thresholds])

# 右侧差异图
ax_r.set_xlabel("Δ structure ratio\n(ProteinSage − ESM-2)", fontsize=SMALL_FONTSIZE)
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
colors_delta = np.where(delta_model >= 0, C_A_STRUCT, C_B_STRUCT)
ax_r.scatter(delta_model, yticks, s=5.6**2, c=colors_delta,
             edgecolors="white", linewidths=0.9, zorder=5)
fig_e.savefig("fig5_e_threshold_comparison.png", dpi=600, transparent=True)
plt.close()

# =========================
# 子图 (f) - TM>0 曲线
# =========================
fig_f, ax_f = plt.subplots(figsize=(90/25.4, 70/25.4))
LINE_W = 2.0
MARKER_S = 4.8
MEW = 0.8

ax_f.plot(thr_line, ps_col1, marker="o", markersize=MARKER_S, linewidth=LINE_W,
          color=C_A_STRUCT, markerfacecolor=C_A_STRUCT,
          markeredgecolor="white", markeredgewidth=MEW, label="ProteinSage")
ax_f.plot(thr_line, esm_col1, marker="o", markersize=MARKER_S, linewidth=LINE_W,
          color=C_B_STRUCT, markerfacecolor=C_B_STRUCT,
          markeredgecolor="white", markeredgewidth=MEW, label="ESM-2")

ax_f.set_ylabel("ratio of tm>0")
ax_f.set_xlabel("Prediction threshold")
ax_f.set_xticks(thr_line)
ax_f.set_xticklabels([f"{t:g}" for t in thr_line])
ax_f.spines["top"].set_visible(False)
ax_f.spines["right"].set_visible(False)
ax_f.yaxis.grid(True, linestyle="--", linewidth=0.5, alpha=0.25)
ax_f.set_axisbelow(True)
ax_f.legend(loc="best", frameon=False)

# 添加数值标签
y0, y1 = ax_f.get_ylim()
dy = (y1 - y0) * 0.04
for xi, yi in zip(thr_line, ps_col1):
    ax_f.text(xi, yi + dy, f"{yi:.3f}", ha="center", va="bottom", fontsize=7.2)
for xi, yi in zip(thr_line, esm_col1):
    ax_f.text(xi, yi + dy, f"{yi:.3f}", ha="center", va="bottom", fontsize=7.2)

plt.tight_layout()
fig_f.savefig("fig5_f_tm_ratio.png", dpi=600, transparent=True)
plt.close()

# =========================
# 子图 (g) - 7TM 曲线
# =========================
fig_g, ax_g = plt.subplots(figsize=(90/25.4, 70/25.4))
ax_g.plot(thr_line, ps_col2, marker="o", markersize=MARKER_S, linewidth=LINE_W,
          color=C_A_STRUCT, markerfacecolor=C_A_STRUCT,
          markeredgecolor="white", markeredgewidth=MEW, label="ProteinSage")
ax_g.plot(thr_line, esm_col2, marker="o", markersize=MARKER_S, linewidth=LINE_W,
          color=C_B_STRUCT, markerfacecolor=C_B_STRUCT,
          markeredgecolor="white", markeredgewidth=MEW, label="ESM-2")

ax_g.set_ylabel("ratio of 7tm")
ax_g.set_xlabel("Prediction threshold")
ax_g.set_xticks(thr_line)
ax_g.set_xticklabels([f"{t:g}" for t in thr_line])
ax_g.spines["top"].set_visible(False)
ax_g.spines["right"].set_visible(False)
ax_g.yaxis.grid(True, linestyle="--", linewidth=0.5, alpha=0.25)
ax_g.set_axisbelow(True)
ax_g.legend(loc="best", frameon=False)

y0, y1 = ax_g.get_ylim()
dy = (y1 - y0) * 0.04
for xi, yi in zip(thr_line, ps_col2):
    ax_g.text(xi, yi + dy, f"{yi:.3f}", ha="center", va="bottom", fontsize=7.2)
for xi, yi in zip(thr_line, esm_col2):
    ax_g.text(xi, yi + dy, f"{yi:.3f}", ha="center", va="bottom", fontsize=7.2)

plt.tight_layout()
fig_g.savefig("fig5_g_7tm_ratio.png", dpi=600, transparent=True)
plt.close()

# =========================
# 子图 (h) - ProteinSage 饼图
# =========================
fig_h, ax_h = plt.subplots(figsize=(90/25.4, 90/25.4))
tab = list(mcolors.TABLEAU_COLORS.values())

def pie_color_map(keys, br_color):
    cmap = {"BR": br_color}
    k2 = [k for k in keys if k != "BR"]
    for i, k in enumerate(k2):
        cmap[k] = lighten_color(tab[i % len(tab)], 0.35)
    return cmap

keys = list(pie_h.keys())
vals = np.array([pie_h[k] for k in keys], dtype=float)
total = vals.sum()
cmap = pie_color_map(keys, C_A_STRUCT)
colors = [cmap[k] for k in keys]
explode = [0.06 if k == "BR" else 0.00 for k in keys]

ax_h.pie(vals, startangle=90, counterclock=False, colors=colors, explode=explode,
         wedgeprops=dict(linewidth=0.8, edgecolor="white"))
ax_h.set_title("ProteinSage (n=2343)", pad=6)

br = pie_h.get("BR", 0)
br_pct = br / total * 100.0 if total > 0 else 0.0
ax_h.text(0.0, -1.15, f"BR: {int(br)} ({br_pct:.1f}%)",
          ha="center", va="top", fontsize=10.2, fontweight="bold")

handles = [Patch(facecolor=cmap[k], edgecolor="white", label=f"{k}: {int(pie_h[k])}") for k in keys]
ax_h.legend(handles=handles, frameon=False, loc="center left",
            bbox_to_anchor=(1.02, 0.50), handletextpad=0.6, labelspacing=0.55)
ax_h.set_aspect("equal")
plt.tight_layout()
fig_h.savefig("fig5_h_pie_proteinsage.png", dpi=600, transparent=True)
plt.close()

# =========================
# 子图 (i) - ESM-2 饼图
# =========================
fig_i, ax_i = plt.subplots(figsize=(90/25.4, 90/25.4))
keys = list(pie_i.keys())
vals = np.array([pie_i[k] for k in keys], dtype=float)
total = vals.sum()
cmap = pie_color_map(keys, C_B_STRUCT)
colors = [cmap[k] for k in keys]
explode = [0.06 if k == "BR" else 0.00 for k in keys]

ax_i.pie(vals, startangle=90, counterclock=False, colors=colors, explode=explode,
         wedgeprops=dict(linewidth=0.8, edgecolor="white"))
ax_i.set_title("ESM-2 (n=2984)", pad=6)

br = pie_i.get("BR", 0)
br_pct = br / total * 100.0 if total > 0 else 0.0
ax_i.text(0.0, -1.15, f"BR: {int(br)} ({br_pct:.1f}%)",
          ha="center", va="top", fontsize=10.2, fontweight="bold")

handles = [Patch(facecolor=cmap[k], edgecolor="white", label=f"{k}: {int(pie_i[k])}") for k in keys]
ax_i.legend(handles=handles, frameon=False, loc="center left",
            bbox_to_anchor=(1.02, 0.50), handletextpad=0.6, labelspacing=0.55)
ax_i.set_aspect("equal")
plt.tight_layout()
fig_i.savefig("fig5_i_pie_esm2.png", dpi=600, transparent=True)
plt.close()

# =========================
# 子图 (j) - Venn3 ProteinSage
# =========================
fig_j, ax_j = plt.subplots(figsize=(90/25.4, 80/25.4))
v = venn3(
    subsets=(venn_PS["onlyA"], venn_PS["onlyB"], venn_PS["AB"],
             venn_PS["onlyC"], venn_PS["AC"], venn_PS["BC"], venn_PS["ABC"]),
    set_labels=("BLAST", "MMseqs2", "ProteinSage"),
    ax=ax_j
)
colors3 = (lighten_color("#BFBFBF", 0.10), lighten_color("#C9D7E6", 0.10), lighten_color(C_A_STRUCT, 0.10))
for pid, col in zip(["100", "010", "001"], colors3):
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
    subsets=(venn_PS["onlyA"], venn_PS["onlyB"], venn_PS["AB"],
             venn_PS["onlyC"], venn_PS["AC"], venn_PS["BC"], venn_PS["ABC"]),
    ax=ax_j
)
_style_venn_common(v, circles)
ax_j.set_axis_off()
plt.tight_layout()
fig_j.savefig("fig5_j_venn_proteinsage.png", dpi=600, transparent=True)
plt.close()

# =========================
# 子图 (k) - Venn3 ESM-2
# =========================
fig_k, ax_k = plt.subplots(figsize=(90/25.4, 80/25.4))
v = venn3(
    subsets=(venn_ESM["onlyA"], venn_ESM["onlyB"], venn_ESM["AB"],
             venn_ESM["onlyC"], venn_ESM["AC"], venn_ESM["BC"], venn_ESM["ABC"]),
    set_labels=("BLAST", "MMseqs2", "ESM-2"),
    ax=ax_k
)
colors3 = (lighten_color("#BFBFBF", 0.10), lighten_color("#C9D7E6", 0.10), lighten_color(C_B_STRUCT, 0.10))
for pid, col in zip(["100", "010", "001"], colors3):
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
    subsets=(venn_ESM["onlyA"], venn_ESM["onlyB"], venn_ESM["AB"],
             venn_ESM["onlyC"], venn_ESM["AC"], venn_ESM["BC"], venn_ESM["ABC"]),
    ax=ax_k
)
_style_venn_common(v, circles)
ax_k.set_axis_off()
plt.tight_layout()
fig_k.savefig("fig5_k_venn_esm2.png", dpi=600, transparent=True)
plt.close()

# =========================
# 子图 (l) - Venn2 对比
# =========================
fig_l, ax_l = plt.subplots(figsize=(90/25.4, 80/25.4))
v = venn2(subsets=(PS_only, ESM_only, PS_ESM_inter),
          set_labels=("ProteinSage", "ESM-2"), ax=ax_l)
colors2 = (lighten_color(C_A_STRUCT, 0.10), lighten_color(C_B_STRUCT, 0.10))
for pid, col in zip(["10", "01"], colors2):
    p = v.get_patch_by_id(pid)
    if p:
        p.set_color(col)
        p.set_alpha(0.35)
        p.set_edgecolor("none")
p = v.get_patch_by_id("11")
if p:
    p.set_alpha(0.22)
    p.set_edgecolor("none")
circles = venn2_circles(subsets=(PS_only, ESM_only, PS_ESM_inter), ax=ax_l)
_style_venn_common(v, circles)
ax_l.set_axis_off()
plt.tight_layout()
fig_l.savefig("fig5_l_venn_comparison.png", dpi=600, transparent=True)
plt.close()

print("所有子图已保存:")
print("  fig5_a_accuracy.png - 准确率对比")
print("  fig5_b_f1score.png - F1分数对比")
print("  fig5_c_precision.png - 精确率对比")
print("  fig5_d_recall.png - 召回率对比")
print("  fig5_e_threshold_comparison.png - 阈值分析（双轴）")
print("  fig5_f_tm_ratio.png - TM>0比例曲线")
print("  fig5_g_7tm_ratio.png - 7TM比例曲线")
print("  fig5_h_pie_proteinsage.png - ProteinSage分类饼图")
print("  fig5_i_pie_esm2.png - ESM-2分类饼图")
print("  fig5_j_venn_proteinsage.png - ProteinSage Venn图（BLAST/MMseqs2）")
print("  fig5_k_venn_esm2.png - ESM-2 Venn图（BLAST/MMseqs2）")
print("  fig5_l_venn_comparison.png - ProteinSage vs ESM-2 Venn对比")