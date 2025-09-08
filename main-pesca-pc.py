import pyautogui
import time
import random

def start_fishing():
    """Executa a primeira parte do processo: aperta F3 e clica no local especificado."""
    print("Iniciando a pesca...")
    time.sleep(0.5) 

    # COORDENADAS PARA PESCA
    # Point(x=2933, y=864) (tela mancer 27")
    mouse_x = 2933
    mouse_y = 864

    # clique para selecionar o jogo
    pyautogui.click(x=mouse_x, y=mouse_y)
    time.sleep(1)

    pyautogui.press('f3')
    time.sleep(1) 

    pyautogui.click(x=mouse_x, y=mouse_y)
    print(f"F3 apertado e clique realizado em ({mouse_x}, {mouse_y}).")
    # time.sleep(1)

def monitor_screen_and_react(target_image_path):

    # Monitora a tela para a imagem da exclamação e reage com Control + Seta.
    print("Começando a monitorar a tela...")
    last_direction = None
    directions = ['up', 'down', 'left', 'right']

    # COORDENADAS PARA MONITORAR EXCLAMAÇÃO
    #region_left = 2743 / region_top = 376 / region_width = 61 / region_height = 39 (tela mancer 27")
    region_left = 2743 # coordenada X
    region_top = 376 # coordenada Y
    region_width = 61 # largura
    region_height = 39 # altura
    search_region = (region_left, region_top, region_width, region_height)
    
    is_first_reaction = True
    
    # Adicionando o temporizador para tratamento de erro
    last_action_time = time.time()
    TIMEOUT = 8

    try:
        while True:
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
                
                # Reseta o temporizador
                last_action_time = time.time()
                
                if is_first_reaction:
                    selected_direction = 'left'
                    is_first_reaction = False
                else:
                    possible_directions = [d for d in directions if d != last_direction]
                    if not possible_directions:
                        possible_directions = directions
                    
                    selected_direction = random.choice(possible_directions)
                
                last_direction = selected_direction
                
                print(f"Pressionando Control + {selected_direction.capitalize()}...")
                pyautogui.hotkey('ctrl', selected_direction)
                
                # Adicionando um atraso para dar tempo de a imagem desaparecer da tela
                time.sleep(1.7) 
            else:
                # Se a imagem não for encontrada, verifique o tempo
                print("Imagem não encontrada. Aguardando...")
                current_time = time.time()
                if current_time - last_action_time > TIMEOUT:
                    print(f"Timeout de {TIMEOUT} segundos alcançado. Reiniciando a pesca...")
                    
                    # Agora clica Control + direcional para baixo
                    pyautogui.hotkey('ctrl', 'down')
                    time.sleep(1)
                    
                    start_fishing()
                    last_action_time = time.time() # Reseta o temporizador após reiniciar
                
                # Aumentando a frequência da verificação quando a imagem não está presente
                time.sleep(0.5) 

    except KeyboardInterrupt:
        print("\nScript interrompido pelo usuário.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    image_file = 'exclamacao-pesca-sem-fundo.png'
    
    start_fishing()
    
    monitor_screen_and_react(image_file)