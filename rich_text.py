#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rich_text.py — Motor de Rich Text estilo Notion y Esquemas Canónicos de Bloques
Implementación pura en la biblioteca estándar de Python (html.parser, html, urllib.parse, re).

Soporta:
- Serialización y deserialización bidireccional de tuplas de texto enriquecido de Notion:
  [["Texto", [["b"], ["i"], ["_"], ["s"], ["c"], ["h", color], ["a", url], ["e", latex]]]]
- Extracción de texto plano (rich_text_to_plain_text)
- Envoltura de texto plano a tuplas (plain_text_to_rich_text)
- Conversión a HTML seguro con sanitización (rich_text_to_html)
- Conversión de HTML a tuplas Notion con pila de estilos (html_to_rich_text)
- Catálogo y validación canónica de los 17 tipos de bloques de Notion (+ sub_page)
"""

import re
import html
import uuid
import json
from html.parser import HTMLParser
from urllib.parse import urlparse

# -----------------------------------------------------------------------------
# Constantes de Decoradores y Colores
# -----------------------------------------------------------------------------

SUPPORTED_DECORATORS = {'b', 'i', '_', 's', 'c', 'h', 'a', 'e'}

VALID_COLORS = {
    'default', 'gray', 'brown', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'red',
    'gray_background', 'brown_background', 'orange_background', 'yellow_background',
    'green_background', 'teal_background', 'blue_background', 'purple_background', 'pink_background', 'red_background'
}

DANGEROUS_URL_SCHEMES = {'javascript', 'data', 'vbscript', 'file'}

# -----------------------------------------------------------------------------
# 1. Funciones de Conversión de Rich Text
# -----------------------------------------------------------------------------

def rich_text_to_plain_text(rich_text):
    """
    Extrae el texto plano limpio de la estructura de tuplas de Notion.
    Ejemplo: [["Hola ", [["b"]]], ["Mundo", []]] -> "Hola Mundo"
    Para ecuaciones en línea representadas con el token canónico "⁍" (U+204D):
      ["⁍", [["e", "formula"]]] -> extrae "formula".
    """
    if rich_text is None:
        return ""
    if isinstance(rich_text, str):
        return rich_text
    if not isinstance(rich_text, (list, tuple)):
        return str(rich_text)

    parts = []
    for segment in rich_text:
        if isinstance(segment, (list, tuple)) and len(segment) > 0:
            raw = str(segment[0] if segment[0] is not None else "")
            decs = segment[1] if len(segment) > 1 and isinstance(segment[1], (list, tuple)) else []
            eq_formula = None
            for d in decs:
                if isinstance(d, (list, tuple)) and len(d) > 0 and d[0] == 'e':
                    eq_formula = str(d[1]) if len(d) > 1 and d[1] is not None else raw
                    break
            if eq_formula is not None and (raw == '⁍' or raw == '\u204d'):
                parts.append(eq_formula)
            else:
                parts.append(raw)
        elif isinstance(segment, str):
            parts.append(segment)
        elif segment is not None:
            parts.append(str(segment))
    return "".join(parts)


def plain_text_to_rich_text(text):
    """
    Envuelve texto plano simple en el formato canónico de tuplas de Notion [[text, []]].
    Si text es None o vacío, devuelve [].
    """
    if text is None:
        return []
    text_str = str(text)
    if not text_str:
        return []
    return [[text_str, []]]


def rich_text_to_html(rich_text, sanitize=True):
    """
    Convierte tuplas de texto enriquecido de Notion a HTML estilizado y seguro.
    Decoradores soportados:
      ["b"]          -> <strong>...</strong>
      ["i"]          -> <em>...</em>
      ["_"]          -> <u>...</u>
      ["s"]          -> <s>...</s>
      ["c"]          -> <code>...</code>
      ["h", color]   -> <mark style="..." class="notion-color-{color}" data-color="{color}">...</mark>
      ["a", url]     -> <a href="{url}" target="_blank" rel="noopener noreferrer">...</a>
      ["e", latex]   -> <span class="inline-equation notion-inline-equation inline-katex-node" data-latex="{latex}" contenteditable="false">{latex}</span>
    """
    if not rich_text or not isinstance(rich_text, (list, tuple)):
        return ""

    output = []
    for segment in rich_text:
        if not isinstance(segment, (list, tuple)) or len(segment) == 0:
            continue

        raw_text = str(segment[0] if segment[0] is not None else "")
        decorators = segment[1] if len(segment) > 1 and isinstance(segment[1], (list, tuple)) else []

        # Comprobar si hay fórmula inline ["e", latex]
        has_equation = False
        eq_latex = ""
        for dec in decorators:
            if isinstance(dec, (list, tuple)) and len(dec) > 0 and dec[0] == 'e':
                has_equation = True
                eq_latex = str(dec[1]) if len(dec) > 1 and dec[1] is not None else (raw_text if raw_text not in ('⁍', '\u204d') else '')
                break

        if has_equation:
            escaped_latex = html.escape(eq_latex)
            token_attr = ' data-token="⁍"' if raw_text in ('⁍', '\u204d') else ''
            inner = f'<span class="inline-equation notion-inline-equation"{token_attr} data-latex="{escaped_latex}">{escaped_latex}</span>'
        else:
            inner = html.escape(raw_text)

        for dec in decorators:
            if not isinstance(dec, (list, tuple)) or len(dec) == 0:
                continue

            tag = str(dec[0])
            if tag == 'b':
                inner = f"<strong>{inner}</strong>"
            elif tag == 'i':
                inner = f"<em>{inner}</em>"
            elif tag == '_':
                inner = f"<u>{inner}</u>"
            elif tag == 's':
                inner = f"<s>{inner}</s>"
            elif tag == 'c':
                inner = f"<code>{inner}</code>"
            elif tag == 'h':
                color = str(dec[1]) if len(dec) > 1 and dec[1] is not None else 'yellow'
                color_str = color.strip()
                color_lower = color_str.lower()
                clean_color = re.sub(r'[^a-zA-Z0-9_\-]', '', color_lower)

                if clean_color in VALID_COLORS:
                    pass
                else:
                    # If color contains invalid characters or arbitrary CSS strings,
                    # extract the leading valid color token from VALID_COLORS
                    token = re.split(r'[^a-z0-9_]', color_lower)[0] if color_lower else ''
                    if token in VALID_COLORS:
                        clean_color = token
                    else:
                        # Fallback safely to 'yellow' / 'yellow_background'
                        if clean_color.endswith('_background') or color_lower.endswith('_background') or token.endswith('_background'):
                            clean_color = 'yellow_background'
                        else:
                            clean_color = 'yellow'

                if clean_color.endswith('_background'):
                    base_bg = clean_color.replace('_background', '')
                    style_attr = f'background-color: {base_bg};'
                else:
                    style_attr = f'color: {clean_color};'
                inner = f'<mark style="{style_attr}" class="notion-color-{clean_color}" data-color="{clean_color}">{inner}</mark>'
            elif tag == 'a':
                raw_url = str(dec[1]).strip() if len(dec) > 1 and dec[1] is not None else '#'
                if sanitize:
                    parsed = urlparse(raw_url)
                    scheme = parsed.scheme.lower()
                    if scheme in DANGEROUS_URL_SCHEMES or raw_url.lower().startswith(('javascript:', 'vbscript:', 'data:')):
                        safe_url = '#'
                    else:
                        safe_url = raw_url
                else:
                    safe_url = raw_url
                inner = f'<a href="{html.escape(safe_url)}" target="_blank" rel="noopener noreferrer">{inner}</a>'
            elif tag == 'e':
                # Ya aplicado como envoltorio principal de contenido
                pass

        output.append(inner)

    return "".join(output)


class _RichTextHTMLParser(HTMLParser):
    """
    Parser HTML basado en la biblioteca estándar que construye tuplas de Notion
    manteniendo una pila de estilos y fusionando segmentos contiguos.
    Soporta ecuaciones en línea con el marcador canónico "⁍" (U+204D).
    """
    def __init__(self):
        super().__init__()
        self.segments = []
        self.style_stack = []
        self.in_equation_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        t = tag.lower()

        if t in ('strong', 'b'):
            self.style_stack.append(['b'])
        elif t in ('em', 'i'):
            self.style_stack.append(['i'])
        elif t == 'u':
            self.style_stack.append(['_'])
        elif t in ('s', 'del', 'strike'):
            self.style_stack.append(['s'])
        elif t == 'code':
            self.style_stack.append(['c'])
        elif t == 'a':
            href = attrs_dict.get('href', '').strip()
            self.style_stack.append(['a', href])
        elif t == 'mark':
            # Extraer color de data-color, class o style
            color = self._extract_color(attrs_dict) or 'yellow_background'
            self.style_stack.append(['h', color])
        elif t == 'span':
            cls = attrs_dict.get('class', '')
            if 'inline-equation' in cls or 'notion-inline-equation' in cls or 'inline-katex-node' in cls or 'data-latex' in attrs_dict:
                latex = attrs_dict.get('data-latex', '')
                self.in_equation_depth += 1
                self.style_stack.append(['e', latex])
                is_canonical = attrs_dict.get('data-token') in ('⁍', '\u204d')
                seg_text = '⁍' if is_canonical else latex
                if latex or 'data-latex' in attrs_dict:
                    active_decs = [list(s) for s in self.style_stack if s is not None and s[0] != 'e']
                    active_decs.append(['e', latex])
                    self.segments.append([seg_text, active_decs])
            else:
                if self.in_equation_depth > 0:
                    self.in_equation_depth += 1
                color = self._extract_color(attrs_dict)
                if color:
                    self.style_stack.append(['h', color])
                else:
                    self.style_stack.append(None)
        elif t == 'br':
            self.handle_data('\n')
        elif t in ('p', 'div'):
            # Si ya hay segmentos y el último no termina en \n, separar párrafos
            if self.segments and not self.segments[-1][0].endswith('\n'):
                self.handle_data('\n')
            self.style_stack.append(None)
        else:
            self.style_stack.append(None)

    def handle_endtag(self, tag):
        t = tag.lower()
        if t == 'span' and self.in_equation_depth > 0:
            self.in_equation_depth -= 1
        if self.style_stack:
            self.style_stack.pop()

    def handle_data(self, data):
        if not data:
            return

        # Si estamos dentro de una ecuación cuyo token '⁍' ya fue emitido, ignorar el texto interno generado por KaTeX
        if self.in_equation_depth > 0:
            active_decs = [s for s in self.style_stack if s is not None]
            for idx, dec in enumerate(active_decs):
                if isinstance(dec, list) and len(dec) > 0 and dec[0] == 'e':
                    if len(dec) == 1 or not dec[1]:
                        dec[1] = data
                        decs_copy = [list(d) for d in active_decs if d[0] != 'e']
                        decs_copy.append(['e', data])
                        self.segments.append(['⁍', decs_copy])
                        return
            return

        active_decs = [s for s in self.style_stack if s is not None]
        # Normalizar tupla de decoradores
        decs_copy = [list(d) for d in active_decs]
        self.segments.append([data, decs_copy])

    def _extract_color(self, attrs_dict):
        # 1. data-color
        if 'data-color' in attrs_dict and attrs_dict['data-color']:
            c = attrs_dict['data-color'].strip().lower()
            if c in VALID_COLORS:
                return c

        # 2. class="... notion-color-<color> ..."
        cls = attrs_dict.get('class', '')
        for c in cls.split():
            if c.startswith('notion-color-'):
                col = c[len('notion-color-'):].strip().lower()
                if col in VALID_COLORS:
                    return col

        # 3. style="background-color: ...; color: ...;"
        style = attrs_dict.get('style', '')
        bg_match = re.search(r'background(?:-color)?\s*:\s*([^;]+)', style, re.I)
        if bg_match:
            c = bg_match.group(1).strip().lower()
            col = f"{c}_background" if not c.endswith('_background') else c
            if col in VALID_COLORS:
                return col

        color_match = re.search(r'(?<!background-)color\s*:\s*([^;]+)', style, re.I)
        if color_match:
            c = color_match.group(1).strip().lower()
            if c in VALID_COLORS:
                return c

        return None


def html_to_rich_text(html_str):
    """
    Parsea una cadena HTML y la convierte en la estructura canónica de tuplas de Notion.
    Fusiona automáticamente segmentos adyacentes con decoradores equivalentes.
    """
    if not html_str:
        return []

    parser = _RichTextHTMLParser()
    parser.feed(str(html_str))

    # Fusionar segmentos contiguos con decoradores idénticos
    merged = []
    for segment in parser.segments:
        text, decs = segment[0], segment[1]
        if not text:
            continue

        if not merged:
            merged.append([text, decs])
            continue

        prev = merged[-1]
        prev_text = prev[0]
        prev_decs = prev[1] if len(prev) > 1 else []

        # Comparar decoradores
        if prev_decs == decs:
            prev[0] = prev_text + text
        else:
            merged.append([text, decs])

    return merged


# -----------------------------------------------------------------------------
# 2. Catálogo Canónico y Validación de Bloques de Notion (17 Tipos + Sub-Page)
# -----------------------------------------------------------------------------

STRUCTURAL_BLOCK_TYPES = {
    'page',
    'column_list',
    'column',
    'divider',
    'transclusion_container',
    'transclusion_reference',
}

TEXT_BLOCK_TYPES = {
    'text',
    'header',
    'sub_header',
    'sub_sub_header',
    'header_4',
    'bulleted_list',
    'numbered_list',
    'to_do',
    'toggle',
    'quote',
    'callout',
}

DATA_CODE_BLOCK_TYPES = {
    'code',
    'equation',
    'table',
    'table_row',
    'collection_view',
    'collection_view_page',
}

MEDIA_BLOCK_TYPES = {
    'image',
    'video',
    'audio',
    'file',
    'pdf',
    'bookmark',
}

NAVIGATION_BLOCK_TYPES = {
    'sub_page',
}

ALL_NOTION_BLOCK_TYPES = (
    STRUCTURAL_BLOCK_TYPES
    | TEXT_BLOCK_TYPES
    | DATA_CODE_BLOCK_TYPES
    | MEDIA_BLOCK_TYPES
    | NAVIGATION_BLOCK_TYPES
)

# Clasificación estructural canónica de Notion: Bloques Contenedores vs Nodos Hoja
CONTAINER_BLOCK_TYPES = {
    'page',
    'column_list',
    'column',
    'text',
    'to_do',
    'bulleted_list',
    'numbered_list',
    'toggle',
    'quote',
    'callout',
    'table',
    'transclusion_container',
}

LEAF_BLOCK_TYPES = {
    'equation',
    'divider',
    'code',
    'image',
    'video',
    'audio',
    'file',
    'pdf',
    'bookmark',
    'table_row',
    'transclusion_reference',
    'sub_page',
}

TOGGLEABLE_HEADER_TYPES = {
    'header',
    'sub_header',
    'sub_sub_header',
    'header_4',
}


def is_container_block(block_type, format_dict=None):
    """
    Determina si un tipo de bloque Notion puede actuar como contenedor de bloques hijos.
    Los encabezados ('header', 'sub_header', 'sub_sub_header', 'header_4') son dinámicamente
    contenedores únicamente cuando format.toggleable es True.
    """
    btype = str(block_type or '').strip().lower()
    if btype in CONTAINER_BLOCK_TYPES:
        return True
    if btype in ('collection_view', 'collection_view_page'):
        return True
    if btype in TOGGLEABLE_HEADER_TYPES:
        if isinstance(format_dict, str):
            try:
                format_dict = json.loads(format_dict or '{}')
            except Exception:
                format_dict = {}
        if isinstance(format_dict, dict) and bool(format_dict.get('toggleable')):
            return True
        return False
    return False


# Esquemas de definición canónica de cada tipo de bloque
BLOCK_SCHEMAS = {
    'page': {
        'family': 'structural',
        'allowed_properties': {'title'},
        'allowed_format': {'page_icon', 'page_cover', 'page_full_width', 'page_small_text', 'folder'},
        'children_allowed': True,
        'default_properties': {'title': []},
        'default_format': {},
    },
    'column_list': {
        'family': 'structural',
        'allowed_properties': set(),
        'allowed_format': set(),
        'children_allowed': True,
        'child_types': {'column'},
        'default_properties': {},
        'default_format': {},
    },
    'column': {
        'family': 'structural',
        'allowed_properties': set(),
        'allowed_format': {'column_ratio'},
        'children_allowed': True,
        'default_properties': {},
        'default_format': {'column_ratio': 0.5},
    },
    'divider': {
        'family': 'structural',
        'allowed_properties': set(),
        'allowed_format': set(),
        'children_allowed': False,
        'default_properties': {},
        'default_format': {},
    },
    'transclusion_container': {
        'family': 'structural',
        'allowed_properties': set(),
        'allowed_format': set(),
        'children_allowed': True,
        'default_properties': {},
        'default_format': {},
    },
    'transclusion_reference': {
        'family': 'structural',
        'allowed_properties': set(),
        'allowed_format': {'transclusion_reference_pointer'},
        'children_allowed': False,
        'default_properties': {},
        'default_format': {'transclusion_reference_pointer': {}},
    },
    'text': {
        'family': 'text',
        'allowed_properties': {'title'},
        'allowed_format': {'block_color'},
        'children_allowed': True,
        'default_properties': {'title': []},
        'default_format': {},
    },
    'header': {
        'family': 'text',
        'allowed_properties': {'title'},
        'allowed_format': {'block_color', 'toggleable'},
        'children_allowed': False,
        'default_properties': {'title': []},
        'default_format': {},
    },
    'sub_header': {
        'family': 'text',
        'allowed_properties': {'title'},
        'allowed_format': {'block_color', 'toggleable'},
        'children_allowed': False,
        'default_properties': {'title': []},
        'default_format': {},
    },
    'sub_sub_header': {
        'family': 'text',
        'allowed_properties': {'title'},
        'allowed_format': {'block_color', 'toggleable'},
        'children_allowed': False,
        'default_properties': {'title': []},
        'default_format': {},
    },
    'header_4': {
        'family': 'text',
        'allowed_properties': {'title'},
        'allowed_format': {'block_color', 'toggleable'},
        'children_allowed': False,
        'default_properties': {'title': []},
        'default_format': {},
    },
    'bulleted_list': {
        'family': 'text',
        'allowed_properties': {'title'},
        'allowed_format': {'block_color'},
        'children_allowed': True,
        'default_properties': {'title': []},
        'default_format': {},
    },
    'numbered_list': {
        'family': 'text',
        'allowed_properties': {'title'},
        'allowed_format': {'block_color'},
        'children_allowed': True,
        'default_properties': {'title': []},
        'default_format': {},
    },
    'to_do': {
        'family': 'text',
        'allowed_properties': {'title', 'checked'},
        'allowed_format': {'block_color'},
        'children_allowed': True,
        'default_properties': {'title': [], 'checked': [['No', []]]},
        'default_format': {},
    },
    'toggle': {
        'family': 'text',
        'allowed_properties': {'title'},
        'allowed_format': {'block_color'},
        'children_allowed': True,
        'default_properties': {'title': []},
        'default_format': {},
    },
    'quote': {
        'family': 'text',
        'allowed_properties': {'title'},
        'allowed_format': {'block_color'},
        'children_allowed': True,
        'default_properties': {'title': []},
        'default_format': {},
    },
    'callout': {
        'family': 'text',
        'allowed_properties': {'title'},
        'allowed_format': {'block_color', 'page_icon'},
        'children_allowed': True,
        'default_properties': {'title': []},
        'default_format': {'page_icon': '💡', 'block_color': 'gray_background'},
    },
    'code': {
        'family': 'data_code',
        'allowed_properties': {'title', 'language'},
        'allowed_format': {'code_wrap'},
        'children_allowed': False,
        'default_properties': {'title': [], 'language': [['python', []]]},
        'default_format': {'code_wrap': False},
    },
    'equation': {
        'family': 'data_code',
        'allowed_properties': {'title'},
        'allowed_format': {'copied_from_pointer', 'metadata'},
        'children_allowed': False,
        'default_properties': {'title': []},
        'default_format': {},
    },
    'table': {
        'family': 'data_code',
        'allowed_properties': set(),
        'allowed_format': {
            'table_block_column_order',
            'table_block_column_header',
            'table_block_row_header',
            'table_block_column_widths',
        },
        'children_allowed': True,
        'child_types': {'table_row'},
        'default_properties': {},
        'default_format': {
            'table_block_column_order': [],
            'table_block_column_header': True,
            'table_block_row_header': False,
            'table_block_column_widths': [],
        },
    },
    'table_row': {
        'family': 'data_code',
        'allowed_properties': None,  # Dinámico por cada column_id
        'allowed_format': set(),
        'children_allowed': False,
        'default_properties': {},
        'default_format': {},
    },
    'collection_view': {
        'family': 'data_code',
        'allowed_properties': {'title'},
        'allowed_format': {'collection_id', 'view_ids'},
        'children_allowed': True,
        'default_properties': {'title': []},
        'default_format': {'collection_id': '', 'view_ids': []},
    },
    'collection_view_page': {
        'family': 'data_code',
        'allowed_properties': {'title'},
        'allowed_format': {'collection_id', 'view_ids', 'page_icon'},
        'children_allowed': True,
        'default_properties': {'title': []},
        'default_format': {'collection_id': '', 'view_ids': []},
    },
    'image': {
        'family': 'media',
        'allowed_properties': {'source', 'caption'},
        'allowed_format': {'block_width', 'display_source', 'block_alignment'},
        'children_allowed': False,
        'default_properties': {'source': [['', []]], 'caption': []},
        'default_format': {'block_width': 700, 'block_alignment': 'center'},
    },
    'video': {
        'family': 'media',
        'allowed_properties': {'source', 'caption'},
        'allowed_format': {'block_width', 'block_alignment', 'display_source'},
        'children_allowed': False,
        'default_properties': {'source': [['', []]], 'caption': []},
        'default_format': {'block_width': 700, 'block_alignment': 'center'},
    },
    'audio': {
        'family': 'media',
        'allowed_properties': {'source'},
        'allowed_format': {'block_width', 'block_alignment'},
        'children_allowed': False,
        'default_properties': {'source': [['', []]]},
        'default_format': {},
    },
    'file': {
        'family': 'media',
        'allowed_properties': {'source', 'title', 'size'},
        'allowed_format': {'block_color'},
        'children_allowed': False,
        'default_properties': {'source': [['', []]], 'title': [['', []]], 'size': [['', []]]},
        'default_format': {},
    },
    'pdf': {
        'family': 'media',
        'allowed_properties': {'source'},
        'allowed_format': {'block_width', 'block_height', 'block_alignment'},
        'children_allowed': False,
        'default_properties': {'source': [['', []]]},
        'default_format': {'block_width': 700, 'block_height': 500, 'block_alignment': 'center'},
    },
    'bookmark': {
        'family': 'media',
        'allowed_properties': {'link', 'title', 'description', 'caption'},
        'allowed_format': {'bookmark_icon', 'bookmark_cover'},
        'children_allowed': False,
        'default_properties': {'link': [['', []]], 'title': [], 'description': [], 'caption': []},
        'default_format': {},
    },
    'sub_page': {
        'family': 'navigation',
        'allowed_properties': {'page_id', 'pageId', 'title'},
        'allowed_format': set(),
        'children_allowed': False,
        'default_properties': {'page_id': '', 'title': ''},
        'default_format': {},
    },
}


def is_valid_block_type(btype):
    """Retorna True si el tipo de bloque pertenece a la suite canónica de Notion."""
    return str(btype or '').strip().lower() in ALL_NOTION_BLOCK_TYPES


def validate_rich_text(tuples):
    """
    Valida que un objeto cumpla la especificación estricta de tuplas de texto enriquecido de Notion.
    Formato: [[text: str, [decorator: [tag: str, *args]]]]
    """
    if tuples is None:
        return True, None
    if not isinstance(tuples, (list, tuple)):
        return False, "Rich text must be a list of segments"

    for seg_idx, segment in enumerate(tuples):
        if not isinstance(segment, (list, tuple)):
            return False, f"Segment at index {seg_idx} must be a list or tuple"
        if len(segment) == 0:
            return False, f"Segment at index {seg_idx} is empty"
        if not isinstance(segment[0], str):
            return False, f"Segment text at index {seg_idx} must be a string, got {type(segment[0]).__name__}"

        if len(segment) > 1 and segment[1] is not None:
            decs = segment[1]
            if not isinstance(decs, (list, tuple)):
                return False, f"Segment decorators at index {seg_idx} must be a list or tuple"
            for dec_idx, dec in enumerate(decs):
                if not isinstance(dec, (list, tuple)):
                    return False, f"Decorator at segment {seg_idx}, index {dec_idx} must be a list or tuple"
                if len(dec) == 0:
                    return False, f"Decorator at segment {seg_idx}, index {dec_idx} is empty"
                tag = str(dec[0])
                if tag not in SUPPORTED_DECORATORS:
                    return False, f"Unsupported decorator tag '{tag}' at segment {seg_idx}, index {dec_idx}"

    return True, None


def validate_block(block_dict):
    """
    Valida un diccionario de bloque según su esquema canónico de Notion.
    Comprueba type, properties, format y content.
    Retorna (is_valid: bool, error_message: str | None).
    """
    if not isinstance(block_dict, dict):
        return False, "Block data must be a dictionary"

    btype = str(block_dict.get('type') or '').strip().lower()
    if not btype:
        return False, "Block 'type' is required"
    if not is_valid_block_type(btype):
        return False, f"Unknown or unsupported block type: '{btype}'"

    schema = BLOCK_SCHEMAS[btype]

    # Validar propiedades
    props = block_dict.get('properties', {})
    if props is not None and not isinstance(props, dict):
        return False, "Block 'properties' must be a dictionary"

    if isinstance(props, dict):
        # Para sub_page, verificar que tenga page_id o pageId
        if btype == 'sub_page':
            if not ('page_id' in props or 'pageId' in props or 'page_id' in block_dict or 'pageId' in block_dict):
                return False, "sub_page block requires 'page_id'"

        # Para propiedades con rich text (ej. title, caption)
        for key, val in props.items():
            if btype != 'sub_page' and key in ('title', 'caption', 'language'):
                if not isinstance(val, (list, tuple)):
                    return False, f"properties.{key} must be a list of rich text segments, got {type(val).__name__}"
                is_valid_rt, err = validate_rich_text(val)
                if not is_valid_rt:
                    return False, f"Invalid rich text in properties.{key}: {err}"


    # Validar format
    fmt = block_dict.get('format', {})
    if fmt is not None and not isinstance(fmt, dict):
        return False, "Block 'format' must be a dictionary"

    if isinstance(fmt, dict):
        if 'column_ratio' in fmt:
            ratio = fmt['column_ratio']
            if not isinstance(ratio, (int, float)) or ratio < 0 or ratio > 1:
                return False, "column_ratio in format must be a float between 0.0 and 1.0"
        if 'table_block_column_order' in fmt:
            col_order = fmt['table_block_column_order']
            if not isinstance(col_order, list):
                return False, "table_block_column_order must be a list of column IDs"

    # Validar content
    content = block_dict.get('content')
    if content is not None:
        if not isinstance(content, list):
            return False, "Block 'content' must be a list of child UUIDs"
        children_allowed = schema.get('children_allowed', False)
        if btype in TOGGLEABLE_HEADER_TYPES:
            children_allowed = bool(fmt.get('toggleable')) if isinstance(fmt, dict) else False
        if not children_allowed and len(content) > 0:
            return False, f"Block type '{btype}' does not permit children in content"

    return True, None


def create_default_block(btype, block_id=None, parent_id=None, space_id='default_space'):
    """
    Crea la estructura de diccionario canónica por defecto para un nuevo bloque de Notion.
    """
    clean_type = str(btype or 'text').strip().lower()
    if clean_type not in BLOCK_SCHEMAS:
        clean_type = 'text'

    schema = BLOCK_SCHEMAS[clean_type]
    bid = str(block_id or uuid.uuid4())
    default_fmt = dict(schema['default_format'])
    is_leaf = clean_type in LEAF_BLOCK_TYPES or (
        clean_type in TOGGLEABLE_HEADER_TYPES and not bool(default_fmt.get('toggleable'))
    )
    default_content = None if is_leaf else []

    return {
        'id': bid,
        'space_id': space_id,
        'version': 1,
        'last_version': 0,
        'type': clean_type,
        'properties': dict(schema['default_properties']),
        'content': default_content,
        'parent_id': parent_id,
        'parent_table': 'block' if parent_id else 'space',
        'alive': 1,
        'format': default_fmt,
        'crdt_format_version': 1,
        'crdt_data': {'clock': 1},
        'permissions': [],
    }
