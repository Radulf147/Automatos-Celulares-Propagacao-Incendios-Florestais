import pygame
import numpy as np
import random

# --- DEFINIÇÃO DE PROPRIEDADES DOS MATERIAIS ---
PROPRIEDADES_MATERIAIS = {
    0: {"nome": "Grama Seca",   "prob_base": 0.25, "tempo_queima": 3, "cor": (154, 205, 50)}, # Verde Claro
    1: {"nome": "Arbusto Seco", "prob_base": 0.15, "tempo_queima": 4, "cor": (218, 165, 32)}, # Dourado
    2: {"nome": "Folha Umida",  "prob_base": 0.05, "tempo_queima": 5, "cor": (85, 107, 47)}, # Verde Oliva Escuro
    3: {"nome": "Madeira Seca", "prob_base": 0.10, "tempo_queima": 7, "cor": (139, 69, 19)}, # Marrom
    4: {"nome": "Arvore Umida", "prob_base": 0.02, "tempo_queima": 10, "cor": (34, 139, 34)}, # Verde Musgo Floresta
    5: {"nome": "Obstaculo",    "prob_base": 0.00, "tempo_queima": 0, "cor": (128, 128, 128)}, # Cinza
    -1: {"nome": "Fogo",        "prob_base": 0.00, "tempo_queima": 0, "cor": (255, 69,  0)}, # Vermelho Alaranjado
    -2: {"nome": "Queimado",    "prob_base": 0.00, "tempo_queima": 0, "cor": (50,  50,  50)} # Preto
}

def obter_cor(estado, fogo_restante):
    if fogo_restante > 0:
        return PROPRIEDADES_MATERIAIS[-1]["cor"]
    return PROPRIEDADES_MATERIAIS[estado]["cor"]

def condicao_inicial(CA_Y, CA_X):
    # Inicializa matriz base (estado 0 - Grama Seca) e matriz de controle de queima
    CA_matriz = np.zeros((CA_Y, CA_X), dtype=int)
    CA_matriz_fogo_restante = np.zeros((CA_Y, CA_X), dtype=int)
    
    # --- ESTRADAS ---
    CA_matriz[145:152, :] = 5
    CA_matriz[:, 95:102]  = 5

    # --- EDIFICAÇÕES (Quadrante Sup-Dir) ---
    CA_matriz[15:85, 130:210] = 5
    CA_matriz[15:55, 220:265] = 5

    # --- BOSQUE 1 (Quadrante Sup-Esq) ---
    CA_matriz[10:135, 5:85]  = 1
    CA_matriz[22:122, 12:78] = 4
    CA_matriz[38:106, 20:68] = 2

    # --- BOSQUE 2 (Quadrante Inf-Dir) ---
    CA_matriz[165:288, 135:288] = 1
    CA_matriz[178:278, 148:278] = 4
    CA_matriz[192:265, 162:265] = 2

    # --- BOSQUE 3 (Quadrante Inf-Esq) ---
    CA_matriz[172:255, 8:82]  = 1
    CA_matriz[182:245, 15:72] = 4

    # --- MANCHAS DE MADEIRA SECA ---
    CA_matriz[100:120, 130:160] = 3
    CA_matriz[218:238, 108:133] = 3
    CA_matriz[158:168, 220:255] = 3

    # --- GERADOR AUTOMÁTICO DE FOCOS ---
    quantidade_de_focos = 7
    centros_fogo = []
    
    for _ in range(quantidade_de_focos):
        y_aleatorio = random.randint(20, CA_Y - 20)
        x_aleatorio = random.randint(20, CA_X - 20)
        centros_fogo.append((y_aleatorio, x_aleatorio))

    raio_espalhamento = 1
    faos_por_regiao = 100

    for centro_y, centro_x in centros_fogo:
        for _ in range(faos_por_regiao):
            dy = random.randint(-raio_espalhamento, raio_espalhamento)
            dx = random.randint(-raio_espalhamento, raio_espalhamento)
            
            ny = centro_y + dy
            nx = centro_x + dx
            
            if 0 <= ny < CA_Y and 0 <= nx < CA_X:
                estado_alvo = CA_matriz[ny][nx]
                if estado_alvo not in (5, -2) and CA_matriz_fogo_restante[ny][nx] == 0:
                    CA_matriz_fogo_restante[ny][nx] = PROPRIEDADES_MATERIAIS[estado_alvo]["tempo_queima"]
                    
    return CA_matriz, CA_matriz_fogo_restante

