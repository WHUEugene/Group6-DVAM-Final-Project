# # -*- coding: utf-8 -*-
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# from matplotlib.patches import Patch
# import matplotlib.colors as mcolors

# def _mm(x): return x / 25.4

# # =========================
# # Style
# # =========================
# BASE_FONTSIZE = 12.0
# SMALL_FONTSIZE = 10.0

# mpl.rcParams.update({
#     "font.family": "sans-serif",
#     "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
#     "font.size": BASE_FONTSIZE,
#     "axes.labelsize": BASE_FONTSIZE,
#     "axes.titlesize": BASE_FONTSIZE,
#     "legend.fontsize": SMALL_FONTSIZE,
#     "xtick.labelsize": SMALL_FONTSIZE,
#     "ytick.labelsize": SMALL_FONTSIZE,
#     "axes.linewidth": 0.6,
#     "lines.linewidth": 1.0,
#     "patch.linewidth": 0.6,
#     "xtick.direction": "in",
#     "ytick.direction": "in",
#     "xtick.top": True,
#     "ytick.right": True,
#     "xtick.major.size": 3.0,
#     "ytick.major.size": 3.0,
#     "grid.linestyle": "--",
#     "grid.linewidth": 0.5,
#     "grid.alpha": 0.25,
#     "savefig.dpi": 600,
#     "figure.dpi": 200,
#     "pdf.fonttype": 42,
#     "ps.fonttype": 42,
#     "axes.unicode_minus": False,
# })

# palette = {
#     "ProteinSage": "#F7C98B",
#     "ESM-2": "#9FBAD5",
#     "cnn": "#F5B8B5",
#     "transformer": "#B7D5C0",
#     "attention": "#C7DCA7",
#     "LSTM": "#9C73A7",
# }
# EDGE_TOTAL = "#3A3A3A"

# def lighten_color(hex_color, amount=0.62):
#     rgb = np.array(mcolors.to_rgb(hex_color))
#     white = np.array([1, 1, 1])
#     return mcolors.to_hex(rgb + (white - rgb) * amount)

# # =========================
# # Data: abcd
# # =========================
# models = ["ProteinSage", "ESM-2", "cnn", "transformer", "attention", "LSTM"]
# data = {
#     "ProteinSage": dict(test_accuracy=0.9956268072128296,
#                         test_f1=0.9882168173789978,
#                         test_precision=0.9889937043190002,
#                         test_recall=0.9874411225318909),
#     "ESM-2":       dict(test_accuracy=0.9904091954231262,
#                         test_f1=0.9765258431434631,
#                         test_precision=0.9659442901611328,
#                         test_recall=0.9873417615890503),
#     "cnn":         dict(test_accuracy=0.9857142857142858,
#                         test_f1=0.9609561752988047,
#                         test_precision=0.9757281553398058,
#                         test_recall=0.9466248037676609),
#     "transformer": dict(test_accuracy=0.9734693877551021,
#                         test_f1=0.9299461123941493,
#                         test_precision=0.9123867069486404,
#                         test_recall=0.9481946624803768),
#     "attention":   dict(test_accuracy=0.9848396501457726,
#                         test_f1=0.9589905362776026,
#                         test_precision=0.9635499207606973,
#                         test_recall=0.9544740973312402),
#     "LSTM":        dict(test_accuracy=0.9723032069970845,
#                         test_f1=0.9224489795918367,
#                         test_precision=0.9608843537414966,
#                         test_recall=0.8869701726844584),
# }
# metrics = ["test_accuracy", "test_f1", "test_precision", "test_recall"]
# titles  = ["Accuracy", "F1-score", "Precision", "Recall"]
# panel_ids = ["(a)", "(b)", "(c)", "(d)"]

# def soft_grid(ax):
#     ax.yaxis.grid(True, linestyle="--", linewidth=0.6, alpha=0.28)
#     ax.set_axisbelow(True)

# def set_adaptive_ylim(ax, values):
#     vmin, vmax = min(values), max(values)
#     span = vmax - vmin if vmax > vmin else 0.01
#     ax.set_ylim(max(0.88, vmin - span*0.15), 1.00)

# def add_bar_labels(ax, xs, heights, fontsize=7.1):
#     for x, v in zip(xs, heights):
#         ax.text(x, v + 0.002, f"{v:.4f}",
#                 ha="center", va="bottom",
#                 fontsize=fontsize, clip_on=False)

# # =========================
# # Data: e
# # =========================
# thresholds = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 0.95])
# total_A  = np.array([4202, 3389, 2916, 2646, 2401, 2210])
# struct_A = np.array([2343, 2322, 2297, 2261, 2151, 2029])
# total_B  = np.array([6382, 4712, 3932, 3178, 2832, 2509])
# struct_B = np.array([2984, 2804, 2711, 2539, 2318, 2194])

# ratio_A = struct_A / total_A
# ratio_B = struct_B / total_B

# C_A_STRUCT = palette["ProteinSage"]
# C_B_STRUCT = palette["ESM-2"]
# C_A_TOTAL  = lighten_color(C_A_STRUCT)
# C_B_TOTAL  = lighten_color(C_B_STRUCT)

# # =========================
# # Figure layout:
# # - abcd height reduced WITHOUT affecting e:
# #   outer is 2 rows × 2 cols, e spans both rows
# # =========================
# fig = plt.figure(figsize=(_mm(340), _mm(200)))
# outer = fig.add_gridspec(
#     2, 2,
#     width_ratios=[2, 1],
#     height_ratios=[0.09, 0.91],   # make abcd (bottom row) shorter/taller by tuning these
#     wspace=0.14,
#     hspace=0.00
# )

# # ---------- Left: abcd ONLY in bottom row (outer[1,0])
# gsL = outer[1, 0].subgridspec(2, 2, wspace=0.22, hspace=0.25)
# axesL = np.array([fig.add_subplot(gsL[i, j]) for i in range(2) for j in range(2)])

