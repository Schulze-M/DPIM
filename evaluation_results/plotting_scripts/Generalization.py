import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


# Generalization
y1 = [0.8357,	0.8390,	0.8049]
y2 = [0.9001,	0.9069,	0.9016]
y3 = [0.9426,	0.9402,	0.8900]
y4 = [0.8767,	0.8639,	0.8470]
y5 = [0.7956,	0.7873,	0.7926]
y6 = [0.8607,	0.8596,	0.8584]
y7 = [0.8430,	0.8446,	0.8344]
y8 = [0.7888,	0.7847,	0.7864]
y9 = [0.8442, 0.8435, 0.8434] # 2017
y10 = [0.6358, 0.6362, 0.6342] # 2015_1
y11 = [0.6271, 0.6243, 0.6242] # 2015_2
y12 = [0.6742, 0.676, 0.6751] # 2015_3
y13 = [0.6508, 0.65, 0.6486]  # 2015_4
y14 = [0.6483, 0.6462, 0.6452] # 2015_5

y1_std = np.array([0.0673,	0.0643,	0.0931])
y2_std = np.array([0.0504,	0.0483,	0.0485])
y3_std = np.array([0.0056,	0.0130,	0.0856])
y4_std = np.array([0.0396,	0.0434,	0.0584])
y5_std = np.array([0.0396,	0.0401,	0.0429])
y6_std = np.array([0.0163,	0.0219,	0.0235])
y7_std = np.array([0.0216,	0.0242,	0.0357])
y8_std = np.array([0.0415,	0.0461,	0.0420])
y9_std = np.array([0.0249, 0.0287, 0.0292]) # 2017
y10_std = np.array([0.0057, 0.0056, 0.0066]) # 2015_1
y11_std = np.array([0.008, 0.0082, 0.0083]) # 2015_2
y12_std = np.array([0.0051, 0.0049, 0.0048]) # 2015_3
y13_std = np.array([0.003, 0.004, 0.005]) # 2015_4
y14_std = np.array([0.006, 0.0069, 0.0081]) # 2015_5

# Set the color palette
c = mpl.colormaps['tab10'].colors

# Set X-axis
x = [3.75, 1.25, 0.125]

# B x H
plt.figure(figsize=(11.7/(3.8*1.3), 8.27/1.3))

plt.scatter(4.25, 0.8772, s=112, c=c[0], label="Closed Problems", marker='|')
plt.scatter(4.25, 0.9586, s=112, c=c[0], label="Incidents", marker='x')
plt.scatter(4.25, 0.9629, s=112, label="Open Problems", facecolors='none', edgecolors=c[4], marker='o')
plt.scatter(4.25, 0.8993, s=112, c=c[2], label="Sepsis Cases - Event Log", marker='|')
plt.scatter(4.25, 0.8611, s=112, c=c[1], label="Domestic Declarations", marker='|')
plt.scatter(4.25, 0.8977, s=112, c=c[1], label="International Declarations", marker='x')
plt.scatter(4.25, 0.8918, s=112, label="Prepaid Travel Cost", facecolors='none', edgecolors=c[1], marker='o')
plt.scatter(4.25, 0.8268, s=112, label="Request for Payment", facecolors='none', edgecolors=c[1], marker='s')
plt.scatter(4.25, 0.9061, s=112, c=c[3], label="BPIC 2017", marker='|')
plt.scatter(4.25, 0.6586, s=112, c=c[4], label="BPIC 2015_1", marker='|')
plt.scatter(4.25, 0.6327, s=112, c=c[4], label="BPIC 2015_2", marker='x')
plt.scatter(4.25, 0.6765, s=112, label="BPIC 2015_3", facecolors='none', edgecolors=c[4], marker='o')
plt.scatter(4.25, 0.6608, s=112, label="BPIC 2015_4", facecolors='none', edgecolors=c[4], marker='s')
plt.scatter(4.25, 0.6608, s=112, label="BPIC 2015_5", facecolors='none', edgecolors=c[4], marker='^')

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

plt.xticks([3, 1, 0.1])

# Label the axes:
plt.xlabel("$\\varepsilon$", fontsize=14)
plt.ylabel("Generalization", fontsize=14)

# Limits of the axes:
plt.xlim(0, 4.3)
plt.ylim(0.6, 1.03)
plt.xticks([3, 1, 0.1])

# Invert the X-axis
plt.gca().invert_xaxis()

plt.savefig('Generalization-Final.pdf', bbox_inches='tight', pad_inches=0)

# Show the plot:
# plt.show()
