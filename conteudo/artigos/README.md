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

## Dois formatos

- **Simples** (`corpo`): artigos práticos curtos-médios (Saúde, ofícios, etc.).
- **Académico** (`tipo: "academico"`): artigos universitários completos, com
  `resumo`, `palavras_chave`, `seccoes[]` (introdução, desenvolvimento,
  conclusão) e `referencias[]`. Ver `conteudo/plano-academico.md`.

## Progresso

| Área | Artigos |
|------|---------|
| Saúde (socorros, doenças, materno-infantil, diabetes, falciforme) | 37 |
| Angola (visão geral, geografia, história, 21 províncias, cultura, símbolos, kwanza) | 34 |
| Ciências (Física, Química, Biologia) | 12 |
| Académico universitário (Direito, Gestão, Economia, Enfermagem, Contabilidade, Psicologia, Informática, Saúde Pública) | 10 |
| Matemática | 10 |
| Português | 5 |
| História/Geografia do mundo | 5 |
| Finanças e empreendedorismo | 5 |
| Agricultura | 5 |
| Tecnologia | 6 |
| Cidadania e documentos | 6 |
| Nutrição | 4 |
| Ofícios | 4 |
| Educação e estudo | 4 |

Total atual: **147 artigos completos** (137 práticos + 10 académicos).
Metas: ~4.822 práticos (`plano.md`) e programa académico de longo prazo
(`plano-academico.md`). Próximos lotes seguem a prioridade dos planos.
