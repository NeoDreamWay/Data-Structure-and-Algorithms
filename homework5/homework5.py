"""
链表节点删除功能实现
实现链表的节点追加、指定值删除、链表展示功能
"""


class Node:
    """链表节点类"""

    def __init__(self, data):
        self.data = data  # 节点存储的数据
        self.next = None  # 指向下一个节点的指针


class LinkedList:
    """链表类"""

    def __init__(self):
        self.head = None  # 链表头节点

    def append(self, value):
        """向链表尾部追加新节点"""
        # 创建新节点
        new_node = Node(value)

        # 空链表时，新节点作为头节点
        if self.head is None:
            self.head = new_node
            return

        # 遍历到链表尾部
        current = self.head
        while current.next:
            current = current.next

        # 将尾部节点的next指向新节点
        current.next = new_node

    def delete(self, value):
        """删除链表中第一个值为value的节点
        返回值：成功删除返回True，未找到返回False
        """
        # 空链表直接返回False
        if self.head is None:
            return False

        # 要删除的是头节点
        if self.head.data == value:
            self.head = self.head.next
            return True

        # 遍历链表查找目标节点
        prev_node = self.head  # 前驱节点
        current_node = self.head.next  # 当前节点

        while current_node:
            if current_node.data == value:
                # 跳过当前节点（删除）
                prev_node.next = current_node.next
                return True
            # 移动指针
            prev_node = current_node
            current_node = current_node.next

        # 未找到目标值
        return False

    def display(self):
        """展示链表所有节点数据"""
        current = self.head
        data_list = []

        # 遍历收集所有节点数据
        while current:
            data_list.append(str(current.data))
            current = current.next

        # 格式化输出
        print(" -> ".join(data_list) if data_list else "空链表")


def main():
    """主函数：测试链表功能"""
    # 创建链表实例
    link_list = LinkedList()

    # 追加初始节点
    for num in [10, 20, 30, 40, 50]:
        link_list.append(num)

    # 展示删除前的链表
    print("删除前：")
    link_list.display()

    # 删除值为30的节点
    link_list.delete(30)

    # 展示删除后的链表
    print("删除30后：")
    link_list.display()

    # 尝试删除不存在的节点（100）
    print("删除100：", link_list.delete(100))


# 程序入口
if __name__ == "__main__":
    main()