import pyautogui
import time
import random
import tkinter as tk
from tkinter import simpledialog, messagebox

# Variáveis globais para controlar a execução do script de pesca e a última direção
fishing_is_active = False
last_direction = None
after_id = None # Variável para controlar o agendamento da tarefa
last_action_time = time.time() # Variável global para o temporizador

def get_fishing_key():
    """
    Pede ao usuário para escolher a tecla de atalho de pesca.
    """
    root = tk.Tk()
    root.withdraw()
    
    keys = [f'F{i}' for i in range(1, 13)]
    
    message = "Escolha a tecla de atalho para pesca (F1 a F12)."
    
    user_key = simpledialog.askstring("Tecla de Atalho", message, parent=root)
    
    if user_key and user_key.upper() in keys:
        print(f"Tecla de atalho salva: {user_key.upper()}")
        return user_key.lower()
    else:
        messagebox.showerror("Erro", "Tecla de atalho inválida. Saindo do script.")
        return None

def get_exclamation_region():
    """
    Guia o usuário para definir o ponto central da região de monitoramento da exclamação.
    """
    root = tk.Tk()
    root.withdraw()
    
    if messagebox.askokcancel("Configurar Região", "Agora vamos configurar a área de busca da exclamação.\n\nColoque o mouse no CENTRO do ícone da exclamação e clique em OK para continuar.", parent=root):
        
        messagebox.showinfo("Captura de Região", "Capturando em 5 segundos...", parent=root)
        print("Capturando ponto central da região em 5 segundos...")
        time.sleep(5)
        
        center_x, center_y = pyautogui.position()

        # Aumentando o tamanho do quadrado de busca para maior confiabilidade
        width = 100
        height = 60
        
        # Calcula as coordenadas do canto superior esquerdo para a região
        left = center_x - width // 2
        top = center_y - height // 2
        region = (left, top, width, height)
        
        print(f"Região de busca salva: {region}")
        return region
    
    return None

def get_fishing_click_coordinates():
    """
    Pede ao usuário para posicionar o mouse e captura as coordenadas de clique de pesca.
    """
    root = tk.Tk()
    root.withdraw()

    if messagebox.askokcancel("Configurar Clique", "Agora vamos configurar o ponto de clique de pesca.\n\nClique em OK para continuar.", parent=root):
        messagebox.showinfo("Captura de Ponto", "Coloque o mouse no local de clique de pesca.\nCapturando em 5 segundos...", parent=root)
        
        print("Capturando ponto de clique em 5 segundos...")
        time.sleep(5)
        
        mouse_x, mouse_y = pyautogui.position()
        print(f"Ponto de clique salvo: ({mouse_x}, {mouse_y})")

        return mouse_x, mouse_y
    
    return None, None

def start_fishing_action(fishing_key, mouse_x, mouse_y):
    """
    Prepara o personagem e inicia a pesca.
    """
    global last_direction
    print("Iniciando a pesca...")
    
    # AÇÃO DE INÍCIO: Vira o personagem para baixo ANTES de lançar a vara.
    pyautogui.hotkey('ctrl', 'down')
    time.sleep(3) # AUMENTO NO TEMPO DE ESPERA
    last_direction = 'down'  # Define a última direção para que não seja escolhida em seguida.

    pyautogui.click(x=mouse_x, y=mouse_y)
    time.sleep(1)

    pyautogui.press(fishing_key)
    time.sleep(1) 

    pyautogui.click(x=mouse_x, y=mouse_y)
    print(f"'{fishing_key.upper()}' apertado e clique realizado em ({mouse_x}, {mouse_y}).")

def monitor_screen_and_react(root, target_image_path, mouse_x, mouse_y, fishing_key, search_region):
    """Monitora a tela e reage se a pesca estiver ativa."""
    global fishing_is_active, last_direction, after_id, last_action_time

    if not fishing_is_active:
        return

    try:
        exclamation_location = pyautogui.locateOnScreen(
            target_image_path,
            confidence=0.8,
            region=search_region
        )
    except Exception as e:
        print(f"Erro na detecção de imagem: {e}")
        exclamation_location = None

    if exclamation_location:
        print("Imagem da exclamação encontrada! Reagindo...")
        
        last_action_time = time.time()
        
        # Lógica para escolher uma direção aleatória diferente da última
        directions = ['up', 'down', 'left', 'right']
        if last_direction and last_direction in directions:
            directions.remove(last_direction)
        
        selected_direction = random.choice(directions)
        last_direction = selected_direction
        
        print(f"Pressionando Control + {selected_direction.capitalize()}...")
        pyautogui.hotkey('ctrl', selected_direction)
        
        # Atraso para a imagem desaparecer
        time.sleep(1.9)
    else:
        print("Imagem não encontrada. Aguardando...")
        current_time = time.time()
        if current_time - last_action_time > 8:
            print("Timeout de 8 segundos alcançado. Reiniciando a pesca...")
            
            # Chama a função principal de iniciar a pesca, que contém a lógica de 'virar para baixo'
            start_fishing_action(fishing_key, mouse_x, mouse_y)
            last_action_time = time.time()

    # Agenda a próxima execução
    after_id = root.after(100, lambda: monitor_screen_and_react(root, target_image_path, mouse_x, mouse_y, fishing_key, search_region))


