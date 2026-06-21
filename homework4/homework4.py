"""
快速排序变体实现

本模块包含两种快速排序的改进版本：
1. 随机化快速排序 —— 通过随机选取 pivot 降低最坏情况概率
2. 三路快速排序 —— 将数组划分为 <、=、> 三个区间，适合大量重复元素
"""

import random
import time


# ==================== 随机化快速排序 ====================

def _randomized_partition(seq, left, right):
    """
    随机化分区：先随机交换 pivot 到末尾，再做标准 Lomuto 分区

    :param seq: 待排序序列
    :param left: 左边界（含）
    :param right: 右边界（含）
    :return: pivot 的最终位置
    """
    # 随机选 pivot，换到末尾
    pivot_pos = random.randint(left, right)
    seq[pivot_pos], seq[right] = seq[right], seq[pivot_pos]

    pivot_val = seq[right]
    store = left - 1

    for scan in range(left, right):
        if seq[scan] <= pivot_val:
            store += 1
            seq[store], seq[scan] = seq[scan], seq[store]

    # pivot 归位
    seq[store + 1], seq[right] = seq[right], seq[store + 1]
    return store + 1


def randomized_quicksort(seq, left, right):
    """
    随机化快速排序（递归实现）

    :param seq: 待排序序列
    :param left: 左边界
    :param right: 右边界
    """
    if left < right:
        pivot_idx = _randomized_partition(seq, left, right)
        randomized_quicksort(seq, left, pivot_idx - 1)
        randomized_quicksort(seq, pivot_idx + 1, right)


# ==================== 三路快速排序 ====================

def three_way_quicksort(seq, left, right):
    """
    三路快速排序（Dutch National Flag 变体）

    将序列划分为三个区间：
    [left, lt)     < pivot
    [lt, gt]       == pivot
    (gt, right]    > pivot

    特别适合处理包含大量重复键的数据。

    :param seq: 待排序序列
    :param left: 左边界
    :param right: 右边界
    """
    if left >= right:
        return

    # 随机选 pivot 并放到最左
    pivot_pos = random.randint(left, right)
    seq[left], seq[pivot_pos] = seq[pivot_pos], seq[left]
    pivot_val = seq[left]

    lt = left       # < pivot 的右边界（不含）
    gt = right      # > pivot 的左边界（不含）
    cur = left + 1  # 当前扫描位置

    while cur <= gt:
        if seq[cur] < pivot_val:
            seq[cur], seq[lt] = seq[lt], seq[cur]
            lt += 1
            cur += 1
        elif seq[cur] > pivot_val:
            seq[cur], seq[gt] = seq[gt], seq[cur]
            gt -= 1
        else:
            cur += 1

    # 递归处理两侧
    three_way_quicksort(seq, left, lt - 1)
    three_way_quicksort(seq, gt + 1, right)


# ==================== 测试与演示 ====================

def _benchmark(sort_func, arr, label):
    """运行排序并输出耗时"""
    copy_arr = list(arr)
    print(f"\n--- {label} ---")
    print(f"原数组：{copy_arr}")

    t0 = time.time()
    sort_func(copy_arr, 0, len(copy_arr) - 1)
    t1 = time.time()

    print(f"排序后：{copy_arr}")
    print(f"耗时：{(t1 - t0) * 1000:.4f} ms")


def main():
    print("=" * 55)
    print("  快速排序变体测试")
    print("=" * 55)

    # 测试 1：随机化快排
    data1 = [2, 34, 56, 3, 24, 53, 45, 35, 99, 87]
    _benchmark(randomized_quicksort, data1, "随机化快速排序")

    # 测试 2：三路快排（含重复元素）
    data2 = [84, 3, 5, 6, 6, 34, 8, 98, 8]
    _benchmark(three_way_quicksort, data2, "三路快速排序")

    print("\n" + "=" * 55)


if __name__ == "__main__":
    main()
