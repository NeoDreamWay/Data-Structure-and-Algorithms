# 无向图的 DFS 与 BFS 遍历

## 题目

给定 5 个顶点 (A, B, C, D, E) 的无向图，写出从顶点 **A** 出发的 **DFS** 和 **BFS** 遍历序列。

> 提示：假设每个顶点的邻接点按**字母顺序**访问。

---

## 图的邻接关系

### 邻接表（按字母顺序排列邻接点）

```
A: [B, C]
B: [A, D]
C: [A, D, E]
D: [B, C, E]
E: [C, D]
```

### 邻接矩阵

|  | A | B | C | D | E |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **A** | 0 | 1 | 1 | 0 | 0 |
| **B** | 1 | 0 | 0 | 1 | 0 |
| **C** | 1 | 0 | 0 | 1 | 1 |
| **D** | 0 | 1 | 1 | 0 | 1 |
| **E** | 0 | 0 | 1 | 1 | 0 |

---

## 一、DFS 深度优先搜索 (Depth-First Search)

### 算法思想

从起始顶点出发，沿着一条路径尽可能深地探索，直到无法继续，然后回溯到上一个未完全探索的顶点，继续深入。

> 使用**栈**（递归隐式栈）实现。

### 遍历过程（从 A 出发，邻接点按字母顺序）

| 步骤 | 当前顶点 | 操作 | 已访问集合 | 说明 |
|:---:|:---:|:---|:---:|:---|
| 1 | A | 访问 A，标记已访问 | {A} | 起点 |
| 2 | A | 找 A 的未访问邻接点：B, C（选 B） | {A} | B 在 C 前（字母顺序） |
| 3 | B | 访问 B，标记已访问 | {A, B} | 从 A 到 B |
| 4 | B | 找 B 的未访问邻接点：A(已访问), **D** | {A, B} | 选 D |
| 5 | D | 访问 D，标记已访问 | {A, B, D} | 从 B 到 D |
| 6 | D | 找 D 的未访问邻接点：B(已访问), **C**, **E** | {A, B, D} | C 在 E 前，选 C |
| 7 | C | 访问 C，标记已访问 | {A, B, D, C} | 从 D 到 C |
| 8 | C | 找 C 的未访问邻接点：A(已访问), D(已访问), **E** | {A, B, D, C} | 选 E |
| 9 | E | 访问 E，标记已访问 | {A, B, D, C, E} | 从 C 到 E |
| 10 | E | 找 E 的未访问邻接点：C(已访问), D(已访问) | {A, B, D, C, E} | 无未访问邻接点，回溯 |
| 11 | - | 所有顶点已访问，结束 | {A, B, D, C, E} | DFS 完成 |

### DFS 遍历序列

```
A -> B -> D -> C -> E
```

### 遍历路径图示

```
        A
       / 
      B   ← 第一步走 B（字母顺序 B < C）
       \
        D
       / 
      C   ← D 的邻接点 C < E，先走 C
       \
        E
```

---

## 二、BFS 广度优先搜索 (Breadth-First Search)

### 算法思想

从起始顶点出发，先访问所有邻接点，再依次访问这些邻接点的邻接点，层层向外扩展。

> 使用**队列**实现。

### 遍历过程（从 A 出发，邻接点按字母顺序）

| 步骤 | 队列状态 | 操作 | 已访问集合 | 说明 |
|:---:|:---|:---|:---:|:---|
| 1 | [A] | 出队 A，访问 A | {A} | 起点入队 |
| 2 | [B, C] | A 的邻接点 B, C 入队（按字母顺序） | {A, B, C} | B 在 C 前 |
| 3 | [C, D] | 出队 B，访问 B；B 的邻接点 D 入队 | {A, B, C, D} | A 已访问，只入 D |
| 4 | [D, E] | 出队 C，访问 C；C 的邻接点 E 入队 | {A, B, C, D, E} | A, D 已访问，入 E |
| 5 | [E] | 出队 D，访问 D；D 的邻接点都已访问 | {A, B, C, D, E} | B, C, E 都已访问 |
| 6 | [] | 出队 E，访问 E；E 的邻接点都已访问 | {A, B, C, D, E} | C, D 已访问 |
| 7 | [] | 队列为空，结束 | {A, B, C, D, E} | BFS 完成 |

### BFS 遍历序列

```
A -> B -> C -> D -> E
```

### 遍历层次图示

```
第 0 层:        A
               / \
第 1 层:      B   C
                 / \
第 2 层:        D   E
             /
第 3 层:    (无新顶点)
```

> BFS 按层遍历：先访问 A（第0层），再访问 B、C（第1层），最后访问 D、E（第2层）。

---

## 三、结果对比

| 遍历方式 | 序列 | 特点 |
|:---:|:---|:---|
| **DFS** | A &rarr; B &rarr; D &rarr; C &rarr; E | 深入探索，回溯后继续 |
| **BFS** | A &rarr; B &rarr; C &rarr; D &rarr; E | 层层扩展，先近后远 |

---

## 四、Python 代码实现

```python
from collections import deque

# 邻接表（按字母顺序排列邻接点）
adj_list = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'D', 'E'],
    'D': ['B', 'C', 'E'],
    'E': ['C', 'D']
}

# DFS 深度优先搜索
def dfs(graph, start):
    visited = set()
    result = []

    def dfs_helper(v):
        visited.add(v)
        result.append(v)
        for neighbor in sorted(graph[v]):
            if neighbor not in visited:
                dfs_helper(neighbor)

    dfs_helper(start)
    return result

# BFS 广度优先搜索
def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    result = [start]

    while queue:
        v = queue.popleft()
        for neighbor in sorted(graph[v]):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                result.append(neighbor)

    return result

# 执行遍历
dfs_result = dfs(adj_list, 'A')
bfs_result = bfs(adj_list, 'A')

print("DFS:", " -> ".join(dfs_result))  # A -> B -> D -> C -> E
print("BFS:", " -> ".join(bfs_result))  # A -> B -> C -> D -> E
```

---

## 五、DFS vs BFS 对比总结

| 特性 | DFS | BFS |
|:---:|:---:|:---:|
| **数据结构** | 栈（递归/显式栈） | 队列 |
| **遍历顺序** | 深度优先，一条路走到底 | 广度优先，层层扩展 |
| **空间复杂度** | $O(h)$，$h$ 为树高 | $O(w)$，$w$ 为最大宽度 |
| **适用场景** | 找路径、连通分量、拓扑排序 | 最短路径、层次遍历、连通性检测 |
| **本题结果** | A &rarr; B &rarr; D &rarr; C &rarr; E | A &rarr; B &rarr; C &rarr; D &rarr; E |
