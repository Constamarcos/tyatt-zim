# Como ligar o modelo de IA à tomada do assistente

O assistente (`assistente.html`) já tem a **tomada** onde o modelo semântico
encaixa. Sem modelo, usa o ranking BM25. Com modelo ligado, reordena os
candidatos por significado. Este guia explica como ligar o modelo — passos a
correr **no computador** (aqui na nuvem não é possível descarregar o modelo).

## A interface (já pronta no assistente)

```js
// ligar um modelo (chamado pela app Flutter/WebView ou por um <script>)
window.tyattLigarModelo({
  // recebe a pergunta e os candidatos do BM25; devolve-os reordenados
  async reordenar(pergunta, candidatos, zim) {
    // candidatos: [{ caminho, titulo, area, score, cobertos }, ...] (top 20)
    // devolver a mesma lista por ordem de relevância semântica
    return candidatos;
  }
});
window.tyattTemModelo();     // true/false
window.tyattDesligarModelo(); // volta ao BM25
```

Verificado: ligar um modelo muda a resposta; desligar volta ao BM25; sem
modelo, nada muda. A tomada é segura — se o modelo falhar, o assistente cai no
BM25 automaticamente.

## Modelo recomendado (Caminho A — re-ranker, não gera texto)

Um **cross-encoder multilingue** que pontua (pergunta, passagem). Opções de
licença aberta, com bom português:
- `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` (re-ranker multilingue), ou
- um **bi-encoder** tipo `intfloat/multilingual-e5-small` (embeddings) se
  preferires pré-calcular vetores dos artigos.

Quantizados a int8, ficam em ~100–300 MB e correm em **CPU via ONNX Runtime
Web (WASM)** — sem necessidade de WebGPU.

## Receita A — re-ranker (mais simples, sem mexer no ZIM)

1. **Exportar o modelo para ONNX** (no computador, uma vez):
   ```bash
   pip install optimum[onnxruntime] transformers
   optimum-cli export onnx \
     --model cross-encoder/mmarco-mMiniLMv2-L12-H384-v1 \
     --task text-classification modelo_onnx/
   # opcional: quantização int8 para ~1/4 do tamanho
   ```
2. **Incluir o ONNX Runtime Web** na app (ficheiro `ort.min.js` + `.wasm`).
3. **Ligar à tomada** — esboço do reordenador:
   ```js
   import * as ort from "./ort.min.js";
   const sessao = await ort.InferenceSession.create("modelo.onnx");
   const tokenizer = /* tokenizer do modelo, ex.: via transformers.js */;

   window.tyattLigarModelo({
     async reordenar(pergunta, candidatos, zim) {
       const pontuados = [];
       for (const c of candidatos) {
         // ler o resumo/primeiros parágrafos do artigo do ZIM
         const passagem = await lerResumoDoZim(zim, c.caminho); // usa zim.procurarCaminho + lerBlob
         const ent = tokenizer(pergunta, passagem);            // pergunta + passagem
         const saida = await sessao.run({ input_ids: ent.ids, attention_mask: ent.mask });
         c.scoreIA = saida.logits.data[0];
         pontuados.push(c);
       }
       return pontuados.sort((a, b) => b.scoreIA - a.scoreIA);
     }
   });
   ```
   Só se reordenam os ~20 candidatos do BM25 → poucas inferências por pergunta,
   rápido mesmo em CPU.

## Receita B — embeddings pré-calculados (cobre todo o acervo)

Para pesquisa semântica sobre **todos** os artigos (não só os 20 do BM25):
1. No `gerar_zim.py`, calcular um vetor por artigo com o bi-encoder e guardá-lo
   no ZIM (à semelhança do índice de texto). ~0,5–1 KB por artigo.
2. Na app, vetorizar só a pergunta e ordenar por produto interno com os vetores
   dos artigos. O modelo corre **uma vez por pergunta**.

## Integração com a app Flutter

O `assistente.html` corre dentro de um **WebView**. A app trata da parte
pesada e opcional:
- oferece o download único do modelo (~300 MB) e guarda-o no dispositivo;
- injeta o reordenador chamando `window.tyattLigarModelo(...)` a partir do
  WebView quando o utilizador ativa a «IA avançada»;
- sem modelo (ou em telemóveis fracos), o assistente funciona na mesma (BM25).

## Testar

Injetar um modelo de mentira (como no teste automático) confirma a tomada sem
precisar do modelo real:
```js
window.tyattLigarModelo({ reordenar: async (p, c) => c.slice().reverse() });
```
Depois, ligar o modelo real e comparar respostas em perguntas onde as palavras
do utilizador diferem das do artigo — é aí que o ganho semântico aparece.
