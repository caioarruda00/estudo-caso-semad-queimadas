# -*- coding: utf-8 -*-
"""Gera o notebook de entrega do estudo de caso SEMAD-GO."""

from pathlib import Path

import nbformat as nbf
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks" / "estudo_caso_semad_queimadas.ipynb"
OUT.parent.mkdir(parents=True, exist_ok=True)

nb = new_notebook(
    metadata={
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    }
)

cells = []

def md(src: str) -> None:
    cells.append(new_markdown_cell(src.strip() + "\n"))

def code(src: str) -> None:
    cells.append(new_code_cell(src.strip() + "\n"))


md(
    """
# Estudo de caso SEMAD-GO — queimadas em Goiás (safra de seca 2024)

Consultoria de dados para a Secretaria de Estado de Meio Ambiente e Desenvolvimento Sustentável de Goiás.

**Objetivo:** calcular medidas de tendência central e de dispersão da variável `focos_calor` e responder ao questionário avaliativo (10 questões).

**Recorte:** 31 municípios reais × 5 meses (junho a outubro de 2024) = 155 registros, em duas regiões:

- Norte/Nordeste (Vão do Paranã / Chapada dos Veadeiros)
- Sul/Sudoeste (fronteira agrícola)

**Convenção deste notebook:** variância e desvio padrão **populacionais** (`ddof=0`), conforme o enunciado. O CV é apresentado em percentual: \(CV = \\sigma / \\mu \\times 100\\%\).
"""
)

md(
    """
## 0. Bibliotecas, leitura e função de medidas
"""
)

code(
    """
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

pd.set_option("display.float_format", "{:.4f}".format)

ROOT = Path.cwd()
if not (ROOT / "data" / "focos_queimada_goias.csv").exists():
    ROOT = ROOT.parent

df = pd.read_csv(ROOT / "data" / "focos_queimada_goias.csv")
print("Linhas:", len(df))
print("Municípios:", df["municipio"].nunique())
print("Meses:", sorted(df["mes"].unique().tolist()))
print(df["regiao"].value_counts())
df.head()
"""
)

code(
    """
def medidas(serie: pd.Series) -> pd.Series:
    \"\"\"Medidas pedidas no enunciado para uma série de focos_calor.\"\"\"
    media = serie.mean()
    dp = serie.std(ddof=0)
    vc = serie.value_counts()
    moda_freq = int(vc.iloc[0])
    modas = vc[vc == moda_freq].index.tolist()
    return pd.Series(
        {
            "n": int(serie.count()),
            "media": media,
            "mediana": serie.median(),
            "moda": modas[0] if len(modas) == 1 else f"multimodal {modas}",
            "freq_moda": moda_freq,
            "minimo": serie.min(),
            "maximo": serie.max(),
            "amplitude": serie.max() - serie.min(),
            "variancia_pop": serie.var(ddof=0),
            "desvio_padrao_pop": dp,
            "cv_percent": (dp / media) * 100,
        }
    )


norte = df.loc[df["regiao"] == "Norte/Nordeste", "focos_calor"]
sul = df.loc[df["regiao"] == "Sul/Sudoeste", "focos_calor"]
completo = df["focos_calor"]

resumo = pd.DataFrame(
    {
        "Norte/Nordeste": medidas(norte),
        "Sul/Sudoeste": medidas(sul),
        "Dataset completo": medidas(completo),
    }
)
resumo
"""
)

code(
    """
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

df.boxplot(column="focos_calor", by="regiao", ax=axes[0], grid=False)
axes[0].set_title("Focos de calor por região")
axes[0].set_xlabel("Região")
axes[0].set_ylabel("Focos de calor (município/mês)")
axes[0].get_figure().suptitle("")

media_mes = (
    df.groupby(["mes", "regiao"], as_index=False)["focos_calor"]
    .mean()
    .pivot(index="mes", columns="regiao", values="focos_calor")
)
media_mes.plot(ax=axes[1], marker="o")
axes[1].set_title("Média de focos por mês e região")
axes[1].set_xlabel("Mês (2024)")
axes[1].set_ylabel("Média de focos de calor")
axes[1].set_xticks([6, 7, 8, 9, 10])
axes[1].legend(title="Região")

fig.tight_layout()
plt.show()
"""
)

md(
    """
## Questão 1 — média por região

Calcule a média de `focos_calor` por município/mês para cada uma das duas regiões. Qual região apresenta a maior média?
"""
)

code(
    """
media_norte = norte.mean()
media_sul = sul.mean()

print(f"Norte/Nordeste: soma={norte.sum()}  n={norte.count()}  media={norte.sum() / norte.count():.4f}")
print(f"Sul/Sudoeste:   soma={sul.sum()}  n={sul.count()}  media={sul.sum() / sul.count():.4f}")
print("Maior média:", "Sul/Sudoeste" if media_sul > media_norte else "Norte/Nordeste")
"""
)

md(
    """
**Resposta.** Norte/Nordeste = **32,02** focos (3362 / 105). Sul/Sudoeste = **43,66** focos (2183 / 50). A região **Sul/Sudoeste** tem a maior média.
"""
)

