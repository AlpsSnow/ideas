import yaml
import os
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle, Wedge, Polygon

# 显示画面
def showPlt(patches, ax):
    p = PatchCollection(patches, match_original = True)
    ax.add_collection(p)
    plt.pause(0.5)    #图片显示暂停的时间，产生动图效果


# 画扇形
def pltWedge(patches, color1, color2, color3):    
    # 画扇形    
    w1 = Wedge(center = [20, 20], r = 10, theta1 = 30, theta2 = 150, facecolor = color1, edgecolor = None, zorder = 1)
    w2 = Wedge(center = [20, 20], r = 10, theta1 = 150, theta2 = 270, facecolor = color2, edgecolor = None, zorder = 1)
    w3 = Wedge(center = [20, 20], r = 10, theta1 = 270, theta2 = 390, facecolor = color3, edgecolor = None, zorder = 1)
    patches.extend([w1, w2, w3])

# 画三角形
def pltPolygon(patches, color1, color2, color3):
    p1 = Polygon([[20-5*3**0.5, 25], [20-2.5*3**0.5, 17.5], [20, 25]],  facecolor = color1, edgecolor = None, zorder = 2)
    p2 = Polygon([[20-2.5*3**0.5, 17.5], [20, 10], [20+2.5*3**0.5, 17.5]],  facecolor = color2, edgecolor = None, zorder = 2)
    p3 = Polygon([[20+2.5*3**0.5, 17.5], [20+5*3**0.5, 25], [20, 25]],  facecolor = color3, edgecolor = None, zorder = 2)
    patches.extend([p1, p2, p3])

# 画同心圆
def pltCircle(patches, color4):
    c1 = Circle((20, 20), 5, facecolor = 'white', edgecolor = None, zorder = 3)
    c2 = Circle((20, 20), 4, facecolor = color4, edgecolor = None, zorder = 4)
    patches.extend([c1, c2])

# 解析yaml文件
def getConf():
    curPath = os.path.dirname(os.path.realpath(__file__))
    yamlPath = os.path.join(curPath,'config.yaml')

    f = open(yamlPath,'r',encoding='utf-8')
    cfg = f.read()    
    dict_obj = yaml.load(cfg, Loader=yaml.FullLoader)  
    return dict_obj

if __name__ == '__main__':
    patches = []
    conf = getConf()
    colors = conf['colors']

    # 准备画布
    fig, ax = plt.subplots(figsize = [8, 8])  # x，y轴的分隔比例

    for color in colors:
        if len(color) != 4:
            print("config.yaml的类容不正（颜色个数不是4）。{0}".format(color))
            continue
        # 清除画布
        plt.cla()

        # 设置x，y轴坐标
        plt.ylim([0, 40])
        plt.xlim([0, 40])

        # 画扇形
        pltWedge(patches, color[0], color[1], color[2])
        showPlt(patches, ax)

        # 画三角形
        pltPolygon(patches, color[0], color[1], color[2])
        showPlt(patches, ax) 

        # 画同心圆
        pltCircle(patches, color[3])   
        showPlt(patches, ax)

        plt.pause(2)      
    
    plt.show()


