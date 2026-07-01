# Tyatt — Base de conhecimento offline (ZIM)

Ficheiros distribuídos via Releases.

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
