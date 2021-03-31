import numpy as np
import time

class Tree:
    # classe Tree cria um nó quando é chamada
    def __init__(self, data):
        self.children = []
        self.parents = []
        self.data = data

    def __str__(self):
    # quando print é chamada para um objeto do tipo Tree, ele exibe o dado do nó 
    # atual e dos filhos apenas desse nó
        children_data = []
        for child in self.children:
            child_data = str(child.data)
            children_data.append(child_data)
        a = "Data: "+str(self.data)+"\n"+"Children: "+str(children_data)
        return a

def verifica_validade(x,y):
    #verifica se estao na mesma linha
    if x//8==y//8:
        return False
    #verifica se estao na mesma coluna
    elif x%8==y%8:
        return False
    #verifica se estao na mesma diagonal principal (\)
    elif abs(x-y)%9==0 and max(x,y)%8>min(x,y)%8:
        return False
    #verifica se estao na mesma diagonal secundaria (/)
    elif abs(x-y)%7==0 and max(x,y)%8<min(x,y)%8:
        return False
    #se todas as verificacoes passaram a posicao e valida
    else:
        return True

#def cria_arvore():

root = Tree(None)
for i in range(64):
    node = Tree(i)
    
    for j in range(i+1, 64):
        if verifica_validade(i,j):
            node_filho = Tree(j)
        else:
            node_filho=Tree(str(j)+"*")
        node_filho.parents.append(i)

        for k in range(j+1,64):
            if type(node_filho.data) != str:
                node_neto = Tree(None)
                node_neto.parents=node_filho.parents
                node_neto.parents.append(j)
                valido=True
                for parent in node_neto.parents:
                    if not verifica_validade(parent,k):
                        valido=False
                        break
                if valido:
                    node_neto.data = k
                else:
                    node_neto.data=str(k)+"*"
                node_filho.children.append(node_neto)
               


        node.children.append(node_filho)

    root.children.append(node)

print(root.children[0].children[9])