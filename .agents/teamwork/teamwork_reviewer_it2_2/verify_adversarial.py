import os
import re
import sys
from html.parser import HTMLParser

class FormatBarExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_format_bar = False
        self.depth = 0
        self.buttons = []
        self.current_button = None

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        classes = attr_dict.get('class', '').split()
        if 'desktop-format-bar' in classes:
            self.in_format_bar = True
            self.depth = 1
            return
        
        if self.in_format_bar:
            self.depth += 1
            if tag == 'button':
                self.buttons.append({
                    'id': attr_dict.get('id', ''),
                    'class': attr_dict.get('class', ''),
                    'style': attr_dict.get('style', ''),
                    'title': attr_dict.get('title', '')
                })

    def handle_endtag(self, tag):
        if self.in_format_bar:
            self.depth -= 1
            if self.depth == 0:
                self.in_format_bar = False

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

parser = FormatBarExtractor()
parser.feed(html)

print(f"Extracted {len(parser.buttons)} buttons from .desktop-format-bar:")
non_dropdown_amber = []
dropdown_found = False

for b in parser.buttons:
    b_id = b['id']
    b_class = b['class']
    b_style = b['style']
    is_dropdown = (b_id == 'btn-insert-dropdown' or 'insert-dropdown-btn' in b_class)
    is_amber_inline = 'accent-amber' in b_style or '#f59e0b' in b_style
    
    print(f" - ID: {b_id:25} Class: {b_class:40} AmberInline: {is_amber_inline}")
    if is_dropdown:
        dropdown_found = True
    elif is_amber_inline:
        non_dropdown_amber.append(b)

if not dropdown_found:
    print("ERROR: #btn-insert-dropdown was not found!")
    sys.exit(1)

if non_dropdown_amber:
    print(f"ERROR: Found non-dropdown buttons with inline amber styling: {non_dropdown_amber}")
    sys.exit(1)

print("PASS: Only #btn-insert-dropdown has amber inline styling among format bar buttons.")
