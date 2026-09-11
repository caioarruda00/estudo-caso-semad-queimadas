"""Cálculo das medidas pedidas no estudo de caso SEMAD-GO."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "focos_queimada_goias.csv"

df = pd.read_csv(CSV)
x = df["focos_calor"]

print("=== BASE ===")
print(f"linhas={len(df)} municipios={df['municipio'].nunique()} regioes={df['regiao'].unique().tolist()}")
print(df["regiao"].value_counts().to_string())
print()


def medidas(serie: pd.Series, rotulo: str) -> dict:
    n = int(serie.count())
    media = float(serie.mean())
    mediana = float(serie.median())
    vmin = float(serie.min())
    vmax = float(serie.max())
    amplitude = vmax - vmin
    var_pop = float(serie.var(ddof=0))
    dp_pop = float(serie.std(ddof=0))
    cv = (dp_pop / media) * 100 if media != 0 else float("nan")
    vc = serie.value_counts()
    moda_freq = int(vc.iloc[0])
    modas = vc[vc == moda_freq].index.tolist()
    print(f"=== {rotulo} (n={n}) ===")
    print(f"media={media:.6f}")
    print(f"mediana={mediana:.6f}")
    print(f"modas={modas} freq={moda_freq}")
    print(f"min={vmin} max={vmax} amplitude={amplitude}")
    print(f"var_pop={var_pop:.6f}")
    print(f"dp_pop={dp_pop:.6f}")
    print(f"cv%={cv:.6f}")
    print(f"media-mediana={media - mediana:.6f}")
    print("top frequencias:")
    print(vc.head(8).to_string())
    print()
    return {
        "n": n,
        "media": media,
        "mediana": mediana,
        "modas": modas,
        "moda_freq": moda_freq,
        "min": vmin,
        "max": vmax,
        "amplitude": amplitude,
        "var_pop": var_pop,
        "dp_pop": dp_pop,
        "cv": cv,
    }


norte = df.loc[df["regiao"] == "Norte/Nordeste", "focos_calor"]
sul = df.loc[df["regiao"] == "Sul/Sudoeste", "focos_calor"]

m_norte = medidas(norte, "Norte/Nordeste")
m_sul = medidas(sul, "Sul/Sudoeste")
m_all = medidas(x, "Dataset completo")

setembro = df.loc[df["mes"] == 9, "focos_calor"]
m_set = medidas(setembro, "Setembro (todos os municipios)")

outlier = df.loc[df["focos_calor"].idxmax()]
print("=== OUTLIER ===")
print(outlier.to_string())
print()

regiao_out = outlier["regiao"]
serie_com = df.loc[df["regiao"] == regiao_out, "focos_calor"]
serie_sem = df.loc[
    (df["regiao"] == regiao_out) & (df.index != outlier.name),
    "focos_calor",
]
print(f"=== {regiao_out} SEM o outlier ===")
print(f"n={serie_sem.count()}")
print(f"media_com={serie_com.mean():.6f} media_sem={serie_sem.mean():.6f} delta={serie_com.mean() - serie_sem.mean():.6f}")
print(f"mediana_com={serie_com.median():.6f} mediana_sem={serie_sem.median():.6f} delta={serie_com.median() - serie_sem.median():.6f}")
print()

print("=== TOTAIS POR REGIAO ===")
print(df.groupby("regiao")["focos_calor"].sum().to_string())
print()
print("=== MEDIA POR MES E REGIAO ===")
print(df.groupby(["regiao", "mes_nome"])["focos_calor"].mean().unstack().to_string())