def funcao_transicao_fogo(CA_matriz_atual, CA_matriz_futura, fogo_restante_atual, fogo_restante_futura, CA_Y, CA_X):
    movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    rng = np.random.default_rng()
    
    for j in range(CA_Y):
        for i in range(CA_X):
            estado_atual = CA_matriz_atual[j][i]
            
            # Obstáculos e áreas queimadas são estáticos
            if estado_atual == 5 or estado_atual == -2:
                CA_matriz_futura[j][i] = estado_atual
                fogo_restante_futura[j][i] = 0
                continue
                
            # Célula ativamente em chamas
            if fogo_restante_atual[j][i] > 0:
                novo_restante = fogo_restante_atual[j][i] - 1
                fogo_restante_futura[j][i] = novo_restante
                CA_matriz_futura[j][i] = -2 if novo_restante == 0 else estado_atual
                continue
                
            # Avalia ignição pelos vizinhos
            vizinhos_fogo = 0
            for dy, dx in movimentos:
                ny, nx = j + dy, i + dx
                
                if 0 <= ny < CA_Y and 0 <= nx < CA_X:
                    if fogo_restante_atual[ny][nx] > 0:
                        vizinhos_fogo += 1
            
            # Regra estocástica baseada no material e carga de calor
            if vizinhos_fogo >= 1:
                prob_base = PROPRIEDADES_MATERIAIS[estado_atual]["prob_base"]
                probabilidade_ignicao = 1.0 - (1.0 - prob_base) ** vizinhos_fogo
                
                if rng.random() < probabilidade_ignicao:
                    CA_matriz_futura[j][i] = estado_atual
                    fogo_restante_futura[j][i] = PROPRIEDADES_MATERIAIS[estado_atual]["tempo_queima"]
                else:
                    CA_matriz_futura[j][i] = estado_atual
                    fogo_restante_futura[j][i] = 0
            else:
                CA_matriz_futura[j][i] = estado_atual
                fogo_restante_futura[j][i] = 0

if __name__ == '__main__':
    width  = 800
    height = 800
    FPS    = 15
    CA_X   = 300
    CA_Y   = 300

    # Inicialização das matrizes
    CA_matriz_0, CA_fogo_0 = condicao_inicial(CA_Y, CA_X)
    CA_matriz_1 = np.zeros((CA_Y, CA_X), dtype=int)
    CA_fogo_1   = np.zeros((CA_Y, CA_X), dtype=int)

    pygame.init()
    gameDisplay = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Simulador de Propagação de Incêndio - CA')
    clock = pygame.time.Clock()

    running = True
    update  = False # Tecla 'u' alterna a passagem do tempo

    deltaX = (width / CA_X)
    deltaY = (height / CA_Y)
    
    tempo = 0

    while running:
        clock.tick(FPS)
        gameDisplay.fill((0, 0, 0))

        # Renderização do grid
        for j in range(CA_Y):
            for i in range(CA_X):
                cor = obter_cor(CA_matriz_0[j][i], CA_fogo_0[j][i])
                
                x = i * deltaX
                y = j * deltaY
                pygame.draw.rect(gameDisplay, cor, (x, y, deltaX + 1, deltaY + 1), 0)

        # Tratamento de eventos
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                if e.key == pygame.K_u:
                    update = not update
                    
        # Atualização do autômato celular
        if update:
            tempo += 1
            funcao_transicao_fogo(CA_matriz_0, CA_matriz_1, CA_fogo_0, CA_fogo_1, CA_Y, CA_X)
            
            # Swap de buffers
            np.copyto(CA_matriz_0, CA_matriz_1)
            np.copyto(CA_fogo_0, CA_fogo_1)
                
        pygame.display.flip()

    pygame.quit()
    print("Fim da simulação. Passos de tempo simulados:", tempo)