import pygame
import numpy as np
import random

# --- DEFINIÇÃO DE CORES PARA OS ESTADOS ---
COR_COMBUSTIVEL = (34, 139, 34)   # Estado 0: Verde Escuro
COR_NAO_INFLAM = (128, 128, 128)  # Estado 1: Cinza
COR_FOGO = (255, 0, 0)            # Estado 2: Vermelho 
COR_QUEIMADO = (139, 69, 19)      # Estado 3: Marrom

def obter_cor(estado):
    if estado == 0: return COR_COMBUSTIVEL
    if estado == 1: return COR_NAO_INFLAM
    if estado == 2: return COR_FOGO
    if estado == 3: return COR_QUEIMADO
    return (0, 0, 0)

def condicao_inicial(CA_Y, CA_X):
    # Inicializa tudo como matriz de zeros (estado 0 - combustível)
    CA_matriz = np.zeros((CA_Y, CA_X), dtype=int)
    
    # Adicionando áreas não inflamáveis (estado 1 - cinza)
    for j in range(20, CA_Y - 20):
        CA_matriz[j][CA_X // 2] = 1
        CA_matriz[j][CA_X // 2 + 1] = 1
    
    for j in range(10, 30):
        for i in range(20, 40):
            CA_matriz[j][i] = 1

    
    # --- GERADOR AUTOMÁTICO DE FOCOS ---
    quantidade_de_focos = 7 # Mude este número para quantos incêndios quiser
    centros_fogo = []
    
    for _ in range(quantidade_de_focos):
        # Sorteia uma coordenada Y e X garantindo que não caia muito na borda
        y_aleatorio = random.randint(20, CA_Y - 20)
        x_aleatorio = random.randint(20, CA_X - 20)
        centros_fogo.append((y_aleatorio, x_aleatorio))

    raio_espalhamento = 1  # Distância máxima que as faíscas podem cair do centro
    faos_por_regiao = 100    # Quantidade de pixels de fogo em cada região

    # Para cada região que definimos na lista acima:
    for centro_y, centro_x in centros_fogo:
        # Sorteia a posição dos pixels de fogo
        for _ in range(faos_por_regiao):
            # Cria um desvio aleatório entre -raio e +raio
            dy = random.randint(-raio_espalhamento, raio_espalhamento)
            dx = random.randint(-raio_espalhamento, raio_espalhamento)
            
            ny = centro_y + dy
            nx = centro_x + dx
            
            # Garante que a faísca não caiu fora dos limites do mapa
            if 0 <= ny < CA_Y and 0 <= nx < CA_X:
                # Transforma a célula sorteada em fogo (estado 2) APENAS se for grama (0)
                if CA_matriz[ny][nx] == 0:    
                    CA_matriz[ny][nx] = 2
                    
    return CA_matriz

def funcao_transicao_fogo(CA_matriz_atual, CA_matriz_futura, CA_Y, CA_X):
    # Os 8 vizinhos possíveis (N, S, O, L, NO, NE, SO, SE)
    movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    for j in range(CA_Y):
        for i in range(CA_X):
            estado_atual = CA_matriz_atual[j][i]
            
            # Se for não-inflamável (1) ou queimado (3), o estado se mantém.
            if estado_atual == 1 or estado_atual == 3:
                CA_matriz_futura[j][i] = estado_atual
                continue
                
            # Se está pegando fogo (2), no próximo turno vira queimado (3).
            if estado_atual == 2:
                CA_matriz_futura[j][i] = 3
                continue
                
            # Se é combustível (0), avalia a possibilidade de ignição.
            if estado_atual == 0:
                vizinhos_fogo = 0
                
                # Conta quantos vizinhos estão ativamente em chamas (estado 2)
                for dy, dx in movimentos:
                    ny, nx = j + dy, i + dx
                    
                    # Checa os limites rigorosos (sem contorno circular)
                    if 0 <= ny < CA_Y and 0 <= nx < CA_X:
                        if CA_matriz_atual[ny][nx] == 2:
                            vizinhos_fogo += 1
                
                # Aplica a regra estocástica
                rng = np.random.default_rng()
                if vizinhos_fogo >= 1:
                    probabilidade_ignicao = vizinhos_fogo / 8.0
                    # Se o sorteio for menor que a probabilidade, pega fogo
                    if rng.random() < probabilidade_ignicao:
                        CA_matriz_futura[j][i] = 2
                    else:
                        CA_matriz_futura[j][i] = 0
                else:
                    # Nenhum vizinho pegando fogo, continua combustível
                    CA_matriz_futura[j][i] = 0

'''
Função principal
'''
if __name__ == '__main__':
    width  = 800
    height = 800
    FPS    = 15 # FPS reduzido para conseguir enxergar o fogo se espalhando
    CA_X   = 300
    CA_Y   = 300

    CA_matriz_0 = condicao_inicial(CA_Y, CA_X)
    CA_matriz_1 = np.zeros((CA_Y, CA_X), dtype=int)

    pygame.init()
    gameDisplay = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Simulador de Propagação de Incêndio - CA')
    clock = pygame.time.Clock()

    running = True
    update  = False # Aperte 'u' para começar a simulação

    deltaX = (width / CA_X)
    deltaY = (height / CA_Y)
    
    tempo = 0

    while running:
        clock.tick(FPS)
        gameDisplay.fill((0, 0, 0))

        # Desenho das células baseado no estado atual
        for j in range(CA_Y):
            for i in range(CA_X):
                estado = CA_matriz_0[j][i]
                cor = obter_cor(estado)
                
                x = i * deltaX
                y = j * deltaY
                # Desenha o quadrado da célula
                pygame.draw.rect(gameDisplay, cor, (x, y, deltaX + 1, deltaY + 1), 0)

        # Trata eventos (teclado e fechar janela)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                if e.key == pygame.K_u:
                    update = not update # Liga/Desliga a passagem do tempo
                    
        # Aplica o autômato celular
        if update:
            tempo += 1
            funcao_transicao_fogo(CA_matriz_0, CA_matriz_1, CA_Y, CA_X)
            
            # Atualiza matrizes (swap)
            # CA_matriz_1 agora contém o estado futuro, que vira o estado atual
            np.copyto(CA_matriz_0, CA_matriz_1)
                
        pygame.display.flip()

    pygame.quit()
    print("Fim da simulação. Passos de tempo simulados:", tempo)