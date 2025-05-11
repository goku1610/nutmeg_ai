def create_graph(code):
    import matplotlib.pyplot as plt
    import numpy as np

    # Use a single namespace for exec
    exec_namespace = {}
    exec(code, exec_namespace)

    plt.savefig("static/graph.png")


if __name__ =="__main__":
    code = """
import matplotlib.pyplot as plt
import numpy as np

# Data for the graph (last 4 matches between Real Madrid and Barcelona)
dates = ['2025-04-20', '2024-10-27', '2024-01-14', '2023-04-05']
real_madrid_scores = [2, 1, 4, 4]
barcelona_scores = [1, 0, 1, 0]

x = np.arange(len(dates))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(10, 6))

# Add score labels on top of bars
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

rects1 = ax.bar(x - width/2, real_madrid_scores, width, label='Real Madrid', color='#00529F')
rects2 = ax.bar(x + width/2, barcelona_scores, width, label='Barcelona', color='#C6001E')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Goals Scored')
ax.set_title('Goals Scored in Last 4 Real Madrid vs Barcelona Matches')
ax.set_xticks(x)
ax.set_xticklabels(dates)
ax.legend()

autolabel(rects1)
autolabel(rects2)

fig.tight_layout()
plt.show()
"""


    create_graph(code)