# xs = np.arange(len(models))
# colors = [palette[m] for m in models]

# for i, (ax, met, title) in enumerate(zip(axesL, metrics, titles)):
#     vals = [data[m][met] for m in models]
#     ax.bar(xs, vals, width=0.72, color=colors, edgecolor="black", linewidth=0.9)
#     set_adaptive_ylim(ax, vals)
#     add_bar_labels(ax, xs, vals)

#     if i < 2:
#         ax.set_xticklabels([])
#     else:
#         ax.set_xticks(xs, models, rotation=35, ha="right")

#     ax.set_title(title)
#     ax.set_ylabel(title)
#     soft_grid(ax)

#     ax.text(0.00, 1.03, panel_ids[i],
#             transform=ax.transAxes, ha="left", va="bottom",
#             fontsize=11.2, fontweight="bold", clip_on=False)

# # ---------- Right: e spans BOTH rows (outer[:,1]) -> e unaffected
# gsR = outer[:, 1].subgridspec(2, 1, height_ratios=[0.16, 0.84], hspace=0.00)

# ax_leg = fig.add_subplot(gsR[0, 0])
# ax_leg.axis("off")
# legend_handles = [
#     Patch(facecolor=C_A_TOTAL,  edgecolor=EDGE_TOTAL, label="Total (ProteinSage)"),
#     Patch(facecolor=C_A_STRUCT, edgecolor="white",    label="Structure (ProteinSage)"),
#     Patch(facecolor=C_B_TOTAL,  edgecolor=EDGE_TOTAL, label="Total (ESM-2)"),
#     Patch(facecolor=C_B_STRUCT, edgecolor="white",    label="Structure (ESM-2)"),
# ]
# ax_leg.legend(handles=legend_handles, loc="center", ncol=2, frameon=False,
#               handletextpad=0.6, columnspacing=1.4, labelspacing=0.7)

# gsE = gsR[1, 0].subgridspec(1, 2, width_ratios=[0.72, 0.28], wspace=0.10)
# ax_e = fig.add_subplot(gsE[0, 0])
# ax_r = fig.add_subplot(gsE[0, 1], sharey=ax_e)

# # y layout
# pair_sep, group_gap = 0.34, 0.55
# bar_h_total, bar_h_struct = 0.30, 0.18
# ypos, meta, y = [], [], 0.0
# for i in range(len(thresholds)):
#     ypos += [y, y + pair_sep]
#     meta += [(i, "A"), (i, "B")]
#     y += pair_sep + group_gap
# ypos = np.array(ypos)

# # prevent top-edge clipping (0.95 line)
# ax_e.set_ylim(-0.45, ypos.max() + bar_h_total)

# max_w = max(total_A.max(), total_B.max())

# def draw_row(yy, total, struct, c_total, c_struct):
#     ax_e.barh(yy, total, height=bar_h_total, color=c_total,
#               edgecolor=EDGE_TOTAL, linewidth=0.7, zorder=1, clip_on=False)
#     ax_e.barh(yy, struct, height=bar_h_struct, color=c_struct,
#               edgecolor="white", linewidth=0.9, zorder=2, clip_on=False)

# for yy, (i, m) in zip(ypos, meta):
#     if m == "A":
#         draw_row(yy, total_A[i], struct_A[i], C_A_TOTAL, C_A_STRUCT)
#     else:
#         draw_row(yy, total_B[i], struct_B[i], C_B_TOTAL, C_B_STRUCT)

# ax_e.set_xlim(0, max_w * 1.06)
# ax_e.set_xlabel("Predicted count")
# ax_e.set_ylabel("Prediction threshold")
# ax_e.spines["top"].set_visible(False)
# ax_e.spines["right"].set_visible(False)
# yticks = [(ypos[2*i] + ypos[2*i+1]) / 2 for i in range(len(thresholds))]
# ax_e.set_yticks(yticks, [f"{t:g}" for t in thresholds])

# # ratio dots
# ratio_vals = np.array([ratio_A[i] if m == "A" else ratio_B[i] for (i, m) in meta])
# tags = np.array([m for (_, m) in meta])

# ax_r.set_xlabel("Structure ratio\n(structure/total)", fontsize=SMALL_FONTSIZE)
# ax_r.xaxis.labelpad = 3.0
# ax_r.spines["top"].set_visible(False)
# ax_r.spines["right"].set_visible(False)
# ax_r.spines["left"].set_visible(False)
# ax_r.tick_params(left=False, labelleft=False)

# ax_r.set_xlim(0.0, 1.0)
# ax_r.set_xticks([0.0, 0.5, 1.0])
# ax_r.set_xticklabels(["0.00", "0.50", "1.00"], fontsize=8.6)

# ms = 5.2
# maskA = tags == "A"
# ax_r.scatter(ratio_vals[maskA], ypos[maskA], s=ms**2, color=C_A_STRUCT,
#              edgecolors="white", linewidths=0.9, zorder=5)
# ax_r.scatter(ratio_vals[~maskA], ypos[~maskA], s=ms**2, color=C_B_STRUCT,
#              edgecolors="white", linewidths=0.9, zorder=5)

# for a in (ax_e, ax_r):
#     a.tick_params(axis="x", which="both", bottom=True, top=False, length=3.0)
#     a.tick_params(axis="y", which="both", length=0)
#     a.xaxis.set_ticks_position("bottom")

# # =========================
# # (e) label alignment with (a)(b) + only e higher
# # =========================
# fig.canvas.draw()
# bb_a = axesL[0].get_position()
# bb_b = axesL[1].get_position()
# bb_e = ax_e.get_position()
# y_align = max(bb_a.y1, bb_b.y1) + 0.004

# E_LABEL_OFFSET = 0.1
# fig.text(bb_e.x0, y_align + E_LABEL_OFFSET, "(e)",
#          fontsize=11.2, fontweight="bold",
#          ha="left", va="bottom")

