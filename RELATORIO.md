# TYATT — Relatório de progresso

_Atualizado em 2026-07-02. Branch: `claude/offline-search-system-4d64aq`._

## Em uma frase

O TYATT já é um **assistente de conhecimento 100% offline** que lê ficheiros
`.zim`, entende perguntas em português, procura em todo o texto e responde —
sem gastar internet.

## Componentes entregues

| Componente | Ficheiro | Estado |
|-----------|----------|--------|
| Assistente inteligente (lê ZIM + motor de resposta) | `assistente.html` | ✅ funcional |
| Pesquisa offline simples (conteúdo embutido) | `index.html` | ✅ funcional |
| Gerador de ZIM próprio (+ índice de texto) | `ferramentas/gerar_zim.py` | ✅ funcional |
| Base de conteúdo (planos + artigos) | `conteudo/` | 🟡 em crescimento |

## Motor do assistente — o que já sabe fazer

- **Lê o formato ZIM em JavaScript**, por fatias (funciona com ficheiros de
  vários GB, sem carregar tudo na memória); descomprime clusters zstd.
- **Abre por ficheiro ou por pasta** (encontra o `.zim` sozinho numa pasta).
- **Pesquisa por texto completo** com ranking BM25: encontra por qualquer
  palavra do corpo, não só do título (ex.: «mosquiteira» → Malária).
- **Compreende a pergunta**: remove palavras vazias, reduz a raízes (stemming
  PT), expande sinónimos, deteta o tipo (o que é / quando / onde / quanto).
- **Auto-questiona-se**: mede confiança e ambiguidade — responde direto quando
  seguro, pergunta «ou querias saber sobre…» quando ambíguo, e assume «o mais
  próximo que encontrei é…» quando o match é fraco (nunca inventa).
- **Leitor de artigos** com secções, imagens vindas do próprio ZIM e ligações
  internas offline.
- **Compatível com Wikipedia** (ZIM sem o nosso índice → pesquisa por título).

## Conteúdo

- **37 artigos completos** escritos de raiz (conteúdo original, sem problemas
  de direitos de autor):
  - 29 de Saúde (primeiros socorros e doenças principais);
  - 8 académicos completos (Direito, Gestão, Enfermagem, Economia,
    Contabilidade, Psicologia, Informática), com resumo, introdução,
    desenvolvimento, conclusão e referências reais.
- **4.822 títulos planeados** em 16 categorias práticas (`conteudo/plano.md`).
- **Programa académico** para os campos mais estudados nos PALOP
  (`conteudo/plano-academico.md`).
- Empacotados, dão um `tyatt_pt.zim` de ~210 KB (37 artigos + 81 atalhos +
  índice de pesquisa). Texto comprimido é leve: milhares de artigos cabem em
  poucos MB.

## Qualidade / testes

Todo o motor é verificado de ponta a ponta num navegador real (Chromium),
com 8 conjuntos de testes automáticos: leitura do ZIM, pesquisa por título,
pesquisa por texto completo, aliases/atalhos, artigos académicos, deteção em
pasta, escala (30 mil artigos < 350 ms) e o conteúdo real do TYATT.

## Limitações honestas

- O assistente **recupera e extrai** — não **gera** texto novo. Se a resposta
  não existir em nenhum artigo, di-lo (não inventa). Quanto mais artigos,
  mais perguntas resolve.
- A meta de milhares de artigos é um **programa contínuo** (geração + revisão
  por docentes), não uma única tarefa.
- A pesquisa semântica por significado (não só por palavras) depende de um
  modelo opcional — ver `conteudo/plano-modelo-ia.md`.

## Próximos passos possíveis

1. **Modelo de IA opcional (~300 MB)** para casar significado da pergunta com o
   conteúdo — desenho técnico em `conteudo/plano-modelo-ia.md`.
2. **Mais artigos** (práticos e académicos), por prioridade dos planos.
3. **Navegação por área/nível** e modo estudante no assistente.
4. **Pipeline de submissão** para docentes/colaboradores contribuírem.
