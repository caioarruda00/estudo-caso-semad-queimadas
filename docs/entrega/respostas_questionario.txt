# Respostas do questionário — SEMAD-GO (queimadas 2024)

Fonte dos cálculos: `notebooks/estudo_caso_semad_queimadas.ipynb`  
Variável: `focos_calor` | Variância e desvio padrão **populacionais** (`ddof=0`)  
Amostra: 155 registros (31 municípios × 5 meses; Norte/Nordeste n=105; Sul/Sudoeste n=50)

---

## Questão 1

**Média Norte/Nordeste** = 3362 / 105 = **32,02 focos** por município/mês  
**Média Sul/Sudoeste** = 2183 / 50 = **43,66 focos** por município/mês  

A região **Sul/Sudoeste** apresenta a maior média.

Código:

```python
norte = df.loc[df["regiao"] == "Norte/Nordeste", "focos_calor"]
sul = df.loc[df["regiao"] == "Sul/Sudoeste", "focos_calor"]
norte.mean()  # 32.019047...
sul.mean()    # 43.66
```

---

## Questão 2

| Região | Média | Mediana | Média - mediana |
| --- | ---: | ---: | ---: |
| Norte/Nordeste | 32,02 | 22,00 | +10,02 |
| Sul/Sudoeste | 43,66 | 32,00 | +11,66 |

Nas duas regiões a média é maior que a mediana, o que indica **distribuição assimétrica à direita** (cauda positiva). Há municípios/meses com focos muito altos que puxam a média para cima, enquanto a maior parte dos registros fica em torno de valores mais baixos (a mediana).

Código:

```python
norte.median()  # 22.0
sul.median()    # 32.0
```

---

## Questão 3

**Norte/Nordeste:** moda = **11** focos (frequência 6 em 105, cerca de 5,7%).  
**Sul/Sudoeste:** não há moda única — 11 valores diferentes empatam com frequência 2 (6, 7, 12, 13, 16, 19, 26, 31, 39, 44 e 92).

O valor modal **não é um bom resumo** neste caso. No Norte a moda aparece poucas vezes e está bem abaixo da média e da mediana. No Sul a repetição máxima é só 2 observações, então a moda quase não descreve o conjunto.

Código:

```python
norte.value_counts().head()
sul.value_counts().head()
```

---

## Questão 4

Amplitude = máximo ? mínimo

- Norte/Nordeste: 172 - 3 = **169**
- Sul/Sudoeste: 184 - 5 = **179**

A amplitude **revela** a extensão total dos dados (do menor ao maior foco observado). Ela **não revela** como os valores se distribuem entre os extremos: se a maioria está perto da média, se há um único outlier ou se a dispersão é generalizada. Por isso não substitui variância, desvio padrão nem CV.

Código:

```python
norte.max() - norte.min()  # 169
sul.max() - sul.min()      # 179
```

---

## Questão 5

Variância populacional: \(\sigma^2 = \sum(x_i - \mu)^2 / N\)

- Norte/Nordeste: **1070,78**
- Sul/Sudoeste: **1510,18**

Código:

```python
norte.var(ddof=0)  # 1070.780590...
sul.var(ddof=0)    # 1510.1844
```

(`ddof=0` porque o enunciado pede variância **populacional**, não amostral.)

---

## Questão 6

Desvio padrão populacional: \(\sigma = \sqrt{\sigma^2}\)

- Norte/Nordeste: **32,72** focos — os valores se afastam da média (32,02) por cerca de 32,7 focos, ou seja, a dispersão típica é da mesma ordem da própria média.
- Sul/Sudoeste: **38,86** focos — afastamento típico de cerca de 38,9 focos em relação à média 43,66.

Em termos absolutos, o Sul/Sudoeste varia mais. Em ambas as regiões o desvio padrão é alto frente à média, o que já antecipa CV elevado.

Código:

```python
norte.std(ddof=0)  # 32.722784...
sul.std(ddof=0)    # 38.861091...
```

---

## Questão 7

\(CV = (\sigma / \mu) \times 100\%\)

- Norte/Nordeste: 32,72 / 32,02 × 100% = **102,20%**
- Sul/Sudoeste: 38,86 / 43,66 × 100% = **89,01%**

Como as médias são diferentes, o **CV** é a medida mais adequada para comparar a variabilidade **relativa**. O desvio padrão bruto favorece a região de média maior e não equaliza a escala.

Com base no CV, a região **Sul/Sudoeste é relativamente mais homogênea** (CV menor). O Norte/Nordeste é mais irregular: a dispersão supera a própria média (CV > 100%).

Código:

```python
cv = lambda s: s.std(ddof=0) / s.mean() * 100
cv(norte)  # 102.197...
cv(sul)    # 89.008...
```

---

## Questão 8

Setembro (mês de pico, `mes = 9`), todos os municípios juntos (n=31), versus o dataset completo (junho a outubro, n=155):

| Recorte | Média | Mediana | Desvio padrão populacional |
| --- | ---: | ---: | ---: |
| Dataset completo | 35,77 | 25,00 | 35,24 |
| Somente setembro | 74,03 | 58,00 | 47,38 |

Setembro mais do que **dobra** o nível médio e também aumenta a dispersão absoluta. Isso mostra o efeito da sazonalidade: no auge da seca o patamar de queimadas sobe em todo o estado e os municípios se afastam mais uns dos outros em número de focos. A comparação confirma que boa parte da variabilidade do semestre está concentrada no mês de pico, e que usar só a média anual/semestral esconde o risco operacional de setembro.

Código:

```python
setembro = df.loc[df["mes"] == 9, "focos_calor"]
setembro.mean(), setembro.median(), setembro.std(ddof=0)
df["focos_calor"].mean(), df["focos_calor"].median(), df["focos_calor"].std(ddof=0)
```

---

## Questão 9

Maior valor do dataset: **Mineiros, setembro/2024, 184 focos** (região Sul/Sudoeste) — outlier.

Recalculo da região Sul/Sudoeste **sem** esse registro (n=49):

| Medida | Com outlier | Sem outlier | Variação |
| --- | ---: | ---: | ---: |
| Média | 43,66 | 40,80 | ?2,86 |
| Mediana | 32,00 | 31,00 | ?1,00 |

A **média** é mais sensível a valores extremos, porque entra na soma de todos os pontos: um único 184 desloca o resultado. A mediana só depende da posição central da série ordenada, então um extremo muda no máximo o valor do meio (aqui, de 32 para 31).

Código:

```python
outlier = df.loc[df["focos_calor"].idxmax()]
sul_sem = df.loc[(df["regiao"] == "Sul/Sudoeste") & (df.index != outlier.name), "focos_calor"]
sul.mean(), sul_sem.mean()
sul.median(), sul_sem.median()
```

---

## Questão 10

O Sul/Sudoeste tem maior magnitude média de focos por município/mês (43,66 contra 32,02) e maior dispersão absoluta (desvio padrão 38,86; amplitude 179). O Norte/Nordeste é relativamente mais instável: CV de 102,20%, média puxada por picos (Cavalcante, Niquelândia, Monte Alegre de Goiás) e mediana de apenas 22 focos. O total de focos é maior no Norte só porque essa região reúne 21 dos 31 municípios da amostra, não porque o risco por localidade seja mais alto. Recomenda-se priorizar a fiscalização contínua na fronteira agrícola do Sul/Sudoeste, onde o patamar elevado é mais homogêneo (CV 89,01%), e complementar com operações pontuais nos municípios-pico do Norte/Nordeste. O planejamento deve usar média, mediana e CV juntos: a média sozinha superestima o município típico, e o total sozinho distorce a comparação entre regiões de tamanhos diferentes.
