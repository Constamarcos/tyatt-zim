# Modelo de IA opcional (~300 MB) — desenho técnico

## A pergunta

É possível juntar ao TYATT um modelo de IA (~300 MB, descarregado à parte,
opcional) que "compare o que o motor encontrou com a pergunta do utilizador" e
escolha/entregue a melhor resposta?

**Resposta: sim, é possível — e é uma excelente ideia.** Mas há uma escolha
técnica que decide se corre bem em telemóveis baratos ou se falha. Há dois
tipos de modelo muito diferentes que cabem em ~300 MB.

## Os dois caminhos (e qual escolher)

### Caminho A — Modelo que COMPREENDE (recomendado) ✅

Um **re-ranker / modelo de embeddings** (bi-encoder ou cross-encoder). Não
escreve texto: lê a pergunta e cada resultado candidato e dá uma **pontuação de
relevância por significado** — exatamente "comparar o que encontrou com o que
foi perguntado". Resolve o caso em que o utilizador usa palavras diferentes das
do artigo (ex.: «fico com febre e arrepios ao fim da tarde» → Malária, mesmo
sem partilhar palavras-chave).

- **Tamanho**: modelos multilingues tipo MiniLM / E5-small quantizados a int8
  ≈ 100–130 MB (embeddings); cross-encoder de re-ranking ≈ 100–300 MB. Cabe.
- **Onde corre**: CPU, via ONNX Runtime Web (WebAssembly). **Não precisa de
  WebGPU** — funciona em telemóveis baratos e em navegadores antigos.
- **Segurança**: é **determinístico e não alucina** — seleciona e pontua texto
  real, nunca inventa factos. Ideal para conteúdo de saúde e académico.
- **Português**: os modelos multilingues lidam bem com PT.

### Caminho B — Modelo que ESCREVE (arriscado) ⚠️

Um **LLM generativo** (tipo ChatGPT em miniatura). Em 300 MB só cabe um modelo
minúsculo (~0,5 mil milhões de parâmetros, 4-bit).

- **Problema 1 — alucinação**: modelos pequenos inventam factos com confiança.
  Num produto pago de saúde e ensino, isso é perigoso e destrói a credibilidade.
- **Problema 2 — hardware**: para velocidade aceitável precisa de WebGPU, que
  falta em muitos telemóveis baratos e Android antigos; em CPU é lento.
- **Conclusão**: a geração de texto não deve ser a base do TYATT. Pode existir,
  no futuro, como camada avançada e claramente opcional — nunca para factos.

**Recomendação: seguir o Caminho A.** Dá o salto de qualidade que o utilizador
quer ("comparar significado"), corre em telemóveis reais, e mantém a promessa
do TYATT: respostas de confiança, sem inventar.

## Arquitetura híbrida (como os motores de busca reais funcionam)

Modelo de "recuperar e depois reordenar" (_retrieve-then-rerank_):

1. **BM25** (já construído, 0 MB extra, sempre ativo) devolve rapidamente os
   ~20 melhores candidatos de todo o ZIM.
2. **Se o modelo estiver instalado**, o re-ranker reordena esses 20 pela
   proximidade de **significado** à pergunta, escolhe o verdadeiro melhor e pode
   extrair a frase-resposta exata (QA extrativo).
3. Resposta entregue com alta confiança.

Opção mais poderosa: pré-calcular um **vetor (embedding) por artigo** ao gerar
o ZIM (guardado como o índice de texto; ~0,5–1 KB por artigo → 50 000 artigos
≈ 25–50 MB). Assim a pesquisa por significado cobre **todo** o acervo, não só os
20 do BM25. O modelo de 300 MB corre uma vez por pergunta (para vetorizar a
pergunta), não sobre todos os artigos.

## Camadas (o "opcional com grande vantagem")

| Camada | Tamanho extra | Quem beneficia |
|--------|---------------|----------------|
| Base — BM25 + extração | 0 MB | todos, em qualquer telemóvel |
| **Cérebro semântico** (re-ranker/embeddings) | ~150–300 MB (opcional) | quem descarrega: respostas por significado |
| Geração de texto (futuro, avançado) | +MB, WebGPU | flag experimental, nunca para factos |

O modelo descarrega-se **uma vez** (como o ZIM) e pode espalhar-se por cartão SD
ou Bluetooth, sem gastar mais internet.

## Como se liga ao que já existe

O assistente já tem o passo de **recuperação** (BM25) e um ponto natural de
extensão: a função que ordena os resultados. Basta inserir aí um
**reordenador opcional** que, se o modelo estiver carregado, repontua os
candidatos. Sem modelo, tudo funciona como agora. Componentes a acrescentar:

- **ONNX Runtime Web** (WASM, alguns MB) incluído na app.
- **Ficheiro do modelo** (~150–300 MB) carregado do dispositivo (ficheiro
  escolhido pelo utilizador ou guardado em OPFS/IndexedDB).
- **Precompute de embeddings** no `gerar_zim.py` (opcional), guardados no ZIM.
- **Hook de reordenação** no `assistente.html` (interface já preparável).

## Restrições honestas

- Download único de ~300 MB é um custo real, mas só uma vez, e partilhável
  offline (SD/Bluetooth) como o ZIM.
- Primeira utilização mais lenta (inicialização do modelo).
- Memória: ~300–500 MB de RAM durante a inferência — confortável em telemóveis
  médios, apertado em aparelhos muito fracos (1 GB) — daí ser **opcional**.
- É preciso obter/validar o modelo (licença aberta, multilingue) e testar em
  aparelhos reais antes de distribuir.

## Recomendação final

Construir o **Caminho A em arquitetura híbrida**: manter o BM25 como base
universal e oferecer o "cérebro semântico" (~150–300 MB) como descarga opcional
que reordena por significado e extrai a resposta exata. É o que dá ao TYATT a
sensação de IA verdadeira, sem alucinações e a correr no telemóvel do dia a dia.
