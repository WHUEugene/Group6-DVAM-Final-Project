import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib as mpl

# ========== Nature 正刊 · 统一样式 ==========
def _mm(x):  # 毫米→英寸
    return x / 25.4

BASE_FONTSIZE  = 7.0
SMALL_FONTSIZE = 6.5

NATURE_RC = {
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
    "grid.linestyle": "--",
    "grid.linewidth": 0.5,
    "grid.alpha": 0.25,
    "savefig.dpi": 600,
    "figure.dpi": 200,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.unicode_minus": False,
}
mpl.rcParams.update(NATURE_RC)

def set_y_headroom(ax, values, bottom=0.0, headroom=0.18):
    """把 y 轴上限设置为 max(values)*(1+headroom)，下限为 bottom。"""
    vmax = float(np.max(values)) if len(values) else 1.0
    ax.set_ylim(bottom, vmax * (1.0 + headroom))

# ---------------------- Data ----------------------
# Panel (a) Development
models_t1 = ["<1B", "7B", "13B"]
carbon_t1 = [8, 55, 76]     # tCO2e
water_t1  = [24, 252, 402]  # kL
x = np.arange(len(models_t1))
width = 0.35

# Panel (b) Training
models_t2 = ["60M", "150M", "300M", "700M", "1B (3T)"]
carbon_t2 = [0.4, 1.0, 2.0, 3.0, 10.0]
water_t2  = [1.8, 3.9, 6.2, 12.0, 42.0]
size_scale = 80
sizes_t2 = [(c + w) * size_scale for c, w in zip(carbon_t2, water_t2)]

# Panel (c) CoE 资源
models_t3 = ["ESM-C (600M)", "PGLM (1B)", "ProteinSage(650M)"]
tokens_t3 = [5.2, 1.0, 0.5]    # y: Training Tokens (T)
data_b3   = [2.4, 0.64, 0.14] # x: Data Size (B seqs)
size_scale3 = 600
sizes_t3 = [(t + d) * size_scale3 for t, d in zip(tokens_t3, data_b3)]

# =========================
# 子图 (a) - Development Phase
# =========================
fig_a, ax1 = plt.subplots(figsize=(_mm(60), _mm(55)))

color_carbon_soft = "#F9C7B8"  # 淡珊瑚
color_water_soft  = "#CFE7F3"  # 淡蓝

bar1 = ax1.bar(x - width/2, carbon_t1, width,
               label='Carbon Emissions (tCO2e)',
               color=color_carbon_soft, edgecolor="black", linewidth=0.6, zorder=2)
bar2 = ax1.bar(x + width/2, water_t1, width,
               label='Water Consumption (kL)',
               color=color_water_soft, edgecolor="black", linewidth=0.6, zorder=2)

# 数值标注
for bars in (bar1, bar2):
    for b in bars:
        h = b.get_height()
        ax1.annotate(f'{h}', (b.get_x() + b.get_width()/2, h),
                     xytext=(0, 1.5), textcoords="offset points",
                     ha='center', va='bottom', fontsize=SMALL_FONTSIZE, clip_on=True)

ax1.set_xlabel("Model Scale")
ax1.set_ylabel("Environmental Impact")
ax1.set_title("Development Phase", pad=2)
ax1.set_xticks(x, models_t1)
ax1.grid(axis='y', linestyle='--', alpha=0.35)
ax1.legend(frameon=False, loc="upper left")

# Y轴留白
set_y_headroom(ax1, values=np.r_[carbon_t1, water_t1], bottom=0.0, headroom=0.18)

# Panel标签
ax1.text(-0.10, 1.03, "(a)", transform=ax1.transAxes,
         ha="left", va="bottom", fontsize=8, fontweight="bold")

plt.tight_layout()
fig_a.savefig("fig_a_development.png", dpi=600, transparent=True, bbox_inches="tight")
plt.close()

# =========================
# 子图 (b) - Training Phase
# =========================
fig_b, ax2 = plt.subplots(figsize=(_mm(60), _mm(55)))

vals = np.linspace(0, 1, len(models_t2))
cmap = plt.get_cmap("Spectral")
colors_bubble = [cmap(v) for v in vals]

ax2.scatter(
    carbon_t2, water_t2,
    s=sizes_t2, alpha=0.85,
    c=vals, cmap=cmap,
    edgecolors="black", linewidth=0.7, marker="o", zorder=2
)
ax2.set_xlabel("Carbon Emissions (tCO2e)")
ax2.set_ylabel("Water Consumption (kL)")
ax2.set_title("Training Phase", pad=2)
ax2.grid(True, linestyle="--", alpha=0.35)
ax2.set_xlim(0, max(carbon_t2) * 1.05)

# Y轴留白
set_y_headroom(ax2, values=water_t2, bottom=0.0, headroom=0.18)

# 图例
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label=label,
           markerfacecolor=c, markeredgecolor='black', markersize=6.5)
    for label, c in zip(models_t2, colors_bubble)
]
ax2.legend(handles=legend_elements, title="Models", frameon=False, loc='upper left')

# Panel标签
ax2.text(-0.10, 1.03, "(b)", transform=ax2.transAxes,
         ha="left", va="bottom", fontsize=8, fontweight="bold")

plt.tight_layout()
fig_b.savefig("fig_b_training.png", dpi=600, transparent=True, bbox_inches="tight")
plt.close()

# =========================
# 子图 (c) - Reduction in Training Resources
# =========================
fig_c, ax3 = plt.subplots(figsize=(_mm(60), _mm(55)))

cmap3 = plt.get_cmap("viridis")
vals3 = np.linspace(0, 1, len(models_t3))
colors_bubble3 = [cmap3(v) for v in vals3]

ax3.scatter(
    data_b3, tokens_t3,
    s=sizes_t3, alpha=0.85,
    c=vals3, cmap=cmap3,
    edgecolors="black", linewidth=0.7, marker="o", zorder=2
)
ax3.set_xlabel("Data Size (B sequences)")
ax3.set_ylabel("Training Tokens (T)")
ax3.set_title("Reduction in Training Resources", pad=2)
ax3.grid(True, linestyle="--", alpha=0.35)
ax3.set_xlim(0, max(data_b3) * 1.10)

# Y轴留白
set_y_headroom(ax3, values=tokens_t3, bottom=0.0, headroom=0.18)

# 图例（左上角留出空隙，左对齐）
legend_elements3 = [
    Line2D([0], [0], marker='o', color='w', label=label,
           markerfacecolor=c, markeredgecolor='black', markersize=6.5)
    for label, c in zip(models_t3, colors_bubble3)
]

lg3 = ax3.legend(
    handles=legend_elements3, title="Models", frameon=False,
    loc='upper left',
    bbox_to_anchor=(0.01, 0.97),
    borderaxespad=0.0,
    handlelength=1.4, handletextpad=0.6, columnspacing=0.8
)
try:
    lg3._legend_box.align = "left"
except Exception:
    pass

# Panel标签
ax3.text(-0.10, 1.03, "(c)", transform=ax3.transAxes,
         ha="left", va="bottom", fontsize=8, fontweight="bold")

plt.tight_layout()
fig_c.savefig("fig_c_coe_resources.png", dpi=600, transparent=True, bbox_inches="tight")
plt.close()

print("所有子图已保存:")
print("  fig_a_development.png - Development Phase (分组柱状图)")
print("  fig_b_training.png - Training Phase (气泡图)")
print("  fig_c_coe_resources.png - Reduction in Training Resources (气泡图)")