"""
最小生成树 (MST) - Prim 和 Kruskal 算法实现

图结构:
    A --2-- B --4-- C
    |        |        |
    3        1        5
    |        |        |
    D --6-- E --2-- F

边列表: (u, v, weight)
"""

import heapq


# 图的边定义
edges = [
    ('A', 'B', 2),
    ('A', 'D', 3),
    ('B', 'C', 4),
    ('B', 'E', 1),
    ('C', 'F', 5),
    ('D', 'E', 6),
    ('E', 'F', 2),
]

vertices = ['A', 'B', 'C', 'D', 'E', 'F']

# 构建邻接表
adj = {v: [] for v in vertices}
for u, v, w in edges:
    adj[u].append((v, w))
    adj[v].append((u, w))


# ==================== Prim 算法 ====================
def prim(start='A'):
    """
    Prim算法：从起点开始，每次选连接已选集合的最小边
    时间复杂度: O(E log V)
    """
    mst = []
    visited = set([start])
    pq = []

    # 初始化优先队列，加入起点的所有邻接边
    for neighbor, weight in adj[start]:
        heapq.heappush(pq, (weight, start, neighbor))

    total_weight = 0

    while pq and len(visited) < len(vertices):
        weight, u, v = heapq.heappop(pq)

        if v in visited:
            continue

        visited.add(v)
        mst.append((u, v, weight))
        total_weight += weight

        # 加入新顶点v的所有邻接边
        for neighbor, w in adj[v]:
            if neighbor not in visited:
                heapq.heappush(pq, (w, v, neighbor))

    return mst, total_weight


# ==================== Kruskal 算法 ====================
class UnionFind:
    """并查集"""
    def __init__(self):
        self.parent = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            self.parent[px] = py
            return True
        return False


def kruskal():
    """
    Kruskal算法：按权重排序，每次选不形成环的最小边
    时间复杂度: O(E log E)
    """
    sorted_edges = sorted(edges, key=lambda x: x[2])

    uf = UnionFind()
    mst = []
    total_weight = 0

    for u, v, w in sorted_edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            total_weight += w
            if len(mst) == len(vertices) - 1:
                break

    return mst, total_weight


# ==================== 主函数 ====================
def main():
    print("=" * 60)
    print("最小生成树 (MST) - Prim 和 Kruskal 算法")
    print("=" * 60)

    print("\n图结构:")
    print("    A --2-- B --4-- C")
    print("    |        |        |")
    print("    3        1        5")
    print("    |        |        |")
    print("    D --6-- E --2-- F")

    print("\n" + "=" * 60)
    print("Prim 算法")
    print("=" * 60)
    prim_mst, prim_weight = prim('A')
    print(f"起点: A")
    for i, (u, v, w) in enumerate(prim_mst, 1):
        print(f"  第{i}步: 选边 ({u}, {v}) = {w}")
    print(f"MST 总权重: {prim_weight}")

    print("\n" + "=" * 60)
    print("Kruskal 算法")
    print("=" * 60)
    print("边按权重排序:")
    sorted_edges = sorted(edges, key=lambda x: x[2])
    for u, v, w in sorted_edges:
        print(f"  ({u}, {v}) = {w}")
    print()
    kruskal_mst, kruskal_weight = kruskal()
    for i, (u, v, w) in enumerate(kruskal_mst, 1):
        print(f"  第{i}步: 选边 ({u}, {v}) = {w}")
    print(f"MST 总权重: {kruskal_weight}")

    print("\n" + "=" * 60)
    print("结果对比")
    print("=" * 60)
    print(f"Prim MST 权重:   {prim_weight}")
    print(f"Kruskal MST 权重: {kruskal_weight}")
    print(f"两种算法结果一致: {'是' if prim_weight == kruskal_weight else '否'}")


if __name__ == "__main__":
    main()
