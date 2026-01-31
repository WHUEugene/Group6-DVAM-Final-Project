# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib as mpl

# ========== Nature 正刊 · 统一样式 ==========
def _mm(x):  # 毫米→英寸
    return x / 25.4

FIGWIDTH_DOUBLE = _mm(183)  # 双栏宽
MAX_HEIGHT      = _mm(170)

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

def fig_size_double(height_mm=55):
    return (FIGWIDTH_DOUBLE, min(MAX_HEIGHT, _mm(height_mm)))

# ---- 统一的“顶部留白”工具 ----
def set_y_headroom(ax, values, bottom=0.0, headroom=0.18):
    """把 y 轴上限设置为 max(values)*(1+headroom)，下限为 bottom。"""
    vmax = float(np.max(values)) if len(values) else 1.0
    ax.set_ylim(bottom, vmax * (1.0 + headroom))

# ---------------------- Data ----------------------
# Panel (a) Development（保持结构，颜色调淡）
models_t1 = ["<1B", "7B", "13B"]
carbon_t1 = [6, 65, 46]     # tCO2e
water_t1  = [24, 252, 402]  # kL
x = np.arange(len(models_t1))
width = 0.35

# Panel (b) Training（保持不变）
models_t2 = ["60M", "150M", "300M", "700M", "1B (3T)"]
carbon_t2 = [0.4, 1.0, 2.0, 3.0, 10.0]
water_t2  = [1.6, 3.6, 5.9, 10.0, 39.0]
size_scale = 80
sizes_t2 = [(c + w) * size_scale for c, w in zip(carbon_t2, water_t2)]

# Panel (c) CoE 资源（保持不变）
models_t3 = ["ESM-C (600M)", "PGLM (1B)", "ProteinSage(650M)"]
tokens_t3 = [6.2, 1.0, 0.5]    # y: Training Tokens (T)
data_b3   = [2.5, 0.94, 0.214] # x: Data Size (B seqs)
size_scale3 = 600
sizes_t3 = [(t + d) * size_scale3 for t, d in zip(tokens_t3, data_b3)]

# ---------------------- Figure ----------------------
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=fig_size_double(55))

# ===== (a) Development：分组柱（仅此图颜色调淡） =====
color_carbon_soft = "#F9C7B8"  # 淡珊瑚
color_water_soft  = "#CFE7F3"  # 淡蓝

bar1 = ax1.bar(x - width/2, carbon_t1, width,
               label='Carbon Emissions (tCO₂e)',
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

# 给 (a) 的 y 轴添加 10% 顶部留白
set_y_headroom(ax1, values=np.r_[carbon_t1, water_t1], bottom=0.0, headroom=0.18)

# ===== (b) Training：气泡图（颜色保持不变） =====
vals = np.linspace(0, 1, len(models_t2))
cmap = plt.get_cmap("Spectral")
colors_bubble = [cmap(v) for v in vals]

ax2.scatter(
    carbon_t2, water_t2,
    s=sizes_t2, alpha=0.85,
    c=vals, cmap=cmap,
    edgecolors="black", linewidth=0.7, marker="o", zorder=2
)
ax2.set_xlabel("Carbon Emissions (tCO₂e)")
ax2.set_ylabel("Water Consumption (kL)")
ax2.set_title("Training Phase", pad=2)
ax2.grid(True, linestyle="--", alpha=0.35)
ax2.set_xlim(0, max(carbon_t2) * 1.05)  # x 轴轻微留白

# 给 (b) 的 y 轴添加 10% 顶部留白（由数据决定上限）
set_y_headroom(ax2, values=water_t2, bottom=0.0, headroom=0.18)

legend_elements = [
    Line2D([0], [0], marker='o', color='w', label=label,
           markerfacecolor=c, markeredgecolor='black', markersize=6.5)
    for label, c in zip(models_t2, colors_bubble)
]
ax2.legend(handles=legend_elements, title="Models", frameon=False, loc='upper left')

# ===== (c) CoE 资源：气泡图（颜色保持不变） =====
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
ax3.set_xlim(0, max(data_b3) * 1.10)    # x 轴轻微留白

# 给 (c) 的 y 轴添加 10% 顶部留白
set_y_headroom(ax3, values=tokens_t3, bottom=0.0, headroom=0.18)

legend_elements3 = [
    Line2D([0], [0], marker='o', color='w', label=label,
           markerfacecolor=c, markeredgecolor='black', markersize=6.5)
    for label, c in zip(models_t3, colors_bubble3)
]

# —— 图 (c) 的图例：左上角但留出空隙，并保持左对齐
lg3 = ax3.legend(
    handles=legend_elements3, title="Models", frameon=False,
    loc='upper left',
    bbox_to_anchor=(0.01, 0.97),   # ← 左/上各留 ~3% / 3% 的空隙
    borderaxespad=0.0,
    handlelength=1.4, handletextpad=0.6, columnspacing=0.8
)
try:
    lg3._legend_box.align = "left"  # 强制文本左对齐（老版本 Matplotlib 无此属性会自动跳过）
except Exception:
    pass


# ===== Panel 标签 =====
for ax, lab in zip((ax1, ax2, ax3), ["(a)", "(b)", "(c)"]):
    ax.text(-0.10, 1.03, lab, transform=ax.transAxes,
            ha="left", va="bottom", fontsize=8, fontweight="bold")

# 布局
plt.subplots_adjust(top=0.91, bottom=0.14, left=0.07, right=0.995, wspace=0.36)

# 保存
out_png = "/nfs_baoding/kubeflow-user/lingdong_2024/pic_nature/pic_result/combined_dev_train_coe_new.png"
out_pdf = "/nfs_baoding/kubeflow-user/lingdong_2024/pic_nature/pic_result/combined_dev_train_coe_new.pdf"
plt.savefig(out_png, bbox_inches="tight")
plt.savefig(out_pdf, bbox_inches="tight")
plt.show()
