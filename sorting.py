import random


def bubble_sort(arr):
    """
    Bubble Sort algorithm (generator for visualization)
    Yields the array, indices being compared, and whether a swap occurred.
    Time Complexity: O(n^2) worst/average, O(n) best
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            # Yield current state and highlight comparison (no swap yet)
            yield arr, (j, j + 1), False
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                # Yield state after swap
                yield arr, (j, j + 1), True


def insertion_sort(arr):
    """
    Insertion Sort algorithm (generator for visualization)
    Time Complexity: O(n^2) worst/average, O(n) best
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Highlight the key element
        yield arr, (i,), False
        while j >= 0 and arr[j] > key:
            # Highlight comparison
            yield arr, (j, j + 1), False
            arr[j + 1] = arr[j]
            # Highlight swap
            yield arr, (j, j + 1), True
            j -= 1
        arr[j + 1] = key
        # Highlight final placement
        yield arr, (j + 1,), False


def selection_sort(arr):
    """
    Selection Sort algorithm (generator for visualization)
    Time Complexity: O(n^2) worst/average/best
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        # Highlight current minimum
        yield arr, (min_idx,), False
        for j in range(i + 1, n):
            # Highlight comparison
            yield arr, (j, min_idx), False
            if arr[j] < arr[min_idx]:
                min_idx = j
                # Highlight new minimum
                yield arr, (min_idx,), False
        # Swap minimum with current position
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield arr, (i, min_idx), True


def quick_sort(arr):
    """
    Quick Sort algorithm (generator for visualization)
    Time Complexity: O(n log n) average, O(n^2) worst
    """

    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        # Highlight pivot
        yield arr, (high,), False
        for j in range(low, high):
            # Highlight comparison
            yield arr, (j, high), False
            if arr[j] <= pivot:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    yield arr, (i, j), True
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        yield arr, (i + 1, high), True
        return i + 1

    def quick_sort_helper(low, high):
        if low < high:
            pi = yield from partition(low, high)
            yield from quick_sort_helper(low, pi - 1)
            yield from quick_sort_helper(pi + 1, high)

    yield from quick_sort_helper(0, len(arr) - 1)


def merge_sort(arr):
    """
    Merge Sort algorithm (generator for visualization)
    Time Complexity: O(n log n) worst/average/best
    """

    def merge(left, mid, right):
        left_arr = arr[left : mid + 1]
        right_arr = arr[mid + 1 : right + 1]
        i = j = 0
        k = left

        while i < len(left_arr) and j < len(right_arr):
            # Highlight comparison
            yield arr, (left + i, mid + 1 + j), False
            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1

        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1

        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1

    def merge_sort_helper(left, right):
        if left < right:
            mid = (left + right) // 2
            yield from merge_sort_helper(left, mid)
            yield from merge_sort_helper(mid + 1, right)
            yield from merge(left, mid, right)

    yield from merge_sort_helper(0, len(arr) - 1)


# Dictionary of all sorting algorithms
SORTING_ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort,
    "Quick Sort": quick_sort,
    "Merge Sort": merge_sort,
}

# Algorithm descriptions and complexities
ALGORITHM_INFO = {
    "Bubble Sort": {
        "description": "Simple sorting algorithm that repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.",
        "time_complexity": "O(n²)",
        "space_complexity": "O(1)",
        "stable": True,
        "in_place": True,
    },
    "Insertion Sort": {
        "description": "Builds the final sorted array one item at a time. It is much less efficient on large lists than more advanced algorithms.",
        "time_complexity": "O(n²)",
        "space_complexity": "O(1)",
        "stable": True,
        "in_place": True,
    },
    "Selection Sort": {
        "description": "Divides the input list into two parts: a sorted sublist of items and an unsorted sublist. The algorithm repeatedly selects the smallest element from the unsorted sublist.",
        "time_complexity": "O(n²)",
        "space_complexity": "O(1)",
        "stable": False,
        "in_place": True,
    },
    "Quick Sort": {
        "description": "Uses a divide-and-conquer strategy. It picks a 'pivot' element and partitions the array around the pivot.",
        "time_complexity": "O(n log n)",
        "space_complexity": "O(log n)",
        "stable": False,
        "in_place": True,
    },
    "Merge Sort": {
        "description": "A divide-and-conquer algorithm that recursively breaks down the problem into smaller subproblems until they become simple enough to solve directly.",
        "time_complexity": "O(n log n)",
        "space_complexity": "O(n)",
        "stable": True,
        "in_place": False,
    },
}
