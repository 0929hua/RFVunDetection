# 导入绘图模块
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
# 构建数据
def to_percent(temp, position):
 return '%1.0f'%(10*temp) + '%'
Y2016 = [0.937, 0.993, 0.933, 0.884]
Y2017 = [0.996, 0.998, 0.999, 0.998]
Y2018 = [0.063, 0.007,0.067, 0.116]
Y2019 = [0.004, 0.002,  0.001, 0.002]
labels = ['Integer overflow','Timestamp','Reentrancy','TX.origin']
bar_width = 0.3
width = 0.1
# list2 = [94, 99.3, 94.3, 71.3]
# list3 = [6, 0.6,5.7, 28.7]
# list4 = [99.3, 99.6, 100, 100]
# list5 = [0.7, 0.4,  0, 0]
fig, ax = plt.subplots()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# 中文乱码的处理
plt.rcParams['font.sans-serif'] =[u'SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 绘图12
plt.bar(np.arange(4), Y2016, label = 'TPR',   color = 'steelblue', alpha = 0.4, width = bar_width)
plt.bar(np.arange(4), Y2018, label = 'FNR',bottom=Y2016,color = 'steelblue', alpha = 0.2, width = bar_width,hatch="xxx")

plt.bar(np.arange(4)+width+bar_width, Y2017, label = 'TNR', color = 'orange', alpha = 0.3, width = bar_width)
plt.bar(np.arange(4)+width+bar_width, Y2019, label = 'FPR',bottom=Y2017 ,color = 'orange', alpha = 0.2, width = bar_width,hatch="xxx")

# 添加轴标签
plt.xlabel('Four Vulnerabilities')
plt.ylabel('Detection Rate')
# 添加刻度标签
plt.xticks(np.arange(4)+bar_width,labels)
# 设置Y轴的刻度范围
plt.ylim([0.45, 1])
#plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
# 显示图例
num1=1.05
num2=0
num3=3
num4=0
plt.legend(bbox_to_anchor=(num1, num2), loc=num3, borderaxespad=num4)
# 显示图形
fig.tight_layout()  # 调整整体空白
plt.show()
