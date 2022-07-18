# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 19:24:15 2022
algoritmo genetico python

@author: jonas
""" 

import math
import random
import numpy as np
from random import sample
import matplotlib.pyplot as plt
# Inicializando as variaveis
criterioDeParada = 1000
totalDeCidades = 20
quantidadeCidades = 0
tamanhoDaPopulacaoAtual = 0
taxaDeMutacao = 0.5
distanciaEntreCidadesTemporaria = np.zeros((totalDeCidades,totalDeCidades))
distanciaEntreCidadesAptidao = np.zeros((totalDeCidades,1))
probabilidadeRoleta = []
x = []
y = []
populacao = [20]
cidadesPelasQuaisCaminhou = []

# funcao principal
def algoritmoGenetico():
    gerarDistanciasAleatoriasEntreCidades()
    codificarPopulacaoDeIndividuos()
    verificaQualMelhorPaiAtravesDeRoleta()
    calcularDistanciaEuclidiana()
    funcaoDeAptidao()
    ordenarCustoCrescente()
    selecionaMelhoresPaisNaPopulacaoAtual()
    resultadoParcial(1)
    for i in range(criterioDeParada):
        crossingOver()
        mutacao()
        calcularDistanciaEuclidiana()
        funcaoDeAptidao()
        ordenarCustoCrescente()
        resultadoParcial(i)
        
# gera a populacao de individuos inicial 
def codificarPopulacaoDeIndividuos():
    for i in range(totalDeCidades):
        sorteados = random.sample(range(0, 20), 20)
        caminharPelasCidades(sorteados)
        populacao.append(sorteados)
    del populacao[0]
    
# simula o caminho pelas cidades
def caminharPelasCidades(sorteadosT):
    sorteadosT.append(sorteadosT[0])
    cidadesPelasQuaisCaminhou.append(sorteadosT)
    
# gera distancias aleatorias entre as cidades
# usamos o random.uniform para gerar as distancias -> ele pega um valor aleatório entre 0 e 1
def gerarDistanciasAleatoriasEntreCidades():
    for i in range(totalDeCidades):
        x.append(random.uniform(0,1))
        y.append(random.uniform(0,1))
        
# calcula distancia euclidiana 
def calcularDistanciaEuclidiana():
    for i in range(totalDeCidades):
        for j in range(totalDeCidades):
            distanciaEntreCidadesTemporaria[i][j] = math.sqrt((x[i]-x[j])**2+(y[i]-y[j])**2)
            
# definindo a funcao de aptidao 
# somar todas as distancias dentre as cidades e valida o menor valor         
def funcaoDeAptidao():
        global distanciaEntreCidadesAptidao
        for linha in range(totalDeCidades):
            distanciaEntreCidadesAptidao[linha] = 0
            for coluna in range(totalDeCidades):
                distanciaEntreCidadesAptidao[linha] = distanciaEntreCidadesAptidao[linha] + distanciaEntreCidadesTemporaria[cidadesPelasQuaisCaminhou[linha][coluna]][cidadesPelasQuaisCaminhou[linha][coluna+1]]*taxaDeMutacao  
                
# orderna do menor para o maior custo
def ordenarCustoCrescente():
    global distanciaEntreCidadesAptidao, populacao
    distanciaEntreCidadesAptidao, populacao = (list(t) for t in zip(*sorted(zip(distanciaEntreCidadesAptidao, populacao))))
    
# seleciona os melhores pais possiveis na populacao
def selecionaMelhoresPaisNaPopulacaoAtual():
        global populacao
        cromossomosRuins = len(populacao)
        cromossomosBons = cromossomosRuins//2
        del populacao[cromossomosBons:cromossomosRuins]
        
# verifica qual melhor pai atraves da metodologia de roleta
def verificaQualMelhorPaiAtravesDeRoleta():
    manter = math.floor(taxaDeMutacao*totalDeCidades)+1
    index = 10
    for i in range(1,manter):
        probabilidadeRoleta.extend(np.repeat(index,i))
        index -= 1
        
# realiza o crossing over entre os cromossomos
def crossingOver():
    escolha1 = sample(range(0, 10), 5)
    escolha2 = sample(range(0, 10), 5)
    for i in range(5):
        pai1 = populacao[escolha1[0]]
        pai2 = populacao[escolha2[0]]
        xp=math.ceil(random.randint(0, 20))
        temp = pai1
        x0=xp
        while pai1[xp] != temp[x0]:
            pai1[xp] = pai2[xp]
            pai2[xp]=temp[xp]
            xs= temp.find(pai1[xp])
            xp=xs
        populacao.append(pai1) 
        populacao.append(pai2)
        
# seleciona uma cidade aleatoriamente na populacao e troca seus cromossomos    
def mutacao():
    for i in range(9):
        individuoSelecionado = random.randint(0, 19)
        cromossomo1 = random.randint(0, 9)
        cromossomo2 = random.randint(0, 9)
        cromossomoTrocaDeLugar = populacao[individuoSelecionado][cromossomo1]
        populacao[individuoSelecionado][cromossomo1] = populacao[individuoSelecionado][cromossomo2]
        populacao[individuoSelecionado][cromossomo2] = cromossomoTrocaDeLugar
        
# retorna o tamanho da populacao
def tamanhoDaPopulacao():
    contador = 0
    for linha in range(len(populacao)):
        for coluna in range(len(populacao)):
            contador = contador + 1
    return contador

# retorna o numero de cidades 
def quantidadeDeCidades():
    contador = 0
    for linha in range(len(populacao)):
            contador = contador + 1
    return contador

# mostra o resultados dos melhores
def resultadoParcial(it):
    global tamanhoDaPopulacaoAtual
    tamanhoDaPopulacaoAtual = tamanhoDaPopulacaoAtual + tamanhoDaPopulacao()
    global quantidadeCidades
    quantidadeCidades = quantidadeCidades + quantidadeDeCidades()
    print("#####################################")
    print("Tamanho da população", tamanhoDaPopulacaoAtual)
    print("Taxa de Mutação", taxaDeMutacao) 
    print("Número de Cidades", quantidadeCidades)  
    print("Menor custo %.4f  " % distanciaEntreCidadesAptidao[0])
    print("Melhor solução", populacao[0])
    print("Iteração número", it)
    print("#####################################")
    print("\n")
    
# exibindo o grafico com resultado do algoritmo genetico 
def exibirResultado(totalDeCidades):
    rota_horizontal = np.zeros([20,1], dtype=np.float64)
    rota_vertical = np.zeros([20,1], dtype=np.float64)
    for i in range (totalDeCidades):
        rota_horizontal[i]=(x[populacao[0][i]])
        rota_vertical[i]=(y[populacao[0][i]])
    plt.figure(4)
    plt.plot(rota_horizontal,rota_vertical,'--y')
    plt.plot(rota_horizontal,rota_vertical,'ob')
    plt.title("Resolução Caixeiro Viajante - Algoritmo Genético")
    plt.show()
    
# iniciando programa              
algoritmoGenetico()

# mostra o resultado
exibirResultado(totalDeCidades)

