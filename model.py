from pathlib import Path
import abc

import config

# 用来assert，所有mark的集合
mark_set = set(config.all_mark)


def assert_mark_list(mark_list):
    """
    检测是否所有mark都在已定义的标签中

    :param mark_list:
    :return:
    """
    flag = all(
        mark in mark_set or mark == config.default_mark
        for mark in mark_list
    )
    return flag


class LineLabel:
    def __init__(self, stem, mark_seq):
        self.stem = stem
        mark_list = list(mark_seq)
        assert assert_mark_list(mark_list), f'这里面有未定义的mark，您检查下呗，您的文件：{mark_list}，已定义的{config.all_mark}'
        self.mark_list = mark_list

    def set_mark(self, line_number, mark):
        assert mark in mark_set, f'马克不在这里！{mark} not in {mark_set}'
        # default_mark不在all_mark中
        # assert mark != config.default_mark, f'默认mark："{config.default_mark}"不应该被写入！'
        self.mark_list[line_number] = mark

    @classmethod
    def from_file(cls, file, length=None, not_exist_ok=False):
        file = Path(file)
        if file.exists():
            raw = file.read_text(encoding=config.encoding)
            mark_seq = raw.splitlines()
        elif not_exist_ok:  # 文件不存在，又不ok，肯定出问题啦！
            raise FileNotFoundError(f'{file} not found!')
        else:
            # assert length, f'您得给定length啊！才能给您初始化：length:{length}'
            mark_seq = [config.default_mark] * length
        stem = file.stem
        return cls(stem=stem, mark_seq=mark_seq)

    @classmethod
    def from_stem(cls, stem, length):
        """
        这里假定从config指定的文件夹加载

        :param stem:
        :param length:
        :return:
        """
        file = Path(config.label_folder) / f'{stem}{config.label_suffix}'
        return cls.from_file(file, length)

    def save(self, folder):
        folder = Path(folder)
        file = folder / f'{self.stem}{config.label_suffix}'
        with open(file, mode='w', encoding=config.encoding) as fp:
            for mark in self.mark_list:
                fp.write(f'{mark}\n')

    def __bool__(self):
        return bool(self.mark_list)


def assert_line_list(line_list):
    """
    判断line的正确性

    :param line_list:
    :return:
    """
    flag = all(
        # 一行里面不能有换行，不能有空行
        ('\n' not in line) and (line.strip())
        for line in line_list
    )
    return flag


class Tech:

    def __init__(self, stem, line_seq):
        self.stem = stem
        line_list = list(line_seq)
        assert assert_line_list(line_list), f'其中有line有问题：{line_list}'
        self.line_list = line_list

    @classmethod
    def from_file(cls, file):
        file = Path(file)
        raw = file.read_text(encoding=config.encoding)
        line_list = raw.splitlines()
        stem = file.stem
        return cls(stem, line_list)

    @classmethod
    def from_stem(cls, stem):
        file = Path(config.all_tech_folder) / f'{stem}{config.tech_suffix}'
        return cls.from_file(file)


class Task(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def load(cls, name):
        """
        加载任务

        :param name:
        :return:
        """
        pass

    @property
    @abc.abstractmethod
    def name(self):
        """
        获取名字的接口

        :return:
        """
        pass


class TechLabelTask(Task):
    def __init__(self, tech: Tech, label: LineLabel):
        assert tech.stem == label.stem, f'名称不匹配：{tech.stem} ==? {label.stem}'
        self.stem = tech.stem
        assert len(tech.line_list) == len(label.mark_list)
        self.tech = tech
        self.label = label

        # 挂两个label代理
        self.set_mark = self.label.set_mark
        # 亲爱的代码的读者，现在请你思考一个问题，这样代理方法，self会传递吗？会有问题吗？
        self.save = self.label.save

        self.from_stem = self.load

    @property
    def name(self):
        return self.stem

    @classmethod
    def load(cls, stem):
        tech = Tech.from_stem(stem)
        label = LineLabel.from_stem(stem, length=len(tech.line_list))
        return cls(tech, label)
