# Artigos TYATT (conteúdo gerado)

Cada ficheiro `*.json` é um lote de artigos completos, no formato usado pelo
assistente e pelo gerador de ZIM:

```json
[
  {
    "id": "malaria",
    "titulo": "Malária — sintomas, prevenção e tratamento",
    "categoria": "Saúde",
    "corpo": "Parágrafo 1...\n\nParágrafo 2...",
    "aliases": ["Paludismo", "Sezões"]
  }
]
```

- **id** — identificador único (sem espaços nem acentos); vira o caminho no ZIM.
- **titulo** — título mostrado; o primeiro parágrafo do corpo é a resposta direta do assistente.
- **categoria** — uma das 16 categorias do plano.
- **corpo** — texto completo; parágrafos separados por `\n\n`.
- **aliases** (opcional) — termos populares que passam a encontrar o artigo
  (viram redirecionamentos no ZIM, como as redireções da Wikipédia). Ex.:
  «tensão alta» encontra «Hipertensão».

## Gerar o ZIM

```bash
pip install libzim
python3 ferramentas/gerar_zim.py            # cria tyatt_pt.zim na raiz
```

O `tyatt_pt.zim` abre no assistente (`assistente.html`), no Kiwix ou na app TYATT.

## Progresso

| Lote | Categoria | Artigos |
|------|-----------|---------|
| `saude-lote-01.json` | Saúde — primeiros socorros | 15 |
| `saude-lote-02.json` | Saúde — doenças principais | 15 |

Total atual: **30 artigos**. Meta: ~4.822 (ver `conteudo/plano.md`).
Próximos lotes seguem a ordem de prioridade do plano.
