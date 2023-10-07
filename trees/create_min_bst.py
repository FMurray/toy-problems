"""
Given a array of ints sorted in ascending order, 
write a function that creates a minimum biary
search tree from the array.
"""
from tree_node import TreeNode, pretty_print


def _createMinBST(arr, start, end):
    if end < start:
        return None
    mid = (start + end) // 2
    n = TreeNode(arr[mid])
    n.left = _createMinBST(arr, start, mid - 1)
    n.right = _createMinBST(arr, mid + 1, end)
    return n


def createMinBST(arr):
    return _createMinBST(arr, 0, len(arr) - 1)


if __name__ == "__main__":
    result = createMinBST(list(range(11)))

    pretty_print(result)
