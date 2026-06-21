from typing import Iterable, Any

class RemoveItem:
    """删除列表中指定索引元素（手动移位实现，不使用pop/del）"""
    def __init__(self, iterable: Iterable[Any]) -> None:
        """
        :param iterable: 可迭代元素，内部转为列表存储
        """
        self.iterable = list(iterable)

    def remove(self, index_to_remove: int) -> list[Any]:
        """
        删除列表中指定索引
        :param index_to_remove: 需要删除的元素下标
        :return: 删除完成后的列表
        """
        length_of_iterable: int = len(self.iterable)
        # 从后往前移动元素覆盖待删除位置
        for i in range(index_to_remove, length_of_iterable - 1):
            self.iterable[i] = self.iterable[i + 1]
        # 截断最后一位多余元素
        self.iterable = self.iterable[:-1]
        return self.iterable


# 测试示例
if __name__ == "__main__":
    fruits = ['apple', 'banana', 'cherry', 'orange', 'mango']
    remove_item = RemoveItem(fruits)
    result = remove_item.remove(1)
    print(result)