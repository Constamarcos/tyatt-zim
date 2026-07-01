# Tyatt — Base de conhecimento offline (ZIM)

Ficheiros distribuídos via Releases.

## TYATT Assistente (`assistente.html`)

Assistente inteligente **100% offline** alimentado pelo teu ficheiro **.zim**
(Wikipédia do Kiwix). Um único ficheiro HTML, sem dependências externas e sem
servidor: lê o ZIM diretamente no navegador, entende a pergunta e responde.

- **Entende perguntas em português**: «o que é…», «quem foi…», «quando…»,
  «onde fica…», «quantos…», «qual é a capital de…» — e extrai do artigo a
  frase que responde (ex.: para «quando», a frase com a data).
- **Leitor ZIM completo em JavaScript**: cabeçalho, índice de títulos
  (`listing/titleOrdered/v1`), redirecionamentos, clusters zstd — lê o
  ficheiro por fatias, nunca o carrega inteiro na memória (funciona com
  ficheiros de vários GB).
- **Pesquisa tolerante**: ignora acentos («malaria» encontra «Malária»),
  maiúsculas, e segue redirecionamentos («paludismo» → «Malária»).
- **Leitor de artigos integrado**: ligações internas continuam offline e as
  imagens são carregadas de dentro do próprio ZIM.

### Como usar

1. Descarrega o `assistente.html` (uma vez) e um ficheiro ZIM da Wikipédia em
   `download.kiwix.org/zim/wikipedia/`.
2. Abre o `assistente.html` no navegador, escolhe o teu `.zim` e pergunta.

### Variantes dos ficheiros ZIM (imagens!)

| Variante | Imagens | Conteúdo | Tamanho (PT) |
|----------|---------|----------|--------------|
| `maxi`   | ✅ sim  | artigos completos | ~12 GB |
| `nopic`  | ❌ não  | artigos completos | ~4 GB |
| `mini`   | ❌ não  | só a introdução de cada artigo | ~1 GB |

Se o teu ZIM «está sem imagens», é porque é `nopic` ou `mini` — para ter
imagens, descarrega a versão **maxi**.

## TYATT Pesquisa (`index.html`)

Sistema de pesquisa **100% offline** — um "Google sem internet". É um único
ficheiro HTML, sem dependências externas: depois de o teres no telefone ou
computador, cada pesquisa é feita localmente e **não gasta nenhum dado**.

### Como usar

1. Descarrega o ficheiro `index.html` (uma única vez).
2. Abre-o em qualquer navegador (Chrome, Firefox, etc.) — funciona mesmo em
   modo avião.
3. Escreve o que quiseres na caixa de pesquisa. A pesquisa ignora acentos,
   aceita palavras incompletas (ex.: «malar» encontra «malária») e ordena os
   resultados por relevância.

### Como acrescentar conteúdo

Há duas formas:

- **Editar o `index.html`**: acrescentar objetos à lista `ARTIGOS`, no formato
  `{id, titulo, categoria, corpo}`.
- **Criar um `conteudo.json`** ao lado do `index.html`, com uma lista de
  artigos no mesmo formato. Se o ficheiro existir, é carregado e indexado
  automaticamente (requer abrir a página através de um servidor, por exemplo
  `python3 -m http.server`; aberto diretamente como ficheiro, só o conteúdo
  embutido é usado).

Para a enciclopédia completa (Wikipedia em português), usa os ficheiros ZIM
das Releases com a app TYATT ou com o [Kiwix](https://kiwix.org).
