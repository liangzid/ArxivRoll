"""
======================================================================
DRAWS --- 

functions to draw plots.

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created: 25 November 2024
======================================================================
"""


# ------------------------ Code --------------------------------------

## normal import 
import json
from typing import List,Tuple,Dict
import random
from pprint import pprint as ppp

from matplotlib import pyplot as plt


def draw_pieChart(data_ls,labels,save_pth):
    sizes=data_ls
    # colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']  # 自定义颜色
    explode = (0.1, 0, 0, 0, 0, 0, 0, 0)  # 突出显示第一个饼图部分

    # 绘制饼图
    plt.pie(sizes, explode=explode, labels=labels,
            # colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)

    # 确保饼图是圆形的
    plt.axis('equal')

    # 添加标题
    # plt.title('美化的饼图示例')

    # 显示图例
    plt.legend(labels, loc="best", bbox_to_anchor=(1, 0, 0.5, 1))

    # 显示图表
    plt.show()























## running entry
if __name__=="__main__":
    main()
    print("EVERYTHING DONE.")


