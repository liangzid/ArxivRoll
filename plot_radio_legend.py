import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
fig, ax = plt.subplots()
colors = ['#00ff00', '#800080', '#0000ff', '#ff0000', '#ffff00']  
labels = ['Llama3.1-Nemotron-70B', 'Yi1.5-34B', 'Llama3-8B', 'Phi-2', 'GPT-J-6B']
alphas = [0.25, 0.25, 0.25, 0.25, 0.25]  
patches = [mpatches.Patch(color=color, label=label, alpha=alpha) for color, label, alpha in zip(colors, labels, alphas)]
legend = ax.legend(handles=patches, loc='center', frameon=False, ncol=5)  
ax.axis('off')
fig.canvas.draw()
bbox = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
fig.set_size_inches(bbox.width+0.2, bbox.height)

plt.savefig('radar_legend.pdf')

plt.show()