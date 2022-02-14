from pathlib import Path

import config
from model import Task, TechLabelTask, LineLabel


def get_keyword_color_map():
    from itertools import cycle
    color = cycle(config.color_list)
    return {
        key_word: next(color)
        for key_word in config.key_word_r_list
    }


def get_task_name_list():
    """
    从config指定的task_file里加载任务

    :return:
    """
    if hasattr(config, 'task_file'):
        task_file = Path(config.task_file)
        if task_file.exists():
            raw = task_file.read_text(encoding=config.encoding)
            return raw.splitlines()
    return []


class TaskManager:
    """
    任务管理器，这个东西应该从controller里分离出来，很棒的一个重构

    """

    def __init__(self, task_name_seq, task_class):
        self.task_name_list = list(task_name_seq)
        self.length = len(self.task_name_list)
        self.name_index_map = {
            name: i
            for i, name in enumerate(self.task_name_list)
        }
        self.name_done_map = {
            name: bool(LineLabel.from_stem(name, length=0))
            for name in self.task_name_list
        }
        # 子类判断
        assert issubclass(task_class, Task)
        self.task_class = task_class
        self.now_task = None
        self.activate(self.task_name_list[0])

    def done(self):
        self.name_done_map[self.now_task.name] = True

    def activate(self, name):
        """
        激活任务

        :param name:
        :return:
        """
        self.now_task = self.task_class.load(name)

    def get_offset_name(self, offset):
        """
        按照偏移量获取任务名

        :param offset:
        :return:
        """
        now_index = self.name_index_map[self.now_task.stem]
        # 加个模，省了出界，负数也能变正数
        switch_index = (now_index + offset) % self.length
        name = self.task_name_list[switch_index]
        return name

    @property
    def next_name(self):
        """
        下一个任务

        :return:
        """
        return self.get_offset_name(1)

    @property
    def previous_name(self):
        """
        上一个任务

        :return:
        """
        return self.get_offset_name(-1)


class ProgressController:
    def __init__(self):
        # 排个序
        print(Path(config.all_tech_folder).absolute())
        all_file = sorted(
            list(Path(config.all_tech_folder).iterdir()),
            key=lambda x: x.name
        )

        task_name_seq = get_task_name_list() or [
            file.stem
            for file in all_file
        ]

        self.task_manager = TaskManager(task_name_seq, TechLabelTask)
        # 激活
        self.activate = self.task_manager.activate

        self.keyword_color_map = get_keyword_color_map()

    @property
    def next_name(self):
        return self.task_manager.next_name

    @property
    def previous_name(self):
        return self.task_manager.previous_name

    @property
    def now_task(self) -> TechLabelTask:
        """

        :return:
        """
        return self.task_manager.now_task

    def save(self):
        """
        保存当前任务的label

        :return:
        """
        self.now_task.save(config.label_folder)

    def change_mark(self, line_number, mark):
        """
        改变当前任务的标签

        :param line_number:
        :param mark:
        :return:
        """
        self.task_manager.done()
        self.now_task.set_mark(line_number, mark)
        self.save()