# plt.subplots_adjust(left=0.06, right=0.975, top=0.965, bottom=0.18)
# plt.show()

# fig.savefig("/nfs_baoding/kubeflow-user/lingdong_2024/pic_nature/pic_result/fig5_merged.pdf", dpi=600)
# fig.savefig("/nfs_baoding/kubeflow-user/lingdong_2024/pic_nature/pic_result/fig5_merged.png",
#             dpi=600, transparent=True)
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# # -*- coding: utf-8 -*-
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# from matplotlib.patches import Patch
# import matplotlib.colors as mcolors

# def _mm(x): return x / 25.4

# # =========================
# # Style
# # =========================
# BASE_FONTSIZE = 12.0
# SMALL_FONTSIZE = 10.0

# mpl.rcParams.update({
#     "font.family": "sans-serif",
#     "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
#     "font.size": BASE_FONTSIZE,
#     "axes.labelsize": BASE_FONTSIZE,
#     "axes.titlesize": BASE_FONTSIZE,
#     "legend.fontsize": SMALL_FONTSIZE,
#     "xtick.labelsize": SMALL_FONTSIZE,
#     "ytick.labelsize": SMALL_FONTSIZE,
#     "axes.linewidth": 0.6,
#     "lines.linewidth": 1.0,
#     "patch.linewidth": 0.6,
#     "xtick.direction": "in",
#     "ytick.direction": "in",
#     "xtick.top": True,
#     "ytick.right": True,
#     "xtick.major.size": 3.0,
#     "ytick.major.size": 3.0,
#     "grid.linestyle": "--",
#     "grid.linewidth": 0.5,
#     "grid.alpha": 0.25,
#     "savefig.dpi": 600,
#     "figure.dpi": 200,
#     "pdf.fonttype": 42,
#     "ps.fonttype": 42,
#     "axes.unicode_minus": False,
# })

# palette = {
#     "ProteinSage": "#F7C98B",
#     "ESM-2": "#9FBAD5",
#     "cnn": "#F5B8B5",
#     "transformer": "#B7D5C0",
#     "attention": "#C7DCA7",
#     "LSTM": "#9C73A7",
# }
# EDGE_TOTAL = "#3A3A3A"

# def lighten_color(hex_color, amount=0.62):
#     rgb = np.array(mcolors.to_rgb(hex_color))
#     white = np.array([1, 1, 1])
#     return mcolors.to_hex(rgb + (white - rgb) * amount)

# # =========================
# # Data: abcd
# # =========================
# models = ["ProteinSage", "ESM-2", "cnn", "transformer", "attention", "LSTM"]
# data = {
#     "ProteinSage": dict(test_accuracy=0.9956268072128296,
#                         test_f1=0.9882168173789978,
#                         test_precision=0.9889937043190002,
#                         test_recall=0.9874411225318909),
#     "ESM-2":       dict(test_accuracy=0.9904091954231262,
#                         test_f1=0.9765258431434631,
#                         test_precision=0.9659442901611328,
#                         test_recall=0.9873417615890503),
#     "cnn":         dict(test_accuracy=0.9857142857142858,
#                         test_f1=0.9609561752988047,
#                         test_precision=0.9757281553398058,
#                         test_recall=0.9466248037676609),
#     "transformer": dict(test_accuracy=0.9734693877551021,
#                         test_f1=0.9299461123941493,
#                         test_precision=0.9123867069486404,
#                         test_recall=0.9481946624803768),
#     "attention":   dict(test_accuracy=0.9848396501457726,
#                         test_f1=0.9589905362776026,
#                         test_precision=0.9635499207606973,
#                         test_recall=0.9544740973312402),
#     "LSTM":        dict(test_accuracy=0.9723032069970845,
#                         test_f1=0.9224489795918367,
#                         test_precision=0.9608843537414966,
#                         test_recall=0.8869701726844584),
# }
# metrics = ["test_accuracy", "test_f1", "test_precision", "test_recall"]
# titles  = ["Accuracy", "F1-score", "Precision", "Recall"]
# panel_ids = ["(a)", "(b)", "(c)", "(d)"]

# def soft_grid(ax):
#     ax.yaxis.grid(True, linestyle="--", linewidth=0.6, alpha=0.28)
#     ax.set_axisbelow(True)

# def set_adaptive_ylim(ax, values):
#     vmin, vmax = min(values), max(values)
#     span = vmax - vmin if vmax > vmin else 0.01
#     ax.set_ylim(max(0.88, vmin - span*0.15), 1.00)

# def add_bar_labels(ax, xs, heights, fontsize=7.1):
#     for x, v in zip(xs, heights):
#         ax.text(x, v + 0.002, f"{v:.4f}",
#                 ha="center", va="bottom",
#                 fontsize=fontsize, clip_on=False)

# # =========================
# # Data: e
# # =========================
# thresholds = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 0.95])
# total_A  = np.array([4202, 3389, 2916, 2646, 2401, 2210])
# struct_A = np.array([2343, 2322, 2297, 2261, 2151, 2029])
# total_B  = np.array([6382, 4712, 3932, 3178, 2832, 2509])
# struct_B = np.array([2984, 2804, 2711, 2539, 2318, 2194])

# ratio_A = struct_A / total_A
# ratio_B = struct_B / total_B

# C_A_STRUCT = palette["ProteinSage"]
# C_B_STRUCT = palette["ESM-2"]
# C_A_TOTAL  = lighten_color(C_A_STRUCT)
# C_B_TOTAL  = lighten_color(C_B_STRUCT)

# # =========================
# # Figure layout:
# # - abcd height reduced WITHOUT affecting e:
# #   outer is 2 rows × 2 cols, e spans both rows
# # =========================
# fig = plt.figure(figsize=(_mm(340), _mm(200)))
# outer = fig.add_gridspec(
#     2, 2,
#     width_ratios=[2, 1],
#     height_ratios=[0.09, 0.91],   # make abcd (bottom row) shorter/taller by tuning these
#     wspace=0.14,
#     hspace=0.00
# )

