# 🔥 Simulador de Propagação de Incêndios Florestais

Um modelo computacional de **Autômato Celular Estocástico com Espaço de Estados Estendido**, desenvolvido em Python, para prever e simular o espalhamento de frentes de fogo em diferentes biomas e condições de combustível celular.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![NumPy](https://img.shields.io/badge/NumPy-Optimized-green.svg)
![Pygame](https://img.shields.io/badge/Pygame-Render-red.svg)

---

## 📋 Sobre o Projeto

Este projeto modela a propagação do fogo utilizando matrizes bidimensionais e Autômatos Celulares. Diferente de abordagens determinísticas simples, esta simulação aplica **Modelos de Combustível** (baseados na literatura de engenharia florestal, como Rothermel e Anderson) para calcular a ignição através de probabilidade de eventos independentes.

O objetivo é evitar anomalias clássicas de simulações em grid (como a super-saturação isotrópica ou "efeito parede sólida") garantindo que o fogo apresente um comportamento orgânico, com frentes de calor irregulares, engasgos e áreas de sobrevivência vegetal.

## ⚙️ Como Funciona (A Matemática)

O autômato avalia a malha utilizando a **Vizinhança de Moore** (8 direções) e um sistema de *swap* de matrizes para garantir que o tempo transcorra de forma perfeitamente síncrona ($t \rightarrow t+1$).

### Espaço de Estados Estendido
Cada célula no grid não possui apenas uma "cor", mas um vetor de estado contendo:
1. **Material (ID):** Define a inflamabilidade base.
2. **Tempo de Queima (Ticks):** Determina a resiliência/duração da chama naquela célula, permitindo que o calor fique ancorado na malha por múltiplas iterações.

### Equação de Ignição
A transição de uma célula intacta para "em chamas" é estocástica. A probabilidade de ignição reage à quantidade de calor ao redor (vizinhos em chamas) combinada à resistência natural do material ($P_{base}$):

$$P_{ignicao} = 1 - (1 - P_{base})^{V_{fogo}}$$

Onde $V_{fogo}$ é o número de células adjacentes ativamente em chamas.

## 🌲 Modelos de Combustível Implementados

O projeto utiliza um dicionário balanceado de propriedades físicas para garantir uma dissipação realista em tempo real (15 FPS).

| Vegetação | Inflamabilidade ($P_{base}$) | Tempo de Queima | Comportamento na Simulação |
| :--- | :--- | :--- | :--- |
| **Grama Seca** | 25% | 3 iterações | Queima rápida, propaga fogo com facilidade formando frentes abertas. |
| **Arbusto Seco** | 15% | 4 iterações | Propagação mediana, serve como ponte térmica. |
| **Folha Úmida** | 5% | 5 iterações | Alta resistência inicial, atua quase como um corta-fogo natural. |
| **Madeira Seca** | 10% | 7 iterações | Demora a inflamar, mas atua como âncora de calor duradoura. |
| **Árvore Úmida** | 2% | 10 iterações | Queima lenta e densa. |

## 🗺️ Level Design Estático

A matriz inicial ($300 \times 300$) é gerada proceduralmente através de *slicing* no NumPy, simulando o mapeamento de uma imagem de satélite dividida em 4 quadrantes principais:
* **Nordeste:** Zona Urbana (Prédios, galpões e estruturas estáticas não-inflamáveis).
* **Noroeste:** Pasto Aberto (Grama seca com moitas isoladas de arbustos).
* **Sudeste:** Bosque Misto (Ilhas detalhadas de vegetação variada).
* **Sudoeste:** Floresta Densa (Miolo espesso de árvores úmidas, folhagens e troncos).

## 🚀 Como Executar Localmente

### Pré-requisitos
Certifique-se de ter o Python 3 instalado e as bibliotecas necessárias:
```bash
pip install numpy pygame
