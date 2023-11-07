import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def display(obst:list,path:list) -> None:
    """
    Given the obstacles `obst` and the complete path `path` it'll display the path of the drone throught the obstacles int the grid.
    It is able to display the plot thanks to matplotlib.
    """
    dispD = [[] for i in range(3)]
    for i in path:
        for k in range(3):
            dispD[k].append(i[0][k])
    fig = plt.figure(figsize=(20,20))
    ax = fig.add_subplot(111, projection='3d')
    x, y, z = 0, 1, 2
    for obstacle in obst:
        a = obstacle[0]
        b = obstacle[1]
        vertices = [
            # XZ
            [(a[x], a[y], a[z]), (b[x], a[y], a[z]), (b[x], a[y], b[z]), (a[x], a[y], b[z])],
            [(a[x], b[y], a[z]), (b[x], b[y], a[z]), (b[x], b[y], b[z]), (a[x], b[y], b[z])],

            # YZ
            [(a[x], a[y], a[z]), (a[x], b[y], a[z]), (a[x], b[y], b[z]), (a[x], a[y], b[z])],
            [(b[x], a[y], a[z]), (b[x], b[y], a[z]), (b[x], b[y], b[z]), (b[x], a[y], b[z])],

            # XY
            [(a[x], a[y], a[z]), (b[x], a[y], a[z]), (b[x], b[y], a[z]), (a[x], b[y], a[z])],
            [(a[x], a[y], b[z]), (b[x], a[y], b[z]), (b[x], b[y], b[z]), (a[x], b[y], b[z])],
        ]
        #ax.plot([a[x], b[x]], [a[y], b[y]], [a[z], b[z]])
        ax.add_collection3d(Poly3DCollection(
            vertices, facecolors='cyan', linewidths=1, edgecolors='k',alpha=.1))

    ax.plot(dispD[0],dispD[1],dispD[2],'r')
    ax.plot([path[0][0][0]],[path[0][0][1]],[path[0][0][2]],'*')

    ax.grid(False)
    ax.set_title('Drone Grid Path')
    plt.show()