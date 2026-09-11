# Estudo de caso SEMAD-GO — queimadas em Goiás (2024)

Consultoria de dados para a Secretaria de Meio Ambiente de Goiás (SEMAD-GO): análise do padrão de queimadas no estado durante a safra de seca de 2024 e recomendação de prioridades de fiscalização ambiental.

Disciplina: Data Science — 8º período.

## Entrega

| Arquivo | O que é |
| --- | --- |
| [notebooks/estudo_caso_semad_queimadas.ipynb](notebooks/estudo_caso_semad_queimadas.ipynb) | Notebook com todos os cálculos (código + saídas) |
| [docs/respostas_questionario.md](docs/respostas_questionario.md) | As 10 respostas numeradas, com código e justificativa |
| [docs/atividade_queimadas_goias.pdf](docs/atividade_queimadas_goias.pdf) | Enunciado original |
| [data/focos_queimada_goias.csv](data/focos_queimada_goias.csv) | Dataset |

## Como reproduzir

```text
pip install -r requirements.txt
jupyter notebook notebooks/estudo_caso_semad_queimadas.ipynb
```

Variância e desvio padrão são **populacionais** (`ddof=0`), como pede o enunciado.

## Resultado principal

- Maior média de focos por município/mês: **Sul/Sudoeste (43,66)** vs Norte/Nordeste (32,02)
- Sul/Sudoeste é relativamente mais homogêneo (**CV 89,01%** vs 102,20%)
- Prioridade de fiscalização contínua: **Sul/Sudoeste**, com operações pontuais nos picos do Norte/Nordeste