# # ---------- Left: abcd ONLY in bottom row (outer[1,0])
# gsL = outer[1, 0].subgridspec(2, 2, wspace=0.22, hspace=0.25)
# axesL = np.array([fig.add_subplot(gsL[i, j]) for i in range(2) for j in range(2)])

# xs = np.arange(len(models))
# colors = [palette[m] for m in models]

# for i, (ax, met, title) in enumerate(zip(axesL, metrics, titles)):
#     vals = [data[m][met] for m in models]
#     ax.bar(xs, vals, width=0.72, color=colors, edgecolor="black", linewidth=0.9)
#     set_adaptive_ylim(ax, vals)
#     add_bar_labels(ax, xs, vals)

#     if i < 2:
#         ax.set_xticklabels([])
#     else:
#         ax.set_xticks(xs, models, rotation=35, ha="right")

#     ax.set_title(title)
#     ax.set_ylabel(title)
#     soft_grid(ax)

#     ax.text(0.00, 1.03, panel_ids[i],
#             transform=ax.transAxes, ha="left", va="bottom",
#             fontsize=11.2, fontweight="bold", clip_on=False)

# # ---------- Right: e spans BOTH rows (outer[:,1]) -> e unaffected
# gsR = outer[:, 1].subgridspec(2, 1, height_ratios=[0.16, 0.84], hspace=0.00)

# ax_leg = fig.add_subplot(gsR[0, 0])
# ax_leg.axis("off")
# legend_handles = [
#     Patch(facecolor=C_A_TOTAL,  edgecolor=EDGE_TOTAL, label="Total (ProteinSage)"),
#     Patch(facecolor=C_A_STRUCT, edgecolor="white",    label="Structure (ProteinSage)"),
#     Patch(facecolor=C_B_TOTAL,  edgecolor=EDGE_TOTAL, label="Total (ESM-2)"),
#     Patch(facecolor=C_B_STRUCT, edgecolor="white",    label="Structure (ESM-2)"),
# ]
# ax_leg.legend(handles=legend_handles, loc="center", ncol=2, frameon=False,
#               handletextpad=0.6, columnspacing=1.4, labelspacing=0.7)

# gsE = gsR[1, 0].subgridspec(1, 2, width_ratios=[0.72, 0.28], wspace=0.10)
# ax_e = fig.add_subplot(gsE[0, 0])
# ax_r = fig.add_subplot(gsE[0, 1], sharey=ax_e)

# # y layout
# pair_sep, group_gap = 0.34, 0.55
# bar_h_total, bar_h_struct = 0.30, 0.18
# ypos, meta, y = [], [], 0.0
# for i in range(len(thresholds)):
#     ypos += [y, y + pair_sep]
#     meta += [(i, "A"), (i, "B")]
#     y += pair_sep + group_gap
# ypos = np.array(ypos)

# # prevent top-edge clipping (0.95 line)
# ax_e.set_ylim(-0.45, ypos.max() + bar_h_total)

# max_w = max(total_A.max(), total_B.max())

# def draw_row(yy, total, struct, c_total, c_struct):
#     ax_e.barh(yy, total, height=bar_h_total, color=c_total,
#               edgecolor=EDGE_TOTAL, linewidth=0.7, zorder=1, clip_on=False)
#     ax_e.barh(yy, struct, height=bar_h_struct, color=c_struct,
#               edgecolor="white", linewidth=0.9, zorder=2, clip_on=False)

# for yy, (i, m) in zip(ypos, meta):
#     if m == "A":
#         draw_row(yy, total_A[i], struct_A[i], C_A_TOTAL, C_A_STRUCT)
#     else:
#         draw_row(yy, total_B[i], struct_B[i], C_B_TOTAL, C_B_STRUCT)

# ax_e.set_xlim(0, max_w * 1.06)
# ax_e.set_xlabel("Predicted count")
# ax_e.set_ylabel("Prediction threshold")
# ax_e.spines["top"].set_visible(False)
# ax_e.spines["right"].set_visible(False)
# yticks = [(ypos[2*i] + ypos[2*i+1]) / 2 for i in range(len(thresholds))]
# ax_e.set_yticks(yticks, [f"{t:g}" for t in thresholds])

# # ratio dots
# ratio_vals = np.array([ratio_A[i] if m == "A" else ratio_B[i] for (i, m) in meta])
# tags = np.array([m for (_, m) in meta])

# ax_r.set_xlabel("Structure ratio\n(structure/total)", fontsize=SMALL_FONTSIZE)
# ax_r.xaxis.labelpad = 3.0
# ax_r.spines["top"].set_visible(False)
# ax_r.spines["right"].set_visible(False)
# ax_r.spines["left"].set_visible(False)
# ax_r.tick_params(left=False, labelleft=False)

# ax_r.set_xlim(0.0, 1.0)
# ax_r.set_xticks([0.0, 0.5, 1.0])
# ax_r.set_xticklabels(["0.00", "0.50", "1.00"], fontsize=8.6)

# ms = 5.2
# maskA = tags == "A"
# ax_r.scatter(ratio_vals[maskA], ypos[maskA], s=ms**2, color=C_A_STRUCT,
#              edgecolors="white", linewidths=0.9, zorder=5)
# ax_r.scatter(ratio_vals[~maskA], ypos[~maskA], s=ms**2, color=C_B_STRUCT,
#              edgecolors="white", linewidths=0.9, zorder=5)

# for a in (ax_e, ax_r):
#     a.tick_params(axis="x", which="both", bottom=True, top=False, length=3.0)
#     a.tick_params(axis="y", which="both", length=0)
#     a.xaxis.set_ticks_position("bottom")

