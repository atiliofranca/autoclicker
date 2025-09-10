import pyautogui
import time
import random
import tkinter as tk
from tkinter import messagebox

def get_coordinates_from_user():
    """
    Pede ao usuário para posicionar o mouse e captura as coordenadas após um timer.
    """
    root = tk.Tk()
    root.withdraw()

    if messagebox.askokcancel("Configurar Clique", "Clique em OK para começar a configurar o ponto de clique.", parent=root):
        messagebox.showinfo("Captura de Ponto", "Coloque o mouse no local de clique.\nCapturando em 5 segundos...", parent=root)
        
        print("Capturando ponto de clique em 5 segundos...")
        time.sleep(5)
        
        mouse_x, mouse_y = pyautogui.position()
        print(f"Ponto de clique salvo: ({mouse_x}, {mouse_y})")
        
        # Janela de confirmação final para começar
        if messagebox.askokcancel("Ponto Salvo!", f"Ponto de clique salvo: ({mouse_x}, {mouse_y})\n\nClique em OK para iniciar a automação.", parent=root):
            return mouse_x, mouse_y
    
    return None, None

# função usada para mover o char em direções aleatórias, para o jogo não fechar por inatividade
def direcoes_aleatorias(num_direcoes=random.randint(4, 10)):
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

# Início do script principal
if __name__ == "__main__":
    time.sleep(2) # tempo de espera do run na aplicação até ir à janela do jogo

    # Obtém as coordenadas do clique do usuário via pop-up
    click_x, click_y = get_coordinates_from_user()

    if click_x is None:
        print("Operação cancelada. Saindo do script.")
        exit()

    for i in range(100):
        print(f"Execução número: {i + 1}")
        time.sleep(1)
        pyautogui.click(x=click_x, y=click_y)
        time.sleep(1)
        direcoes_aleatorias()
        numero_aleatorio = random.randint(183, 203)
        print(f'O tempo de espera será de {numero_aleatorio} segundos')
        for i in range (numero_aleatorio):
            print(f'faltam {numero_aleatorio-i} segundos')
            time.sleep(1)

    print("Todas as 100 repetições foram concluídas!")