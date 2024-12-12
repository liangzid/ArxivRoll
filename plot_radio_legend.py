# import matplotlib.pyplot as plt
# import numpy as np
# import matplotlib

# # 使用合适的后端，如果是在非图形界面环境中运行
# matplotlib.use('Agg')

# # 数据
# labels = np.array(['A', 'B', 'C', 'D', 'E'])
# data1 = np.array([0.6, 0.7, 0.8, 0.5, 0.9])
# data2 = np.array([0.4, 0.6, 0.7, 0.3, 0.8])

# # 角度
# angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
# angles += angles[:1]

# # 数据闭合
# data1 = np.concatenate((data1,[data1[0]]))
# data2 = np.concatenate((data2,[data2[0]]))

# # 绘图
# fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
# ax.fill(angles, data1, color='red', alpha=0.25)
# ax.plot(angles, data1, color='red', label='Data 1')
# ax.fill(angles, data2, color='blue', alpha=0.25)
# ax.plot(angles, data2, color='blue', label='Data 2')

# # 设置
# ax.set_xticks(angles[:-1])
# ax.set_xticklabels(labels)
# ax.legend(loc='upper right')

# # 保存图表为 PDF 文件
# plt.savefig('radar_chart.pdf')
# print(1)
# plt.close(fig)  # 关闭图形，释放内存
import json
import matplotlib.pyplot as plt
import numpy as np


with open('/home/zi/arxivSpider/Results--Radar.json', 'r') as file:
    json_data = json.load(file)

scores_dict = json_data["microsoft/phi-2"]["RobenchAveragedScore"]

data1 = np.array([scores_dict["cs"], scores_dict["fin"], scores_dict["math"], scores_dict["econ"],
                   scores_dict["eess"], scores_dict["physics"], scores_dict["stat"], scores_dict["q-bio"]])*100

scores_dict = json_data["meta-llama/Meta-Llama-3-8B"]["RobenchAveragedScore"]

data2 = np.array([scores_dict["cs"], scores_dict["fin"], scores_dict["math"], scores_dict["econ"],
                   scores_dict["eess"], scores_dict["physics"], scores_dict["stat"], scores_dict["q-bio"]])*100

scores_dict = json_data["nvidia/Llama-3.1-Nemotron-70B-Instruct-HF"]["RobenchAveragedScore"]

data3 = np.array([scores_dict["cs"], scores_dict["fin"], scores_dict["math"], scores_dict["econ"],
                   scores_dict["eess"], scores_dict["physics"], scores_dict["stat"], scores_dict["q-bio"]])*100

scores_dict = json_data["EleutherAI/gpt-j-6B"]["RobenchAveragedScore"]

data4 = np.array([scores_dict["cs"], scores_dict["fin"], scores_dict["math"], scores_dict["econ"],
                   scores_dict["eess"], scores_dict["physics"], scores_dict["stat"], scores_dict["q-bio"]])*100

scores_dict = json_data["01-ai/Yi-1.5-34B-Chat"]["RobenchAveragedScore"]

data5 = np.array([scores_dict["cs"], scores_dict["fin"], scores_dict["math"], scores_dict["econ"],
                   scores_dict["eess"], scores_dict["physics"], scores_dict["stat"], scores_dict["q-bio"]])*100

labels = np.array(['CS', 'Q-Fin', 'Math', 'Econ', 'EESS', 'Phy', 'Stat', 'Bio'])

angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()



data_20=np.array([10,10,10,10,10,10,10,10])
data_40=np.array([20,20,20,20,20,20,20,20])
data_60=np.array([30,30,30,30,30,30,30,30])
data_80=np.array([40,40,40,40,40,40,40,40])
data_100=np.array([50,50,50,50,50,50,50,50])

data_20 = np.concatenate((data_20, [data_20[0]]))
data_40 = np.concatenate((data_40, [data_40[0]]))
data_60 = np.concatenate((data_60, [data_60[0]]))
data_80 = np.concatenate((data_80, [data_80[0]]))
data_100 = np.concatenate((data_100, [data_100[0]]))

data1 = np.concatenate((data1, [data1[0]]))
data2 = np.concatenate((data2, [data2[0]]))
data3 = np.concatenate((data3, [data3[0]]))
data4 = np.concatenate((data4, [data4[0]]))
data5 = np.concatenate((data5, [data5[0]]))
angles += angles[:1]


fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(polar=True))
ax.fill(angles, data3, color='green', alpha=0.25, label='Llama3.1-Nemotron-70B')
ax.plot(angles, data3, color='green', alpha=0.25,marker='o', markersize=15,linewidth=10)
ax.fill(angles, data5, color='purple', alpha=0.25, label='Yi1.5-34B')
ax.plot(angles, data5, color='purple', alpha=0.25,marker='o',  markersize=15,linewidth=10)
ax.fill(angles, data2, color='blue', alpha=0.25, label='Llama3-8B')
ax.plot(angles, data2, color='blue', alpha=0.25,marker='o',  markersize=15,linewidth=10)
ax.fill(angles, data1, color='red', alpha=0.25, label='Phi-2')
ax.plot(angles, data1, color='red', alpha=0.25,marker='o',  markersize=15,linewidth=10)
ax.fill(angles, data4, color='yellow', alpha=0.25, label='GPT-J-6B')
ax.plot(angles, data4, color='yellow', alpha=0.25,marker='o', markersize=15,linewidth=10)

ax.fill(angles, data_20, color='black', alpha=0)
ax.plot(angles, data_20, color='black', alpha=0.25,linewidth=2)
ax.fill(angles, data_40, color='black', alpha=0)
ax.plot(angles, data_40, color='black', alpha=0.25,linewidth=2)
ax.fill(angles, data_60, color='black', alpha=0)
ax.plot(angles, data_60, color='black', alpha=0.25,linewidth=2)
ax.fill(angles, data_80, color='black', alpha=0)
ax.plot(angles, data_80, color='black', alpha=0.25,linewidth=2)
ax.fill(angles, data_100, color='black', alpha=0)
ax.plot(angles, data_100, color='black', alpha=0.25,linewidth=2)


ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontsize=36)



ax.set_ylim(0, 50)
ax.tick_params(axis='y', labelsize=36)
ax.yaxis.grid(False) 
ax.spines['polar'].set_visible(False)
ax.axis('off')
ax.legend(loc='upper right', bbox_to_anchor=(1.12, 1.12),fontsize=16)
plt.tight_layout()
plt.savefig('radar_legend.pdf')

plt.show()