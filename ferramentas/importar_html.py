#!/usr/bin/env python3
"""Importa ficheiros HTML para o formato de artigo TYATT.

Lê todos os .html de uma pasta (por omissão conteudo/importar/), extrai o
título e o texto de cada um, e gera um ficheiro de artigos em
conteudo/artigos/ pronto a entrar no ZIM (via gerar_zim.py).

Serve para trazer conteúdos guardados em HTML — páginas geradas por IA
(deepseek_html_*.html), notas, artigos exportados — sem os copiar à mão.

Uso:
    python3 ferramentas/importar_html.py [pasta_html] [--saida nome-lote.json]
                                          [--categoria "Categoria"]

O tokenizador e o formato são os mesmos que gerar_zim.py já entende
(formato simples: {id, titulo, categoria, corpo}). Os ids repetidos —
contra os artigos que já existem — são ignorados, para não duplicar.
"""
import argparse
import json
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA_ARTIGOS = RAIZ / "conteudo" / "artigos"
PASTA_IMPORTAR = RAIZ / "conteudo" / "importar"

# elementos cujo conteúdo nunca é texto do artigo
IGNORAR = {"script", "style", "head", "noscript", "svg", "nav", "footer",
           "header", "aside", "button", "form", "select", "option"}
# elementos de bloco: fecham um parágrafo (inserimos quebra de linha)
BLOCO = {"p", "br", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr",
         "section", "article", "blockquote", "ul", "ol", "table", "hr"}


