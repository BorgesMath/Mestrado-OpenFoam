# CASO: 


Primeiro caso conversado entre eu e o prof. É um bem simples, de Hagen-Poiuselle. Tava na duvida entre a diferença conceitual desse para o de Helle-Shaw, ele usa as mesmas equações? mas o Hagen é mais geral e o de Helle em estruturas na ordem do micro? Tinh já feito uma de Hagen para treinar no inicio desse semestre e segui ele

![image.png](Plot_ICOFOAM_files/e45dc6b0-1d3f-4d69-b374-0306b844f6d4.png)

# GEOMETRIA

scale   0.1;

vertices
(
    (0 0 0)   //0
    (10 0 0)   //1
    (10 1 0)   //2
    (0 1 0)   //3
    (0 0 0.1) //4
    (10 0 0.1) //5
    (10 1 0.1) //6
    (0 1 0.1) //7
);

# Convergencia Da Malha
# Construção Fiz a malha de maneira bem simples, ja que a geometria era 10x1, tentei seguir um esquema semelhante

  blocks
(
    hex (0 1 2 3 4 5 6 7) (50 5 1) simpleGrading (1 1 1)
);


# Simulações
- **Malha 0**: Malha (25 5 1) ->   125
- **Malha 1**: Malha (50 5 1) ->   250
- **Malha 2**: Malha (80 8 1) ->   640
- **Malha 3**: Malha (100 10 1) -> 1000
- **Malha 4**: Malha (150 15 1) -> 2250

Fiz ate o resultado ficar semelhante ao analitico, **deveria ter feito mais simulações para ver ser o resultado se manteria perto e de aumentasse não varia tanto o resultado**


```python
import matplotlib.pyplot as plt
import numpy as np

# Dados
malha = np.array([125, 250, 640, 1000, 2250])  # Tamanho da malha
valores = np.array([1.365237e-04, 1.365223e-04, 1.304570e-04, 1.290517e-04, 1.276557e-04])  # Valores

# Plot
plt.figure(figsize=(8, 5))
plt.plot(malha, valores, marker='o', linestyle='-', color='b', label="Variação de Valor")
plt.grid()
plt.title("Análise de Malha - Pressão Fixa P = 102.856", fontsize=14)
plt.xlabel("Tamanho da Malha", fontsize=12)
plt.ylabel("Valores (m³/s)", fontsize=12)
plt.xticks(malha)  # Garantir que todos os pontos aparecem
plt.legend(fontsize=10)
plt.tight_layout()
plt.show()

```


    
![png](Plot_ICOFOAM_files/Plot_ICOFOAM_8_0.png)
    


# CODIGO PARA AUTOMATIZAR A SIMULAÇÃO E MUDANÇA DE PRESSÃO

#!/bin/bash

# Valores de pressão para variação
pressures=(110 120 130 140 150)

# Nome do caso base
base_case="HagenPouiselle_Malha4"

# Verificar se o caso base existe
if [ ! -d "$base_case" ]; then
    echo "Erro: Diretório do caso base '$base_case' não encontrado."
    exit 1
fi

# Loop para executar simulações com diferentes valores de pressão
for pressure in "${pressures[@]}"; do
    # Nome do novo caso
    case_name="${base_case}_P${pressure}"
    echo "Criando caso: $case_name com pressão $pressure"

    # Copiar o caso base
    cp -r "$base_case" "$case_name"

    # Modificar a pressão no arquivo '0/p'
    foamDictionary "$case_name/0/p" -entry boundaryField.inlet.value -set "uniform $pressure"

    # Executar blockMesh e icoFoam
    cd "$case_name" || exit
    blockMesh
    icoFoam
    cd ..

    echo "Simulação finalizada para: $case_name"
done

# Resultados



```python
import numpy as np
import matplotlib.pyplot as plt

# Dados fornecidos
pressures = np.array([102.856, 110, 120, 130, 140, 150])  # Pa
P_atm = 101.325  # Pa
DeltaP = pressures - P_atm  # Diferença de pressão

# Parâmetros
h = 0.1  # m
mu = 1  
L = 1  # m

# Cálculo de Q analítico
Q_analitico = (DeltaP * h**3) / (12 * mu * L)

# Dados simulados (vazão Q para cada pressão)
Q_simulado = np.array([
    1.276557e-04, 
    7.233240e-04,
    1.557140e-03,
    2.390961e-03,
    3.224864e-03,
    4.058845e-03
])


E = abs(Q_analitico - Q_simulado)

# Plotagem
plt.figure(figsize=(10, 6))

# Curva analítica
plt.plot(pressures, Q_analitico, label="Q Analítico", linestyle="--", color="blue", linewidth=2, alpha=0.8)

# Pontos simulados
plt.scatter(pressures, Q_simulado, label="Q Simulado", color="red", s=80, edgecolor="black", zorder=5)

# Personalizações
plt.title("Pressão vs Vazão", fontsize=14)
plt.xlabel("Pressão (Pa)", fontsize=12)
plt.ylabel("Vazão (m³/s)", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Mostrando o gráfico
plt.show()

```


    
![png](Plot_ICOFOAM_files/Plot_ICOFOAM_12_0.png)
    


.



```python
E = abs(Q_analitico - Q_simulado)
plt.plot(pressures, E, label="Q Analítico", linestyle="--", color="blue", linewidth=2, alpha=0.8)

# Personalizações
plt.title("Erro vs Pressão", fontsize=14)
plt.xlabel("Pressão (Pa)", fontsize=12)
plt.ylabel("Erro", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Mostrando o gráfico
plt.show()
```


    
![png](Plot_ICOFOAM_files/Plot_ICOFOAM_14_0.png)
    





```python
import pandas as pd
df = pd.DataFrame({
    'Pressões (Pa)': pressures,
    'Delta P (Pa)': DeltaP,
    'Q Analítico (m³/s)': Q_analitico,
    'Q Simulado (m³/s)': Q_simulado,
    'Erro (m³/s)': E
})
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Pressões (Pa)</th>
      <th>Delta P (Pa)</th>
      <th>Q Analítico (m³/s)</th>
      <th>Q Simulado (m³/s)</th>
      <th>Erro (m³/s)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>102.856</td>
      <td>1.531</td>
      <td>0.000128</td>
      <td>0.000128</td>
      <td>7.236667e-08</td>
    </tr>
    <tr>
      <th>1</th>
      <td>110.000</td>
      <td>8.675</td>
      <td>0.000723</td>
      <td>0.000723</td>
      <td>4.073333e-07</td>
    </tr>
    <tr>
      <th>2</th>
      <td>120.000</td>
      <td>18.675</td>
      <td>0.001556</td>
      <td>0.001557</td>
      <td>8.900000e-07</td>
    </tr>
    <tr>
      <th>3</th>
      <td>130.000</td>
      <td>28.675</td>
      <td>0.002390</td>
      <td>0.002391</td>
      <td>1.377667e-06</td>
    </tr>
    <tr>
      <th>4</th>
      <td>140.000</td>
      <td>38.675</td>
      <td>0.003223</td>
      <td>0.003225</td>
      <td>1.947333e-06</td>
    </tr>
    <tr>
      <th>5</th>
      <td>150.000</td>
      <td>48.675</td>
      <td>0.004056</td>
      <td>0.004059</td>
      <td>2.595000e-06</td>
    </tr>
  </tbody>
</table>
</div>




```python

```
