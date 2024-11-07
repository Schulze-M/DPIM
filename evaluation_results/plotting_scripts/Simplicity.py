import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.ticker import StrMethodFormatter


# Simplicity
y1 = [0.7267,	0.7344,	0.7176]
y2 = [0.7277,	0.7345,	0.7311]
y3 = [0.7643,	0.7748,	0.7932]
y4 = [0.5679,	0.5653,	0.5678]
y5 = [0.5683,	0.5584,	0.5573]
y6 = [0.5077,	0.5059,	0.5048]
y7 = [0.5411,	0.5426,	0.5577]
y8 = [0.5616,	0.5638,	0.5577]
y9 = [0.5258, 0.5218, 0.5181] # 2017
y10 = [0.3668, 0.3655, 0.3643] # 2015_1
y11 = [0.3619, 0.3646, 0.3638] # 2015_2
y12 = [0.3583, 0.3585, 0.3582] # 2015_3
y13 = [0.3814, 0.3815, 0.3791] # 2015_4
y14 = [0.3824, 0.3814, 0.3788] # 2015_5

y1_std = np.array([0.0640,	0.0687,	0.0641])
y2_std = np.array([0.0500,	0.0581,	0.0575])
y3_std = np.array([0.0479,	0.0524,	0.0897])
y4_std = np.array([0.0392,	0.0416,	0.0556])
y5_std = np.array([0.0331,	0.0367,	0.0408])
y6_std = np.array([0.0217,	0.0233,	0.0254])
y7_std = np.array([0.0272,	0.0267,	0.0282])
y8_std = np.array([0.0337,	0.0359,	0.0385])
y9_std = np.array([0.0328, 0.032, 0.0306]) # 2017
y10_std = np.array([0.0043, 0.0049, 0.0059]) # 2015_1
y11_std = np.array([0.0086, 0.0082, 0.008])  # 2015_2
y12_std = np.array([0.0004, 0.0016, 0.0001])  # 2015_3
y13_std = np.array([0.0055, 0.0055, 0.0066])  # 2015_4
y14_std = np.array([0.0037, 0.0044, 0.005])  # 2015_5

# Set the color palette
c = mpl.colormaps['tab10'].colors

# Set X-axis
x = [3.75, 1.25, 0.125]

# B x H
plt.figure(figsize=(11.7/(3.8*1.3), 8.27/1.3))

plt.scatter(4.25, 0.6800, s=112, c=c[0], label="Closed Problems", marker='|')
plt.scatter(4.25, 0.6970, s=112, c=c[0], label="Incidents", marker='x')
plt.scatter(4.25, 0.7143, s=112, label="Open Problems", facecolors='none', edgecolors=c[4], marker='o')
plt.scatter(4.25, 0.5500, s=112, c=c[2], label="Sepsis Cases - Event Log", marker='|')
plt.scatter(4.25, 0.5922, s=112, c=c[1], label="Domestic Declarations", marker='|')
plt.scatter(4.25, 0.4574, s=112, c=c[1], label="International Declarations", marker='x')
plt.scatter(4.25, 0.5105, s=112, label="Prepaid Travel Cost", facecolors='none', edgecolors=c[1], marker='o')
plt.scatter(4.25, 0.6000, s=112, label="Request for Payment", facecolors='none', edgecolors=c[1], marker='s')
plt.scatter(4.25, 0.5724, s=112, c=c[3], label="BPIC 2017", marker='|')
plt.scatter(4.25, 0.3600, s=112, c=c[4], label="BPIC 2015_1", marker='|')
plt.scatter(4.25, 0.3544, s=112, c=c[4], label="BPIC 2015_2", marker='x')
plt.scatter(4.25, 0.3536, s=112, label="BPIC 2015_3", facecolors='none', edgecolors=c[4], marker='o')
plt.scatter(4.25, 0.3744, s=112, label="BPIC 2015_4", facecolors='none', edgecolors=c[4], marker='s')
plt.scatter(4.25, 0.3574, s=112, label="BPIC 2015_5", facecolors='none', edgecolors=c[4], marker='^')

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
plt.fill_between(x=x, y1=y2 - y2_std, y2=y2 + y2_std, alpha=0.125, facecolor=c[0])
plt.fill_between(x=x, y1=y3 - y3_std, y2=y3 + y3_std, alpha=0.15, facecolor=c[0])
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
plt.ylabel("Simplicity", fontsize=14)

# Limits of the axes:
plt.xlim(0, 4.3)
plt.ylim(0.3, 1.03)
plt.xticks([3, 1, 0.1])

# Invert the X-axis
plt.gca().invert_xaxis()

plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))

plt.savefig('Simplicity-Final.pdf', bbox_inches='tight', pad_inches=0)

# Show the plot:
# plt.show()
