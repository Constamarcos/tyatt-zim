#!/usr/bin/env python3
"""Gera o ficheiro tyatt_pt.zim a partir dos artigos em conteudo/artigos/*.json.

Uso:  python3 ferramentas/gerar_zim.py [saida.zim]
Requisitos:  pip install libzim
"""
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

from libzim.writer import Creator, Item, StringProvider, Hint

RAIZ = Path(__file__).resolve().parent.parent
PASTA_ARTIGOS = RAIZ / "conteudo" / "artigos"
SAIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "tyatt_pt.zim"


def caminho_de(artigo):
    """Caminho ZIM do artigo: id se existir, senão o título transliterado."""
    bruto = artigo.get("id") or artigo["titulo"]
    limpo = unicodedata.normalize("NFD", bruto).encode("ascii", "ignore").decode()
    limpo = re.sub(r"[^A-Za-z0-9]+", "_", limpo).strip("_")
    return limpo or "artigo"


def html_de(artigo):
    paragrafos = "".join(
        f"<p>{p.strip()}</p>" for p in artigo["corpo"].split("\n") if p.strip()
    )
    return (
        "<html><head><meta charset='utf-8'>"
        f"<title>{artigo['titulo']}</title></head><body>"
        f"<h1>{artigo['titulo']}</h1>"
        f"<p><i>Categoria: {artigo['categoria']}</i></p>"
        f"{paragrafos}"
        "<hr><p><small>TYATT — conteúdo original, offline.</small></p>"
        "</body></html>"
    )


class ArtigoItem(Item):
    def __init__(self, artigo):
        super().__init__()
        self.artigo = artigo

    def get_path(self):
        return caminho_de(self.artigo)

    def get_title(self):
        return self.artigo["titulo"]

    def get_mimetype(self):
        return "text/html"

    def get_contentprovider(self):
        return StringProvider(html_de(self.artigo))

    def get_hints(self):
        return {Hint.FRONT_ARTICLE: True}


def principal():
    artigos, vistos = [], set()
    for ficheiro in sorted(PASTA_ARTIGOS.glob("*.json")):
        for artigo in json.loads(ficheiro.read_text(encoding="utf-8")):
            caminho = caminho_de(artigo)
            if caminho in vistos:
                print(f"AVISO: id repetido ignorado: {caminho} ({ficheiro.name})")
                continue
            vistos.add(caminho)
            artigos.append(artigo)

    if not artigos:
        sys.exit("Nenhum artigo encontrado em conteudo/artigos/")

    with Creator(str(SAIDA)).config_indexing(True, "por") as c:
        c.set_mainpath(caminho_de(artigos[0]))
        c.add_metadata("Title", "TYATT — Conhecimento offline")
        c.add_metadata("Language", "por")
        c.add_metadata("Creator", "Osendre Comércio e Serviços Lda")
        c.add_metadata("Publisher", "TYATT")
        c.add_metadata("Date", date.today().isoformat())
        c.add_metadata("Description", "Base de conhecimento original TYATT em português")
        for artigo in artigos:
            c.add_item(ArtigoItem(artigo))

        # aliases → redirecionamentos (como as redireções da Wikipédia):
        # permitem que termos populares ("tensão alta") encontrem o artigo
        # ("Hipertensão"). O assistente segue-os automaticamente.
        redirecoes, caminhos = 0, set(caminho_de(a) for a in artigos)
        for artigo in artigos:
            destino = caminho_de(artigo)
            for alias in artigo.get("aliases", []):
                origem = unicodedata.normalize("NFD", alias).encode("ascii", "ignore").decode()
                origem = re.sub(r"[^A-Za-z0-9]+", "_", origem).strip("_")
                if origem and origem not in caminhos:
                    caminhos.add(origem)
                    c.add_redirection(origem, alias, destino, {Hint.FRONT_ARTICLE: True})
                    redirecoes += 1

    tamanho = SAIDA.stat().st_size
    print(f"{SAIDA.name}: {len(artigos)} artigos + {redirecoes} atalhos, {tamanho/1024:.0f} KB")


if __name__ == "__main__":
    principal()
