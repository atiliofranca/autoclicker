depois de clonar o projeto:

1 - Crie um Ambiente Virtual:

python3 -m venv venv_autoclicker

2 - Ative o Ambiente Virtual:

No Linux ou macOS:
source venv_autoclicker/bin/activate

No Windows (PowerShell/CMD):
.\venv_autoclicker\Scripts\activate

Depois de criado, você verá (venv_autoclicker) aparecer no início do seu prompt do terminal, indicando que o ambbiente virtual está ativo

3 - Instale as bibliotecas dentro do seu ambiente virtual:
pip install -r requirements.txt

----

encontrando as coordenadas da sua tela

Coordenadas para clique de pesca

Passo 1 - Execute o arquivo auxiliar.py
no terminal irá aparecer as coordenadas atuais

ou

Passo 1 - Execute o script de exibição de posição do mouse:
python -c "import pyautogui; pyautogui.displayMousePosition()"
(vai aparecer a mesma informação no terminal)

Passo 2 - Copie as coordenadas e coloque-as no código
vai estar logo após o comentário '# COORDENADAS PARA PESCA'

Coordenadas para monitoramento do ícone de exclamação:

Passo 1 - Mesmo do anterior. Escolha a melhor opção para você

Passo 2 - Crie um quadrado/retângulo imaginário na área que a exclamação aparece

Passo 3 - Mova o mouse para o canto superior esquerdo desse quadrado/retângulo onde a exclamação aparece no jogo e anote as coordenadas X e Y. Elas serão o seu region_left e region_top

Passo 4 - Mova o mouse para o canto inferior direito do quadrado vermelho e anote os novos valores

Passo 5 - Calcule a largura e a altura.
Largura (width) = X do canto inferior direito - X do canto superior esquerdo
Altura (height) = Y do canto inferior direito - Y do canto superior esquerdo

Passo 6 - Aplique as informações no código:
region_left = 2743 # coordenada X - canto superior esquerdo
region_top = 376 # coordenada Y - canto superior esquerdo
region_width = 61 # largura - X do canto inferior direito - X do canto superior esquerdo
region_height = 39 # altura - Y do canto inferior direito - Y do canto superior esquerdo