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
财经
彩票
房产
股票
家居
教育
科技
社会
时尚
时政
体育
星座
游戏
娱乐
""".split()
# # 把默认标记放在最后一个
# all_mark.append(default_mark)
key_word_r_list = """
NBA
nba
英超
TGA
中国
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