# # =========================
# # (e) label alignment with (a)(b) + only e higher
# # =========================
# fig.canvas.draw()
# bb_a = axesL[0].get_position()
# bb_b = axesL[1].get_position()
# bb_e = ax_e.get_position()
# y_align = max(bb_a.y1, bb_b.y1) + 0.004

# E_LABEL_OFFSET = 0.1
# fig.text(bb_e.x0, y_align + E_LABEL_OFFSET, "(e)",
#          fontsize=11.2, fontweight="bold",
#          ha="left", va="bottom")

# plt.subplots_adjust(left=0.06, right=0.975, top=0.965, bottom=0.18)
# plt.show()

# fig.savefig("/nfs_baoding/kubeflow-user/lingdong_2024/pic_nature/pic_result/fig5_merged.pdf", dpi=600)
# fig.savefig("/nfs_baoding/kubeflow-user/lingdong_2024/pic_nature/pic_result/fig5_merged.png",
#             dpi=600, transparent=True)
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Patch
import matplotlib.colors as mcolors
from matplotlib_venn import venn3, venn2, venn3_circles, venn2_circles


# Venn
from matplotlib_venn import venn3, venn2

def _mm(x): return x / 25.4

# =========================
# Style
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
def _style_venn_common(v, circle_artists=None):
    # subset numbers
    if getattr(v, "subset_labels", None) is not None:
        for t in v.subset_labels:
            if t is None:
                continue
            t.set_fontsize(9.6)
            t.set_color("#222222")

    # set labels
    if getattr(v, "set_labels", None) is not None:
        for t in v.set_labels:
            if t is None:
                continue
            t.set_fontsize(9.6)
            t.set_color("#222222")
            t.set_fontweight("normal")

    # circle outlines
    if circle_artists is not None:
        for c in circle_artists:
            if c is None:
                continue
            c.set_lw(1.1)
            c.set_ls("-")
            c.set_edgecolor("#444444")
            c.set_alpha(0.85)


def draw_venn3_nature(ax, reg, labels, colors3, panel_label):
    # reg keys: onlyA, onlyB, AB, onlyC, AC, BC, ABC
    v = venn3(
        subsets=(reg["onlyA"], reg["onlyB"], reg["AB"],
                 reg["onlyC"], reg["AC"], reg["BC"], reg["ABC"]),
        set_labels=labels,
        ax=ax
    )

    # Fill style: light + clean, borders removed (use circles for borders)
    id_to_color = {"100": colors3[0], "010": colors3[1], "001": colors3[2]}
    for pid, col in id_to_color.items():
        p = v.get_patch_by_id(pid)
        if p is not None:
            p.set_color(col)
            p.set_alpha(0.35)
            p.set_edgecolor("none")

    # intersections a bit darker but still soft
    for pid in ["110", "101", "011", "111"]:
        p = v.get_patch_by_id(pid)
        if p is not None:
            p.set_alpha(0.22)
            p.set_edgecolor("none")

    # Crisp circle outlines
    circles = venn3_circles(
        subsets=(reg["onlyA"], reg["onlyB"], reg["AB"],
                 reg["onlyC"], reg["AC"], reg["BC"], reg["ABC"]),
        ax=ax
    )

    _style_venn_common(v, circles)

    # Panel label
    ax.text(-0.12, 1.06, panel_label,
            transform=ax.transAxes,
            ha="left", va="bottom",
            fontsize=11.2, fontweight="bold", clip_on=False)

    # Clean axes
    ax.set_axis_off()


def draw_venn2_nature(ax, a_only, b_only, ab, labels2, colors2, panel_label):
    v = venn2(subsets=(a_only, b_only, ab), set_labels=labels2, ax=ax)

    # fills
    p10 = v.get_patch_by_id("10")
    p01 = v.get_patch_by_id("01")
    p11 = v.get_patch_by_id("11")
    if p10 is not None:
        p10.set_color(colors2[0]); p10.set_alpha(0.35); p10.set_edgecolor("none")
    if p01 is not None:
        p01.set_color(colors2[1]); p01.set_alpha(0.35); p01.set_edgecolor("none")
    if p11 is not None:
        p11.set_alpha(0.22); p11.set_edgecolor("none")

    circles = venn2_circles(subsets=(a_only, b_only, ab), ax=ax)
    _style_venn_common(v, circles)

    ax.text(-0.12, 1.06, panel_label,
            transform=ax.transAxes,
            ha="left", va="bottom",
            fontsize=11.2, fontweight="bold", clip_on=False)

    ax.set_axis_off()

# =========================
# Data: abcd
# =========================
models = ["ProteinSage", "ESM-2", "cnn", "transformer", "attention", "LSTM"]
data = {
    "ProteinSage": dict(test_accuracy=0.9956268072128296,
                        test_f1=0.9882168173789978,
                        test_precision=0.9889937043190002,
                        test_recall=0.9874411225318909),
    "ESM-2":       dict(test_accuracy=0.9904091954231262,
                        test_f1=0.9765258431434631,
                        test_precision=0.9659442901611328,
                        test_recall=0.9873417615890503),
    "cnn":         dict(test_accuracy=0.9857142857142858,
                        test_f1=0.9609561752988047,
                        test_precision=0.9757281553398058,
                        test_recall=0.9466248037676609),
    "transformer": dict(test_accuracy=0.9734693877551021,
                        test_f1=0.9299461123941493,
                        test_precision=0.9123867069486404,
                        test_recall=0.9481946624803768),
    "attention":   dict(test_accuracy=0.9848396501457726,
                        test_f1=0.9589905362776026,
                        test_precision=0.9635499207606973,
                        test_recall=0.9544740973312402),
    "LSTM":        dict(test_accuracy=0.9723032069970845,
                        test_f1=0.9224489795918367,
                        test_precision=0.9608843537414966,
                        test_recall=0.8869701726844584),
}
metrics = ["test_accuracy", "test_f1", "test_precision", "test_recall"]
titles  = ["Accuracy", "F1-score", "Precision", "Recall"]
panel_ids = ["(a)", "(b)", "(c)", "(d)"]

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

