import subprocess
import json
import re
import os
import markdown

# Ensure node_modules is in the path for the subprocess
# We use the absolute path of the repo root to be robust
_PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_PLUGIN_DIR)
_NODE_MODULES = os.path.join(_REPO_ROOT, "node_modules")
os.environ["NODE_PATH"] = _NODE_MODULES

def render_katex(source, language, class_name, options, md, **kwargs):
    """
    Render KaTeX at build time using Node.js.
    """
    is_block = class_name == 'arithmatex' or kwargs.get('is_block', True)
    if 'display' in options:
        is_block = options['display']

    js_code = f"""
const katex = require('katex');
try {{
    const html = katex.renderToString({json.dumps(source)}, {{
        displayMode: {str(is_block).lower()},
        throwOnError: false
    }});
    process.stdout.write(html);
}} catch (e) {{
    process.stderr.write(e.message);
    process.exit(1);
}}
"""
    try:
        result = subprocess.run(
            ['node', '-e', js_code],
            capture_output=True,
            text=True,
            check=True,
            env=os.environ
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        # In case of error, we return the original source but could also log it
        error_msg = e.stderr.strip() or e.stdout.strip() or "Unknown KaTeX error"
        return f'<span class="katex-error" title="{error_msg}">{source}</span>'
    except Exception as e:
        return f'<span class="katex-error" title="{str(e)}">{source}</span>'

# Reusable Markdown instance for cell rendering
_md_cell = markdown.Markdown(extensions=[
    'abbr', 'admonition', 'attr_list', 'def_list', 'footnotes', 
    'md_in_html', 'toc', 'pymdownx.arithmatex', 'pymdownx.betterem', 
    'pymdownx.caret', 'pymdownx.details', 'pymdownx.emoji', 
    'pymdownx.highlight', 'pymdownx.inlinehilite', 'pymdownx.keys', 
    'pymdownx.magiclink', 'pymdownx.mark', 'pymdownx.smartsymbols', 
    'pymdownx.tabbed', 'pymdownx.tasklist', 'pymdownx.tilde'
])

def render_sheet(source, language, class_name, options, md, **kwargs):
    """
    Render custom "Sheet" tables at build time.
    """
    lines = source.strip().split('\n')
    grid = []
    cell_border_regex = re.compile(r'(?<!\\)\|')

    for line in lines:
        if cell_border_regex.search(line):
            cells = [c.strip() for c in cell_border_regex.split(line)]
            if len(cells) >= 2 and cells[0] == '' and cells[-1] == '':
                grid.append(cells[1:-1])

    if not grid:
        return f'<pre class="{class_name}"><code>{source}</code></pre>'

    row_count = len(grid)
    col_count = max(len(row) for row in grid)
    for i in range(row_count):
        while len(grid[i]) < col_count:
            grid[i].append('')

    header_regex = re.compile(r'^\s*?(:)?(-+)(:)?\s*?(?:(?<!\\)~(.*?))?$')
    header_row = -1
    for r in range(row_count):
        if all(header_regex.match(cell) for cell in grid[r]):
            header_row = r
            break

    header_col = -1
    for c in range(col_count):
        if all(header_regex.match(grid[r][c]) for r in range(row_count)):
            header_col = c
            break

    table_html = ['<table class="sheet">']
    dom_grid = [[None for _ in range(col_count)] for _ in range(row_count)]

    for r in range(row_count):
        if r == header_row:
            continue
        
        for c in range(col_count):
            if c == header_col:
                continue

            content = grid[r][c]

            if content == '^':
                pr = r - 1
                while pr >= 0 and (pr == header_row or (dom_grid[pr][c] and dom_grid[pr][c].get('merged'))):
                    pr -= 1
                if pr >= 0 and dom_grid[pr][c] and not dom_grid[pr][c].get('merged'):
                    dom_grid[pr][c]['rowspan'] += 1
                    dom_grid[r][c] = {'merged': True}
                    continue

            if content == '<':
                pc = c - 1
                while pc >= 0 and (pc == header_col or (dom_grid[r][pc] and dom_grid[r][pc].get('merged'))):
                    pc -= 1
                if pc >= 0 and dom_grid[r][pc] and not dom_grid[r][pc].get('merged'):
                    dom_grid[r][pc]['colspan'] += 1
                    dom_grid[r][c] = {'merged': True}
                    continue

            tag = 'th' if (c < header_col or r < header_row) else 'td'
            cell_content = content
            classes = []
            styles = ""
            
            style_split = content.split('~', 1)
            if len(style_split) > 1:
                cell_content = style_split[0]
                style_str = style_split[1]
                class_matches = re.findall(r'(?<=^|\.)([a-zA-Z0-9_-]+)', style_str)
                classes.extend(class_matches)
                style_match = re.search(r'\{(.*?)\}', style_str)
                if style_match:
                    styles = style_match.group(1)

            # Render content using the separate Markdown instance
            rendered_content = _md_cell.convert(cell_content)
            rendered_content = re.sub(r'^<p>(.*?)</p>$', r'\1', rendered_content, flags=re.DOTALL)

            dom_grid[r][c] = {
                'tag': tag,
                'content': rendered_content,
                'rowspan': 1,
                'colspan': 1,
                'classes': classes,
                'styles': styles
            }

    for r in range(row_count):
        if r == header_row:
            continue
            
        tr_content = []
        for c in range(col_count):
            if c == header_col:
                continue
                
            cell = dom_grid[r][c]
            if not cell or cell.get('merged'):
                continue
            
            class_attr = f' class="{" ".join(cell["classes"])}"' if cell['classes'] else ''
            style_attr = f' style="{cell["styles"]}"' if cell['styles'] else ''
            rowspan_attr = f' rowspan="{cell["rowspan"]}"' if cell['rowspan'] > 1 else ''
            colspan_attr = f' colspan="{cell["colspan"]}"' if cell['colspan'] > 1 else ''
            
            tr_content.append(f'<{cell["tag"]}{class_attr}{style_attr}{rowspan_attr}{colspan_attr}>{cell["content"]}</{cell["tag"]}>')
        
        if tr_content:
            table_html.append(f'<tr>{"".join(tr_content)}</tr>')
    
    table_html.append('</table>')
    return "".join(table_html)
