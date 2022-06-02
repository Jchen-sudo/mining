# feature of python 3.11, for better type hints
from __future__ import annotations
import re
import logging
from typing import Dict, Set, Tuple, Union, List, Callable


# 实际上使用正则去匹配bytes类型的数据是做不到的
# 所以说我考虑做一个bytes -> char的映射
# 把[0,255]的字符想办法编码到[0,127]这个范围内，就能去构造正则匹配了
# 一个简单的思路是将[0,255]编码到两位[0,127]的字符

# 另外一个思路是使用cp437译码，不过需要考虑怎么解决通配符的问题……
# >>> b"\xf1\xf2".decode("cp437")
# '±≥'
# 这个能直接拿正则跑，不过\w不知道能不能匹配
# 暂且先不考虑吧

class treeNode():
    def __init__(self, value: str = "") -> None:
        self._val = value
        self._pre = None
        self._suc = []
        self._cnt = 0
        self._repeat_cnt = [1, 1]

    def val(self) -> str:
        """
        获取节点的值
        """
        return self._val

    def suc(self) -> List[treeNode]:
        """
        获取节点的子节点集合
        suc means successor
        应该叫child的，麻了
        """
        return self._suc

    def cnt(self) -> int:
        """
        获取节点的计数值
        """
        return self._cnt

    def pre(self) -> Union[treeNode, None]:
        """
        获取节点的父节点
        """
        return self._pre

    def repeat_cnt(self) -> List[int]:
        """
        返回这个节点的重复次数，可能有多个值
        """
        return self._repeat_cnt

    def set_val(self, value: str) -> None:
        """
        设置节点的值
        """
        self._val = value

    def set_pre(self, pre: treeNode) -> None:
        """
        设置节点的父节点
        """
        self._pre = pre

    def inc_cnt(self, cnt: int = 1) -> None:
        """
        增加节点的计数值
        """
        self._cnt += cnt

    def dec_cnt(self, cnt: int = 1) -> None:
        """
        减少节点的计数值
        """
        self._cnt -= cnt

    def set_repeat_cnt(self, repeat_cnt: List[int]) -> None:
        """
        设置节点的重复次数
        """
        assert len(repeat_cnt) == 2
        self._repeat_cnt = repeat_cnt
    
    def add_repeat_cnt(self, repeat_cnt: List[int]) -> None:
        """
        添加节点的重复次数
        """
        assert len(repeat_cnt) == 2
        self._repeat_cnt[0] += repeat_cnt[0]
        self._repeat_cnt[1] += repeat_cnt[1]

    def get_suc_by_value(self, value: str) -> Union[treeNode, None]:
        """
        根据值获取节点的子节点
        """
        for node in self._suc:
            if node.val() == value:
                return node
        return None

    def get_suc_by_value_ensure_exist(self, value: str) -> treeNode:
        """
        根据值获取节点的子节点，如果不存在则报错
        这个函数实际上是给pylance看的
        麻了
        """
        node = self.get_suc_by_value(value)
        if node is None:
            logging.error("=====节点不存在=====")
            print(f"试图节点{self}的不存在的子节点，值为{value}")
            raise Exception("value not found")
        return node

    def set_suc(self, suc_node: treeNode, update_value: int = 1, is_update_cnt: bool = True) -> None:
        """
        设置节点的子节点
        这个函数包括了更新父节点计数的代码，不要重复
        """
        if suc_node in self._suc:
            # 如果已经存在了一个值相同的节点，那么就不需要新建节点了
            if is_update_cnt:
                self.inc_cnt(update_value)
        else:
            # 这个是针对新建的节点
            self._suc.append(suc_node)
            if is_update_cnt:
                self.inc_cnt(update_value)  # 增加节点的计数
            suc_node.set_pre(self)
            # suc_node.inc_cnt(update_value) # 增加前驱结点的计数，会出问题

    def set_suc_by_value(self, value: str, update_suc_cnt: bool = False) -> None:
        """
        根据值设置节点的子节点
        """
        logging.debug(f"insert node value {value}")
        logging.debug(f"this node is {self}, node value {self._val}")
        for node in self._suc:
            if node.val() == value:
                logging.debug(f"existing node {node}")
                logging.debug(f"inserting to this node")
                node.inc_cnt()
                self.set_suc(node, is_update_cnt=update_suc_cnt)
                return
        # 如果没有找到那么就新建一个节点
        logging.debug(f"no existing node found")
        new_node = treeNode(value)
        new_node.inc_cnt()
        logging.debug(f"creating new node {new_node}")
        self.set_suc(new_node, is_update_cnt=update_suc_cnt)

    def del_suc(self, suc_node: treeNode) -> None:
        """
        删除节点的子节点
        然而对于需要删除子节点的情况，父节点应当是不具有其他的子节点的
        """
        if suc_node in self._suc:
            temp_nodes = suc_node.suc()
            self._suc.remove(suc_node)
            for node in temp_nodes:
                # 删除一条链中的某个节点应当不会影响权重
                self.set_suc(node, False)
            # 防止合并之后出现冲突
            self.ensure_suc_value_unique()
        else:
            logging.error("=====节点不存在=====")
            print(f"试图删除非节点{self}的子节点{suc_node}")
            self._print_trace()

    def merge_node(self, node: treeNode, is_root: bool = False, is_update_cnt: bool = False) -> None:
        """
        将node合并到self
        注意直接merge两棵树的根节点会出现问题，在这种情况下请设置is_root=True
        """
        # 如果出现了node的某个子节点值和self的某个子节点相同
        # 那么merge时需要保证这两个子节点的子节点也不会出现冲突
        if node.repeat_cnt() != []:
            # 合并节点的重复次数
            value_list = self.repeat_cnt()
            for value in node.repeat_cnt():
                value_list.append(value)
            self.set_repeat_cnt([min(value_list), max(value_list)])
        for suc_node in node.suc():
            exist = False
            for self_suc_node in self._suc:
                if suc_node.val() == self_suc_node.val():
                    # 递归地合并子节点
                    self_suc_node.merge_node(suc_node)
                    # 需要手动更新权重
                    self_suc_node.inc_cnt(suc_node.cnt())
                    if is_root | is_update_cnt:  # 难绷 # 又打了个补丁，更难绷
                        self.inc_cnt(suc_node.cnt())
                    exist = True
                    break
            if not exist:
                self.set_suc(suc_node, node.cnt(), is_update_cnt=is_root | is_update_cnt)

    def del_suc_by_value(self, value: str) -> None:
        """
        根据值删除子节点
        每个子节点的值必定是不同的，但是也不一定……
        节点的“升级”会导致出现相同值的子节点，这个需要保证不会出现
        """
        self.ensure_suc_value_unique()
        for node in self._suc:
            if node.val() == value:
                self.del_suc(node)
                return
        logging.error("=====节点不存在=====")
        print(f"试图删除节点{self}的值为{value}的子节点")
        self._print_trace()

    def cut_suc(self, suc_node: treeNode) -> None:
        """
        剪枝——删除suc_node对应的枝
        """
        if suc_node not in self._suc:
            logging.error("=====节点不存在=====")
            print(f"试图剪枝节点{self}的子节点{suc_node}")
            self._print_trace()
            return
        node_cnt = suc_node.cnt()
        self._suc.remove(suc_node)
        pointer = self
        while pointer != None:
            # 写出了C语言指针的感觉，绷
            pointer.dec_cnt(node_cnt)
            pointer = pointer.pre()

    def ensure_suc_value_unique(self) -> None:
        """
        确保节点的子节点的值是不同的
        """
        value_set = {}
        for node in self._suc:
            if node.val() in value_set:
                value_set[node.val()].merge_node(node, is_update_cnt=True)
                self._suc.remove(node)
            else:
                value_set[node.val()] = node
        for node in self._suc:
            node.ensure_suc_value_unique()

    def create_pattern(self, repeat_thres: int) -> str:
        """
        从节点创建正则表达式
        """
        pattern = self._val
        if self.repeat_cnt()[0] != 1 and self.repeat_cnt()[1] != 1:
            if self.repeat_cnt()[0] == self.repeat_cnt()[1]:
                pattern += "{"
                pattern += f"{self.repeat_cnt()[0]}"
                pattern += "}"
            elif self.repeat_cnt()[1] - self.repeat_cnt()[0] > repeat_thres:
                pattern = f"({pattern}*)"
            else:
                pattern += "{" + f"{self.repeat_cnt()[0]},{self.repeat_cnt()[1]}" + "}"
        if len(self._suc) == 0:
            return pattern
        elif len(self._suc) == 1:
            return pattern + self._suc[0].create_pattern(repeat_thres)
        else:
            pattern += "("
            for node in self._suc:
                # 递归的生成
                pattern += node.create_pattern(repeat_thres)
                pattern += "|"
            pattern = pattern[:-1]
            pattern += ")"
            return pattern

    def cut_suc_on_condition(self, thres: float, func: Callable[[List[treeNode]], Dict[treeNode, float]]) -> None:
        """
        剪枝——根据条件剪枝
        """
        score_dict = func(self._suc)
        for node in score_dict:
            if score_dict[node] < thres:
                self.cut_suc(node)

    def do_cut_suc(self, thres: float, func: Callable[[List[treeNode]], Dict[treeNode, float]]) -> None:
        """
        递归地进行剪枝
        """
        if len(self._suc) > 0:  # in case divided by zero
            self.cut_suc_on_condition(thres, func)
            for suc_node in self._suc:
                suc_node.do_cut_suc(thres, func)

    def _check_repeat(self, repeat_thres: int) -> Tuple[bool, treeNode, int]:
        """
        检查重复模式的节点，从当前节点开始(需要保证当前节点只有一个后继结点)
        返回一个Tuple，如果包含重复模式，则返回包含了True和重复模式开始的节点和重复的次数。
        否则返回False和下一个等待判断的节点还有0
        如果下一个等待判断的节点是本身，那就可以结束这个分支的检查了（非常无聊的设置）
        ! 有bug，输入样例"aaabbb"触发，我没找着问题在哪里
        TODO: 修bug
        """
        if len(self._suc) != 1:
            logging.error(
                "You should call the _check_repeat method ONLY WHEN THE NODE ONLY HAS ONE SUCCESSOR!")
            return False, self, 0
        repeat = 1
        pointer = self._suc[0]
        saved_pointer = self
        while repeat < repeat_thres:
            if len(pointer.suc()) == 0:
                logging.debug(
                    "encouter terminal node, no need to continue, return self")
                return False, self, 0
            if len(pointer.suc()) != 1:
                return False, pointer, 0
            if pointer.val() != saved_pointer._val:  # 遇到不一样的值，重新计数
                repeat = 1
                saved_pointer = pointer
            else:
                repeat += 1
            pointer = pointer.suc()[0]
        # 如果到了这里则意味着已经出现了需要替换的重复模式
        while pointer.val() == saved_pointer.val():
            repeat += 1
            if len(pointer.suc()) != 1: # 如果并到while的条件里就会漏掉末尾的匹配
                break
            pointer = pointer.suc()[0]
        return True, saved_pointer, repeat

    def do_remove_repeat_pattern(self, thres: int) -> None:
        """
        删除重复的节点
        """
        if len(self._suc) == 1:
            status, next_node, repeat_cnt = self._check_repeat(thres)
            if status:
                # next_node肯定只有一个子节点
                for _ in range(repeat_cnt - 1):  # 重复了n次只要删掉n-1个就行了嘛
                    next_node.add_repeat_cnt(next_node.suc()[0].repeat_cnt())
                    next_node.del_suc(next_node.suc()[0])  # 我有预感这里会爆bug
                # 继续去递归检查是否有重复模式
                next_node.do_remove_repeat_pattern(thres)
            else:
                if next_node == self:
                    # 这个分支没有重复的模式了
                    return
                else:
                    # 到下一个有分支的节点去检查
                    next_node.do_remove_repeat_pattern(thres)
        else:
            # 这个是有分支的情况，那么只要对每个分支进行检查就行了
            for suc_node in self._suc:
                suc_node.do_remove_repeat_pattern(thres)

    def search_for_delimiter(self, delimiter: List[str], delimiter_group: Dict[str, List[treeNode]]) -> None:
        """
        递归搜索节点分支中的分界符
        """
        if len(self._suc) == 0:
            # 这是叶子节点的情况
            if "" in delimiter_group:
                delimiter_group[""].append(self)
            else:
                delimiter_group[""] = [self]
            return
        for node in self._suc:
            if node.val() in delimiter:
                # 如果遇到定界符了就直接存储
                if node.val() in delimiter_group:
                    delimiter_group[node.val()].append(node)
                else:
                    delimiter_group[node.val()] = [node]
            else:
                # 要不然的话还是只能继续遍历
                node.search_for_delimiter(delimiter, delimiter_group)

    def recurse_for_upgrade(self, upgrade_func: Callable[[str], str], stop_node: Set[treeNode]) -> None:
        """
        递归更新节点的值
        upgrade_dict是一个升级的映射关系
        """
        if self in stop_node:
            return
        self._val = upgrade_func(self._val)
        for suc_node in self._suc:
            suc_node.recurse_for_upgrade(upgrade_func, stop_node)

    def upgrade_node(self, upgrade_thres: int, delimiter: List[str], upgrade_func: Callable[[str], str]) -> None:
        """
        将匹配特定字符的节点改成通配符节点
        """
        if len(self._suc) == 0:
            # 叶节点
            return
        elif len(self._suc) == 1:
            # 只有一个子节点
            # 继续向下递归
            self._suc[0].upgrade_node(upgrade_thres, delimiter, upgrade_func)
        elif len(self._suc) >= upgrade_thres:
            # 有多个节点且超过了阈值
            # 去寻找分界符，也就是框架前一步提取出来的常见词汇
            # 在各个节点中查找定界符，按照下一个遇到的定界符进行分组
            # 如果没有分界符那就会一直走到结束
            # delimiter_group 维护一个对照表：
            # 定界符d -> [下一个就是定界符d的分支中定界符对应的节点]
            # 实际上我们还需要考虑一个特殊的定界也就是字符串末尾的情况
            # 这种情况定界符可以理解成""
            # 这部分功能调用search_for_delimiter函数实现
            delimiter_group = {}
            self.search_for_delimiter(delimiter, delimiter_group)
            # 接下来对每个定界符对应的节点分组向前进行迭代
            # 举个例子，定界符是delimiter：
            #       aaaaabbbb},"delimiter
            #       abcdef012},"delimiter
            #                ^
            # 那么光标就从定界符的位置向前移动，每次移动一个节点，
            # ~~直到各个分支中光标位置的元素值不同~~
            # 直到当前节点为止
            stop_position = set()
            # 这些停止的位置会被加入到stop_position中
            # 这些可以用来标记节点修改的范围
            # 这是一个比较保守的办法，但是可以尽可能避免出问题
            # 其实还能更加激进一些
            for key in delimiter_group:
                node_group = delimiter_group[key]
                # 对每个分组进行迭代
                continue_flag = True
                while True:
                    common_value = node_group[0].val()
                    # 首先所有的节点值应该是一样的，并且最多最多到当前节点的下一个就得停下来
                    for node in node_group:
                        if node.val() != common_value or node.pre() == self:
                            continue_flag = False
                            break
                    if not continue_flag:
                        break
                    # 接下来就是向前移动一个节点
                    new_node_group = []
                    for node in node_group:
                        if node.pre() not in new_node_group:
                            new_node_group.append(node.pre())
                    node_group = new_node_group
                    if node_group == []:
                        break
                for node in node_group:
                    for suc_node in node.suc():
                        stop_position.add(suc_node)
            # 把每个节点换成“更高级的”节点
            for node in self._suc:
                node.recurse_for_upgrade(upgrade_func, stop_position)
            self.ensure_suc_value_unique()
            # 继续向下递归
            for node in self._suc:
                node.upgrade_node(upgrade_thres, delimiter, upgrade_func)
        else:
            for node in self._suc:
                node.upgrade_node(upgrade_thres, delimiter, upgrade_func)

    def _print_trace(self) -> None:
        """
        调试用，希望见不到
        """
        logging.error(f"父节点{self}")
        logging.error(f"- 值：{self.val()}")
        logging.error(f"- 前驱结点：{self.pre()}")
        logging.error("- 后继结点列表：\n{}".format("-- {}:value: {}".format(node, node.val())
              for node in self.suc()))
        logging.error("==================")

    def print_node_info(self, tab: int = 1) -> None:
        """
        调试用，递归地打印节点
        """
        tab_str = "--" * tab
        logging.info(
            tab_str + f" val：\033[31m{self.val()}\033[0m cnt：\033[32m{self.cnt()}\033[0m " +
            f"repeat：\033[33m{self.repeat_cnt()}\033[0m childs：\033[34m{len(self._suc)}\033[0m")
        for suc_node in self._suc:
            suc_node.print_node_info(tab + 1)


