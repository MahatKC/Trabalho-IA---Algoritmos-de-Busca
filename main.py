import numpy as np
import time

class Tree:
    # classe Tree cria um nó quando é chamada
    def __init__(self, data):
        self.children = []
        self.data = data

    def __str__(self):
    # quando print é chamada para um objeto do tipo Tree, ele exibe o dado do nó 
    # atual e dos filhos apenas desse nó
        children_data = []
        for child in self.children:
            child_data = str(child.data)
            if len(child.children)==0:
                child_data += "*"
            children_data.append(child_data)
        a = "Data: "+str(self.data)+"\n"+"Children: "+str(children_data)
        return a

root = Tree(None)
for i in range(64):
    node = Tree(i)
    
    for j in range(64):
        if j!=i:
            node_filho = Tree(j)
            node.children.append(node_filho)

    root.children.append(node)