# =========================
# Data: e
# =========================
thresholds = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 0.95])
total_A  = np.array([4202, 3389, 2916, 2646, 2401, 2210])
struct_A = np.array([2343, 2322, 2297, 2261, 2151, 2029])
total_B  = np.array([6382, 4712, 3932, 3178, 2832, 2509])
struct_B = np.array([2984, 2804, 2711, 2539, 2318, 2194])

ratio_A = struct_A / total_A
ratio_B = struct_B / total_B

C_A_STRUCT = palette["ProteinSage"]
C_B_STRUCT = palette["ESM-2"]
C_A_TOTAL  = lighten_color(C_A_STRUCT)
C_B_TOTAL  = lighten_color(C_B_STRUCT)

# =========================
# Data: f,g
# =========================
thr_line = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 0.95])

esm_col1 = np.array([0.7124725, 0.8026315, 0.8761440, 0.9018250, 0.9269060, 0.9465920])  # tm>0
esm_col2 = np.array([0.4675650, 0.5950760, 0.6894710, 0.7989300, 0.8185020, 0.8744510])  # 7tm
ps_col1  = np.array([0.6358880, 0.7789910, 0.8916320, 0.9561600, 0.9870890, 0.9945700])  # tm>0
ps_col2  = np.array([0.5575920, 0.6851580, 0.7877230, 0.8544970, 0.8958770, 0.9181000])  # 7tm

# =========================
# Pie data: h,i
# =========================
pie_h = {
    "BR": 2343 - 8 - 119,
    "Other": 119,
    "Unknown": 8,
}
pie_i = {
    "BR": 2984 - (79 + 258 + 71 + 83 + 102 + 443 + 152),
    "AU": 79,
    "BaxI_1": 258,
    "NrfD": 71,
    "Rcel-like": 83,
    "HeR": 102,
    "Other": 443,
    "Unknown": 152,
}

# =========================
# Venn region sizes from your output
# =========================
# BLAST / MMseqs2 / ProteinSage
venn_PS = dict(
    onlyA=124, onlyB=0,  AB=19,
    onlyC=538, AC=119,   BC=20,
    ABC=1539
)

# BLAST / MMseqs2 / ESM-2
venn_ESM = dict(
    onlyA=39, onlyB=15, AB=131,
    onlyC=160, AC=204,  BC=5,
    ABC=1427
)

# ProteinSage / ESM-2
PS_total = 2216
ESM_total = 1796
PS_ESM_inter = 1513
PS_only = PS_total - PS_ESM_inter
ESM_only = ESM_total - PS_ESM_inter

# =========================
# Figure layout: (Top) abcde | (Middle) fghi | (Bottom) jkl venns
# =========================
fig = plt.figure(figsize=(_mm(340), _mm(420)))

G = fig.add_gridspec(3, 1, height_ratios=[1.0, 1.0, 0.65], hspace=0.42)

# -------------------------
# TOP block: abcde (unchanged)
# -------------------------
top = G[0].subgridspec(2, 2, width_ratios=[2, 1], height_ratios=[0.09, 0.91],
                      wspace=0.14, hspace=0.00)

gsL = top[1, 0].subgridspec(2, 2, wspace=0.22, hspace=0.25)
axesL = np.array([fig.add_subplot(gsL[i, j]) for i in range(2) for j in range(2)])

xs = np.arange(len(models))
colors = [palette[m] for m in models]

for i, (ax, met, title) in enumerate(zip(axesL, metrics, titles)):
    vals = [data[m][met] for m in models]
    ax.bar(xs, vals, width=0.72, color=colors, edgecolor="black", linewidth=0.9)
    set_adaptive_ylim(ax, vals)
    add_bar_labels(ax, xs, vals)

    if i < 2:
        ax.set_xticklabels([])
    else:
        ax.set_xticks(xs, models, rotation=35, ha="right")

    ax.set_title(title)
    ax.set_ylabel(title)
    soft_grid(ax)

    ax.text(0.00, 1.03, panel_ids[i],
            transform=ax.transAxes, ha="left", va="bottom",
            fontsize=11.2, fontweight="bold", clip_on=False)

gsR = top[:, 1].subgridspec(2, 1, height_ratios=[0.16, 0.84], hspace=0.00)

ax_leg = fig.add_subplot(gsR[0, 0])
ax_leg.axis("off")
legend_handles = [
    Patch(facecolor=C_A_TOTAL,  edgecolor=EDGE_TOTAL, label="Total (ProteinSage)"),
    Patch(facecolor=C_A_STRUCT, edgecolor="white",    label="Structure (ProteinSage)"),
    Patch(facecolor=C_B_TOTAL,  edgecolor=EDGE_TOTAL, label="Total (ESM-2)"),
    Patch(facecolor=C_B_STRUCT, edgecolor="white",    label="Structure (ESM-2)"),
]
ax_leg.legend(handles=legend_handles, loc="center", ncol=2, frameon=False,
              handletextpad=0.6, columnspacing=1.4, labelspacing=0.7)

gsE = gsR[1, 0].subgridspec(1, 2, width_ratios=[0.72, 0.28], wspace=0.10)
ax_e = fig.add_subplot(gsE[0, 0])
ax_r = fig.add_subplot(gsE[0, 1], sharey=ax_e)

pair_sep, group_gap = 0.34, 0.55
bar_h_total, bar_h_struct = 0.30, 0.18
ypos, meta, y = [], [], 0.0
for i in range(len(thresholds)):
    ypos += [y, y + pair_sep]
    meta += [(i, "A"), (i, "B")]
    y += pair_sep + group_gap
ypos = np.array(ypos)
ax_e.set_ylim(-0.45, ypos.max() + bar_h_total)

max_w = max(total_A.max(), total_B.max())

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

