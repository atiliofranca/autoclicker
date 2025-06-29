import pyautogui
import time

# usado para saber o x e y que o pyautogui vai clicar no arquivo main
# executa-se essas linhas de comando, e em até 5 segundos, deve-se clicar na tela para ter as coordenadas
time.sleep(5)
print(pyautogui.position())