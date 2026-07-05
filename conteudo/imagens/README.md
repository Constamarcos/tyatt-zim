# Imagens dos artigos (offline)

Coloca aqui imagens para os artigos. O nome do ficheiro deve ser o **id do
artigo** (o mesmo `id` do JSON), com extensão `.webp` (recomendado), `.png`
ou `.jpg`. Exemplos:

```
conteudo/imagens/angola.webp
conteudo/imagens/malaria.webp
conteudo/imagens/provincia-do-huambo.webp
```

Ao gerar o ZIM (`python3 ferramentas/gerar_zim.py`), cada imagem cujo nome
coincida com o id de um artigo é **embutida no ZIM** e mostrada:
- no cartão de resposta do assistente;
- no topo do artigo completo.

Tudo funciona **offline** — a imagem já vai dentro do ficheiro, não gasta dados.

## Formato

- **`.webp`** é o ideal: boa qualidade com ficheiros pequenos.
- Miniaturas (largura ~400–800 px) chegam para o ecrã e mantêm o ZIM leve.

## ⚠️ Direitos de autor (produto pago)

Usa apenas imagens com **licença livre** (ex.: Wikimedia Commons com licença
aberta, domínio público, ou próprias). **Evita** cartazes de filmes/séries,
capas de álbum e logótipos comerciais — são material protegido e não podem ser
distribuídos num produto pago, mesmo que apareçam na Wikipédia (aí estão ao
abrigo de «uso legítimo», que não se aplica à redistribuição).

Prioriza imagens dos temas do TYATT: Angola (províncias, cultura, história),
saúde, ciências, agricultura.
