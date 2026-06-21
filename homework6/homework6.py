class Node:
    """链表节点"""
    def __init__(self, value):
        self.value = value
        self.next = None


def build_linked_list(values):
    """根据数值列表构建链表"""
    if not values:
        return None
    head = Node(values[0])
    current = head
    for item in values[1:]:
        current.next = Node(item)
        current = current.next
    return head


def display_linked_list(head):
    """打印链表所有节点"""
    current = head
    while current:
        if current.next:
            print(current.value, end=" -> ")
        else:
            print(current.value)
        current = current.next


def remove_node(head, target_value):
    """
    删除链表中第一个值为 target_value 的节点
    使用哨兵节点简化头节点删除逻辑
    """
    sentinel = Node(0)
    sentinel.next = head
    previous = sentinel
    current = head

    while current:
        if current.value == target_value:
            previous.next = current.next
            break
        previous = current
        current = current.next

    return sentinel.next


def main():
    print("=" * 40)
    print("  链表节点删除工具")
    print("=" * 40)

    data = [10, 20, 30, 40, 50]
    head = build_linked_list(data)

    print("\n原始链表：")
    display_linked_list(head)

    try:
        target = int(input("\n请输入要删除的节点值："))
    except ValueError:
        print("输入错误！请输入整数。")
        return

    head = remove_node(head, target)

    print("\n删除后的链表：")
    display_linked_list(head)

    print("=" * 40)


if __name__ == "__main__":
    main()
