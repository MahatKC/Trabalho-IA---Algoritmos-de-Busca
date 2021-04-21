#Leonardo Vanzin
#Mateus Karvat Camara

#importa bibliotecas do Python a serem utilizadas
import numpy as np
import time
import copy

class Tree:
    # classe Tree cria um nó quando é chamada
    def __init__(self, data):
        # cada nó possui uma lista de seus nós filhos (children), uma lista dos pais (parents) que inclui todos os seus antepassados,
        # e o dado a ser armazenado
        self.children = []
        self.parents = []
        self.data = data

    def __str__(self):
    # quando print é chamada para um objeto do tipo Tree, ele exibe o dado do nó 
    # atual e dos filhos apenas desse nó
        children_data = []
        
        # o laço abaixo acessa cada filho do nó atual e recupera seu dado, colocando-o na lista "children_data"
        for child in self.children:
            child_data = str(child.data)
            children_data.append(child_data)
        
        a = "Data: "+str(self.data)+"\n"+"Children: "+str(children_data)
        return a

def verifica_validade(x,y):
    #a função verifica_validade checa se é válido posicionar uma rainha no tabuleiro no índice x e outra no índice y, retornando variável booleana

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

def inicia_arvore():
    #visto que o primeiro nível da árvore não segue o mesmo padrão que os demais, ele é criado fora da função recursiva na função inicia_arvore
    raiz = Tree(None)

    #o laço abaixo cria um nó para cada possível índice do tabuleiro e adiciona tais nós à lista de filhos da raiz da árvore
    #em sequência, chama-se a função recursive criar árvore para cada um desses nós
    for i in range(64):
        node = Tree(i)

        raiz.children.append(node)

        cria_arvore(node, i, 1)
    
    return raiz

def cria_arvore(node_pai, indice_pai, nivel):
    #a função cria_arvore é recursiva e é chamada para cada nó, criando os seus nós filhos
    
    #a arvore é criada no nivel 1 e deve ter no máximo 8 níves. logo, se nivel==9, a criação da árvore deve cessar
    if nivel==9:
        return None
    
    #verifica-se se o pai pode ter filhos. caso a posição de um nó seja inválida, tal nó é armazenado com um *, o que torna seu tipo de dado
    #uma string. Ex: o nó 1 como filho do nó 0 é inválido, logo é armazenado como '1*'. Logo, os filhos de '1*' não são criados.
    if type(node_pai.data) != str:
        #cria-se filhos para o nó pai atual com índices maiores que o do nó pai. Logo, a árvore é criada apenas com numeração crescente
        #Isto é: 0->10->25->...
        #isso elimina a verificação redundante em combinações já testadas, como 0->25->10->...
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
            
            #se o nó é inválido, ele é criado com um *, o que faz com que seu tipo de dado seja uma string
            else:
                node_atual.data=str(indice_atual)+"*"
            
            #após a criação do nó, ele é adicionado a lista de filhos de seu pai
            node_pai.children.append(node_atual)

            #incrementa-se o contador de nível da árvore
            nivel += 1
            
            #chama-se a função de forma recursiva para criar o próximo nível da árvore a partir do nó atual
            cria_arvore(node_atual, indice_atual, nivel)

def busca_em_profundidade_preliminar(no_inicial):
    #a função cria as variáveis necesárias para a busca em profundidade recursiva e exibe informações sobre a busca realizada
    
    caminhos=[0] #coloca o valor da posicao zero de respostas invalidas como 0 incialmente, 
                 #aqui foi utilizado uma lista de um único elemento para realizar passagem de parâmetro por referência no Python
    pilha = [] #cria a pilha que vai ser utilizada na busca em profundidade
    respostas_validas = [] #cria lista que sera armazenado os caminhos validos
    busca_em_profundidade_recursivo(no_inicial, pilha, respostas_validas, caminhos) #chama a função recursiva
    print("Número de respostas válidas:",len(respostas_validas)) #imprime o número de listas que que estao dentro de respostas_validas 
    print("Número de respostas inválidas:", caminhos[0]) #imprime a primeira posicao da lista, que contem o numero de caminhos invalidos
    print("Caminhos válidos:")
    exibir_respostas_validas(respostas_validas) #chama funcao para imprimir os caminhos validos

