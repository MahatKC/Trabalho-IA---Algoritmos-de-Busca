import numpy as np
import time
import copy

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

def cria_arvore(node_pai, indice_pai, nivel):
    #a arvore é criada no nivel 1 e deve ter no máximo 8 níves. logo, se nivel==9, a criação da árvore deve cessar
    if nivel==9:
        return None
    #verifica-se se o pai pode ter filhos. caso a posição de um nó seja inválida, tal nó é armazenado com um *, o que torna seu tipo de dado
    #uma string.
    if type(node_pai.data) != str:
        #cria-se filhos para o nó pai atual com índices maiores que o do nó pai. Logo, a árvore é criada apenas com numeração ascendente
        #Isto é: 0->10->25->...
        #isso elimina a verificação repetida em combinações já testadas, como 0->25->10->...
        for indice_atual in range(indice_pai+1,64):
            #cria-se um nó vazio
            node_atual = Tree(None)
            #copia-se os nós do pai para o nó recém-criado
            node_atual.parents=copy.deepcopy(node_pai.parents)
            #adiciona-se o pai na lista de pais do nó atual
            node_atual.parents.append(indice_pai)
            valido=True
            #verifica-se se a posição do nó atual é válida em relação a cada um dos nós pai que o precederam na árvore
            for parent in node_atual.parents:
                if not verifica_validade(parent,indice_atual):
                    valido=False
                    break
            #caso o nó seja válido, adiciona-se o índice atual a ele
            if valido:
                node_atual.data = indice_atual
            else:
                node_atual.data=str(indice_atual)+"*"
            #após a criação do nó, ele é adicionado a lista de filhos de seu pai
            node_pai.children.append(node_atual)

            #incrementa-se o contador de nível da árvore
            nivel += 1
            #chama-se a função de forma recursiva para criar o próximo nível da árvore a partir do nó atual
            cria_arvore(node_atual, indice_atual, nivel)

def inicia_arvore():
    #visto que o primeiro nível da árvore não segue o mesmo padrão que os demais, ele é criado fora da função recursiva
    raiz = Tree(None)
    for i in range(64):
        node = Tree(i)

        raiz.children.append(node)

        cria_arvore(node, i, 1)
    
    return raiz

def busca_em_profundidade_preliminar(no_inicial):
    pilha = []
    busca_em_profundidade_recursivo(no_inicial, pilha)

def busca_em_profundidade_recursivo(no_referencia, pilha):
    pilha.append(no_referencia)
    for no_filho in no_referencia.children:
        busca_em_profundidade_recursivo(no_filho,pilha)
    if len(pilha)>8:
        print(f"Tamanho da pilha: {len(pilha)}")
        pilha_para_printar = []
        for nozinho in pilha[1:]:
            pilha_para_printar.append(nozinho.data)
        print(pilha_para_printar)
        print("-"*10)
    pilha.pop(pilha.index(no_referencia))

raiz = inicia_arvore()
busca_em_profundidade_preliminar(raiz)