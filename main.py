# aplicação usada para teste para rachar eggs automaticamente dentro do jogo pokebro

import pyautogui
import time
import random

time.sleep(2) # tempo de espera do run na aplicação até ir à janela do jogo

# função usada para mover o char em direções aleatórias, para o jogo não fechar por inatividade
def direcoes_aleatorias(num_direcoes = random.randint(4, 10)): # aleatoreamente é escolhida de 4 até 10 direções
    direcoes_disponiveis = ['up', 'down', 'left', 'right']
    direcoes_a_acionar = []
    print(f"Preparando para acionar {num_direcoes} direções aleatórias...")

    for _ in range(num_direcoes):
        direcao_escolhida = random.choice(direcoes_disponiveis)
        direcoes_a_acionar.append(direcao_escolhida)
    print(f"Direções escolhidas para acionar: {direcoes_a_acionar}")

    for i, direcao in enumerate(direcoes_a_acionar):
        pyautogui.press(direcao)
        tempo_aleatorio = random.uniform(0.3, 0.8) # intervalo de acionamento de uma direção para outra, escolhido aleatoreamente entre 0,3 e 0,8 seg
        time.sleep(tempo_aleatorio)

# random.randint(4, 10): usado para aleatóriedade de números inteiros
# random.uniform(0.3, 0.8): usado para aleatoriedade de números fracionados

for i in range(100): # REGRA DE NEGÓCIO 1: esse clique precisa ser feito 100 vezes por egg
    print(f"Execução número: {i + 1}")
    time.sleep(1)
    pyautogui.click(x=2032, y=494) # coletado manualmente usando arquivo auxiliar.py. Essa localização muda de tela para tela
    time.sleep(1)
    direcoes_aleatorias()
    numero_aleatorio = random.randint(183, 203) # REGRA DE NEGÓCIO 2: intervalo de um clique ao outro deve ser ser pelo menos 180 seg. Está de 183 à 203 para aletoriedade
    print(f'O tempo de espera será de {numero_aleatorio} segundos')
    for i in range (numero_aleatorio):
        print(f'faltam {numero_aleatorio-i} segundos') # contagem regressiva até o próximo clique
        time.sleep(1)

print("Todas as 100 repetições foram concluídas!")