def exibir_respostas_validas(respostas_validas): 
    #função auxiliar para organizar as listas e imprimí-las bonitinho
    
    for resposta in respostas_validas:
    #percorre as listas que estao em respostas_validas
        
        resposta_para_printar = [] #cria uma lista para cada lista de caminhos validos
        
        for nozinho in resposta:
        #percorre  o conteudo das lista que estao dentro da lista respostas_validas
            resposta_para_printar.append(nozinho.data) 
            #coloca o valor de cada no na lista, isso porque o conteudo das listas eram os endereços dos nos
        print(resposta_para_printar) #imprime os caminhos validos

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

def tempera_simulada(M, P, L, alpha, T0, tree):
    #M= maximo de iterações do laço externo
    #P= maximo de iterações do laço interno
    #L= limite do número de sucessos
    #alpha= fator de redução da temperatura
    #T0= temperatura inicial
    #tree= raiz da árvore a ser buscada
    
    #algoritmo da tempera simulada tal qual descrito na literatura
    #ligeiras modificações foram realizadas para que os laços e condições se comportem como esperado no Python
    T=T0
    j=1
    S=RandomS0()

    while j<=M:
        i=1
        nSucesso=0
        while nSucesso<L and i<=P:
            Si=Perturba(S)
            delta_Fi = func_obj(Si,tree) - func_obj(S,tree)
            exp = np.exp(-delta_Fi/T)
            if delta_Fi<=0 or exp>Randomiza():
                S=Si
                nSucesso += 1
            i+=1
        T*=alpha

        j+=1
        if nSucesso==0:
            break
        
    #o retorno da função tempera_simulada é o custo da resposta obtida após o fim do algoritmo e o estado alcançado
    #ambas as variáveis de retorno podem ser usadas para checagem da eficácia do algoritmo
    return func_obj(S,tree), S

def Randomiza():
    #gera numero aleatorio entre 0 e 1
    return np.random.rand()

def RandomS0():
    #cria um estado S0 aleatório
    
    rng = np.random.default_rng()
    #gera uma lista de 8 inteiros distintos aleatoriamente
    x = rng.choice(64, size=8, replace=False)
    x_list = list(x)
    #ordena a lista de modo a torná-la estritamente crescente
    x_list.sort()

    return x_list

def func_obj(Si,tree):
    #função objetivo da busca na árvore

    cost = 0
    x = Si[0]   #x é o elemento de interesse da lista Si
    node = tree.children[x]  #acessa nó x no primeiro nivel da árvore
    for nivel in range(1,8):
        x = Si[nivel]   #atualiza x

        #cria lista com os dados dos filhos do nó de interesse
        children_data = []
        for child in node.children:
            children_data.append(child.data)

        #se x está entre os nós filhos do atual nó, passa-se o atual nó para o nó
        #cujo dado é x
        if x in children_data:
            indice_x = children_data.index(x)
            node = node.children[indice_x]
        #do contrário, o nó que contém x é um nó folha e calcula-se o custo de tal nó
        #o custo é calculado pelo número de filhos que o nó em questão não tem
        #ou seja, se ele está no 7º nível, ele não tem um filho no 8º nível nem no 9º e seu custo é 20
        else:
            cost = (9-nivel)*10
            break
    return cost

def Perturba(S):
    #sorteia o índice do elemento a ser perturbado
    indice = np.random.randint(8)

    #variavel booleana pra garantir a checagem correta dos IFs
    check = False

    while S[indice]-indice>=56:
        indice = np.random.randint(8)

    #se não é o último elemento
    if indice<7:
        #se o valor é 0, obriga a somar 1, exceto se o próximo valor é 1, 
        #aí não faz nada para evitar criar valores repetidos
        if S[indice]==0:
            check=True
            if S[indice+1]!=1:
                S[indice]+=1
        #se o elemento posterior é o número suscessor ao número atual, 
        #obriga a subtrair em 1 o número atual, visto que ele não é 0
        elif S[indice+1]==S[indice]+1:
            if indice>0:
                if S[indice-1]!=S[indice]-1:
                    S[indice]-=1
            check=True
        else:
            if indice>0:
                if S[indice-1]!=S[indice]-1:
                    S[indice]-=1
            check=True
    
    #se não é o primeiro elemento
    else:
        #se o elemento anterior é o número antecessor ao número atual, 
        # obriga a somar 1 no número atual, desde que ele não seja 63
        if S[indice-1]==S[indice]-1:
            check=True
            if S[indice]!=63:
                S[indice]+=1
        #se for 63 (mas o anterior não era 62), subtrai 1 dele
        elif S[indice]==63:
            S[indice]-=1
            check=True
    
    #se não for nenhum dos casos especiais acima, que obrigaria a somar ou subtrair,
    #escolhe aleatoriamente entre subtração e soma de 1
    if not check:
        #escolhe um número aleatório entre -1 e 1, então aplica função sinal nele,
        #obtendo -1 ou 1 aleatoriamente. então adiciona o resultado ao elemento 
        #perturbado
        perturbacao = int(np.sign(np.random.rand()*2-1))
        S[indice]+= perturbacao
    
    rng = np.random.default_rng()
    tamanho = 8-(indice+1)  #número de elementos a serem substituídos
    intervalo = 63-S[indice]    #intervalo de valores possível
    
    #cria uma lista de valores a serem substituídos após o valor perturbado
    try:
        x = rng.choice(intervalo, size=tamanho, replace=False)
    except:
        #prints para debug caso a função acima se comporte de forma inesperada
        print(f"tamanho={tamanho}, intervalo={intervalo}")
        print(S)
        print(f"indice={indice}, S[indice]={S[indice]}")
    x += int(S[indice]+1)
    x_list = list(x)
    x_list.sort()

    #substitui os valores de S pelos valores de x_list
    for i in range(len(x_list)):
        S[indice+1+i]=x_list[i]

    return S