ax_e.set_xlim(0, max_w * 1.06)
ax_e.set_xlabel("Predicted count")
ax_e.set_ylabel("Prediction threshold")
ax_e.spines["top"].set_visible(False)
ax_e.spines["right"].set_visible(False)

yticks = [(ypos[2*i] + ypos[2*i+1]) / 2 for i in range(len(thresholds))]
ax_e.set_yticks(yticks, [f"{t:g}" for t in thresholds])

delta_model = ratio_A - ratio_B
y_centers = np.array(yticks)

ax_r.set_xlabel("Δ structure ratio\n(ProteinSage − ESM-2)", fontsize=SMALL_FONTSIZE)
ax_r.xaxis.labelpad = 3.0
ax_r.spines["top"].set_visible(False)
ax_r.spines["right"].set_visible(False)
ax_r.spines["left"].set_visible(False)
ax_r.tick_params(left=False, labelleft=False)

max_abs = float(np.max(np.abs(delta_model))) if len(delta_model) else 0.1
pad = max_abs * 0.35 + 1e-6
ax_r.set_xlim(-max_abs - pad, max_abs + pad)

tick_max = max_abs if max_abs > 1e-6 else 0.05
ax_r.set_xticks([-tick_max, 0.0, tick_max])
ax_r.set_xticklabels([f"{-tick_max:.2f}", "0", f"{tick_max:.2f}"], fontsize=8.6)
ax_r.axvline(0.0, color="#555555", linewidth=0.8, linestyle="--", zorder=1)

colors_delta = np.where(delta_model >= 0, C_A_STRUCT, C_B_STRUCT)
ax_r.scatter(delta_model, y_centers, s=5.6**2, c=colors_delta,
             edgecolors="white", linewidths=0.9, zorder=5)

for a in (ax_e, ax_r):
    a.tick_params(axis="x", which="both", bottom=True, top=False, length=3.0)
    a.tick_params(axis="y", which="both", length=0)
    a.xaxis.set_ticks_position("bottom")

fig.canvas.draw()
bb_a = axesL[0].get_position()
bb_b = axesL[1].get_position()
bb_e = ax_e.get_position()
y_align = max(bb_a.y1, bb_b.y1) + 0.004
fig.text(bb_e.x0, y_align + 0.085, "(e)", fontsize=11.2, fontweight="bold",
         ha="left", va="bottom")

# -------------------------
# MIDDLE block: fghi (keep your current layout)
# -------------------------
mid = G[1].subgridspec(
    2, 2,
    width_ratios=[1.5, 1],
    height_ratios=[1, 1],
    wspace=0.02,
    hspace=0.86
)

ax_f = fig.add_subplot(mid[0, 0])
ax_g = fig.add_subplot(mid[1, 0], sharex=ax_f)
ax_h = fig.add_subplot(mid[0, 1])
ax_i = fig.add_subplot(mid[1, 1])

def set_tight_ylim(ax, y1, y2, pad=0.05):
    vmin = float(min(y1.min(), y2.min()))
    vmax = float(max(y1.max(), y2.max()))
    span = vmax - vmin if vmax > vmin else 0.01
    ax.set_ylim(vmin - span * pad * 1.6, vmax + span * pad * 1.6)

def add_point_labels(ax, x, y, fontsize=7.2):
    y0, y1 = ax.get_ylim()
    dy = (y1 - y0) * 0.04
    for xi, yi in zip(x, y):
        ax.text(xi, yi + dy, f"{yi:.3f}",
                ha="center", va="bottom", fontsize=fontsize, clip_on=False)

def style_line(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(top=False, right=False)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.5, alpha=0.25)
    ax.set_axisbelow(True)

LINE_W = 2.0
MARKER_S = 4.8
MEW = 0.8

ln_ps_f, = ax_f.plot(thr_line, ps_col1, marker="o", markersize=MARKER_S, linewidth=LINE_W,
                     color=C_A_STRUCT, markerfacecolor=C_A_STRUCT,
                     markeredgecolor="white", markeredgewidth=MEW, label="ProteinSage")
ln_esm_f, = ax_f.plot(thr_line, esm_col1, marker="o", markersize=MARKER_S, linewidth=LINE_W,
                      color=C_B_STRUCT, markerfacecolor=C_B_STRUCT,
                      markeredgecolor="white", markeredgewidth=MEW, label="ESM-2")
ax_f.set_ylabel("ratio of tm>0")
style_line(ax_f)
set_tight_ylim(ax_f, ps_col1, esm_col1)
add_point_labels(ax_f, thr_line, ps_col1)
add_point_labels(ax_f, thr_line, esm_col1)

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
style_line(ax_g)
set_tight_ylim(ax_g, ps_col2, esm_col2)
add_point_labels(ax_g, thr_line, ps_col2)
add_point_labels(ax_g, thr_line, esm_col2)

ax_f.text(0.00, 1.13, "(f)", transform=ax_f.transAxes, ha="left", va="bottom",
          fontsize=11.2, fontweight="bold", clip_on=False)
ax_g.text(0.00, 1.13, "(g)", transform=ax_g.transAxes, ha="left", va="bottom",
          fontsize=11.2, fontweight="bold", clip_on=False)

ax_f.legend(handles=[ln_ps_f, ln_esm_f], labels=["ProteinSage", "ESM-2"],
            loc="upper center", bbox_to_anchor=(0.5, 1.39),
            ncol=2, frameon=False, handletextpad=0.6, columnspacing=1.4)

tab = list(mcolors.TABLEAU_COLORS.values())

def pie_color_map(keys, br_color):
    cmap = {"BR": br_color}
    k2 = [k for k in keys if k != "BR"]
    for i, k in enumerate(k2):
        cmap[k] = lighten_color(tab[i % len(tab)], 0.35)
    return cmap

