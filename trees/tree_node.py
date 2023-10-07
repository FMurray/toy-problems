class TreeNode:
    left = None
    right = None
    val = None

    def __init__(self, val=None):
        self.val = val

    def __str__(self) -> str:
        lines = []
        level = [self]
        while level:
            next_level = list()
            line = ""
            for node in level:
                if node is not None:
                    line += str(node.val) + " "
                    next_level.append(node.left)
                    next_level.append(node.right)
                else:
                    line += "N "
            lines.append(line)
            level = [n for n in next_level if n is not None]
        return "\n".join(lines)


def pretty_print(node, level=0, prefix="Root: ", is_left=True):
    if node is not None:
        pretty_print(node.right, level + 1, "Right: ", False)
        print("     " * level + prefix + str(node.val))
        pretty_print(node.left, level + 1, "Left: ", True)
