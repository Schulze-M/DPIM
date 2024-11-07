import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.ticker import StrMethodFormatter


# Precision
y1 = [0.8804,	0.8845,	0.9057]
y2 = [0.8288,	0.8338,	0.7915]
y3 = [0.9488,	0.9455,	0.8874]
y4 = [0.2292,	0.2270,	0.3195]
y5 = [0.2177,	0.2078,	0.2012]
y6 = [0.1000,	0.1019,	0.1076]
y7 = [0.1204,	0.1201,	0.1238]
y8 = [0.1963,	0.1989,	0.1885]
y9 = [0.0803, 0.0879, 0.0824] # 2017
y10 = [0.0215, 0.0255, 0.0524] # 2015_1
y11 = [0.0192, 0.015, 0.0204] # 2015_2
y12 = [0.0437, 0.0317, 0.0332] # 2015_3
y13 = [0.0073, 0.0088, 0.0174] # 2015_4
y14 = [0.0531, 0.0903, 0.1356] # 2015_5

y1_std = np.array([0.0730,	0.0646,	0.1193])
y2_std = np.array([0.0966,	0.0991,	0.1417])
y3_std = np.array([0.0421,	0.0396,	0.2308])
y4_std = np.array([0.0588,	0.0709,	0.1957])
y5_std = np.array([0.0386,	0.0303,	0.0352])
y6_std = np.array([0.0129,	0.0214,	0.0909])
y7_std = np.array([0.0220,	0.0277,	0.0550])
y8_std = np.array([0.0361,	0.0325,	0.0457])
y9_std = np.array([0.0539, 0.0751, 0.0588]) # 2017
y10_std = np.array([0.0268, 0.0354, 0.0527]) # 2015_1
y11_std = np.array([0.016, 0.015, 0.0306]) # 2015_2
y12_std = np.array([0.0445, 0.0438, 0.0378]) # 2015_3
y13_std = np.array([0.0067, 0.0098, 0.0191]) # 2015_4
y14_std = np.array([0.0937, 0.1249, 0.131]) # 2015_5

# Set the color palette
c = mpl.colormaps['tab10'].colors

# Set X-axis
x = [3.75, 1.25, 0.125]

# B x H
plt.figure(figsize=(11.7/(3.8*1.3), 8.27/1.3))

plt.scatter(4.25, 0.7967, s=112, c=c[0], label="Closed Problems", marker='|')
plt.scatter(4.25, 0.8083, s=112, c=c[0], label="Incidents", marker='x')
plt.scatter(4.25, 0.9066, s=112, label="Open Problems", facecolors='none', edgecolors=c[4], marker='o')
plt.scatter(4.25, 0.1911, s=112, c=c[2], label="Sepsis Cases - Event Log", marker='|')
plt.scatter(4.25, 0.247,  s=112, c=c[1], label="Domestic Declarations", marker='|')
plt.scatter(4.25, 0.0988, s=112, c=c[1], label="International Declarations", marker='x')
plt.scatter(4.25, 0.1095, s=112, label="Prepaid Travel Cost", facecolors='none', edgecolors=c[1], marker='o')
plt.scatter(4.25, 0.2873, s=112, label="Request for Payment", facecolors='none', edgecolors=c[1], marker='s')
plt.scatter(4.25, 0.1021, s=112, c=c[3], label="BPIC 2017", marker='|')
plt.scatter(4.25, 0.0055, s=112, c=c[4], label="BPIC 2015_1", marker='|')
plt.scatter(4.25, 0.0047, s=112, c=c[4], label="BPIC 2015_2", marker='x')
plt.scatter(4.25, 0.0057, s=112, label="BPIC 2015_3", facecolors='none', edgecolors=c[4], marker='o')
plt.scatter(4.25, 0.0068, s=112, label="BPIC 2015_4", facecolors='none', edgecolors=c[4], marker='s')
plt.scatter(4.25, 0.0053, s=112, label="BPIC 2015_5", facecolors='none', edgecolors=c[4], marker='^')

