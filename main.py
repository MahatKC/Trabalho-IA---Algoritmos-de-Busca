import numpy as np
import time
import copy
#Leonardo Vanzin
#Mateus Karvat Camara
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

def exibir_respostas_validas(respostas_validas): #função para organizar as listas para imprimir bonitinho
    for resposta in respostas_validas:#percorre as lista que estao em respostas_validas
        resposta_para_printar = [] #cria uma lista para cada lista de caminhos validos
        for nozinho in resposta:#percorre  o conteudo das lista que estao dentro da lista respostas_validas
            resposta_para_printar.append(nozinho.data) #coloca o valor de cada no na lista, isso porque o conteudo das listas eram os endereços dos nos
        print(resposta_para_printar) #imprime os caminhos validos

def busca_em_profundidade_preliminar(no_inicial):
    caminhos=[0] #coloca o valor da posicao zero de respostas invalidas como 0 incialmente, 
                 #foi utilizado uma lista pois ao passar uma variavel como parametro para uma funcao é somente passado o valor dela e nao a referencia
    pilha = [] #cria a pilha que vai ser utilizada na busca em profundidade
    respostas_validas = [] #cria lista que sera armazenado os caminhos validos
    busca_em_profundidade_recursivo(no_inicial, pilha, respostas_validas, caminhos)
    print("Número de respostas válidas:",len(respostas_validas)) #imprime o numero de listas que que estao dentro de respostas_validas 
    print("Número de respostas inválidas:", caminhos[0]) #imprime a primeira posicao da lista, que contem o numero de caminhos invalidos
    print("Caminhos válidos:")
    exibir_respostas_validas(respostas_validas) #chama funcao para imprimir os caminhos validos

def busca_em_profundidade_recursivo(no_referencia, pilha, respostas_validas, caminhos):
    pilha.append(no_referencia) #passa o no inicial
    for no_filho in no_referencia.children: #percorre a arvore, indo de filho em filho
        busca_em_profundidade_recursivo(no_filho, pilha, respostas_validas, caminhos)
    if (len(pilha)>9) : #seleciona os caminhos que sao maior que 9, porque sao os caminhos que possuem os 8 niveis
        if pilha[1:-1] not in respostas_validas: #verifica se ja existe um dentro da lista, para evitar respostas repetidas
            respostas_validas.append(pilha[1:-1]) #coloca na lista de respostas validas tirando o no raiz e o ultimo filho, o ultimo filho é tirado pois o pai dele ja é o 8 nivel
    elif (len(pilha)==9 and pilha[-1].data==63):#como o 63 é o ultimo no possivel ele nao tem filho, mas tem casos em que o 63 é valido para a resposta, 
                                                #assim verificamos se no 8 nivel tem o 63 e com isso colocamos ele na lista
        if pilha[1:] not in respostas_validas: #neste caso como o 63 é o ultimo nivel e ele nao possui filho, tiramos somente o no raiz
            respostas_validas.append(pilha[1:])
    else:
        caminhos[0]+=1 #contabiliza quantos caminhos invalidos foram encontrados na primeira posicao da lista
    pilha.pop(pilha.index(no_referencia)) #seguindo o algoritmo da busca em profundidade elimina-se o no da pilha

T0=time.time()# pega o tempo antes de inciar a arvore
raiz = inicia_arvore()
T1=time.time()# pega o tempo depois de inciar a arvore e antes de realizar as busca
busca_em_profundidade_preliminar(raiz)
T2=time.time()# pega o tempo depois da busca
print(f"Tempo para criar a árvore: {round(T1-T0,3)} segundos") #calcula o tempo gasto durante a criação da arvore
print(f"Tempo para busca em profundidade: {round(T2-T1,3)} segundos") #calcula o tempo gasto durante a execução da busca