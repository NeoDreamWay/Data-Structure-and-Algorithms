import matplotlib.pyplot as plt
import matplotlib.patches as patches


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class BST:
    def __init__(self):
        self.root = None

    def insert(self, val):
        """插入节点到BST"""
        if not self.root:
            self.root = TreeNode(val)
            return

        node = self.root
        while True:
            if val < node.val:
                if node.left:
                    node = node.left
                else:
                    node.left = TreeNode(val)
                    return
            else:
                if node.right:
                    node = node.right
                else:
                    node.right = TreeNode(val)
                    return

    def find_max(self, node):
        """找子树中的最大值（中序前驱）"""
        while node.right:
            node = node.right
        return node

    def find_min(self, node):
        """找子树中的最小值（中序后继）"""
        while node.left:
            node = node.left
        return node

    def delete_predecessor(self, root, val):
        """删除节点，用中序前驱替换"""
        if not root:
            return None

        if val < root.val:
            root.left = self.delete_predecessor(root.left, val)
        elif val > root.val:
            root.right = self.delete_predecessor(root.right, val)
        else:
            # 找到要删除的节点
            if not root.left:
                return root.right
            if not root.right:
                return root.left

            # 用中序前驱（左子树最大值）替换
            predecessor = self.find_max(root.left)
            root.val = predecessor.val
            root.left = self.delete_predecessor(root.left, predecessor.val)

        return root

    def delete_successor(self, root, val):
        """删除节点，用中序后继替换"""
        if not root:
            return None

        if val < root.val:
            root.left = self.delete_successor(root.left, val)
        elif val > root.val:
            root.right = self.delete_successor(root.right, val)
        else:
            # 找到要删除的节点
            if not root.left:
                return root.right
            if not root.right:
                return root.left

            # 用中序后继（右子树最小值）替换
            successor = self.find_min(root.right)
            root.val = successor.val
            root.right = self.delete_successor(root.right, successor.val)

        return root

    def inorder(self, root):
        """中序遍历"""
        result = []
        if root:
            result.extend(self.inorder(root.left))
            result.append(root.val)
            result.extend(self.inorder(root.right))
        return result


def draw_tree(root, title="BST", filename="bst.png"):
    """使用matplotlib绘制二叉树"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 9))
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
        circle = patches.Circle((x, y), node_radius, facecolor='#2196F3',
                                edgecolor='#1565C0', linewidth=2, zorder=2)
        ax.add_patch(circle)

        # 写节点值
        ax.text(x, y, str(node.val), ha='center', va='center',
                fontsize=11, fontweight='bold', color='white', zorder=3)

        # 递归画子节点
        spread = 35 / (2 ** level)
        child_y = y - 16

        if node.left:
            draw_node(node.left, x - spread, child_y, level + 1, x, y)
        if node.right:
            draw_node(node.right, x + spread, child_y, level + 1, x, y)

    draw_node(root, 50, 88, 0)
    ax.text(50, 97, title, ha='center', va='center',
            fontsize=16, fontweight='bold', color='#333333')

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.show()
    print(f"已保存: {filename}")


# ==================== 主程序 ====================

# 任务1：依次插入序列，画出最终BST
print("=" * 50)
print("任务1：依次插入 [50, 30, 70, 20, 40, 60, 80]")
print("=" * 50)

bst1 = BST()
insert_sequence = [50, 30, 70, 20, 40, 60, 80]
for val in insert_sequence:
    bst1.insert(val)
    print(f"插入 {val} 后，中序遍历: {bst1.inorder(bst1.root)}")

draw_tree(bst1.root, title="BST 插入序列 [50,30,70,20,40,60,80]",
          filename="bst_insert.png")

# 任务2：删除根节点50，两种策略
print("\n" + "=" * 50)
print("任务2：删除根节点 50")
print("=" * 50)

# 策略1：中序前驱
bst_pre = BST()
for val in insert_sequence:
    bst_pre.insert(val)
print(f"删除前中序遍历: {bst_pre.inorder(bst_pre.root)}")

predecessor = bst_pre.find_max(bst_pre.root.left)
print(f"中序前驱（左子树最大值）: {predecessor.val}")

bst_pre.root = bst_pre.delete_predecessor(bst_pre.root, 50)
print(f"用中序前驱替换后中序遍历: {bst_pre.inorder(bst_pre.root)}")
draw_tree(bst_pre.root, title="删除50 - 中序前驱策略（40替换）",
          filename="bst_delete_predecessor.png")

# 策略2：中序后继
bst_suc = BST()
for val in insert_sequence:
    bst_suc.insert(val)

successor = bst_suc.find_min(bst_suc.root.right)
print(f"\n中序后继（右子树最小值）: {successor.val}")

bst_suc.root = bst_suc.delete_successor(bst_suc.root, 50)
print(f"用中序后继替换后中序遍历: {bst_suc.inorder(bst_suc.root)}")
draw_tree(bst_suc.root, title="删除50 - 中序后继策略（60替换）",
          filename="bst_delete_successor.png")


print("""
能混用,但是不推荐。

两种策略各自都能独立保证BST性质，替换后中序遍历仍然有序，所以每次删除时选哪种都可以。
但不推荐混用的原因在于：混用后树的结构变得随机不可预测，同一操作序列可能产生完全不同的树，
不利于调试和测试，也让平衡性更难保证。
实际工程中通常固定选用一种策略，一般选中序后继，代码更简洁；
教学或作业中则按题目要求或固定用一种即可。
需要维持平衡时，可根据左右子树高度差决定，左子树更高用中序前驱，右子树更高用中序后继。
总之，能混用，但固定用一种更规范。
""")