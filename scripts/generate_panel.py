#!/usr/bin/env python3
"""
Genera index.html (el Panel de Herramientas) escaneando las carpetas del
repositorio. Cualquier carpeta en la raíz que tenga un index.html adentro
se incluye automáticamente como una tarjeta.

Para personalizar el título, descripción, categoría, etiqueta o color de
una tarjeta, agrega un archivo "meta.json" dentro de esa misma carpeta:

    {
      "title": "Nombre del proyecto",
      "description": "Breve descripción.",
      "category": "Nombre de la sección",
      "tag": "Dashboard",
      "accent": "purple"   // purple | magenta | teal
    }

Si una carpeta no tiene meta.json, se usa el nombre de la carpeta como
título por defecto, sin descripción, en la categoría "Otros proyectos".

Este script se ejecuta automáticamente en cada push via GitHub Actions
(ver .github/workflows/update-panel.yml). No hace falta correrlo a mano.
"""
import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {".git", ".github", "scripts", "assets", "node_modules"}
OUTPUT_PATH = os.path.join(REPO_ROOT, "index.html")
LOGO_PATH = "./assets/iungo-logo.png"


def load_meta(folder_path, folder_name):
    meta_path = os.path.join(folder_path, "meta.json")
    if os.path.exists(meta_path):
        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)
    else:
        meta = {}
    meta.setdefault("title", folder_name.replace("-", " ").title())
    meta.setdefault("description", "")
    meta.setdefault("category", "Otros proyectos")
    meta.setdefault("tag", "Proyecto")
    meta.setdefault("accent", "purple")
    meta["url"] = "./{}/".format(folder_name)
    return meta


def discover_projects():
    projects = []
    for entry in sorted(os.listdir(REPO_ROOT)):
        if entry in EXCLUDE_DIRS or entry.startswith("."):
            continue
        full_path = os.path.join(REPO_ROOT, entry)
        if not os.path.isdir(full_path):
            continue
        if not os.path.exists(os.path.join(full_path, "index.html")):
            continue
        projects.append(load_meta(full_path, entry))
    return projects


TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Panel de Tableros y Procesos — iUNGO</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root{{
    --purple:#623F82;
    --purple-dark:#3E2854;
    --purple-soft:#EFEAF4;
    --magenta:#852D81;
    --magenta-soft:#F7E9F5;
    --teal:#1EAAC6;
    --teal-soft:#E4F6FA;
    --bg:#F5F5F8;
    --card:#FFFFFF;
    --text:#22242E;
    --text-muted:#6B6D7C;
    --border:#E3E2E9;
  }}
  *{{box-sizing:border-box;}}
  body{{margin:0;background:var(--bg);color:var(--text);font-family:'Source Sans 3',Arial,sans-serif;font-size:14px;line-height:1.4;}}
  h1,h2,h3,.brand-font{{font-family:'Montserrat',Arial,sans-serif;}}

  header.topbar{{
    background:var(--purple);color:#fff;padding:26px 32px;
    display:flex;align-items:center;gap:16px;border-bottom:4px solid var(--teal);
  }}
  header.topbar img.logo{{height:42px;width:auto;background:#fff;border-radius:6px;padding:5px 10px;}}
  header.topbar .title h1{{margin:0;font-size:22px;font-weight:700;}}
  header.topbar .title p{{margin:4px 0 0;font-size:13px;color:#E4D9EE;}}

  main{{max-width:1100px;margin:0 auto;padding:36px 24px 60px;}}

  .section{{margin-bottom:36px;}}
  .section h2{{
    font-size:13px;text-transform:uppercase;letter-spacing:.6px;color:var(--text-muted);
    font-weight:700;margin:0 0 14px;padding-bottom:8px;border-bottom:1px solid var(--border);
  }}

  .grid{{display:grid;grid-template-columns:repeat(auto-fill, minmax(260px, 1fr));gap:16px;}}

  .card{{
    background:var(--card);border:1px solid var(--border);border-radius:10px;padding:20px;
    display:flex;flex-direction:column;gap:10px;text-decoration:none;color:inherit;
    transition:.15s;position:relative;overflow:hidden;
  }}
  .card:hover{{border-color:var(--purple);box-shadow:0 6px 18px rgba(98,63,130,.14);transform:translateY(-2px);}}
  .card .tag{{
    align-self:flex-start;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;
    padding:3px 9px;border-radius:20px;background:var(--purple-soft);color:var(--purple);
  }}
  .card.accent-magenta .tag{{background:var(--magenta-soft);color:var(--magenta);}}
  .card.accent-teal .tag{{background:var(--teal-soft);color:#0F7A90;}}
  .card h3{{margin:0;font-size:16px;font-weight:700;color:var(--text);}}
  .card p{{margin:0;font-size:13px;color:var(--text-muted);flex-grow:1;}}
  .card .cta{{
    font-size:13px;font-weight:700;color:var(--purple);display:flex;align-items:center;gap:6px;margin-top:4px;
  }}
  .card:hover .cta{{color:var(--magenta);}}
  .card .cta svg{{transition:.15s;}}
  .card:hover .cta svg{{transform:translateX(3px);}}

  footer{{text-align:center;color:var(--text-muted);font-size:11px;padding:20px 24px 30px;}}

  .empty-state{{color:var(--text-muted);font-size:13px;padding:20px;text-align:center;border:1px dashed var(--border);border-radius:10px;}}
</style>
</head>
<body>

<header class="topbar">
  <img class="logo" src="{logo_path}" alt="iUNGO">
  <div class="title">
    <h1>Panel de Tableros y Procesos</h1>
    <p>iUNGO — Finanzas y Contabilidad</p>
  </div>
</header>

<main>
{sections_html}
</main>

<footer>Este panel se genera y actualiza automáticamente vía GitHub Actions · iUNGO F&amp;A</footer>

</body>
</html>
"""

ARROW_SVG = '<svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7h8M8 3l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def render_card(p):
    accent_class = ""
    if p["accent"] == "magenta":
        accent_class = " accent-magenta"
    elif p["accent"] == "teal":
        accent_class = " accent-teal"
    return """
            <a class="card{accent_class}" href="{url}">
              <span class="tag">{tag}</span>
              <h3>{title}</h3>
              <p>{description}</p>
              <span class="cta">Abrir {arrow}</span>
            </a>""".format(
        accent_class=accent_class,
        url=p["url"],
        tag=p["tag"],
        title=p["title"],
        description=p["description"],
        arrow=ARROW_SVG,
    )


def render_sections(projects):
    if not projects:
        return '  <div class="empty-state">Aún no hay proyectos cargados.</div>'
    categories = []
    for p in projects:
        if p["category"] not in categories:
            categories.append(p["category"])
    sections = []
    for cat in categories:
        items = [p for p in projects if p["category"] == cat]
        cards_html = "".join(render_card(p) for p in items)
        sections.append(
            '  <div class="section">\n    <h2>{cat}</h2>\n    <div class="grid">{cards}\n    </div>\n  </div>'.format(
                cat=cat, cards=cards_html
            )
        )
    return "\n\n".join(sections)


def main():
    projects = discover_projects()
    html = TEMPLATE.format(
        logo_path=LOGO_PATH,
        sections_html=render_sections(projects),
    )
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("Panel generado con {} proyecto(s): {}".format(
        len(projects), ", ".join(p["title"] for p in projects)
    ))


if __name__ == "__main__":
    main()
