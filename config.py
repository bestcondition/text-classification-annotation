"""
配置文件
"""
from util import get_real_path

"""
数据 相关
"""

# 存放所有技术要求的文件夹
all_tech_folder = get_real_path(r'tech')

# 任务文件
task_file = get_real_path(r'task/0.txt')

# 标签存放位置
label_folder = get_real_path('label')

"""
server 相关
"""

# 监听ip
host = '127.0.0.1'

# 监听端口
port = 7396

"""
code 相关
"""
encoding = 'utf-8'
label_suffix = '.txt'
tech_suffix = '.txt'
default_mark = ' '

"""
标签
"""

# 标签列表，一行一个
# all_mark = """
# 1
# 2
# 3
# """.split()
all_mark = """
规范要求
其他
热缩套管
PVC管
号码管
线扎
白硅管
护套
端子
导线
塑壳
保险管
黄腊管
插片
波纹管
""".split()
# # 把默认标记放在最后一个
# all_mark.append(default_mark)
key_word_r_list = """
要求
热缩
线扎
导线
端子
PVC套?管
号码
护套
白硅
保险
保持
黄蜡
插片
磁环
为
带
用
套
波纹管
""".split()
color_list = """
blue
green
red
yellow
aqua
cyan
fuchsia
pink
greenyellow
gold
""".split()
