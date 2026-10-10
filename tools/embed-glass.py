"""Embed the local SVG filters in CSS; run after editing res/filters/*.svg.

Data URLs keep file:// previews independent of external SVG loading rules.
This runs only when editing assets, never in the browser.
"""

from pathlib import Path
from urllib.parse import quote
import re


root = Path(__file__).resolve().parents[1]
names = ('nav', 'nav-pressed', 'pill', 'pill-pressed', 'card')
lines = ['/* Generated from res/filters/*.svg by tools/embed-glass.py. */', '.glass {']

for name in names:
    source = (root / 'res' / 'filters' / f'{name}.svg').read_text()
    source = re.sub(r'<!--.*?-->', '', source, flags=re.S)
    source = re.sub(r'>\s+<', '><', source.strip())
    lines.append(f'    --lens-{name}: url("data:image/svg+xml,{quote(source, safe="")}#lens");')

lines.append('}')
(root / 'css' / 'liquid-filters.css').write_text('\n'.join(lines) + '\n')
