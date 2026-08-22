import os
import re
import json
import subprocess
import shutil
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def render_katex(source, is_block):
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
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error rendering KaTeX: {e}")
        return source

def get_base_path():
    """Extracts the base path from zensical.toml's site_url."""
    try:
        with open('zensical.toml', 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'site_url\s*=\s*"(.*?)"', content)
            if match:
                url = match.group(1)
                path = urlparse(url).path.rstrip('/')
                return path
    except Exception as e:
        print(f"Error reading zensical.toml: {e}")
    return ""

def optimize_html_file(file_path, site_dir, base_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    changed = False

    # 1. Optimize Math
    math_elements = soup.find_all(class_='arithmatex')
    for el in math_elements:
        text = el.get_text().strip()
        math_content = text
        math_content = re.sub(r'^(\\\(|\\\[|\s)+', '', math_content)
        math_content = re.sub(r'(\\\)|\\\]|\s)+$', '', math_content)
        is_block = (el.name == 'div') or text.strip().startswith('\\[')

        if math_content:
            rendered = render_katex(math_content, is_block)
            new_soup = BeautifulSoup(rendered, 'html.parser')
            el.replace_with(new_soup)
            changed = True

    # 2. Fix SVG paths
    # We resolve relative paths in the built HTML to absolute paths including the subpath (base_path).
    svg_links = soup.find_all(href=re.compile(r'\.svg$'))
    for link_el in svg_links:
        orig_href = link_el.get('href', '')
        if orig_href.startswith(('http', '/', '#')):
            continue
            
        # Resolve path relative to site root
        html_rel_path = os.path.relpath(file_path, site_dir)
        html_dir = os.path.dirname(html_rel_path)
        
        # Zensical has already adjusted orig_href to be relative to the HTML file's location.
        # We just need to resolve it against the HTML's directory to get the site-root relative path.
        abs_svg_path = os.path.normpath(os.path.join(html_dir, orig_href))
        
        # Combine with base_path for deployment
        # e.g. /blog + /academic-notes/...
        root_relative = base_path + '/' + abs_svg_path.replace(os.sep, '/')
        root_relative = re.sub(r'/+', '/', root_relative) # Remove double slashes
        
        print(f"  Fixing SVG path: {orig_href} -> {root_relative}")
        link_el['href'] = root_relative
        changed = True

    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return True
    return False

def copy_svg_assets():
    print("Syncing SVG assets...")
    docs_dir = 'docs'
    site_dir = 'site'
    if not os.path.exists(site_dir):
        return
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.svg'):
                rel_path = os.path.relpath(os.path.join(root, file), docs_dir)
                dest_path = os.path.join(site_dir, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(os.path.join(root, file), dest_path)

def main():
    site_dir = 'site'
    if not os.path.exists(site_dir):
        print(f"Directory {site_dir} not found.")
        return

    copy_svg_assets()
    
    # Always get the base path from zensical.toml for consistency with site_url
    base_path = get_base_path()
    print(f"Detected base path: '{base_path}'")

    count = 0
    for root, dirs, files in os.walk(site_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if optimize_html_file(file_path, site_dir, base_path):
                    count += 1
    
    print(f"Optimized {count} HTML files.")

if __name__ == "__main__":
    main()
