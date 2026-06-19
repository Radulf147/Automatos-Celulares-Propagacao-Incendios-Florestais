# Simulador de Propagação de Incêndios Florestais

Um modelo computacional de Autômato Celular Estocástico, desenvolvido em Python, para prever e simular o espalhamento de frentes de fogo.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![NumPy](https://img.shields.io/badge/NumPy-Optimized-green.svg)
![Pygame](https://img.shields.io/badge/Pygame-Render-red.svg)

---

## Sobre o Projeto

Este projeto modela a propagação do fogo utilizando matrizes bidimensionais e Autômatos Celulares. O repositório documenta a implementação baseada no artigo "A Cellular Automata Model for Fire Spreading Prediction" (Quartieri et al., 2010) e apresenta uma refatoração arquitetural proposta para corrigir limitações mecânicas identificadas na formulação original.

Para fins de análise acadêmica e demonstração matemática, o repositório conta com duas versões do algoritmo (`Fire_Sprea.py` e `heterogeneo.py`), que evidenciam o impacto da modelagem de estados estendidos e do controle de tempo de queima no comportamento da simulação.

---

## Os Dois Modelos (Comparativo Arquitetural)

O projeto contém dois executáveis principais que demonstram a evolução da lógica de propagação operando em tempo real (15 FPS).

### 1. Fire_Sprea.py (Implementação Fiel ao Artigo)
Representa a reprodução estrita da modelagem teórica original.
* **Estados:** Trabalha com 4 estados discretos genéricos (0: combustível, 1: não inflamável, 2: em chamas, 3: queimado).
* **Mecânica:** A probabilidade de ignição é linear, definida por $p(N_b) = N_b / 8$. A transição do estado em chamas para queimado ocorre em exatos 1 passo de tempo (tick).
* **Comportamento:** Apresenta um gargalo físico denominado "apagamento rápido". O tempo de vida excessivamente curto da chama cria uma muralha inativa instantânea nas bordas, causando perda de apoio térmico e o autoapagamento precoce da simulação.

### 2. heterogeneo.py (Refatoração: Propagação Orgânica e Realista)
Ajusta a arquitetura para solucionar o gargalo mecânico, introduzindo Modelos de Combustível baseados na literatura de engenharia florestal.
* **Mecânica:** Implementa um Espaço de Estados Estendido, utilizando matrizes paralelas de Material e Tempo de Queima. Ajusta punitivamente as probabilidades base e utiliza tempos de queima variáveis como âncoras térmicas (ex: Árvores úmidas duram 10 ticks).
* **Comportamento:** O fogo sofre engasgos matemáticos intencionais. A chama contorna certas células, deixa ilhas de vegetação intactas e forma frentes de ataque irregulares (cabeças e flancos), aproximando o comportamento visual do rigor físico de uma queimada real.

---

## Como Funciona a Refatoração (A Matemática)

No modelo refatorado (`heterogeneo.py`), o autômato avalia a malha utilizando a **Vizinhança de Moore** (8 direções) e um sistema de *swap* de matrizes para garantir a sincronia matemática temporal ($t \rightarrow t+1$).

### Espaço de Estados Estendido
Diferente da versão fiel, cada célula no grid possui um vetor de estado contendo:
1. **Material (ID):** Define a inflamabilidade base ($P_{base}$).
2. **Tempo de Queima (Ticks):** Determina a resiliência/duração da chama naquela célula, permitindo que o calor dissipe de forma heterogênea.

### Equação de Ignição Estocástica
A transição de uma célula intacta para "em chamas" reage à quantidade de calor ao redor (vizinhos em chamas) combinada à resistência natural do material:

$$P_{ignicao} = 1 - (1 - P_{base})^{V_{fogo}}$$

Onde $V_{fogo}$ é o número de células adjacentes ativamente em chamas.

---

## Level Design Estático

A malha inicial ($300 \times 300$) de ambos os scripts é populada de forma procedural e estática. Através de *slicing* no NumPy, as matrizes são desenhadas com estradas não inflamáveis e "clusters" de biomas específicos para testar transições florestais. O sistema conta com geradores automatizados que plantam focos iniciais aleatórios no mapa antes do início da iteração temporal.

---

## Como Executar Localmente

### Pré-requisitos
Certifique-se de ter o Python 3 instalado e as bibliotecas necessárias:
```bash
pip install numpy pygame
