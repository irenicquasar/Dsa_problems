#red black trees
#CLRS implementation
import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv
from networkx.drawing.nx_agraph import graphviz_layout

class Node:
    def __init__(self, key, color):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:

    def __init__(self):
        self.root = None

    def insert(self, key):
        node = Node(key, 'red')
        if self.root is None:
            self.root = node
            self.root.color = 'black'
            return
        parent = None
        current = self.root
        while current is not None:
            parent = current
            if node.key < current.key:
                current = current.left
            else:
                current = current.right
        node.parent = parent
        if node.key < parent.key:
            parent.left = node
        else:
            parent.right = node
        self.insert_fixup(node)

    def insert_fixup(self, node):
        while node.parent is not None and node.parent.color == 'red':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle is not None and uncle.color == 'red':
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self.right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle is not None and uncle.color == 'red':
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self.left_rotate(node.parent.parent)
        self.root.color = 'black'

    def left_rotate(self, node):
        y = node.right
        node.right = y.left
        if y.left is not None:
            y.left.parent = node
        y.parent = node.parent
        if node.parent is None:
            self.root = y
        else:
            if node == node.parent.left:
                node.parent.left = y
            else:
                node.parent.right = y
        y.left = node
        node.parent = y

    def right_rotate(self, node):
        y = node.left
        node.left = y.right
        if y.right is not None:
            y.right.parent = node
        y.parent = node.parent
        if node.parent is None:
            self.root = y
        else:
            if node == node.parent.right:
                node.parent.right = y
            else:
                node.parent.left = y
        y.right = node
        node.parent = y
    
    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        else:
            if u == u.parent.left:
                u.parent.left = v
            else:
                u.parent.right = v
        v.parent = u.parent

    def delete(self, key):
        node = self.search(key)
        if node is None:
            return
        y = node
        y_original_color = y.color
        if node.left is None:
            x = node.right
            self.transplant(node, node.right)
        elif node.right is None:
            x = node.left
            self.transplant(node, node.left)
        else:
            y = self.minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self.transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color
        if y_original_color == 'black':
            self.delete_fixup(x)

    def delete_fixup(self, node):
        while node != self.root and node.color == 'black':
            if node == node.parent.left:
                w = node.parent.right
                if w.color == 'red':
                    w.color = 'black'
                    node.parent.color = 'red'
                    self.left_rotate(node.parent)
                    w = node.parent.right
                if w.left.color == 'black' and w.right.color == 'black':
                    w.color = 'red'
                    node = node.parent
                else:
                    if w.right.color == 'black':
                        w.left.color = 'black'
                        w.color = 'red'
                        self.right_rotate(w)
                        w = node.parent.right
                    w.color = node.parent.color
                    node.parent.color = 'black'
                    w.right.color = 'black'
                    self.left_rotate(node.parent)
                    node = self.root
            else:
                w = node.parent.left
                if w.color == 'red':
                    w.color = 'black'
                    node.parent.color = 'red'
                    self.right_rotate(node.parent)
                    w = node.parent.left
                if w.right.color == 'black' and w.left.color == 'black':
                    w.color = 'red'
                    node = node.parent
                else:
                    if w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        self.left_rotate(w)
                        w = node.parent.left
                    w.color = node.parent.color
                    node.parent.color = 'black'
                    w.left.color = 'black'
                    self.right_rotate(node.parent)
                    node = self.root
        node.color = 'black'

    def minimum(self, node):
        while node.left is not None:
            node = node.left
        return node
    
    def maximum(self, node):
        while node.right is not None:
            node = node.right
        return node
    
    def search(self, key):
        node = self.root
        while node is not None and node.key != key:
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return node
    
    def inorder(self, node):
        if node is not None:
            self.inorder(node.left)
            print(node.key, node.color)
            self.inorder(node.right)

    def preorder(self, node):
        if node is not None:
            print(node.key, node.color)
            self.preorder(node.left)
            self.preorder(node.right)

    def postorder(self, node):
        if node is not None:
            self.postorder(node.left)
            self.postorder(node.right)
            print(node.key, node.color)

    def levelorder(self):
        queue = []
        queue.append(self.root)
        while len(queue) > 0:
            node = queue.pop(0)
            print(node.key, node.color)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)    

if __name__ == '__main__':
    tree = RedBlackTree()
    l=[10,85,15,70,20,60,30,50]
    for i in l:
        tree.insert(i)
"""
#print tree 
    print('inorder')
    tree.inorder(tree.root)
    print('preorder')
    tree.preorder(tree.root)
    print('postorder')
    tree.postorder(tree.root)
    print('levelorder')
    tree.levelorder()
"""

def build_edges_colors(node, edges=None, colors=None):
    if edges is None or colors is None:
        edges = []
        colors = {}
    if node:
        colors[node.key] = node.color
        if node.left:
            edges.append((node.key, node.left.key))
            build_edges_colors(node.left, edges, colors)
        if node.right:
            edges.append((node.key, node.right.key))
            build_edges_colors(node.right, edges, colors)
    return edges, colors

def draw_tree(tree):
    edges, colors = build_edges_colors(tree.root)
    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    pos = graphviz_layout(graph, prog='dot')
    node_colors = [colors[node] for node in graph.nodes()]
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, node_size=2000)
    plt.show()

#Usage:
draw_tree(tree)