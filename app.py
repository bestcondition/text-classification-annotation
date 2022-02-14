from flask import Flask, render_template, url_for, redirect
from pathlib import Path

import config
from controller import ProgressController

controller = ProgressController()

app = Flask(__name__)


class ProcessView:
    def __init__(self, process_controller: ProgressController):
        self._controller = process_controller
        self.file_list = self._controller.task_manager.task_name_list
        self.name_done_map = self._controller.task_manager.name_done_map
        # 点击的文件索引
        self.index = 0


class TechView:
    def __init__(self, process_controller: ProgressController):
        self._controller = process_controller
        # line列表
        self.line_list = self._controller.now_task.tech.line_list
        # mark列表
        self.pair_mark_list = self._controller.now_task.label.mark_list
        # 设定的mark
        self.all_mark_list = config.all_mark
        # 当前文件的stem
        self.file_stem = self._controller.now_task.name
        # file列表
        self.file_list = self._controller.task_manager.task_name_list
        # 文件索引map
        self.name_index_map = self._controller.task_manager.name_index_map
        # 关键词索引和突出颜色的映射
        self.keyword_color_map = self._controller.keyword_color_map

    @property
    def next_url(self):
        """
        下一个链接

        :return:
        """
        url = url_for('tech', stem=self._controller.next_name)
        return url

    @property
    def previous_url(self):
        """
        上一个链接

        :return:
        """
        url = url_for('tech', stem=self._controller.previous_name)
        return url

    @property
    def process_url(self):
        """
        查看总览

        :return:
        """

        url = url_for('view')
        return url


@app.route('/')
def index():
    # return render_template('text_label.html', view=TechView(controller))
    return redirect(url_for("tech", stem=controller.now_task.name))


@app.route('/tech/<stem>')
def tech(stem):
    """
    显示技术要求

    :param stem:
    :return:
    """
    controller.activate(stem)
    return render_template('text_label.html', view=TechView(controller))


@app.route('/change/<int:line_number>/<mark>')
def change_mark(line_number, mark):
    try:
        controller.change_mark(line_number, mark)
        return 'ok'
    except AssertionError as e:
        print(e)
        return str(e), 400
    except BaseException as e:
        print(e)
        return str(e), 500


@app.route('/view')
def view():
    return render_template('process.html', view=ProcessView(controller))


if __name__ == '__main__':
    app.run(host=config.host, port=config.port)
