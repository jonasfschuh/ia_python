from math import inf as infinity
from random import choice
import platform
import time
from os import system
HUMANO = -1
COMPUTADOR = +1
tabuleiro = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
def main():
    limparConsole()
    escolha_humano = ''
    escolha_computador = ''
    primeiroJogador = ''
    while escolha_humano != 'O' and escolha_humano != 'X':
        print('')
        escolha_humano = input('Escolha X ou O\nEscolhido: ').upper()
    if escolha_humano == 'X':
        escolha_computador = 'O'
    else:
        escolha_computador = 'X'
    limparConsole()
    while primeiroJogador != 'S' and primeiroJogador != 'N':
        primeiroJogador = input('Quer começar primeiro?[s/n]: ').upper()
    while len(verificaCelulasLimpas(tabuleiro)) > 0 and not fimDeJogo(tabuleiro):
        if primeiroJogador == 'N':
            (escolha_computador, escolha_humano)
            primeiroJogador = ''
        jogada_humano(escolha_computador, escolha_humano)
        jogada_computador(escolha_computador, escolha_humano)
    if venceu(tabuleiro, HUMANO):
        limparConsole()
        print(f'Vez do humano [{escolha_humano}]')
        desenhar(tabuleiro, escolha_computador, escolha_humano)
        print('PARABÉNS!')
    elif venceu(tabuleiro, COMPUTADOR):
        limparConsole()
        print(f'Vez do computador [{escolha_computador}]')
        desenhar(tabuleiro, escolha_computador, escolha_humano)
        print('PERDEU Playboy!')
    else:
        limparConsole()
        desenhar(tabuleiro,  escolha_computador, escolha_humano)
        print('EMPATE!')
    exit()
    
#Verifica se acabou o jogo
def fimDeJogo(estado_atual):
    return venceu(estado_atual, HUMANO) or venceu(estado_atual, COMPUTADOR)

#verificar se um dos jogadores venceu
def venceu(estado, jogador):
    combinacoes_vitoria = [
        [estado[0][0], estado[0][1], estado[0][2]],
        [estado[1][0], estado[1][1], estado[1][2]],
        [estado[2][0], estado[2][1], estado[2][2]],
        [estado[0][0], estado[1][0], estado[2][0]],
        [estado[0][1], estado[1][1], estado[2][1]],
        [estado[0][2], estado[1][2], estado[2][2]],
        [estado[0][0], estado[1][1], estado[2][2]],
        [estado[2][0], estado[1][1], estado[0][2]],
    ]
    if [jogador, jogador, jogador] in combinacoes_vitoria:
        return True
    else:
        return False
    
#Verifica quais celulas estao limpas
def verificaCelulasLimpas(estado):
    celulas = []
    for pos_x, linha in enumerate(estado):
        for pos_y, celula in enumerate(linha):
            if celula == 0:
                celulas.append([pos_x, pos_y])
    return celulas

#Verifica o estado atual do tabuleiro
def verificarEstado(estado):
    score = 0
    if venceu(estado, COMPUTADOR):
        score += 1
    elif venceu(estado, HUMANO):
        score = -1
    else:
        score = 0
    return score

#Valida se o movimento eh valido
#Para ser valido, a posicao no tabuleiro deve estar vazia
def movimentoEhValido(pos_x, pos_y):
    if [pos_x, pos_y] in verificaCelulasLimpas(tabuleiro):
        return True
    else:
        return False
    
#Realiza uma jogada no tabuleiro
def jogadaEm(pos_x, pos_y, jogador):
    if not movimentoEhValido(pos_x, pos_y):
        return False
    else:
        tabuleiro[pos_x][pos_y] = jogador
        return True
    
#Limpa o console
def limparConsole():
    system('cls')
    
#Desenha o tabuleiro na tela
def desenhar(estado, escolha_computador, escolha_humano):
    possiveis_simbolos = {
        -1: escolha_humano,
        +1: escolha_computador,
        0: ' '
    }
    linha_base = '...............'
    print('\n' + linha_base)
    for linha in estado:
        for celula in linha:
            simbolo = possiveis_simbolos[celula]
            print(f'| {simbolo} |', end='')
        print('\n' + linha_base)
        
#Define qual vai ser a jogada que o computador vai fazer
def jogada_computador(escolha_computador, escolha_humano):
    celulasLimpas = len(verificaCelulasLimpas(tabuleiro))
    if celulasLimpas == 0 or fimDeJogo(tabuleiro):
        return
    limparConsole()
    print(f'Jogada do computador:  [{escolha_computador}]')
    desenhar(tabuleiro, escolha_computador, escolha_humano)
    if celulasLimpas == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(tabuleiro, celulasLimpas, COMPUTADOR)
        x, y = move[0], move[1]
    jogadaEm(x, y, COMPUTADOR)
    time.sleep(1)
    
#O humano define qual jogada vai ser
def jogada_humano(escolha_computador, escolha_humano):
    celulasVazias = len(verificaCelulasLimpas(tabuleiro))
    if celulasVazias == 0 or fimDeJogo(tabuleiro):
        return
    jogada = -1
    jogadas = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }
    limparConsole()
    print(f'Escolha do humano [{escolha_humano}]')
    desenhar(tabuleiro, escolha_computador, escolha_humano)
    while jogada < 1 or jogada > 9:
        jogada = int(input('Utilize o teclado númerico (números de 1 a 9) : '))
        coordenada = jogadas[jogada]
        podeMover = jogadaEm(coordenada[0], coordenada[1], HUMANO)
        if not podeMover:
            print('Movimento inválido')
            move = -1
            
#Verifica qual a melhor jogada, dependendo do jogador que esta naquela posicao do tabuleiro
def calcularMelhorJogada(jogador):
    if jogador == COMPUTADOR:
        return [-1, -1, -infinity]
    else:
        return [-1, -1, +infinity]
    
#Define a proxima jogada para o jogador
def defineProximaJogada(jogador, celulasVazias, estado, melhorJogada):
    for celula in verificaCelulasLimpas(estado):
        x, y = celula[0], celula[1]
        estado[x][y] = jogador
        score = minimax(estado, celulasVazias - 1, -jogador)
        estado[x][y] = 0
        score[0], score[1] = x, y
        if jogador == COMPUTADOR:
            if score[2] > melhorJogada[2]:
                return score
        else:
            if score[2] < melhorJogada[2]:
                return score
            
#Funcao heuristica para definir o melhor movimento para o computador
def minimax(estado, celulasVazias, jogador):
    melhorJogada = calcularMelhorJogada(jogador)
    if celulasVazias == 0 or fimDeJogo(estado):
        score = verificarEstado(estado)
        return [-1, -1, score]
    melhorJogada = defineProximaJogada(jogador, celulasVazias, estado, melhorJogada)  
    return melhorJogada

if __name__ == '__main__':
    main()
