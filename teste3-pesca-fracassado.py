import pyautogui
import time
import random
import tkinter as tk
from tkinter import simpledialog, messagebox
from screeninfo import get_monitors

# Variáveis globais para controlar a execução do script de pesca e a última direção
fishing_is_active = False
last_direction = None
after_id_fishing = None
after_id_pet = None

# Variáveis globais para a nova funcionalidade de carinho
pet_is_active = False
pet_coordinates = None
last_pet_time = 0

# Variável para controlar o início do script
is_first_start = True

# --- Variáveis para a janela de configuração ---
config_data = {}
config_window = None
config_step = 0
timer_label = None

def get_primary_monitor_dimensions():
    """Retorna as dimensões e a posição do monitor principal usando screeninfo."""
    for monitor in get_monitors():
        if monitor.is_primary:
            return monitor.width, monitor.height, monitor.x, monitor.y
    monitor = get_monitors()[0]
    return monitor.width, monitor.height, monitor.x, monitor.y

def center_on_primary(window, width, height):
    """Centraliza uma janela no monitor principal."""
    mon_width, mon_height, mon_x, mon_y = get_primary_monitor_dimensions()
    x = mon_x + (mon_width // 2) - (width // 2)
    y = mon_y + (mon_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# --- Funções de Automação ---

def start_fishing_action(fishing_key, mouse_x, mouse_y):
    """Prepara o personagem e inicia a pesca."""
    global last_direction
    print("Iniciando a pesca...")
    
    pyautogui.hotkey('ctrl', 'down')
    time.sleep(3)
    last_direction = 'down'

    pyautogui.click(x=mouse_x, y=mouse_y)
    time.sleep(1)
    pyautogui.press(fishing_key)
    time.sleep(1) 
    pyautogui.click(x=mouse_x, y=mouse_y)
    print(f"'{fishing_key.upper()}' apertado e clique realizado em ({mouse_x}, {mouse_y}).")

def update_pet_countdown(root, pet_label):
    """Atualiza o contador de segundos para o próximo carinho."""
    global pet_is_active, last_pet_time, after_id_pet

    if pet_is_active:
        seconds_left = max(0, 100 - (time.time() - last_pet_time))
        pet_label.config(text=f"Carinho em: {int(seconds_left)}s")
        after_id_pet = root.after(1000, lambda: update_pet_countdown(root, pet_label))
    else:
        pet_label.config(text="Carinho: Desativado")

def pet_action_loop(root):
    """Verifica e executa a ação de dar carinho."""
    global pet_is_active, last_pet_time, pet_coordinates

    if pet_is_active and (time.time() - last_pet_time) > 100:
        print("Tempo de carinho alcançado. Dando carinho no Pokémon...")
        pyautogui.click(x=pet_coordinates[0], y=pet_coordinates[1])
        last_pet_time = time.time()
    
    root.after(1000, lambda: pet_action_loop(root))

def monitor_screen_and_react(root, target_image_path, direction_label):
    """Monitora a tela e reage se a pesca estiver ativa."""
    global fishing_is_active, last_direction, after_id_fishing, last_action_time
    mouse_x, mouse_y = config_data['fishing_click']
    fishing_key = config_data['fishing_key']
    search_region = config_data['exclamation_region']
    
    if not fishing_is_active:
        return

    if last_direction:
        direction_label.config(text=f"Direção: {last_direction.capitalize()}")
    
    try:
        exclamation_location = pyautogui.locateOnScreen(
            target_image_path,
            confidence=0.8,
            region=search_region
        )
    except Exception as e:
        exclamation_location = None

    if exclamation_location:
        last_action_time = time.time()
        
        directions = ['up', 'down', 'left', 'right']
        if last_direction and last_direction in directions:
            directions.remove(last_direction)
        
        selected_direction = random.choice(directions)
        last_direction = selected_direction
        
        pyautogui.hotkey('ctrl', selected_direction)
        
        time.sleep(1.9)
    else:
        if time.time() - last_action_time > 8:
            start_fishing_action(fishing_key, mouse_x, mouse_y)
            last_action_time = time.time()

    after_id_fishing = root.after(100, lambda: monitor_screen_and_react(root, target_image_path, mouse_x, mouse_y, fishing_key, search_region, direction_label))

# --- Funções para a Configuração em uma Única Janela ---

def start_capture_timer(coords_type):
    """Inicia o timer para capturar as coordenadas e avança para o próximo passo."""
    global config_window, config_step
    timer_countdown = 5
    
    # Remove widgets da etapa anterior
    for widget in config_window.winfo_children():
        widget.pack_forget()
    
    timer_label = tk.Label(config_window, text=f"Capturando em {timer_countdown} segundos...", font=("Arial", 16))
    timer_label.pack(pady=20)
    
    def countdown_and_capture():
        nonlocal timer_countdown
        if timer_countdown > 0:
            timer_label.config(text=f"Capturando em {timer_countdown} segundos...")
            timer_countdown -= 1
            config_window.after(1000, countdown_and_capture)
        else:
            coords = pyautogui.position()
            if coords_type == 'exclamation_center':
                config_data['exclamation_region'] = (coords.x - 50, coords.y - 30, 100, 60)
            else:
                config_data[coords_type] = (coords.x, coords.y)
            timer_label.pack_forget()
            config_step += 1
            setup_gui_logic()
    
    config_window.after(1000, countdown_and_capture)

def set_pet_active(state):
    global pet_is_active, config_step
    pet_is_active = state
    config_step += 1
    setup_gui_logic()

def setup_gui_logic():
    """Gerencia a sequência de passos de configuração em uma única janela."""
    global config_step, config_window, pet_is_active
    
    # Remove widgets da etapa anterior
    for widget in config_window.winfo_children():
        widget.pack_forget()

    main_frame = tk.Frame(config_window, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    config_window.label = tk.Label(main_frame, text="", wraplength=380, font=("Arial", 12))
    config_window.label.pack(pady=10)

    if config_step == 0:
        config_window.label.config(text="Passo 1: Qual a tecla de atalho (F1-F12)?")
        config_window.entry = tk.Entry(main_frame, width=30)
        config_window.entry.pack(pady=5)
        config_window.button = tk.Button(main_frame, text="Próximo", command=lambda: setup_gui_logic())
        config_window.button.pack(pady=10)
    elif config_step == 1:
        fishing_key = config_window.entry.get().upper()
        if fishing_key in [f'F{i}' for i in range(1, 13)]:
            config_data['fishing_key'] = fishing_key.lower()
            config_window.label.config(text="Passo 2: Ativar carinho?")
            yes_button = tk.Button(main_frame, text="Sim", command=lambda: set_pet_active(True))
            no_button = tk.Button(main_frame, text="Não", command=lambda: set_pet_active(False))
            yes_button.pack(side=tk.LEFT, padx=5)
            no_button.pack(side=tk.RIGHT, padx=5)
        else:
            messagebox.showerror("Erro", "Tecla inválida.", parent=config_window)
            config_step = -1
            setup_gui_logic()
            return
    elif config_step == 2:
        config_window.label.config(text="Passo 3: Ponto de carinho. Mova o mouse e clique para capturar.")
        capture_button = tk.Button(main_frame, text="Capturar", command=lambda: start_capture_timer('pet_coordinates'))
        capture_button.pack(pady=10)
    elif config_step == 3:
        config_window.label.config(text="Passo 4: Ponto da exclamação. Mova o mouse e clique para capturar.")
        capture_button = tk.Button(main_frame, text="Capturar", command=lambda: start_capture_timer('exclamation_center'))
        capture_button.pack(pady=10)
    elif config_step == 4:
        config_window.label.config(text="Passo 5: Ponto de clique. Mova o mouse e clique para capturar.")
        capture_button = tk.Button(main_frame, text="Capturar", command=lambda: start_capture_timer('fishing_click'))
        capture_button.pack(pady=10)
    elif config_step == 5:
        config_window.destroy()
        create_control_window()
        return

    config_step += 1

def start_setup():
    """Inicia a janela de configuração."""
    global config_window
    
    config_window = tk.Tk()
    config_window.title("Configuração Inicial")
    center_on_primary(config_window, 400, 200)
    
    setup_gui_logic()
    
    config_window.mainloop()

# --- Funções de Controle da Janela Principal ---

def start_script(root, start_button, stop_button, direction_label, pet_label):
    """Inicia o script de pesca e a janela de controle."""
    global fishing_is_active, last_direction, last_action_time, last_pet_time, is_first_start
    
    if fishing_is_active:
        stop_script(root, start_button, stop_button, direction_label, pet_label)
        
    fishing_is_active = True
    print("Script ativado.")
    
    start_button.config(relief="sunken")
    stop_button.config(relief="raised")
    
    last_action_time = time.time()
    last_direction = None
    
    if is_first_start:
        last_pet_time = time.time()
        root.after(0, lambda: pet_action_loop(root))
        root.after(0, lambda: update_pet_countdown(root, pet_label))
        is_first_start = False
    
    time.sleep(1)
    
    fishing_key = config_data['fishing_key']
    mouse_x, mouse_y = config_data['fishing_click']
    start_fishing_action(fishing_key, mouse_x, mouse_y)

    monitor_screen_and_react(root, 'exclamacao-pesca-sem-fundo.png', mouse_x, mouse_y, fishing_key, config_data['exclamation_region'], direction_label)

def stop_script(root, start_button, stop_button, direction_label, pet_label):
    """Para o script de pesca."""
    global fishing_is_active, after_id_fishing
    if fishing_is_active:
        fishing_is_active = False
        print("Script desativado.")
        
        stop_button.config(relief="sunken")
        start_button.config(relief="raised")
        
        direction_label.config(text="Direção: ---")
        
        if after_id_fishing:
            root.after_cancel(after_id_fishing)
            after_id_fishing = None

def exit_script(root):
    """Fecha a janela e encerra a aplicação."""
    global fishing_is_active, after_id_fishing, after_id_pet
    fishing_is_active = False
    if after_id_fishing:
        root.after_cancel(after_id_fishing)
    if after_id_pet:
        root.after_cancel(after_id_pet)
    root.destroy()
    print("Aplicação encerrada.")

def create_control_window():
    """Cria e exibe a janela de controle."""
    root = tk.Tk()
    root.title("Controle de Pesca")
    
    mon_width, mon_height, mon_x, mon_y = get_primary_monitor_dimensions()
    root.geometry(f'+{mon_x + 10}+{mon_y + mon_height - 100}')
    root.attributes('-topmost', True)

    frame_info = tk.Frame(root, padx=10, pady=5)
    frame_info.pack(fill=tk.X)

    direction_label = tk.Label(frame_info, text="Direção: ---")
    direction_label.pack(side=tk.LEFT, padx=5)

    pet_label = tk.Label(frame_info, text="Carinho: ---")
    pet_label.pack(side=tk.RIGHT, padx=5)

    frame_buttons = tk.Frame(root, padx=10, pady=10)
    frame_buttons.pack()
    
    start_button = tk.Button(frame_buttons, text="Iniciar Pesca", relief="raised", command=lambda: start_script(root, start_button, stop_button, direction_label, pet_label))
    start_button.pack(side=tk.LEFT, padx=5)
    
    stop_button = tk.Button(frame_buttons, text="Parar Pesca", relief="raised", command=lambda: stop_script(root, start_button, stop_button, direction_label, pet_label))
    stop_button.pack(side=tk.RIGHT, padx=5)
    
    frame_exit = tk.Frame(root, pady=5)
    frame_exit.pack()
    
    exit_button = tk.Button(frame_exit, text="Sair", bg="red", fg="white", command=lambda: exit_script(root))
    exit_button.pack(side=tk.BOTTOM, pady=5)
    
    pet_action_loop(root)
    
    root.mainloop()

if __name__ == "__main__":
    start_setup()