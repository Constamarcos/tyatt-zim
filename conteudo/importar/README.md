# Pasta de importação de HTML

Coloca aqui ficheiros `.html` (ou `.htm`) para os trazer ao ZIM do TYATT
sem ter de os reescrever à mão. Serve para conteúdos que já tens guardados
em HTML: páginas geradas por IA (`deepseek_html_*.html`), artigos exportados,
notas, etc.

## Como usar

1. Copia os teus ficheiros `.html` para dentro desta pasta
   (`conteudo/importar/`).
2. Corre a ferramenta de importação:

   ```
   python3 ferramentas/importar_html.py --categoria "Geral" --saida importados-lote-01.json
   ```

   Podes primeiro **conferir** sem gravar nada, usando `--rever`:

   ```
   python3 ferramentas/importar_html.py --rever
   ```

3. A ferramenta cria `conteudo/artigos/importados-lote-01.json` com os artigos
   extraídos (título + texto). Ids repetidos com artigos já existentes são
   ignorados, para não duplicar.
4. Gera o ZIM atualizado:

   ```
   python3 ferramentas/gerar_zim.py
   ```

## O que a ferramenta faz

- Extrai o **título** do primeiro `<h1>`; se não houver, do `<title>`; se
  ainda assim não houver, do nome do ficheiro.
- Extrai o **texto** dos parágrafos, títulos e listas, ignorando scripts,
  estilos e menus.
- Salta ficheiros com texto muito curto (menos de 200 caracteres) — quase
  sempre não são artigos reais.

## Nota

Os `.html` colocados aqui **não** entram no ZIM diretamente — são apenas a
fonte. O que entra no ZIM é o JSON gerado em `conteudo/artigos/`. Depois de
importar, podes apagar os `.html` desta pasta se quiseres.
