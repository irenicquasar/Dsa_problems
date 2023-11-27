#red black trees
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
    #this function is used to convert the tree into a networkx graph
    def to_networkx(self):
        def add_nodes_and_edges(graph, colors, node):
            if node is not None:
                # Add the node to the graph
                graph.add_node(node.key)
                # Add the node's color to the colors dictionary
                colors[node.key] = node.color
                if node.left is not None:
                    graph.add_edge(node.key, node.left.key)
                    add_nodes_and_edges(graph, colors, node.left)
                else:
                    graph.add_edge(node.key, 'NIL')
                    colors['NIL'] = 'black'
                if node.right is not None:
                    graph.add_edge(node.key, node.right.key)
                    add_nodes_and_edges(graph, colors, node.right)
                else:
                    graph.add_edge(node.key, 'NIL')
                    colors['NIL'] = 'black'

        graph = nx.DiGraph()
        colors = {}
        add_nodes_and_edges(graph, colors, self.root)
        edges = list(graph.edges())
        return graph, colors, edges
    
    def __init__(self):
        self.root = None

    #this function is used to insert a node into the tree
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

    #this function is used to fix the tree after insertion
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

    #this function is used to left rotate the tree
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

    #this function is used to right rotate the tree
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

    #this function is used to transplant the tree    
    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent
        return v

    #this function is used to delete a node from the tree
    def delete(self, key):
        node = self.search(key)
        if node is None:
            return
        y = node
        y_original_color = y.color
        if node.left is None:
            x = self.transplant(node, node.right)
        elif node.right is None:
            x = self.transplant(node, node.left)
        else:
            y = self.minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                if x is not None:
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
            if x is not None:
                self.delete_fixup(x)

    #this function is used to fix the tree after deletion
    def delete_fixup(self, node):
        while node != self.root and node.color == 'black':
            if node == node.parent.left:
                w = node.parent.right
                if w is not None and w.color == 'red':
                    w.color = 'black'
                    node.parent.color = 'red'
                    self.left_rotate(node.parent)
                    w = node.parent.right
                if w is not None and w.left is not None and w.right is not None and w.left.color == 'black' and w.right.color == 'black':
                    w.color = 'red'
                    node = node.parent
                else:
                    if w is not None and w.right is not None and w.right.color == 'black':
                        if w.left is not None:
                            w.left.color = 'black'
                        w.color = 'red'
                        self.right_rotate(w)
                        w = node.parent.right
                    if w is not None:
                        w.color = node.parent.color
                        node.parent.color = 'black'
                        if w.right is not None:
                            w.right.color = 'black'
                        self.left_rotate(node.parent)
                        node = self.root
            else:
                w = node.parent.left
                if w is not None and w.color == 'red':
                    w.color = 'black'
                    node.parent.color = 'red'
                    self.right_rotate(node.parent)
                    w = node.parent.left
                if w is not None and w.right is not None and w.left is not None and w.right.color == 'black' and w.left.color == 'black':
                    w.color = 'red'
                    node = node.parent
                else:
                    if w is not None and w.left is not None and w.left.color == 'black':
                        if w.right is not None:
                            w.right.color = 'black'
                        w.color = 'red'
                        self.left_rotate(w)
                        w = node.parent.left
                    if w is not None:
                        w.color = node.parent.color
                        node.parent.color = 'black'
                        if w.left is not None:
                            w.left.color = 'black'
                        self.right_rotate(node.parent)
                        node = self.root
        node.color = 'black'

    #this function is used to find the minimum node in the tree
    def minimum(self, node):
        while node.left is not None:
            node = node.left
        return node
    
    #this function is used to find the maximum node in the tree
    def maximum(self, node):
        while node.right is not None:
            node = node.right
        return node
    
    #this function is used to search for a node in the tree
    def search(self, key, node=None):
        if node is None:
            node = self.root
        while node is not None and node.key != key:
            if key < node.key:
                node = node.left
            else:
                node = node.right
        if node is None:
            return "Key not found in the tree"
        else:
            return node

#this function is used to build the edges and colors of the tree
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

#this function is used to draw the tree
def draw_tree(tree):
    graph, colors, edges = tree.to_networkx()
    if len(graph) == 1:
        # Add a self-loop edge if the graph only contains a single node
        node = list(graph.nodes())[0]
        graph.add_edge(node, node)
    graph.add_edges_from(edges)
    pos = graphviz_layout(graph, prog='dot')
    node_colors = [colors[node] for node in graph.nodes()]
    nx.draw(graph, pos, with_labels=False, node_color=node_colors, node_size=2000)
    nx.draw_networkx_labels(graph, pos, font_color='white')
    plt.show()

if __name__ == '__main__':
    tree = RedBlackTree()
    l=[10,85,15,70,20,60,30,50]
    for i in l:
        tree.insert(i)   
    search=tree.search(420)
    if isinstance(search, str):
        print(search)
    else:
        print(search.key)            
    draw_tree(tree)
    tree.delete(15)
    draw_tree(tree)