def start_script(root, fishing_key, mouse_x, mouse_y, search_region, image_file, start_button, stop_button):
    """Inicia o script de pesca e a janela de controle."""
    global fishing_is_active, last_direction, last_action_time
    
    # Se o script já estiver rodando, primeiro para ele
    if fishing_is_active:
        stop_script(root, start_button, stop_button)
        
    fishing_is_active = True
    print("Script ativado.")
    
    # Atualiza a aparência dos botões
    start_button.config(relief="sunken")
    stop_button.config(relief="raised")
    
    # PASSO 1: Clica no local para focar a janela do jogo
    print("Focando a janela do jogo...")
    pyautogui.click(x=mouse_x, y=mouse_y)
    time.sleep(1) # Espera a janela ganhar foco
    
    # Reinicia o temporizador e a direção
    last_action_time = time.time()
    last_direction = None
    
    # PASSO 2 E 3: Executa a ação inicial de virar para baixo e pescar
    start_fishing_action(fishing_key, mouse_x, mouse_y)

    # Inicia a monitoração, agora agendada pelo `root.after`
    monitor_screen_and_react(root, image_file, mouse_x, mouse_y, fishing_key, search_region)

def stop_script(root, start_button, stop_button):
    """Para o script de pesca."""
    global fishing_is_active, after_id
    if fishing_is_active:
        fishing_is_active = False
        print("Script desativado.")
        
        # Atualiza a aparência dos botões
        stop_button.config(relief="sunken")
        start_button.config(relief="raised")
        
        if after_id:
            root.after_cancel(after_id)
            after_id = None

def exit_script(root):
    """Fecha a janela e encerra a aplicação."""
    global fishing_is_active
    fishing_is_active = False
    if after_id:
        root.after_cancel(after_id)
    root.destroy()
    print("Aplicação encerrada.")

def create_control_window(fishing_key, mouse_x, mouse_y, search_region, image_file):
    """Cria e exibe a janela de controle."""
    root = tk.Tk()
    root.title("Controle de Pesca")
    
    # Posicionar a janela no canto inferior direito
    root.geometry(f'+{root.winfo_screenwidth() - 220}+{root.winfo_screenheight() - 100}') 
    
    # Manter a janela sempre acima
    root.attributes('-topmost', True)

    frame_buttons = tk.Frame(root, padx=10, pady=10)
    frame_buttons.pack()
    
    start_button = tk.Button(frame_buttons, text="Iniciar Pesca", relief="raised", command=lambda: start_script(root, fishing_key, mouse_x, mouse_y, search_region, image_file, start_button, stop_button))
    start_button.pack(side=tk.LEFT, padx=5)
    
    stop_button = tk.Button(frame_buttons, text="Parar Pesca", relief="raised", command=lambda: stop_script(root, start_button, stop_button))
    stop_button.pack(side=tk.RIGHT, padx=5)
    
    frame_exit = tk.Frame(root, pady=5)
    frame_exit.pack()
    
    exit_button = tk.Button(frame_exit, text="Sair", bg="red", fg="white", command=lambda: exit_script(root))
    exit_button.pack(side=tk.BOTTOM, pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    image_file = 'exclamacao-pesca-sem-fundo.png'

    # 1. Obter a tecla de atalho
    fishing_key = get_fishing_key()
    if not fishing_key:
        exit()

    # 2. Obter as coordenadas da exclamação
    search_region = get_exclamation_region()
    if not search_region:
        exit()
        
    # 3. Obter as coordenadas de clique de pesca
    mouse_x, mouse_y = get_fishing_click_coordinates()
    if mouse_x is None:
        exit()
    
    # Inicia a janela de controle
    print("Configurações salvas. A janela de controle está pronta.")
    create_control_window(fishing_key, mouse_x, mouse_y, search_region, image_file)