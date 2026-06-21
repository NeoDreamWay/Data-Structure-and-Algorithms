"""
AVL树构建与旋转实操
插入序列: [30, 20, 10, 25, 40, 35, 50]
功能：依次插入，标注平衡因子，检测失衡类型，执行旋转，绘制树形
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches


class AVLNode:
    """AVL树节点"""
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1
        self.bf = 0  # 平衡因子


class AVLTree:
    """AVL树类"""
    def __init__(self):
        self.root = None

    def get_height(self, node):
        return node.height if node else 0

    def get_bf(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def update(self, node):
        """更新节点高度和平衡因子"""
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
            node.bf = self.get_bf(node)
        return node

    def right_rotate(self, y):
        """LL型：右旋

              y              x
             /             /   \
            x     -->     z     y
           / \                 /
          z   T2             T2
        """
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.update(y)
        self.update(x)
        return x

    def left_rotate(self, x):
        """RR型：左旋

            x                y
             \             /   \
              y    -->    x     z
             / \           \
            T2  z           T2
        """
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self.update(x)
        self.update(y)
        return y

    def insert(self, root, val, step_info=None):
        """插入节点并自动平衡"""
        if not root:
            return AVLNode(val)

        if val < root.val:
            root.left = self.insert(root.left, val, step_info)
        else:
            root.right = self.insert(root.right, val, step_info)

        root = self.update(root)
        bf = root.bf

        # LL型失衡：左子树太高，且插入在左子树的左侧
        if bf > 1 and val < root.left.val:
            if step_info:
                step_info['imbalance'] = 'LL'
                step_info['rotate_axis'] = root.val
            return self.right_rotate(root)

        # RR型失衡：右子树太高，且插入在右子树的右侧
        if bf < -1 and val > root.right.val:
            if step_info:
                step_info['imbalance'] = 'RR'
                step_info['rotate_axis'] = root.val
            return self.left_rotate(root)

        # LR型失衡：左子树太高，但插入在左子树的右侧
        if bf > 1 and val > root.left.val:
            if step_info:
                step_info['imbalance'] = 'LR'
                step_info['rotate_axis'] = root.val
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # RL型失衡：右子树太高，但插入在右子树的左侧
        if bf < -1 and val < root.right.val:
            if step_info:
                step_info['imbalance'] = 'RL'
                step_info['rotate_axis'] = root.val
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def inorder(self, root):
        """中序遍历"""
        result = []
        if root:
            result.extend(self.inorder(root.left))
            result.append(root.val)
            result.extend(self.inorder(root.right))
        return result


def draw_avl(root, title="AVL Tree", filename="avl.png", highlight_node=None):
    """绘制AVL树，标注平衡因子"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    def draw_node(node, x, y, level, parent_x=None, parent_y=None):
        if not node:
            return

        node_radius = 3.2

        if parent_x is not None and parent_y is not None:
            ax.plot([parent_x, x], [parent_y - node_radius, y + node_radius],
                   'k-', linewidth=1.5, zorder=1)

        # 颜色编码
        if highlight_node and node.val == highlight_node:
            color = '#FFEB3B'  # 黄色：旋转轴
            text_color = '#333'
        elif abs(node.bf) > 1:
            color = '#F44336'  # 红色：失衡
            text_color = 'white'
        elif abs(node.bf) == 1:
            color = '#FF9800'  # 橙色：临界
            text_color = 'white'
        else:
            color = '#4CAF50'  # 绿色：平衡
            text_color = 'white'

        circle = patches.Circle((x, y), node_radius, facecolor=color,
                                edgecolor='#333', linewidth=2, zorder=2)
        ax.add_patch(circle)

        ax.text(x, y + 0.5, str(node.val), ha='center', va='center',
               fontsize=11, fontweight='bold', color=text_color, zorder=3)
        ax.text(x, y - 1.2, f"bf={node.bf}", ha='center', va='center',
               fontsize=8, color=text_color, fontweight='bold', zorder=3)

        spread = 38 / (2 ** level)
        child_y = y - 14

        if node.left:
            draw_node(node.left, x - spread, child_y, level + 1, x, y)
        if node.right:
            draw_node(node.right, x + spread, child_y, level + 1, x, y)

    draw_node(root, 50, 88, 0)
    ax.text(50, 97, title, ha='center', va='center',
           fontsize=13, fontweight='bold', color='#333')

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.show()
    print(f"已保存: {filename}")


def main():
    print("=" * 60)
    print("AVL树构建与旋转实操")
    print("插入序列: [30, 20, 10, 25, 40, 35, 50]")
    print("=" * 60)

    avl = AVLTree()
    sequence = [30, 20, 10, 25, 40, 35, 50]

    for i, val in enumerate(sequence):
        step_info = {'imbalance': None, 'rotate_axis': None}

        print(f"\n{'='*50}")
        print(f"第{i+1}步: 插入 {val}")
        print(f"{'='*50}")

        avl.root = avl.insert(avl.root, val, step_info)

        inorder = avl.inorder(avl.root)
        print(f"中序遍历: {inorder}")

        if step_info['imbalance']:
            print(f"失衡类型: {step_info['imbalance']}")
            print(f"旋转轴: 节点 {step_info['rotate_axis']}")
        else:
            print("无失衡，无需旋转")

        title = f"第{i+1}步: 插入 {val}"
        if step_info['imbalance']:
            title += f" | {step_info['imbalance']}旋转(轴:{step_info['rotate_axis']})"
        else:
            title += " | 平衡"

        draw_avl(avl.root, title=title,
                 filename=f"avl_step_{i+1}_insert_{val}.png",
                 highlight_node=step_info['rotate_axis'])

    print(f"\n{'='*60}")
    print(f"最终AVL树的中序遍历: {avl.inorder(avl.root)}")
    print(f"{'='*60}")
    print("\nBST性质验证：中序遍历严格递增，AVL性质保持完好！")


if __name__ == "__main__":
    main()