def draw_pie(ax, dct, br_color, title, panel_label):
    keys = list(dct.keys())
    vals = np.array([dct[k] for k in keys], dtype=float)
    total = vals.sum()

    cmap = pie_color_map(keys, br_color)
    colors = [cmap[k] for k in keys]
    explode = [0.06 if k == "BR" else 0.00 for k in keys]

    ax.pie(vals, startangle=90, counterclock=False, colors=colors, explode=explode,
           wedgeprops=dict(linewidth=0.8, edgecolor="white"))

    ax.text(-0.50, 1.10, panel_label, transform=ax.transAxes, ha="left", va="bottom",
            fontsize=11.2, fontweight="bold", clip_on=False)
    ax.set_title(title, pad=6)

    br = dct.get("BR", 0)
    br_pct = br / total * 100.0 if total > 0 else 0.0
    ax.text(0.0, -1.15, f"BR: {int(br)} ({br_pct:.1f}%)",
            ha="center", va="top", fontsize=10.2, fontweight="bold")

    handles = [Patch(facecolor=cmap[k], edgecolor="white", label=f"{k}: {int(dct[k])}") for k in keys]
    ax.legend(handles=handles, frameon=False, loc="center left",
              bbox_to_anchor=(1.02, 0.50), handletextpad=0.6, labelspacing=0.55)

    ax.set_aspect("equal")
    ax.set_axis_off()

draw_pie(ax_h, pie_h, br_color=C_A_STRUCT, title="ProteinSage (n=2343)", panel_label="(h)")
draw_pie(ax_i, pie_i, br_color=C_B_STRUCT, title="ESM-2 (n=2984)", panel_label="(i)")

# -------------------------
# BOTTOM block: jkl venns (new)
# -------------------------
venn_blk = G[2].subgridspec(1, 3, wspace=0.40)

ax_j = fig.add_subplot(venn_blk[0, 0])
ax_k = fig.add_subplot(venn_blk[0, 1])
ax_l = fig.add_subplot(venn_blk[0, 2])

def _clean_venn_axes(ax):
    ax.set_axis_off()

def draw_venn3(ax, reg, labels, colors3, panel_label):
    v = venn3(
        subsets=(reg["onlyA"], reg["onlyB"], reg["AB"],
                 reg["onlyC"], reg["AC"], reg["BC"], reg["ABC"]),
        set_labels=labels,
        ax=ax
    )
    # color patches (soft)
    for patch, col in zip([v.get_patch_by_id('100'),
                           v.get_patch_by_id('010'),
                           v.get_patch_by_id('001')], colors3):
        if patch is not None:
            patch.set_color(col)
            patch.set_alpha(0.55)
            patch.set_edgecolor("white")
            patch.set_linewidth(1.0)

    # make intersection patches a bit darker
    for pid in ['110', '101', '011', '111']:
        p = v.get_patch_by_id(pid)
        if p is not None:
            p.set_alpha(0.35)
            p.set_edgecolor("white")
            p.set_linewidth(1.0)

    # label style
    if v.set_labels is not None:
        for t in v.set_labels:
            if t is not None:
                t.set_fontsize(9.6)
    if v.subset_labels is not None:
        for t in v.subset_labels:
            if t is not None:
                t.set_fontsize(9.6)

    ax.text(-0.12, 1.08, panel_label, transform=ax.transAxes,
            ha="left", va="bottom", fontsize=11.2, fontweight="bold", clip_on=False)

    _clean_venn_axes(ax)

def draw_venn2(ax, a_only, b_only, ab, labels2, colors2, panel_label):
    v = venn2(subsets=(a_only, b_only, ab), set_labels=labels2, ax=ax)
    for patch, col in zip([v.get_patch_by_id('10'), v.get_patch_by_id('01')], colors2):
        if patch is not None:
            patch.set_color(col)
            patch.set_alpha(0.55)
            patch.set_edgecolor("white")
            patch.set_linewidth(1.0)
    p = v.get_patch_by_id('11')
    if p is not None:
        p.set_alpha(0.35)
        p.set_edgecolor("white")
        p.set_linewidth(1.0)

    if v.set_labels is not None:
        for t in v.set_labels:
            if t is not None:
                t.set_fontsize(9.6)
    if v.subset_labels is not None:
        for t in v.subset_labels:
            if t is not None:
                t.set_fontsize(9.6)

    ax.text(-0.12, 1.08, panel_label, transform=ax.transAxes,
            ha="left", va="bottom", fontsize=11.2, fontweight="bold", clip_on=False)
    _clean_venn_axes(ax)

draw_venn3_nature(
    ax_j, venn_PS,
    labels=("BLAST", "MMseqs2", "ProteinSage"),
    colors3=(lighten_color("#BFBFBF", 0.10), lighten_color("#C9D7E6", 0.10), lighten_color(C_A_STRUCT, 0.10)),
    panel_label="(j)"
)

draw_venn3_nature(
    ax_k, venn_ESM,
    labels=("BLAST", "MMseqs2", "ESM-2"),
    colors3=(lighten_color("#BFBFBF", 0.10), lighten_color("#C9D7E6", 0.10), lighten_color(C_B_STRUCT, 0.10)),
    panel_label="(k)"
)

draw_venn2_nature(
    ax_l, a_only=PS_only, b_only=ESM_only, ab=PS_ESM_inter,
    labels2=("ProteinSage", "ESM-2"),
    colors2=(lighten_color(C_A_STRUCT, 0.10), lighten_color(C_B_STRUCT, 0.10)),
    panel_label="(l)"
)

plt.subplots_adjust(left=0.06, right=0.975, top=0.965, bottom=0.06)
plt.show()

fig.savefig("/nfs_baoding/kubeflow-user/lingdong_2024/pic_nature/pic_result/fig5_merged_with_lines.pdf", dpi=600)
fig.savefig("/nfs_baoding/kubeflow-user/lingdong_2024/pic_nature/pic_result/fig5_merged_with_lines.png",
            dpi=600, transparent=True)
