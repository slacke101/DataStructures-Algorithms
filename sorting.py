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