class trieTree():
    def __init__(self, dataset: List[List[str]], delimiter: List[str],
                 cut_func: Callable[[List[treeNode]], Dict[treeNode, float]],
                 cut_thres: float, repeat_thres: int, repeat_cnt_thres: int,
                 upgrade_thres: int, upgrade_func: Callable[[str], str]) -> None:
        """
        建立用于生成正则的字典树。
        这个类实际上是对于treeNode的包装（我感觉）

        参数定义：
            dataset：用于建立字典树的数据集
            delimiter：分界符
            cut_func：用于判断剪枝情况的函数
            cut_thres：剪枝情况的阈值
            repeat_thres：需要合并的重复次数，超过了这个重复次数的单个字符会合并为<pattern>{repeat_time1, repeat_time2,...}
            repeat_cnt_thres：用于合并过多的重复次数模式，如果重复次数的模式过多，则会生成<pattern>*形式的正则
            upgrade_thres：用于将出现的普通的字符串模式替换为通配符
            upgrade_func：将出现的普通字符串模式转换为通配符的函数，可自定义
        """
        self._root = treeNode()
        self._dataset = dataset
        for data in self._dataset:
            logging.debug(f"insert {data}")
            self.insert(data)
        self._cut_func = cut_func
        self._delimiter = delimiter
        self._cut_thres = cut_thres
        self._repeat_thres = repeat_thres
        self._repeat_cnt_thres = repeat_cnt_thres
        self._upgrade_thres = upgrade_thres
        self._upgrade_func = upgrade_func

    def get_root(self) -> treeNode:
        """
        获取根节点
        """
        return self._root

    def get_dataset(self) -> List[List[str]]:
        """
        获取数据集
        """
        return self._dataset

    def get_delimiter(self) -> List[str]:
        """
        获取分隔符
        """
        return self._delimiter

    def get_cut_func(self) -> Callable[[List[treeNode]], Dict[treeNode, float]]:
        """
        获取剪枝函数
        """
        return self._cut_func

    def get_thres(self) -> float:
        """
        获取剪枝阈值
        """
        return self._cut_thres

    def insert(self, data: List[str]) -> None:
        """
        插入数据
        """
        pointer = self.get_root()
        is_root = True
        for value in data:
            pointer.set_suc_by_value(value, is_root)
            pointer = pointer.get_suc_by_value_ensure_exist(value)
            is_root = False

    def create_regex(self) -> str:
        """
        通过字典树创建正则表达式
        """
        return self.get_root().create_pattern(repeat_thres=self._repeat_cnt_thres)

    def cut_suc(self) -> None:
        self._root.do_cut_suc(self._cut_thres, self._cut_func)

    def merge_repeat(self) -> None:
        self._root.do_remove_repeat_pattern(self._repeat_thres)

    def upgrade_node(self) -> None:
        self._root.upgrade_node(self._upgrade_thres, self._delimiter, self._upgrade_func)

    def iter(self, epoch: int = 1) -> None:
        for ep in range(epoch):
            # print("=======================")
            # print(f"         {ep}")
            # print("=======================")
            self.cut_suc()
            self.upgrade_node()
            self.merge_repeat()
            # print(len(self.create_regex()))
            # self.print_info()
            #print(self.create_regex())

    def print_info(self) -> None:
        """
        打印树信息
        """
        self._root.print_node_info()


def example_cut_condition_func(suc: List[treeNode]) -> Dict[treeNode, float]:
    """
    示例剪枝条件函数
    """
    node_sum = 0
    for node in suc:
        node_sum += node.cnt()
    node_avg = node_sum / len(suc)
    score_dict = {}
    for node in suc:
        score_dict[node] = node.cnt() / node_avg
    return score_dict

def example_upgrade_func(value: str) -> str:
    """
    示例升级函数
    """
    import string
    if value in "0123456789":
        return r"\d"
    if value in string.ascii_lowercase:
        return r"[a-z]"
    if value in string.ascii_uppercase:
        return r"[A-Z]"
    if value == "_" or value == "[a-z]" or value == "[A-Z]" or value == r"\d":
        return r"\w"
    return "."