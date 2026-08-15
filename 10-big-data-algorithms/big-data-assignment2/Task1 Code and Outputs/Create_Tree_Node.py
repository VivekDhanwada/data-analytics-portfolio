class TreeNode:
    def __init__(self, is_leaf):
        self.is_leaf = is_leaf
        self.entries = []  # For leaf: (x, y, id), for internal: (bounding_box, child_node)

    def add_entry(self, entry):
        self.entries.append(entry)

    def compute_bounding_box(self):
        if self.is_leaf:
            xs = [entry[0] for entry in self.entries]
            ys = [entry[1] for entry in self.entries]
        else:
            xs = [e[0][0] for e in self.entries] + [e[0][2] for e in self.entries]
            ys = [e[0][1] for e in self.entries] + [e[0][3] for e in self.entries]

        return (min(xs), min(ys), max(xs), max(ys))

def create_rtree(points, max_entries=4):
    def build_tree(entries, is_leaf):
        if len(entries) <= max_entries:
            node = TreeNode(is_leaf)
            for e in entries:
                node.add_entry(e)
            return node

        # Sort and divide entries
        entries.sort(key=lambda x: x[0])  # sort by x
        mid = len(entries) // 2
        left_entries = entries[:mid]
        right_entries = entries[mid:]

        left_child = build_tree(left_entries, is_leaf)
        right_child = build_tree(right_entries, is_leaf)

        parent = TreeNode(False)
        parent.add_entry((left_child.compute_bounding_box(), left_child))
        parent.add_entry((right_child.compute_bounding_box(), right_child))
        return parent

    leaf_entries = [(x, y, pid) for x, y, pid in points]
    return build_tree(leaf_entries, True)