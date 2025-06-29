import pyautogui
import time
import random

time.sleep(2)

def direcoes_aleatorias(num_direcoes = random.randint(4, 10)):
    direcoes_disponiveis = ['up', 'down', 'left', 'right']
    direcoes_a_acionar = []
    print(f"Preparando para acionar {num_direcoes} direções aleatórias...")

    for _ in range(num_direcoes):
        direcao_escolhida = random.choice(direcoes_disponiveis)
        direcoes_a_acionar.append(direcao_escolhida)
    print(f"Direções escolhidas para acionar: {direcoes_a_acionar}")

    for i, direcao in enumerate(direcoes_a_acionar):
        pyautogui.press(direcao)
        tempo_aleatorio = random.uniform(0.3, 0.8)
        time.sleep(tempo_aleatorio)

for i in range(100):
    print(f"Execução número: {i + 1}")
    time.sleep(1)
    pyautogui.click(x=2032, y=494)
    time.sleep(1)
    direcoes_aleatorias()
    numero_aleatorio = random.randint(183, 203)
    print(f'O tempo de espera será de {numero_aleatorio} segundos')
    for i in range (numero_aleatorio):
        print(f'faltam {numero_aleatorio-i} segundos')
        time.sleep(1)

print("Todas as 100 repetições foram concluídas!")