# 随机快速排序与三路快速排序比较

## 一、算法概述

### 1.1 随机快速排序 (Randomized QuickSort)

**核心思想**：在标准快速排序的基础上，**随机选择 pivot**，避免对近乎有序的数据产生最坏情况。

**分区方式**：Lomuto 分区 —— 将数组划分为 `≤ pivot` 和 `> pivot` 两个区域。

```
[ 小于等于pivot ]  [ pivot ]  [ 大于pivot ]
```

### 1.2 三路快速排序 (3-Way QuickSort)

**核心思想**：将数组划分为 **三个区域**：`< pivot`、`== pivot`、`> pivot`，特别适合处理**大量重复元素**的数据。

```
[ 小于pivot ]  [ 等于pivot ]  [ 大于pivot ]
   ^ lt          ^ cur           ^ gt
```

---

## 二、核心代码对比

### 2.1 随机快速排序

```python
def randomized_partition(arr, left, right):
    # 随机选pivot，换到末尾
    pivot_pos = random.randint(left, right)
    arr[pivot_pos], arr[right] = arr[right], arr[pivot_pos]

    pivot = arr[right]
    store = left - 1

    for scan in range(left, right):
        if arr[scan] <= pivot:
            store += 1
            arr[store], arr[scan] = arr[scan], arr[store]

    arr[store + 1], arr[right] = arr[right], arr[store + 1]
    return store + 1
```

**特点**：
- 只处理两个分区（≤ pivot 和 > pivot）
- 随机选 pivot 后，和标准快排一样做分区

### 2.2 三路快速排序

```python
def three_way_quicksort(arr, left, right):
    if left >= right:
        return

    # 随机选pivot放最左
    pivot_pos = random.randint(left, right)
    arr[left], arr[pivot_pos] = arr[pivot_pos], arr[left]
    pivot = arr[left]

    lt = left       # < pivot 的右边界
    gt = right      # > pivot 的左边界
    cur = left + 1  # 扫描指针

    while cur <= gt:
        if arr[cur] < pivot:
            arr[cur], arr[lt] = arr[lt], arr[cur]
            lt += 1
            cur += 1
        elif arr[cur] > pivot:
            arr[cur], arr[gt] = arr[gt], arr[cur]
            gt -= 1
        else:
            cur += 1

    # 递归处理两侧（中间等于pivot的部分已排好）
    three_way_quicksort(arr, left, lt - 1)
    three_way_quicksort(arr, gt + 1, right)
```

**特点**：
- 三个指针：`lt`（小于区右界）、`cur`（扫描）、`gt`（大于区左界）
- 等于 pivot 的元素集中在中间，不再递归处理

---

## 三、详细对比

| 对比维度 | 随机快速排序 | 三路快速排序 |
|:---:|:---:|:---:|
| **分区数量** | 2 个（≤ pivot, > pivot） | 3 个（<, =, > pivot） |
| **重复元素处理** | 和 pivot 相等的元素分散到两侧 | 等于 pivot 的元素集中在中间，跳过不递归 |
| **随机选 pivot** | ✅ 是 | ✅ 是 |
| **最坏时间复杂度** | O(n²)（概率极低） | O(n²)（概率极低） |
| **平均时间复杂度** | O(n log n) | O(n log n) |
| **大量重复元素场景** | 性能下降（重复元素导致不平衡分区） | **性能优异**（等于区直接跳过） |
| **空间复杂度** | O(log n)（递归栈） | O(log n)（递归栈） |
| **稳定性** | 不稳定 | 不稳定 |
| **代码复杂度** | 简单 | 稍复杂（三个指针） |

---

## 四、适用场景

| 场景 | 推荐算法 | 原因 |
|:---:|:---:|:---|
| 数据随机分布，无大量重复 | **随机快速排序** | 代码简洁，常数因子小 |
| 数据包含大量重复键值 | **三路快速排序** | 等于区直接跳过，避免重复元素导致的不平衡 |
| 数据近乎有序 | **随机快速排序** | 随机选 pivot 打破有序性 |
| 需要稳定排序 | 两者都不适用 | 快排系列均为不稳定排序 |

---

## 五、示例演示

### 5.1 随机快速排序（随机数据）

```
原数组：[2, 34, 56, 3, 24, 53, 45, 35, 99, 87]
排序后：[2, 3, 24, 34, 35, 45, 53, 56, 87, 99]
```

### 5.2 三路快速排序（含重复数据）

```
原数组：[84, 3, 5, 6, 6, 34, 8, 98, 8]
排序后：[3, 5, 6, 6, 8, 8, 34, 84, 98]
```

> 注意：三路快排中两个 `6` 和两个 `8` 在分区时会被直接归入"等于区"，无需额外递归处理。

---

## 六、性能分析

### 大量重复元素时的性能差异

假设数组长度为 n，其中 90% 的元素都等于某个值：

| 算法 | 分区情况 | 递归深度 |
|:---:|:---:|:---:|
| 随机快排 | 一侧几乎全满 | O(n) |
| 三路快排 | 等于区占 90%，两侧很小 | O(log n) |

**结论**：三路快排在大量重复元素场景下，递归深度显著降低，性能远优于普通快排。

---

## 七、总结

| 要点 | 说明 |
|:---:|:---|
| **随机快排** | 通用场景首选，简单高效，通过随机化避免最坏情况 |
| **三路快排** | 重复元素多的场景首选，将等于pivot的元素隔离，减少无效递归 |
| **共同点** | 都使用随机选pivot策略，都是不稳定的比较排序 |
| **选择建议** | 数据重复少 → 随机快排；数据重复多 → 三路快排 |
