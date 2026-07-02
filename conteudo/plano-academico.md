# TYATT Académico — a biblioteca universitária offline dos PALOP

## Visão

Uma base de **artigos académicos completos** em português — resumo, introdução,
desenvolvimento e conclusão, com referências reais — cobrindo os campos mais
estudados em Angola e nos PALOP. Consultável offline, com um assistente que
navega e explica o conteúdo de forma inteligente. O objetivo é dar a qualquer
estudante, do Huambo a Cabinda, uma biblioteca de curso no bolso, sem internet.

## O padrão de cada artigo (obrigatório)

Cada artigo é **completo**, não resumido, e segue a estrutura académica:

1. **Título** e **área** (Direito, Gestão, Enfermagem, ...).
2. **Resumo** (abstract) — 5 a 8 linhas que respondem à pergunta central.
   É o que o assistente lê como resposta direta.
3. **Palavras-chave** — 4 a 6 termos.
4. **Introdução** — contexto, problema, objetivo e relevância.
5. **Desenvolvimento** — dividido em secções com subtítulos: conceitos,
   teorias, autores, exemplos aplicados ao contexto angolano/PALOP.
6. **Conclusão** — síntese e implicações.
7. **Referências e leituras recomendadas** — apenas obras e autores **reais**
   e reconhecidos. Nunca se inventam citações, páginas ou DOIs.

Extensão-alvo: 1.500 a 3.000 palavras. Nível: ensino superior (adaptável ao
médio). Linguagem rigorosa mas clara, com exemplos do contexto angolano.

## Campos prioritários (os mais estudados em Angola e PALOP)

| Área | Exemplos de subáreas |
|------|----------------------|
| Direito | constitucional, administrativo, civil, penal, trabalho, comercial |
| Gestão e Administração | recursos humanos, marketing, estratégia, operações |
| Economia | micro, macro, desenvolvimento, monetária, angolana |
| Contabilidade e Finanças | financeira, analítica, auditoria, fiscalidade |
| Enfermagem | fundamentos, médico-cirúrgica, saúde pública, materno-infantil |
| Medicina e Ciências da Saúde | fisiologia, patologia, epidemiologia, farmacologia |
| Engenharia Civil | estruturas, hidráulica, materiais, topografia |
| Engenharia Informática | programação, redes, bases de dados, sistemas |
| Engenharia Eletrotécnica | circuitos, energia, eletrónica |
| Psicologia | geral, desenvolvimento, social, organizacional, clínica |
| Ciências da Educação / Pedagogia | didática, currículo, avaliação, psicopedagogia |
| Sociologia | teorias, métodos, sociologia africana |
| Ciência Política e Relações Internacionais | Estado, democracia, integração africana |
| Letras e Linguística | linguística, literaturas africanas de língua portuguesa |
| Agronomia | fitotecnia, solos, produção animal, extensão rural |
| Geologia e Minas | petróleo, mineração, recursos |
| Matemática e Estatística | análise, álgebra, probabilidades, estatística aplicada |
| Física e Química | mecânica, eletromagnetismo, química geral e orgânica |
| História e Filosofia | história de Angola e de África, epistemologia, ética |
| Teologia e Ciências Religiosas | (procura relevante nos PALOP) |

## Arquitetura técnica (como fica inteligente e navegável)

- **Formato de dados**: JSON estruturado (ver `conteudo/artigos/README.md`),
  com `tipo: "academico"`, `area`, `nivel`, `resumo`, `palavras_chave`,
  `seccoes[]` e `referencias[]`.
- **Empacotamento**: `ferramentas/gerar_zim.py` gera um ZIM openZIM indexado,
  renderizando cada artigo em HTML com secções navegáveis, e criando
  redirecionamentos a partir das palavras-chave (atalhos de pesquisa).
- **Assistente inteligente** (`assistente.html`): lê o ZIM offline, responde
  com o resumo do artigo, permite abrir o artigo completo com secções, navegar
  por área, e seguir referências internas.

### Roteiro de inteligência (próximos passos técnicos)

1. **Pesquisa por texto completo** (não só por título): construir um índice
   invertido compacto durante a geração do ZIM, para o assistente encontrar
   artigos por qualquer termo do corpo — essencial com dezenas de milhares de
   artigos. (Hoje a pesquisa é por título + palavras-chave.)
2. **Navegação por área e nível**: menus "Direito → Constitucional → ...".
3. **Modo estudante**: "explica mais simples", "dá exemplos", "resume para o
   exame", "faz perguntas de revisão" a partir do artigo aberto.
4. **Índice de secções** clicável dentro de cada artigo.

## Escala — a verdade e o caminho

Gerar 50.000 artigos completos é um **programa de longo prazo**, não uma única
tarefa. Realisticamente:

- **Geração assistida (agora)**: dezenas de artigos completos por sessão de
  trabalho; milhares ao longo de muitas sessões.
- **Revisão humana (essencial)**: professores e técnicos angolanos validam
  antes de publicar — sobretudo Saúde e Direito.
- **Comunidade**: docentes e estudantes submetem e revêem artigos no mesmo
  formato JSON, multiplicando o ritmo.

O TYATT não precisa de esperar pelos 50.000 para ter valor: com alguns milhares
de artigos completos nas áreas mais procuradas, já é a melhor biblioteca
offline académica em português para os PALOP. Construímos o sistema, semeamos o
padrão, e crescemos por área, com qualidade a não negociar.
