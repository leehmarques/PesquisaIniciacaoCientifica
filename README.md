# Prediction of Adverse Vaccine Reactions using NMF
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Data Science](https://img.shields.io/badge/Data_Science-NMF-blue?style=for-the-badge)
![UFABC](https://img.shields.io/badge/UFABC-Iniciação_Científica-green?style=for-the-badge)

This repository contains the computational pipeline developed for the Scientific Initiation (IC) project at the **Federal University of ABC (UFABC)**. 

The project aims to develop a predictive computational model to identify new and potential adverse reactions associated with different vaccines. The approach is based on **Non-Negative Matrix Factorization (NMF)**, a collaborative filtering technique widely used in recommendation systems, enhanced with Tikhonov (L2) Regularization and joint learning using the MedDRA hierarchy.

## 📊 Data Sources
* **FDALabel (FDA):** Used to build the primary association matrix between Vaccine (Trade Name) and Adverse Reaction (PT - Preferred Term).
* **MedDRA Hierarchy:** Used as a guidance matrix (HLGT Name x PT) to improve the factorization's predictive accuracy.

## 🏗️ Project Structure
The code is modularized to ensure readability, scalability, and ease of experimentation:

* `main.py`: The main orchestrator script. It handles data loading, sets experimental hyperparameters, and executes the training and validation loops.
* `nmf_model.py`: Contains the mathematical core, including matrix initialization, the NMF algorithm with joint factorization and regularization, and the Leave-One-Out cross-validation logic.
* `visualization.py`: Handles the generation of high-resolution plots for Top-K accuracy and Frobenius error convergence.
* `processing.py`: (Optional utility) Handles API requests to download FDALabel data and performs text cleaning and MedDRA merges.

## 🚀 How to Run

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/nmf-pharmacovigilance-ic.git](https://github.com/YOUR_USERNAME/nmf-pharmacovigilance-ic.git)
   cd nmf-pharmacovigilance-ic

2. **Install the required libraries:**
```bash
pip install pandas numpy matplotlib requests

```


3. **Run the main experiment:**
Ensure the dataset (`fdalabel_base_completa.csv`) is in the root directory (Note: large CSV files are ignored via `.gitignore`).
```bash
python main.py

```


The script will output the Top-K hit rates in the console and save `accuracy_comparison.png` and `error_convergence.png` to the directory.

## 👨‍🔬 Authorship & Acknowledgements

* **Researcher:** Letícia Marques Ferreira
* **Advisor:** Prof. Dr. Suzana de Siqueira Santos
* **Institution:** Federal University of ABC (UFABC) - 2025/2026

---

---

# Predição de Reações Adversas de Vacinas usando NMF

Este repositório contém o pipeline computacional desenvolvido para o projeto de Iniciação Científica (IC) da **Universidade Federal do ABC (UFABC)**.

O projeto tem como objetivo desenvolver um modelo computacional preditivo para identificar novas e possíveis reações adversas associadas a diferentes imunizantes. A abordagem baseia-se na **Fatoração de Matrizes Não-Negativas (NMF)**, uma técnica de filtragem colaborativa amplamente utilizada em sistemas de recomendação, aprimorada com Regularização de Tikhonov (L2) e aprendizado conjunto utilizando a hierarquia MedDRA.

## 📊 Fontes de Dados

* **FDALabel (FDA):** Utilizado para construir a matriz principal de associações entre Vacina (Trade Name) e Reação Adversa (PT - Preferred Term).
* **Hierarquia MedDRA:** Utilizada como matriz de suporte (HLGT Name x PT) para guiar o aprendizado e melhorar a acurácia preditiva da fatoração.

## 🏗️ Estrutura do Projeto

O código foi modularizado para garantir legibilidade, escalabilidade e facilidade de experimentação:

* `main.py`: O script orquestrador principal. Ele gerencia o carregamento de dados, define os hiperparâmetros experimentais e executa os ciclos de treino e validação.
* `nmf_model.py`: Contém o núcleo matemático, incluindo a inicialização das matrizes, o algoritmo NMF com fatoração conjunta e regularização, e a lógica de validação cruzada *Leave-One-Out*.
* `visualization.py`: Responsável pela geração de gráficos de alta resolução para análise da acurácia Top-K e convergência do Erro Frobenius.
* `processing.py`: (Utilitário) Gerencia as requisições à API para descarregar os dados do FDALabel, além de realizar a limpeza de texto e os cruzamentos com o MedDRA.

## 🚀 Como Executar

1. **Clonar o repositório:**
```bash
git clone [https://github.com/SEU_USUARIO/nmf-pharmacovigilance-ic.git](https://github.com/SEU_USUARIO/nmf-pharmacovigilance-ic.git)
cd nmf-pharmacovigilance-ic

```


2. **Instalar as bibliotecas necessárias:**
```bash
pip install pandas numpy matplotlib requests

```


3. **Executar o experimento principal:**
Certifique-se de que o conjunto de dados (`fdalabel_base_completa.csv`) está na diretoria raiz (Nota: ficheiros CSV pesados são ignorados pelo `.gitignore`).
```bash
python main.py

```


O script imprimirá as taxas de acerto Top-K na consola e guardará as imagens `accuracy_comparison.png` e `error_convergence.png` na diretoria local.

## 👨‍🔬 Autoria e Agradecimentos

* **Pesquisadora:** Letícia Marques Ferreira
* **Orientadora:** Profª. Drª. Suzana de Siqueira Santos
* **Instituição:** Universidade Federal do ABC (UFABC) - Edital 01/2025

```

```