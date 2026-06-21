"""
B-Tree 构建与可视化 (m=3)
插入序列: [10, 20, 5, 6, 12, 30, 25]
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch


class BTreeNode:
    """B-Tree节点"""
    def __init__(self, leaf=False):
        self.keys = []        # 键值列表（升序）
        self.children = []    # 子节点列表
        self.leaf = leaf      # 是否为叶子节点


class BTree:
    """B-Tree实现 (m阶)"""
    def __init__(self, m=3):
        self.m = m
        self.min_keys = (m // 2) - 1   # 最小键数 = 1 (m=3)
        self.max_keys = m - 1           # 最大键数 = 2 (m=3)
        self.root = BTreeNode(leaf=True)

    def insert(self, key):
        """插入键值"""
        root = self.root
        if len(root.keys) == self.max_keys:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(self.root)
            self.root = new_root
            self._split(new_root, 0)
            self._insert_non_full(new_root, key)
        else:
            self._insert_non_full(root, key)

    def _insert_non_full(self, node, key):
        """向非满节点插入"""
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == self.max_keys:
                self._split(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key)

    def _split(self, parent, i):
        """分裂parent的第i个子节点"""
        m = self.m
        t = (m + 1) // 2          # t = 2 (m=3时)
        y = parent.children[i]
        z = BTreeNode(leaf=y.leaf)
        mid_index = t - 1         # 中间键的索引 = 1

        z.keys = y.keys[mid_index + 1:]
        mid_key = y.keys[mid_index]
        y.keys = y.keys[:mid_index]

        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

        parent.keys.insert(i, mid_key)
        parent.children.insert(i + 1, z)

    def inorder(self):
        """中序遍历获取所有键值"""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            for i in range(len(node.keys)):
                if not node.leaf and i < len(node.children):
                    self._inorder(node.children[i], result)
                result.append(node.keys[i])
            if not node.leaf and len(node.children) > len(node.keys):
                self._inorder(node.children[-1], result)

    def validate(self):
        """验证B-Tree所有性质"""
        errors = []

        def check_node(node, depth=0, min_key=None, max_key=None):
            # 性质1: 非根节点键数 >= min_keys
            if node != self.root:
                if len(node.keys) < self.min_keys:
                    errors.append(f"节点{node.keys}键数{len(node.keys)} < 最小{self.min_keys}")

            # 性质2: 所有节点键数 <= max_keys
            if len(node.keys) > self.max_keys:
                errors.append(f"节点{node.keys}键数{len(node.keys)} > 最大{self.max_keys}")

            # 性质3: 键值升序
            for i in range(1, len(node.keys)):
                if node.keys[i] <= node.keys[i-1]:
                    errors.append(f"节点{node.keys}键值非升序")

            # 性质4: 非叶子节点的孩子数 = 键数 + 1
            if not node.leaf:
                if len(node.children) != len(node.keys) + 1:
                    errors.append(f"节点{node.keys}孩子数{len(node.children)} != 键数+1")

                # 性质5: 子节点键值范围检查
                for i, child in enumerate(node.children):
                    child_min = node.keys[i-1] if i > 0 else min_key
                    child_max = node.keys[i] if i < len(node.keys) else max_key
                    for k in child.keys:
                        if child_min is not None and k <= child_min:
                            errors.append(f"子节点键{k} <= 最小边界{child_min}")
                        if child_max is not None and k >= child_max:
                            errors.append(f"子节点键{k} >= 最大边界{child_max}")
                    check_node(child, depth + 1, child_min, child_max)

        # 性质6: 所有叶子节点在同一深度
        leaf_depths = []
        def collect_depths(node, depth=0):
            if node.leaf:
                leaf_depths.append(depth)
            else:
                for child in node.children:
                    collect_depths(child, depth + 1)

        collect_depths(self.root)
        if len(set(leaf_depths)) > 1:
            errors.append(f"叶子节点深度不一致: {leaf_depths}")

        check_node(self.root)
        return errors


def draw_btree(node, ax, x, y, level=0, parent_x=None, parent_y=None, node_width=5, node_height=2.2):
    """递归绘制B-Tree节点"""
    if not node:
        return x

    n_keys = len(node.keys)
    width = n_keys * node_width + 0.3

    # 绘制节点矩形
    rect = FancyBboxPatch((x - width/2, y - node_height/2), width, node_height,
                          boxstyle="round,pad=0.15", 
                          facecolor='#E3F2FD' if not node.leaf else '#C8E6C9',
                          edgecolor='#1565C0' if not node.leaf else '#2E7D32',
                          linewidth=2.5, zorder=2)
    ax.add_patch(rect)

    # 键值分隔线
    for i in range(1, n_keys):
        sep_x = x - width/2 + i * node_width
        ax.plot([sep_x, sep_x], [y - node_height/2 + 0.15, y + node_height/2 - 0.15], 
               'k-', linewidth=1.5, zorder=3)

    # 绘制键值
    for i, key in enumerate(node.keys):
        key_x = x - width/2 + (i + 0.5) * node_width
        ax.text(key_x, y, str(key), ha='center', va='center', 
               fontsize=14, fontweight='bold', color='#333', zorder=4)

    # 标注节点类型和孩子数
    label = "叶子" if node.leaf else f"内部({len(node.children)}子)"
    ax.text(x, y + node_height/2 + 0.6, label, ha='center', va='bottom', 
           fontsize=10, color='#555', fontweight='bold', zorder=4)

    # 画连线到父节点
    if parent_x is not None and parent_y is not None:
        ax.plot([parent_x, x], [parent_y - node_height/2 - 0.25, y + node_height/2 + 0.25], 
               'k-', linewidth=2, zorder=1)

    # 递归绘制子节点
    if not node.leaf and node.children:
        child_y = y - 6
        total_children = len(node.children)

        if total_children == 1:
            child_positions = [x]
        elif total_children == 2:
            spacing = 22
            child_positions = [x - spacing/2, x + spacing/2]
        elif total_children == 3:
            spacing = 18
            child_positions = [x - spacing, x, x + spacing]
        else:
            spacing = 14
            start_x = x - (total_children - 1) * spacing / 2
            child_positions = [start_x + i * spacing for i in range(total_children)]

        for i, child in enumerate(node.children):
            draw_btree(child, ax, child_positions[i], child_y, level + 1, x, y)

    return x


def visualize_btree(btree, title="B-Tree", filename="btree.png"):
    """可视化B-Tree"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    draw_btree(btree.root, ax, 50, 88)

    ax.text(50, 97, title, ha='center', va='center', 
           fontsize=18, fontweight='bold', color='#333')

    # 图例
    legend_y = 3
    ax.add_patch(FancyBboxPatch((5, legend_y - 0.9), 4.5, 1.8, boxstyle="round,pad=0.15",
                                facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=2))
    ax.text(10.5, legend_y, "内部节点", ha='left', va='center', fontsize=12, fontweight='bold')

    ax.add_patch(FancyBboxPatch((30, legend_y - 0.9), 4.5, 1.8, boxstyle="round,pad=0.15",
                                facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=2))
    ax.text(35.5, legend_y, "叶子节点", ha='left', va='center', fontsize=12, fontweight='bold')

    ax.text(70, legend_y, f"m={btree.m}  |  max_keys={btree.max_keys}  |  min_keys={btree.min_keys}", 
           ha='center', va='center', fontsize=12, color='#555', fontweight='bold')

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.show()
    print(f"已保存: {filename}")


