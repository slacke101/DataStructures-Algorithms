import random


class Node:
    """Node class for linked list and tree structures"""

    def __init__(self, data):
        self.data = data
        self.next = None
        self.left = None
        self.right = None


class LinkedList:
    """Linked List implementation with visualization support"""

    def __init__(self):
        self.head = None
        self.size = 0

    def insert_at_beginning(self, data):
        """Insert a node at the beginning of the list"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
        yield self.to_array(), [0], "Inserted {} at beginning".format(data)

    def insert_at_end(self, data):
        """Insert a node at the end of the list"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
        yield self.to_array(), [self.size - 1], "Inserted {} at end".format(data)

    def delete_node(self, data):
        """Delete the first occurrence of a node with given data"""
        if not self.head:
            yield self.to_array(), [], "List is empty"
            return

        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            yield self.to_array(), [0], "Deleted {} from beginning".format(data)
            return

        current = self.head
        index = 0
        while current.next and current.next.data != data:
            current = current.next
            index += 1

        if current.next:
            current.next = current.next.next
            self.size -= 1
            yield (
                self.to_array(),
                [index + 1],
                "Deleted {} from position {}".format(data, index + 1),
            )
        else:
            yield self.to_array(), [], "{} not found in list".format(data)

    def search(self, data):
        """Search for a node with given data"""
        current = self.head
        index = 0
        while current:
            yield (
                self.to_array(),
                [index],
                "Searching for {} at position {}".format(data, index),
            )
            if current.data == data:
                yield (
                    self.to_array(),
                    [index],
                    "Found {} at position {}".format(data, index),
                )
                return
            current = current.next
            index += 1
        yield self.to_array(), [], "{} not found in list".format(data)

    def to_array(self):
        """Convert linked list to array for visualization"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result


class Stack:
    """Stack implementation with visualization support"""

    def __init__(self):
        self.items = []
        self.max_size = 10

    def push(self, item):
        """Push an item onto the stack"""
        if len(self.items) >= self.max_size:
            yield self.items, [], "Stack is full"
            return
        self.items.append(item)
        yield self.items, [len(self.items) - 1], "Pushed {} onto stack".format(item)

    def pop(self):
        """Pop an item from the stack"""
        if not self.items:
            yield self.items, [], "Stack is empty"
            return
        item = self.items.pop()
        yield self.items, [], "Popped {} from stack".format(item)

    def peek(self):
        """Peek at the top item without removing it"""
        if not self.items:
            yield self.items, [], "Stack is empty"
            return
        yield self.items, [len(self.items) - 1], "Peeked at {}".format(self.items[-1])

    def to_array(self):
        """Return a shallow copy for visualization"""
        return self.items.copy()


class Queue:
    """Queue implementation with visualization support"""

    def __init__(self):
        self.items = []
        self.max_size = 10

    def enqueue(self, item):
        """Add an item to the queue"""
        if len(self.items) >= self.max_size:
            yield self.items, [], "Queue is full"
            return
        self.items.append(item)
        yield self.items, [len(self.items) - 1], "Enqueued {}".format(item)

    def dequeue(self):
        """Remove and return the first item from the queue"""
        if not self.items:
            yield self.items, [], "Queue is empty"
            return
        item = self.items.pop(0)
        yield self.items, [], "Dequeued {}".format(item)

    def peek(self):
        """Peek at the first item without removing it"""
        if not self.items:
            yield self.items, [], "Queue is empty"
            return
        yield self.items, [0], "Peeked at {}".format(self.items[0])

    def to_array(self):
        """Return a shallow copy for visualization"""
        return self.items.copy()


class BinaryTree:
    """Binary Tree implementation with visualization support"""

    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, data):
        """Insert a node into the binary tree"""
        if not self.root:
            self.root = Node(data)
            self.size += 1
            yield self.to_array(), [0], "Inserted {} as root".format(data)
            return

        queue = [self.root]
        index = 0
        while queue:
            current = queue.pop(0)
            if not current.left:
                current.left = Node(data)
                self.size += 1
                yield self.to_array(), [index], "Inserted {} as left child".format(data)
                return
            if not current.right:
                current.right = Node(data)
                self.size += 1
                yield (
                    self.to_array(),
                    [index],
                    "Inserted {} as right child".format(data),
                )
                return
            queue.append(current.left)
            queue.append(current.right)
            index += 1

    def inorder_traversal(self):
        """Perform inorder traversal"""

        def inorder_helper(node, index):
            if node:
                yield from inorder_helper(node.left, 2 * index + 1)
                yield self.to_array(), [index], "Visited {}".format(node.data)
                yield from inorder_helper(node.right, 2 * index + 2)

        yield from inorder_helper(self.root, 0)

    def to_array(self):
        """Convert binary tree to array representation"""
        if not self.root:
            return []

        result = []
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            if current:
                result.append(current.data)
                queue.append(current.left)
                queue.append(current.right)
            else:
                result.append(None)

        # Remove trailing None values
        while result and result[-1] is None:
            result.pop()

        return result


# -----------------------------------------------------------------------------
# Additional Data Structures (Array and Binary Heap)
# -----------------------------------------------------------------------------


class ArrayStructure:
    """Simple dynamic array wrapper for visualization support"""

    def __init__(self):
        self.items = []

    # For uniformity with other structures, operations are generators that yield
    # (state, highlight_indices, message)
    def insert(self, value):
        self.items.append(value)
        yield self.to_array(), [len(self.items) - 1], f"Appended {value}"

    def delete(self, value=None):
        if not self.items:
            yield self.items, [], "Array is empty"
            return
        if value is None:
            removed = self.items.pop()
            yield self.to_array(), [], f"Popped {removed} from end"
        else:
            try:
                idx = self.items.index(value)
                self.items.pop(idx)
                yield self.to_array(), [idx], f"Removed {value} at index {idx}"
            except ValueError:
                yield self.to_array(), [], f"{value} not found"

    def search(self, value):
        for idx, item in enumerate(self.items):
            yield self.to_array(), [idx], f"Checking index {idx}"
            if item == value:
                yield self.to_array(), [idx], f"Found {value} at index {idx}"
                return
        yield self.to_array(), [], f"{value} not found"

    def to_array(self):
        return self.items.copy()


class BinaryHeap:
    """Min Binary Heap with visualization support"""

    def __init__(self):
        self.heap = []  # using list representation

    def _parent(self, i):
        return (i - 1) // 2 if i else None

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, value):
        self.heap.append(value)
        idx = len(self.heap) - 1
        yield self.to_array(), [idx], f"Inserted {value}"
        # Bubble up
        while idx > 0 and self.heap[idx] < self.heap[self._parent(idx)]:
            p = self._parent(idx)
            self._swap(idx, p)
            yield self.to_array(), [idx, p], "Heapify up"
            idx = p

    def delete(self):
        if not self.heap:
            yield self.heap, [], "Heap is empty"
            return
        self._swap(0, -1)
        removed = self.heap.pop()
        yield self.to_array(), [0], f"Removed root {removed}"
        # Heapify down
        idx = 0
        n = len(self.heap)
        while True:
            left, right = 2 * idx + 1, 2 * idx + 2
            smallest = idx
            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right
            if smallest != idx:
                self._swap(idx, smallest)
                yield self.to_array(), [idx, smallest], "Heapify down"
                idx = smallest
            else:
                break

    def search(self, value):
        for idx, item in enumerate(self.heap):
            yield self.to_array(), [idx], f"Checking index {idx}"
            if item == value:
                yield self.to_array(), [idx], f"Found {value} at index {idx}"
                return
        yield self.to_array(), [], f"{value} not found"

    def to_array(self):
        return self.heap.copy()


# Data structure generators for visualization
DATA_STRUCTURES = {
    "Linked List": LinkedList,
    "Stack": Stack,
    "Queue": Queue,
    "Binary Tree": BinaryTree,
    "Array": ArrayStructure,
    "Binary Heap": BinaryHeap,
}

# Data structure information
DATA_STRUCTURE_INFO = {
    "Linked List": {
        "description": "A linear data structure where elements are stored in nodes, and each node points to the next node in the sequence.",
        "operations": ["Insert at beginning", "Insert at end", "Delete", "Search"],
        "time_complexity": {
            "insertion": "O(1) at beginning, O(n) at end",
            "deletion": "O(1) at beginning, O(n) at end",
            "search": "O(n)",
        },
    },
    "Stack": {
        "description": "A linear data structure that follows the Last In First Out (LIFO) principle.",
        "operations": ["Push", "Pop", "Peek"],
        "time_complexity": {"push": "O(1)", "pop": "O(1)", "peek": "O(1)"},
    },
    "Queue": {
        "description": "A linear data structure that follows the First In First Out (FIFO) principle.",
        "operations": ["Enqueue", "Dequeue", "Peek"],
        "time_complexity": {"enqueue": "O(1)", "dequeue": "O(1)", "peek": "O(1)"},
    },
    "Binary Tree": {
        "description": "A hierarchical data structure where each node has at most two children, referred to as left child and right child.",
        "operations": ["Insert", "Traverse"],
        "time_complexity": {"insertion": "O(n)", "traversal": "O(n)"},
    },
    "Array": {
        "description": "A sequence of elements accessible by contiguous indices.",
        "operations": ["Insert", "Delete", "Search"],
        "time_complexity": {
            "insert": "O(1) amortized (append)",
            "delete": "O(n)",
            "search": "O(n)",
        },
    },
    "Binary Heap": {
        "description": "A complete binary tree that maintains the heap property; here implemented as a min-heap.",
        "operations": ["Insert", "Delete (root)", "Search"],
        "time_complexity": {
            "insert": "O(log n)",
            "delete": "O(log n)",
            "search": "O(n)",
        },
    },
}
