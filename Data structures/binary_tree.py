"""Example use case for a binary tree: a binary search tree for student IDs.

A binary tree is useful when we need to store data in a structured way that
supports fast searching, inserting, and deleting. In this example, each node
stores a student ID, and the left/right branches keep values in sorted order.
"""


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def insert(root, value):
    if root is None:
        return Node(value)

    if value < root.value:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)

    return root


def search(root, target):
    while root is not None:
        if target == root.value:
            return True
        if target < root.value:
            root = root.left
        else:
            root = root.right
    return False


# Example: storing student IDs to quickly check if a student is registered.
student_ids = Node(100)
student_ids = insert(student_ids, 50)
student_ids = insert(student_ids, 150)
student_ids = insert(student_ids, 25)
student_ids = insert(student_ids, 75)
student_ids = insert(student_ids, 125)
student_ids = insert(student_ids, 175)

print(search(student_ids, 125))  # True
print(search(student_ids, 90))   # False
