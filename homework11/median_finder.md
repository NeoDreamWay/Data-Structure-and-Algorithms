# 双堆求中位数 (MedianFinder)

## 问题描述

设计一个数据结构 `MedianFinder`，支持两个操作：
- `addNum(num)`：添加一个整数
- `findMedian()`：返回当前所有数字的中位数

要求用**两个堆**实现（一个大顶堆、一个小顶堆），并分析时间复杂度。

---

## 核心思路

### 双堆策略

| 堆 | 存储内容 | 堆顶含义 |
|---|---|---|
| **大顶堆** (`max_heap`) | 较小的一半数字 | 这部分的最大值 |
| **小顶堆** (`min_heap`) | 较大的一半数字 | 这部分的最小值 |

### 平衡规则

始终保持：
- `size(max_heap) == size(min_heap)`（偶数个数字）
- `size(max_heap) == size(min_heap) + 1`（奇数个数字）

> 即：大顶堆的元素个数 **等于或比** 小顶堆 **多1个**

### 中位数计算

| 总个数 | 中位数来源 |
|---|---|
| 奇数 | 大顶堆的堆顶（较小一半的最大值） |
| 偶数 | 两堆顶的平均值 |

---

## 代码实现

```python
import heapq

class MedianFinder:
    def __init__(self):
        # 大顶堆（用负数模拟Python的小顶堆）
        self.max_heap = []
        # 小顶堆
        self.min_heap = []

    def addNum(self, num: int) -> None:
        # 1. 决定放入哪个堆
        if not self.max_heap or num <= -self.max_heap[0]:
            heapq.heappush(self.max_heap, -num)  # 放入较小的一半
        else:
            heapq.heappush(self.min_heap, num)   # 放入较大的一半

        # 2. 平衡两个堆的大小
        if len(self.max_heap) > len(self.min_heap) + 1:
            # 大顶堆太多，移一个到小顶堆
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)
        elif len(self.min_heap) > len(self.max_heap):
            # 小顶堆太多，移一个到大顶堆
            val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -val)

    def findMedian(self) -> float:
        if len(self.max_heap) > len(self.min_heap):
            return float(-self.max_heap[0])  # 奇数个
        else:
            return (-self.max_heap[0] + self.min_heap[0]) / 2.0  # 偶数个
```

---

## 执行流程示例

测试序列：`[3, 1, 4, 1, 5]`

| 步骤 | 操作 | 大顶堆(较小一半) | 小顶堆(较大一半) | 中位数 | 说明 |
|---|---|---|---|---|---|
| 1 | `addNum(3)` | `[3]` | `[]` | `3.0` | 第一个数，放入大顶堆 |
| 2 | `addNum(1)` | `[1]` | `[3]` | `2.0` | 1<3，平衡后各1个，取平均 |
| 3 | `addNum(4)` | `[1, 3]` | `[4]` | `3.0` | 4>3，放入小顶堆，大顶堆多1个 |
| 4 | `addNum(1)` | `[1, 1]` | `[3, 4]` | `2.0` | 1<=1，放入大顶堆，平衡后各2个 |
| 5 | `addNum(5)` | `[1, 1, 3]` | `[4, 5]` | `3.0` | 5>3，放入小顶堆，大顶堆多1个 |

---

## 时间复杂度分析

| 操作 | 时间复杂度 | 说明 |
|---|---|---|
| `addNum(num)` | **O(log n)** | 堆的插入/删除操作 |
| `findMedian()` | **O(1)** | 直接访问堆顶元素 |

### 为什么不是 O(n)？

- 不需要对所有数据排序，只需要维护两个堆顶
- 堆的插入/删除只涉及树高路径，时间复杂度为 O(log n)
- 获取堆顶是 O(1) 操作

---

## 空间复杂度

- **O(n)**：所有元素都存储在两个堆中

---

## 关键要点

1. **Python 没有大顶堆**：用负数存入小顶堆来模拟
2. **先放再平衡**：先决定放入哪个堆，再通过堆顶元素移动来平衡大小
3. **大顶堆可以多1个**：这样奇数时直接取大顶堆顶，无需额外判断
4. **比较用堆顶**：判断 num 属于哪一半时，和大顶堆顶（较小一半的最大值）比较

---

## 完整代码文件

- `median_finder.py`：可直接运行的 Python 实现