md(
    """
## Questão 2 — mediana versus média (simetria)

Calcule a mediana de `focos_calor` para cada região e compare com a média da Questão 1. A diferença sugere distribuição simétrica ou assimétrica? Justifique.
"""
)

code(
    """
print("Norte/Nordeste  media={:.4f}  mediana={:.1f}  diferenca={:.4f}".format(
    norte.mean(), norte.median(), norte.mean() - norte.median()
))
print("Sul/Sudoeste    media={:.4f}  mediana={:.1f}  diferenca={:.4f}".format(
    sul.mean(), sul.median(), sul.mean() - sul.median()
))
"""
)

md(
    """
**Resposta.** Mediana Norte/Nordeste = **22**; Sul/Sudoeste = **32**. Nas duas regiões a média é maior que a mediana (diferenças de +10,02 e +11,66). Isso indica **assimetria à direita**: poucos município-mês com focos muito altos puxam a média, enquanto o centro da distribuição (mediana) permanece mais baixo.
"""
)

md(
    """
## Questão 3 — moda

Identifique a moda de `focos_calor` em cada região. O valor modal é um bom resumo dos dados? Justifique com a frequência de repetição.
"""
)

code(
    """
print("Norte/Nordeste — 8 valores mais frequentes:")
print(norte.value_counts().head(8))
print()
print("Sul/Sudoeste — 12 valores mais frequentes:")
print(sul.value_counts().head(12))
"""
)

md(
    """
**Resposta.** Norte/Nordeste: moda = **11** (frequência 6 em 105, cerca de 5,7%). Sul/Sudoeste: **não há moda única** — 11 valores empatam com frequência 2. A moda **não é um bom resumo**: no Norte ela é rara e fica bem abaixo da média e da mediana; no Sul a repetição máxima é só 2 observações, então o valor modal quase não representa o conjunto.
"""
)

md(
    """
## Questão 4 — amplitude

Calcule a amplitude (máximo - mínimo) em cada região. O que ela revela — e o que ela NÃO revela — sobre a variabilidade?
"""
)

code(
    """
print("Norte/Nordeste: max={}  min={}  amplitude={}".format(
    norte.max(), norte.min(), norte.max() - norte.min()
))
print("Sul/Sudoeste:   max={}  min={}  amplitude={}".format(
    sul.max(), sul.min(), sul.max() - sul.min()
))
"""
)

md(
    """
**Resposta.** Amplitude Norte/Nordeste = **169** (172 - 3). Sul/Sudoeste = **179** (184 - 5). A amplitude mostra só a distância entre os extremos. Ela **não** diz se a maioria dos pontos está perto da média, se a dispersão é geral ou se um único outlier explica o intervalo. Por isso não substitui variância, desvio padrão nem CV.
"""
)

md(
    """
## Questão 5 — variância populacional

\\(\\sigma^2 = \\dfrac{\\sum (x_i - \\mu)^2}{N}\\)
"""
)

code(
    """
print("Norte/Nordeste var_pop =", norte.var(ddof=0))
print("Sul/Sudoeste   var_pop =", sul.var(ddof=0))
print()
print("Conferencia pela definição (Norte/Nordeste):")
mu = norte.mean()
print(((norte - mu) ** 2).sum() / len(norte))
"""
)

md(
    """
**Resposta.** Variância populacional Norte/Nordeste = **1070,78**. Sul/Sudoeste = **1510,18**. Usamos `ddof=0` porque o enunciado pede variância populacional (dividir por N, não por N-1).
"""
)

md(
    """
## Questão 6 — desvio padrão populacional

\\(\\sigma = \\sqrt{\\sigma^2}\\). Interprete o valor em relação à respectiva média.
"""
)

code(
    """
dp_norte = norte.std(ddof=0)
dp_sul = sul.std(ddof=0)
print("Norte/Nordeste dp={:.4f}  media={:.4f}  dp/media={:.4f}".format(
    dp_norte, norte.mean(), dp_norte / norte.mean()
))
print("Sul/Sudoeste   dp={:.4f}  media={:.4f}  dp/media={:.4f}".format(
    dp_sul, sul.mean(), dp_sul / sul.mean()
))
"""
)

md(
    """
**Resposta.** Desvio padrão Norte/Nordeste = **32,72** focos: os valores se afastam da média 32,02 por cerca de 32,7 focos (dispersão típica da mesma ordem da média). Sul/Sudoeste = **38,86** focos frente à média 43,66. Em termos absolutos o Sul varia mais; nas duas regiões o desvio padrão é alto em relação à média.
"""
)

md(
    """
## Questão 7 — coeficiente de variação

\\(CV = \\dfrac{\\sigma}{\\mu} \\times 100\\%\\)

Como as médias são diferentes, o que é mais adequado para comparar a variabilidade relativa: o desvio padrão bruto ou o CV? Qual região é relativamente mais homogênea?
"""
)