def print_tree(node, indent=0):
    """打印树结构（文本形式）"""
    prefix = "  " * indent
    leaf_mark = "[叶子]" if node.leaf else "[内部]"
    print(f"{prefix}{leaf_mark} 键值={node.keys}, 孩子数={len(node.children)}")
    if not node.leaf:
        for i, child in enumerate(node.children):
            print(f"{prefix}  └─ 子节点[{i}]:")
            print_tree(child, indent + 4)


def main():
    print("=" * 60)
    print("B-Tree 构建与可视化 (m=3)")
    print("插入序列: [10, 20, 5, 6, 12, 30, 25]")
    print("=" * 60)

    btree = BTree(m=3)
    sequence = [10, 20, 5, 6, 12, 30, 25]

    for i, key in enumerate(sequence):
        print(f"\n--- 第{i+1}步: 插入 {key} ---")
        btree.insert(key)
        print(f"中序遍历: {btree.inorder()}")

    print(f"\n{'='*60}")
    print("最终B-Tree结构:")
    print(f"{'='*60}")
    print_tree(btree.root)

    visualize_btree(btree, title="3阶B-Tree: 插入序列 [10,20,5,6,12,30,25]", 
                    filename="btree_final.png")

    print(f"\n{'='*60}")
    print("B-Tree性质验证:")
    print(f"{'='*60}")
    errors = btree.validate()
    if errors:
        print("❌ 发现错误:")
        for e in errors:
            print(f"  - {e}")
    else:
        print("✅ 所有B-Tree性质均满足！")
        print(f"  • 阶数 m = {btree.m}")
        print(f"  • 最大键数 = {btree.max_keys}")
        print(f"  • 最小键数(非根) = {btree.min_keys}")
        print(f"  • 叶子节点深度相同")
        print(f"  • 所有键值升序排列")
        print(f"  • 中序遍历结果: {btree.inorder()}")


if __name__ == "__main__":
    main()
