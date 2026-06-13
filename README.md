# 🔥 Simulador de Propagação de Incêndios Florestais

Um modelo computacional de **Autômato Celular Estocástico com Espaço de Estados Estendido**, desenvolvido em Python, para prever e simular o espalhamento de frentes de fogo em diferentes biomas e condições de combustível celular.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![NumPy](https://img.shields.io/badge/NumPy-Optimized-green.svg)
![Pygame](https://img.shields.io/badge/Pygame-Render-red.svg)

---

## 📋 Sobre o Projeto

Este projeto modela a propagação do fogo utilizando matrizes bidimensionais e Autômatos Celulares. Diferente de abordagens determinísticas simples, esta simulação aplica **Modelos de Combustível** (baseados na literatura de engenharia florestal, como Rothermel e Anderson) para calcular a ignição através de probabilidade de eventos independentes.

Para fins de análise acadêmica e demonstração matemática, o repositório conta com **duas versões do algoritmo** (`super-saturada.py` e `heterogeneo.py`), que evidenciam como o balanceamento de hiperparâmetros estocásticos altera drasticamente o comportamento da simulação.

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

---

## ⚖️ Os Dois Modelos (O Paradoxo Estocástico)

O projeto contém dois executáveis principais que diferem exclusivamente no dicionário de `PROPRIEDADES_MATERIAIS`, demonstrando na prática o desafio do balanceamento probabilístico em tempo real (15 FPS).

### 1. `super-saturada.py` (O "Efeito Papel Higiênico")
Utiliza probabilidades base muito elevadas e um tempo de residência curto, gerando a anomalia visual da super-saturação isotrópica.
* **Grama Seca:** $P_{base} = 0.80$ | Duração: 1 tick
* **Comportamento:** O cálculo estocástico se aproxima rapidamente de 100% com o suporte de apenas 1 vizinho ativo. Visualmente, a frente de onda avança como uma parede sólida e contínua, consumindo todo o material de forma linear (semelhante à queima de uma folha de papel higiênico), sem apresentar as falhas naturais de um incêndio.

### 2. `heterogeneo.py` (Propagação Orgânica e Realista)
Ajusta punitivamente as probabilidades base para compensar a alta taxa de quadros, aumentando o tempo de queima para atuar como âncora térmica.
* **Grama Seca:** $P_{base} = 0.25$ | Duração: 3 ticks
* **Comportamento:** O fogo sofre "engasgos" matemáticos intencionais. A chama contorna certas células, deixa ilhas de vegetação verde intactas e forma frentes de ataque irregulares (cabeças e flancos), aproximando o Autômato Celular ao rigor físico de uma queimada florestal real.

---

## 🗺️ Level Design Estático

A matriz inicial ($300 \times 300$) de ambos os scripts é gerada proceduralmente através de *slicing* no NumPy, simulando o mapeamento de uma imagem de satélite dividida em 4 quadrantes principais por estradas não-inflamáveis:
* **Nordeste:** Zona Urbana (Prédios, galpões e estruturas estáticas em cinza).
* **Noroeste:** Pasto Aberto (Grama seca com moitas isoladas de arbustos).
* **Sudeste:** Bosque Misto (Ilhas detalhadas de vegetação variada).
* **Sudoeste:** Floresta Densa (Miolo espesso de árvores úmidas, folhagens e troncos).

---

## 🚀 Como Executar Localmente

### Pré-requisitos
Certifique-se de ter o Python 3 instalado e as bibliotecas necessárias:
```bash
pip install numpy pygame
