"""
双堆求中位数 (MedianFinder)

设计一个数据结构，支持两个操作：
- addNum(num): 添加一个整数
- findMedian(): 返回当前所有数字的中位数

使用两个堆实现：
- 大顶堆(max_heap): 存储较小的一半数字，堆顶是这部分的最大值
- 小顶堆(min_heap): 存储较大的一半数字，堆顶是这部分的最小值

始终保持: size(max_heap) == size(min_heap) 或 size(max_heap) == size(min_heap) + 1

时间复杂度:
- addNum: O(log n)
- findMedian: O(1)
"""

import heapq


class MedianFinder:
    """双堆求中位数"""

    def __init__(self):
        # 大顶堆（用负数模拟）：存较小的一半
        self.max_heap = []
        # 小顶堆：存较大的一半
        self.min_heap = []

    def addNum(self, num: int) -> None:
        """
        添加一个数字
        时间复杂度: O(log n)
        """
        if not self.max_heap or num <= -self.max_heap[0]:
            # 放入大顶堆（较小的一半）
            heapq.heappush(self.max_heap, -num)
        else:
            # 放入小顶堆（较大的一半）
            heapq.heappush(self.min_heap, num)

        # 平衡两个堆的大小
        # 要求: max_heap 的大小等于 min_heap，或比它大1
        if len(self.max_heap) > len(self.min_heap) + 1:
            # 大顶堆太多，移一个到小顶堆
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)
        elif len(self.min_heap) > len(self.max_heap):
            # 小顶堆太多，移一个到大顶堆
            val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -val)

    def findMedian(self) -> float:
        """
        返回中位数
        时间复杂度: O(1)
        """
        if len(self.max_heap) > len(self.min_heap):
            # 奇数个，大顶堆堆顶就是中位数
            return float(-self.max_heap[0])
        else:
            # 偶数个，两堆顶的平均值
            return (-self.max_heap[0] + self.min_heap[0]) / 2.0

    def __repr__(self):
        """返回可读的字符串表示"""
        max_h = [-x for x in self.max_heap]
        max_h.sort()
        min_h = sorted(self.min_heap)
        return f"MedianFinder(max_heap={max_h}, min_heap={min_h})"


def main():
    """主函数 - 测试示例"""
    print("=" * 60)
    print("双堆求中位数 - 测试")
    print("=" * 60)

    mf = MedianFinder()

    # 测试序列: [3, 1, 4, 1, 5]
    test_sequence = [3, 1, 4, 1, 5]

    for num in test_sequence:
        print(f"\n--- addNum({num}) ---")
        mf.addNum(num)
        median = mf.findMedian()
        print(f"当前状态: {mf}")
        print(f"中位数: {median}")

    print(f"\n{'='*60}")
    print(f"最终中位数: {mf.findMedian()}")
    print(f"{'='*60}")

    # 额外测试：偶数个和奇数个的情况
    print("\n\n额外测试 - 偶数个数 [1, 2, 3, 4]:")
    mf2 = MedianFinder()
    for num in [1, 2, 3, 4]:
        mf2.addNum(num)
        print(f"addNum({num}) -> 中位数: {mf2.findMedian()}")

    print("\n额外测试 - 奇数个数 [10, 20, 30]:")
    mf3 = MedianFinder()
    for num in [10, 20, 30]:
        mf3.addNum(num)
        print(f"addNum({num}) -> 中位数: {mf3.findMedian()}")


if __name__ == "__main__":
    main()
