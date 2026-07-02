#!/usr/bin/env python3
"""Gera o ficheiro tyatt_pt.zim a partir dos artigos em conteudo/artigos/*.json.

Uso:  python3 ferramentas/gerar_zim.py [saida.zim]
Requisitos:  pip install libzim
"""
import json
import math
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

from libzim.writer import Creator, Item, StringProvider, Hint

# ── Motor de pesquisa: tokenização partilhada com o assistente (JS) ──────────
# A mesma normalização tem de existir dos dois lados, senão a pesquisa falha.
STOPWORDS = set(
    "de da do das dos e a o as os um uma uns umas em no na nos nas por para com que "
    "se ao aos ou mas mais muito pouco nao sim ja la aqui ali isto isso aquilo este "
    "esta esse essa aquele aquela seu sua seus suas meu minha teu tua nosso nossa dele "
    "dela deles delas qual quais quem quando onde quanto quanta quantos quantas porque "
    "como ser sao foi era eram sendo tem ter ha haver estar esta estao me te lhe nos vos "
    "sobre entre ate desde apos contra sob eu tu ele ela nos eles elas ser tambem".split()
)


def _normalizar(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", s)


def _stem(t):
    return t[:-1] if len(t) > 4 and t.endswith("s") else t


def _tokens(s):
    return [_stem(t) for t in _normalizar(s).split() if len(t) >= 2 and t not in STOPWORDS]

RAIZ = Path(__file__).resolve().parent.parent
PASTA_ARTIGOS = RAIZ / "conteudo" / "artigos"
SAIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "tyatt_pt.zim"


def caminho_de(artigo):
    """Caminho ZIM do artigo: id se existir, senão o título transliterado."""
    bruto = artigo.get("id") or artigo["titulo"]
    limpo = unicodedata.normalize("NFD", bruto).encode("ascii", "ignore").decode()
    limpo = re.sub(r"[^A-Za-z0-9]+", "_", limpo).strip("_")
    return limpo or "artigo"


ARTIGOS_INICIAIS = ("a ", "o ", "as ", "os ", "um ", "uma ", "uns ", "umas ")


def aliases_de(artigo):
    """Atalhos de pesquisa de um artigo: os aliases declarados mais variantes
    automáticas do título — sem o artigo inicial e sem o subtítulo — para que
    títulos como «A Separação de Poderes no Estado de Direito» sejam
    encontrados por «separação de poderes»."""
    atalhos = list(artigo.get("aliases", []))
    titulo = artigo["titulo"]
    variantes = {titulo}
    # parte principal, antes de um separador de subtítulo
    principal = re.split(r"\s+[—:–-]\s+", titulo, maxsplit=1)[0]
    variantes.add(principal)
    for v in list(variantes):
        baixo = v.lower()
        for art in ARTIGOS_INICIAIS:
            if baixo.startswith(art):
                atalhos.append(v[len(art):])
                break
    return atalhos


def paragrafos_html(texto):
    return "".join(f"<p>{p.strip()}</p>" for p in texto.split("\n") if p.strip())


def html_de(artigo):
    """Renderiza um artigo em HTML. Suporta dois formatos:
    - simples: campo 'corpo' com o texto todo;
    - académico: 'resumo', 'palavras_chave', 'seccoes'[] e 'referencias'[].
    O primeiro conteúdo visível (resumo ou 1.º parágrafo) é a resposta direta
    que o assistente lê, por isso vem sempre no topo.
    """
    partes = [f"<h1>{artigo['titulo']}</h1>"]
    area = artigo.get("area") or artigo.get("categoria", "")
    nivel = artigo.get("nivel")
    cabecalho = f"Área: {area}" + (f" · Nível: {nivel}" if nivel else "")
    partes.append(f"<p><i>{cabecalho}</i></p>")

    if artigo.get("tipo") == "academico":
        if artigo.get("resumo"):
            partes.append("<h2>Resumo</h2>" + paragrafos_html(artigo["resumo"]))
        if artigo.get("palavras_chave"):
            chaves = ", ".join(artigo["palavras_chave"])
            partes.append(f"<p><b>Palavras-chave:</b> {chaves}</p>")
        for seccao in artigo.get("seccoes", []):
            partes.append(f"<h2>{seccao['titulo']}</h2>" + paragrafos_html(seccao["corpo"]))
        if artigo.get("referencias"):
            itens = "".join(f"<li>{r}</li>" for r in artigo["referencias"])
            partes.append(f"<h2>Referências e leituras recomendadas</h2><ul>{itens}</ul>")
    else:
        partes.append(paragrafos_html(artigo["corpo"]))

    return (
        "<html><head><meta charset='utf-8'>"
        f"<title>{artigo['titulo']}</title></head><body>"
        + "".join(partes)
        + "<hr><p><small>TYATT — conteúdo original, offline.</small></p>"
        "</body></html>"
    )


def campos_pesados(artigo):
    """Devolve pares (texto, peso) de um artigo para o índice de texto completo.
    O título, a área e as palavras-chave pesam mais do que o corpo, para que
    um artigo cujo TEMA é a pergunta suba acima de outro que só a menciona."""
    pares = [(artigo["titulo"], 6)]
    pares.append((artigo.get("area") or artigo.get("categoria", ""), 3))
    for alias in aliases_de(artigo):
        pares.append((alias, 4))
    if artigo.get("tipo") == "academico":
        pares.append((" ".join(artigo.get("palavras_chave", [])), 5))
        pares.append((artigo.get("resumo", ""), 3))
        for seccao in artigo.get("seccoes", []):
            pares.append((seccao.get("titulo", ""), 3))
            pares.append((seccao.get("corpo", ""), 1))
    else:
        pares.append((artigo.get("corpo", ""), 1))
    return pares


def construir_indice(artigos):
    """Índice invertido com pesos por campo, para pesquisa por texto completo
    (ranking BM25 no assistente). Formato compacto:
    { N, avgdl, d:[[caminho,titulo,area,dl],...], p:{ termo:[[docId,tf],...] } }"""
    docs, postings, comprimentos = [], {}, []
    for doc_id, artigo in enumerate(artigos):
        tf = {}
        for texto, peso in campos_pesados(artigo):
            for termo in _tokens(texto):
                tf[termo] = tf.get(termo, 0) + peso
        dl = sum(tf.values()) or 1
        comprimentos.append(dl)
        docs.append([
            caminho_de(artigo),
            artigo["titulo"],
            artigo.get("area") or artigo.get("categoria", ""),
            dl,
        ])
        for termo, freq in tf.items():
            postings.setdefault(termo, []).append([doc_id, freq])
    avgdl = sum(comprimentos) / len(comprimentos) if comprimentos else 1
    return {"N": len(docs), "avgdl": round(avgdl, 2), "d": docs, "p": postings}


class IndiceItem(Item):
    """Guarda o índice de texto completo dentro do próprio ZIM, num caminho
    conhecido, fora da lista de artigos (não é um artigo pesquisável)."""

    def __init__(self, indice):
        super().__init__()
        self.dados = json.dumps(indice, ensure_ascii=False, separators=(",", ":"))

    def get_path(self):
        return "tyatt_indice_texto"

    def get_title(self):
        return ""

    def get_mimetype(self):
        return "application/json"

    def get_contentprovider(self):
        return StringProvider(self.dados)

    def get_hints(self):
        return {Hint.FRONT_ARTICLE: False}


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

        # índice de texto completo embutido (pesquisa inteligente do assistente)
        c.add_item(IndiceItem(construir_indice(artigos)))

        # aliases → redirecionamentos (como as redireções da Wikipédia):
        # permitem que termos populares ("tensão alta") ou o título sem o artigo
        # inicial ("Separação de Poderes...") encontrem o artigo. O assistente
        # segue-os automaticamente.
        redirecoes, caminhos = 0, set(caminho_de(a) for a in artigos)
        for artigo in artigos:
            destino = caminho_de(artigo)
            for alias in aliases_de(artigo):
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