# Plot all graphs
plt.plot(x, y1, c=c[0], linewidth=2, label="Closed Problems", marker='|', markersize=12)
plt.plot(x, y2, c=c[0], linewidth=2, label="Incidents", marker='x', markersize=12)
plt.plot(x, y3, c=c[0], linewidth=2, label="Open Problems", fillstyle='none', marker='o', markersize=12, markerfacecolor='tab:blue', markerfacecoloralt='lightsteelblue', markeredgecolor=c[0])
plt.plot(x, y4, c=c[2], linewidth=2, label="Sepsis Cases - Event Log", marker='|', markersize=12)
plt.plot(x, y5, c=c[1], linewidth=2, label="Domestic Declarations", marker='|', markersize=12)
plt.plot(x, y6, c=c[1], linewidth=2, label="International Declarations", marker='x', markersize=12)
plt.plot(x, y7, c=c[1], linewidth=2, label="Prepaid Travel Cost", fillstyle='none', marker='o', markersize=12, markerfacecolor='tab:blue', markerfacecoloralt='lightsteelblue', markeredgecolor=c[1])
plt.plot(x, y8, c=c[1], linewidth=2, label="Request for Payment", fillstyle='none', marker='s', markersize=12, markerfacecolor='tab:blue', markerfacecoloralt='lightsteelblue', markeredgecolor=c[1])
plt.plot(x, y9, c=c[3], linewidth=2, label="BPIC 2017", marker='|', markersize=12)
plt.plot(x, y10, c=c[4], linewidth=2, label="BPIC 2015_1", marker='|', markersize=12)
plt.plot(x, y11, c=c[4], linewidth=2, label="BPIC 2015_2", marker='x', markersize=12)
plt.plot(x, y12, c=c[4], linewidth=2, label="BPIC 2015_3", fillstyle='none', marker='o', markersize=12, markerfacecolor='tab:blue', markerfacecoloralt='lightsteelblue', markeredgecolor=c[4])
plt.plot(x, y13, c=c[4], linewidth=2, label="BPIC 2015_4", fillstyle='none', marker='s', markersize=12, markerfacecolor='tab:blue', markerfacecoloralt='lightsteelblue', markeredgecolor=c[4])
plt.plot(x, y14, c=c[4], linewidth=2, label="BPIC 2015_5", fillstyle='none', marker='^', markersize=12, markerfacecolor='tab:blue', markerfacecoloralt='lightsteelblue', markeredgecolor=c[4])

plt.fill_between(x=x, y1=y1 - y1_std, y2=y1 + y1_std, alpha=0.1, facecolor=c[0])
plt.fill_between(x=x, y1=y2 - y2_std, y2=y2 + y2_std, alpha=0.1, facecolor=c[0])
plt.fill_between(x=x, y1=y3 - y3_std, y2=y3 + y3_std, alpha=0.1, facecolor=c[0])
plt.fill_between(x=x, y1=y4 - y4_std, y2=y4 + y4_std, alpha=0.1, facecolor=c[2])
plt.fill_between(x=x, y1=y5 - y5_std, y2=y5 + y5_std, alpha=0.1, facecolor=c[1])
plt.fill_between(x=x, y1=y6 - y6_std, y2=y6 + y6_std, alpha=0.1, facecolor=c[1])
plt.fill_between(x=x, y1=y7 - y7_std, y2=y7 + y7_std, alpha=0.1, facecolor=c[1])
plt.fill_between(x=x, y1=y8 - y8_std, y2=y8 + y8_std, alpha=0.1, facecolor=c[1])
plt.fill_between(x=x, y1=y9 - y9_std, y2=y9 + y9_std, alpha=0.1, facecolor=c[3])
plt.fill_between(x=x, y1=y10 - y10_std, y2=y10 + y10_std, alpha=0.1, facecolor=c[4])
plt.fill_between(x=x, y1=y11 - y11_std, y2=y11 + y11_std, alpha=0.1, facecolor=c[4])
plt.fill_between(x=x, y1=y12 - y12_std, y2=y12 + y12_std, alpha=0.1, facecolor=c[4])
plt.fill_between(x=x, y1=y13 - y13_std, y2=y13 + y13_std, alpha=0.1, facecolor=c[4])
plt.fill_between(x=x, y1=y14 - y14_std, y2=y14 + y14_std, alpha=0.1, facecolor=c[4])

# Label the axes:
plt.xlabel("$\\varepsilon$", fontsize=14)
plt.ylabel("Precision", fontsize=14)

# Limits of the axes:
plt.xlim(0, 4.3)
plt.ylim(0, 1.03)
plt.xticks([3, 1, 0.1])

# Invert the X-axis
plt.gca().invert_xaxis()

plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))

plt.savefig('Precision-Final.pdf', bbox_inches='tight', pad_inches=0)

# Show the plot:
# plt.show()