T0=time.time()# pega o tempo antes de inciar a arvore
raiz = inicia_arvore()
T1=time.time()# pega o tempo depois de inciar a arvore e antes de realizar as busca
busca_em_profundidade_preliminar(raiz)
T2=time.time()# pega o tempo depois da busca
#o algoritmo de têmpera simulada obteve desempenho ruim, logo é executado múltiplas vezes
for i in range(100):
    #cria-se listas vazias para armazenar o custo e estado obtido após cada execução do algoritmo
    custos=[]
    estados=[]

    #o algoritmo é chamado com os parâmetros que apresentaram melhor resultado na busca por parâmetros (descrita no relatório)
    custo, S = tempera_simulada(50,160,32,0.98,200, raiz)

    #armazena-se o custo e estado da presente execução do algoritmo nas listas
    custos.append(custo)
    estados.append(S)
T3=time.time()#tempo após tempera simulada
menor_custo_sa = min(custos)
melhor_estado_sa = estados[custos.index(min(custos))]
print(f"Melhor custo obtido pela têmpera simulada: {menor_custo_sa}. Estado: {melhor_estado_sa}") #exibe o melhor estado obtido na tempera simulada
#por critério de comparação, testa-se uma busca totalmente aleatória similar à tempera simulada
T4=time.time()#tempo antes da busca aleatória
for i in range(100):
    custos_random=[]
    estados_random=[]

    S_random = RandomS0()
    custo_random = func_obj(S_random, raiz)

    custos_random.append(custo_random)
    estados_random.append(S_random)
T5=time.time()#tempo após busca aleatória
menor_custo_rand = min(custos_random)
melhor_estado_rand = estados_random[custos_random.index(min(custos_random))]
print(f"Melhor custo obtido pela busca aleatória: {menor_custo_rand}. Estado: {melhor_estado_rand}") #exibe o melhor estado obtido na busca aleatória

t_random = T5-T4
t_prof = T2-T1
t_sa = T3-T2
speedup_sa_rand=round(t_sa/t_random,1)
speedup_prof_sa=round(t_sa/t_prof,1)

print(f"Tempo para criar a árvore: {round(T1-T0,3)} segundos") #calcula o tempo gasto durante a criação da arvore
print(f"Tempo para busca em profundidade: {round(t_prof,3)} segundos") #calcula o tempo gasto durante a execução da busca
print(f"Tempo para execução da têmpera simulada: {round(t_sa,3)} segundos")
print(f"Tempo para execução da busca aleatória: {round(t_random,3)} segundos")
if menor_custo_rand==menor_custo_sa:
    print(f"A busca aleatória foi {speedup_sa_rand} mais rápida e obteve o mesmo custo que a têmpera simulada.")
elif abs(menor_custo_rand-menor_custo_sa)==10:
    print(f"A busca aleatória foi {speedup_sa_rand} mais rápida e obteve custo similar à têmpera simulada.")
else:
    print(f"A busca aleatória foi {speedup_sa_rand} mais rápida que a têmpera simulada.")
if menor_custo_sa>0:
    print(f"A busca em profundidade foi {speedup_prof_sa} mais rápida que a têmpera simulada e chegou a todas as respostas corretas, enquanto a têmpera simulada não chegou em nenhuma.")
else:
        print(f"A busca em profundidade foi {speedup_prof_sa} mais rápida que a têmpera simulada e chegou a todas as respostas corretas, enquanto a têmpera simulada chegou a apenas uma.")