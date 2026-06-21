import matplotlib.pyplot as plt
import matplotlib.patches as patches


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def array_to_bst(arr):
    """将数组按层序遍历还原为链表结构的二叉树"""
    if not arr or arr[0] is None:
        return None

    root = TreeNode(arr[0])
    queue = [root]
    i = 1

    while queue and i < len(arr):
        node = queue.pop(0)

        # 左子节点
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1

        # 右子节点
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            queue.append(node.right)
        i += 1

    return root


def draw_tree(root):
    """使用 matplotlib 绘制二叉树"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    def draw_node(node, x, y, level, parent_x=None, parent_y=None):
        if not node:
            return

        node_radius = 2.8

        # 画连线
        if parent_x is not None and parent_y is not None:
            ax.plot([parent_x, x], [parent_y - node_radius, y + node_radius],
                    'k-', linewidth=1.5, zorder=1)

        # 画节点圆圈
        circle = patches.Circle((x, y), node_radius, facecolor='#4CAF50',
                                edgecolor='#2E7D32', linewidth=2, zorder=2)
        ax.add_patch(circle)

        # 写节点值
        ax.text(x, y, str(node.val), ha='center', va='center',
                fontsize=11, fontweight='bold', color='white', zorder=3)

        # 递归画子节点
        spread = 30 / (2 ** level)
        child_y = y - 16

        if node.left:
            draw_node(node.left, x - spread, child_y, level + 1, x, y)
        if node.right:
            draw_node(node.right, x + spread, child_y, level + 1, x, y)

    draw_node(root, 50, 88, 0)
    ax.text(50, 97, '二叉树结构图', ha='center', va='center',
            fontsize=16, fontweight='bold', color='#333333')

    plt.tight_layout()
    plt.savefig('binary_tree.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.show()


# 主程序
arr = [10, 5, 15, 3, 7, None, 20]
root = array_to_bst(arr)
draw_tree(root)



print(r"""
          10
         /  \
        5    15
       / \     \
      3   7    20
    """)