code(
    """
cv_norte = norte.std(ddof=0) / norte.mean() * 100
cv_sul = sul.std(ddof=0) / sul.mean() * 100
print(f"CV Norte/Nordeste = {cv_norte:.4f}%")
print(f"CV Sul/Sudoeste   = {cv_sul:.4f}%")
print("Mais homogênea (menor CV):", "Sul/Sudoeste" if cv_sul < cv_norte else "Norte/Nordeste")
"""
)

md(
    """
**Resposta.** CV Norte/Nordeste = **102,20%**. CV Sul/Sudoeste = **89,01%**. O **CV** é a medida adequada para comparar variabilidade relativa, porque as médias são diferentes; o desvio padrão bruto não equaliza a escala. Pelo CV, o **Sul/Sudoeste é relativamente mais homogêneo**. No Norte a dispersão supera a própria média (CV > 100%).
"""
)

md(
    """
## Questão 8 — setembro (mês de pico) versus dataset completo

Filtre `mes = 9` e calcule média, mediana e desvio padrão de todos os municípios juntos. Compare com junho–outubro. O que isso indica sobre a sazonalidade na variabilidade?
"""
)

code(
    """
setembro = df.loc[df["mes"] == 9, "focos_calor"]

comparacao = pd.DataFrame(
    {
        "Dataset completo (jun–out)": [
            completo.mean(),
            completo.median(),
            completo.std(ddof=0),
        ],
        "Somente setembro": [
            setembro.mean(),
            setembro.median(),
            setembro.std(ddof=0),
        ],
    },
    index=["media", "mediana", "desvio_padrao_pop"],
)
comparacao
"""
)

md(
    """
**Resposta.** Completo: média **35,77**, mediana **25,00**, desvio padrão **35,24**. Setembro: média **74,03**, mediana **58,00**, desvio padrão **47,38**. O mês de pico mais do que dobra o nível médio e aumenta a dispersão absoluta. A sazonalidade da seca concentra risco em setembro: o patamar sobe em todo o estado e os municípios se afastam mais uns dos outros em número de focos. Usar só a média do semestre esconde o pico operacional.
"""
)

md(
    """
## Questão 9 — outlier e robustez da média

Localize o registro com o maior `focos_calor`. Recalcule média e mediana da região dele sem esse ponto. Qual medida de tendência central é mais sensível a extremos? Por quê?
"""
)

code(
    """
idx = df["focos_calor"].idxmax()
outlier = df.loc[idx]
print(outlier[["municipio", "regiao", "mes_nome", "focos_calor"]].to_string())

regiao_out = outlier["regiao"]
com = df.loc[df["regiao"] == regiao_out, "focos_calor"]
sem = df.loc[(df["regiao"] == regiao_out) & (df.index != idx), "focos_calor"]

print()
print(f"Região {regiao_out}")
print(f"n com outlier={com.count()}  n sem={sem.count()}")
print(f"media    com={com.mean():.4f}  sem={sem.mean():.4f}  delta={com.mean() - sem.mean():.4f}")
print(f"mediana  com={com.median():.4f}  sem={sem.median():.4f}  delta={com.median() - sem.median():.4f}")
"""
)

md(
    """
**Resposta.** Outlier: **Mineiros, setembro/2024, 184 focos** (Sul/Sudoeste). Sem esse registro, a média da região cai de **43,66** para **40,80** (-2,86) e a mediana de **32** para **31** (-1). A **média** é mais sensível a extremos porque todos os valores entram na soma; a mediana só depende da posição central da série ordenada.
"""
)

md(
    """
## Questão 10 — parecer técnico (prioridade de fiscalização)

Com base em todas as medidas, compare nível médio e variabilidade das duas regiões e indique a prioridade de fiscalização — considerando magnitude e dispersão, não apenas os totais.
"""
)

code(
    """
totais = df.groupby("regiao")["focos_calor"].agg(["sum", "mean", "median", "count"])
totais["cv_percent"] = [
    norte.std(ddof=0) / norte.mean() * 100,
    sul.std(ddof=0) / sul.mean() * 100,
]
totais
"""
)

md(
    """
**Parecer.** O Sul/Sudoeste tem maior magnitude média de focos por município/mês (43,66 contra 32,02) e maior dispersão absoluta (desvio padrão 38,86; amplitude 179). O Norte/Nordeste é relativamente mais instável: CV de 102,20%, média puxada por picos (Cavalcante, Niquelândia, Monte Alegre de Goiás) e mediana de apenas 22 focos. O total de focos é maior no Norte só porque essa região reúne 21 dos 31 municípios da amostra, não porque o risco por localidade seja mais alto. Recomenda-se priorizar a fiscalização contínua na fronteira agrícola do Sul/Sudoeste, onde o patamar elevado é mais homogêneo (CV 89,01%), e complementar com operações pontuais nos municípios-pico do Norte/Nordeste. O planejamento deve usar média, mediana e CV juntos: a média sozinha superestima o município típico, e o total sozinho distorce a comparação entre regiões de tamanhos diferentes.
"""
)

nb.cells = cells
OUT.write_text(nbf.writes(nb), encoding="utf-8")
print("Notebook gravado em", OUT)