class ExtratorHTML(HTMLParser):
    """Extrai o título e o texto corrido de um HTML, respeitando os blocos.

    Guarda o primeiro <h1> como título; se não houver, usa o <title>.
    Junta o texto visível, separando parágrafos nos limites de bloco.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ignora = 0          # profundidade dentro de elementos a ignorar
        self.em_titulo_tag = False
        self.em_h1 = False
        self.titulo_head = ""    # conteúdo de <title>
        self.titulo_h1 = ""      # conteúdo do 1.º <h1>
        self.partes = []         # texto acumulado

    def handle_starttag(self, tag, attrs):
        if tag in IGNORAR:
            self.ignora += 1
        elif tag == "title":
            self.em_titulo_tag = True
        elif tag == "h1" and not self.titulo_h1:
            self.em_h1 = True
        if tag in BLOCO:
            self.partes.append("\n")

    def handle_endtag(self, tag):
        if tag in IGNORAR and self.ignora > 0:
            self.ignora -= 1
        elif tag == "title":
            self.em_titulo_tag = False
        elif tag == "h1":
            self.em_h1 = False
        if tag in BLOCO:
            self.partes.append("\n")

    def handle_data(self, data):
        if self.ignora:
            return
        if self.em_titulo_tag:
            self.titulo_head += data
        if self.em_h1:
            self.titulo_h1 += data
        self.partes.append(data)

    def resultado(self):
        titulo = (self.titulo_h1 or self.titulo_head).strip()
        texto = "".join(self.partes)
        # normaliza espaços dentro de cada linha e colapsa linhas vazias
        linhas = [re.sub(r"[ \t]+", " ", l).strip() for l in texto.split("\n")]
        paragrafos = [l for l in linhas if l]
        # o <h1> foi apanhado como texto: se a 1.ª linha for o título, remove-a
        # (o renderizador do ZIM já mostra o título por cima do corpo)
        if paragrafos and titulo and paragrafos[0].strip() == titulo:
            paragrafos = paragrafos[1:]
        corpo = "\n".join(paragrafos)
        return titulo, corpo


def _slug(texto):
    limpo = unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode()
    limpo = re.sub(r"[^A-Za-z0-9]+", "-", limpo).strip("-").lower()
    return limpo or "artigo"


def _titulo_do_nome(caminho):
    """Título de recurso a partir do nome do ficheiro (para HTML sem <h1>)."""
    base = caminho.stem
    # nomes tipo deepseek_html_20260706_ab12cd não dão bom título
    if re.fullmatch(r"deepseek_html_\d+.*", base) or re.fullmatch(r"[0-9_]+", base):
        return ""
    return base.replace("_", " ").replace("-", " ").strip().capitalize()


def ids_existentes():
    """Todos os ids/slugs já presentes em conteudo/artigos/ (para não duplicar)."""
    ids = set()
    if not PASTA_ARTIGOS.is_dir():
        return ids
    for f in PASTA_ARTIGOS.glob("*.json"):
        try:
            for a in json.loads(f.read_text(encoding="utf-8")):
                bruto = a.get("id") or a.get("titulo", "")
                ids.add(_slug(bruto))
        except (json.JSONDecodeError, TypeError):
            print(f"AVISO: ignorei {f.name} (JSON inválido)")
    return ids


def importar(pasta, categoria):
    ficheiros = sorted(pasta.glob("*.html")) + sorted(pasta.glob("*.htm"))
    if not ficheiros:
        sys.exit(f"Nenhum .html encontrado em {pasta}")

    ja_existem = ids_existentes()
    artigos, vistos = [], set()
    saltados = {"curto": 0, "sem_titulo": 0, "duplicado": 0}

    for f in ficheiros:
        html = f.read_text(encoding="utf-8", errors="replace")
        extrator = ExtratorHTML()
        try:
            extrator.feed(html)
        except Exception as e:  # HTML malformado não deve parar tudo
            print(f"AVISO: erro a ler {f.name}: {e}")
            continue
        titulo, corpo = extrator.resultado()

        if not titulo:
            titulo = _titulo_do_nome(f)
        if not titulo:
            # usa a 1.ª linha do corpo como título, em último recurso
            primeira = corpo.split("\n", 1)[0] if corpo else ""
            titulo = primeira[:80].strip()
        if not titulo:
            saltados["sem_titulo"] += 1
            print(f"SALTADO (sem título): {f.name}")
            continue

        # corpo demasiado curto = provavelmente não é um artigo real
        if len(corpo) < 200:
            saltados["curto"] += 1
            print(f"SALTADO (curto, {len(corpo)} car.): {f.name} — «{titulo}»")
            continue

        ident = _slug(titulo)
        if ident in ja_existem or ident in vistos:
            saltados["duplicado"] += 1
            print(f"SALTADO (duplicado): {ident} — «{titulo}»")
            continue
        vistos.add(ident)

        artigos.append({
            "id": ident,
            "titulo": titulo,
            "categoria": categoria,
            "corpo": corpo,
            "_origem": f.name,   # rasto de onde veio (informativo)
        })
        print(f"OK: {f.name} → «{titulo}» ({len(corpo)} car.)")

    print(f"\n{len(artigos)} artigos importados; "
          f"saltados: {saltados['duplicado']} duplicados, "
          f"{saltados['curto']} curtos, {saltados['sem_titulo']} sem título.")
    return artigos


def main():
    ap = argparse.ArgumentParser(description="Importa HTML para artigos TYATT.")
    ap.add_argument("pasta", nargs="?", default=str(PASTA_IMPORTAR),
                    help="pasta com os ficheiros .html (por omissão conteudo/importar/)")
    ap.add_argument("--saida", default="importados-lote-01.json",
                    help="nome do ficheiro de artigos a criar em conteudo/artigos/")
    ap.add_argument("--categoria", default="Importado",
                    help="categoria a atribuir aos artigos importados")
    ap.add_argument("--rever", action="store_true",
                    help="mostra o resultado sem gravar (para conferir antes)")
    args = ap.parse_args()

    pasta = Path(args.pasta)
    if not pasta.is_dir():
        sys.exit(f"Pasta não encontrada: {pasta}\n"
                 f"Cria a pasta e coloca lá os .html, depois volta a correr.")

    artigos = importar(pasta, args.categoria)
    if not artigos:
        sys.exit("Nada para gravar.")

    if args.rever:
        for a in artigos:
            print(f"\n=== {a['titulo']} [{a['id']}] ===")
            print(a["corpo"][:300] + ("…" if len(a["corpo"]) > 300 else ""))
        print("\n(modo --rever: nada foi gravado)")
        return

    destino = PASTA_ARTIGOS / args.saida
    destino.write_text(
        json.dumps(artigos, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nGravado: {destino.relative_to(RAIZ)} ({len(artigos)} artigos)")
    print("Agora corre:  python3 ferramentas/gerar_zim.py")


if __name__ == "__main__":
    main()
