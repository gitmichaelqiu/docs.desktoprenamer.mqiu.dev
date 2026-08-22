document.addEventListener("DOMContentLoaded", function() {
    const renderSheets = () => {
        // Find blocks with .sheet class (from superfences) or .language-sheet (fallback)
        const codeBlocks = document.querySelectorAll('.sheet code, code.language-sheet');
        
        codeBlocks.forEach(code => {
            const pre = code.parentElement;
            if (!pre || pre.tagName !== 'PRE') return;
            
            // Check if already processed
            if (pre.dataset.sheetProcessed) return;
            pre.dataset.sheetProcessed = "true";
            const source = code.textContent;
            const lines = source.split('\n');
            const grid = [];
            const cellBorderRegex = /(?<!\\)\|/;

            for (let line of lines) {
                if (cellBorderRegex.test(line)) {
                    let cells = line.split(cellBorderRegex).map(c => c.trim());
                    if (cells.length >= 2 && cells[0] === '' && cells[cells.length - 1] === '') {
                        grid.push(cells.slice(1, -1));
                    }
                }
            }

            if (grid.length === 0) return;

            // Normalize grid
            const rowCount = grid.length;
            const colCount = Math.max(...grid.map(row => row.length));
            for (let i = 0; i < rowCount; i++) {
                while (grid[i].length < colCount) grid[i].push('');
            }

            // Find header boundaries
            const headerRegex = /^\s*?(:)?(-+)(:)?\s*?(?:(?<!\\)~(.*?))?$/;
            let headerRow = -1;
            for (let r = 0; r < rowCount; r++) {
                if (grid[r].every(cell => headerRegex.test(cell))) {
                    headerRow = r;
                    break;
                }
            }

            let headerCol = -1;
            for (let c = 0; c < colCount; c++) {
                let isHeaderCol = true;
                for (let r = 0; r < rowCount; r++) {
                    if (!headerRegex.test(grid[r][c])) {
                        isHeaderCol = false;
                        break;
                    }
                }
                if (isHeaderCol) {
                    headerCol = c;
                    break;
                }
            }

            // Build DOM elements table
            const table = document.createElement('table');
            table.className = 'sheet';
            const domGrid = Array.from({ length: rowCount }, () => Array(colCount).fill(null));

            for (let r = 0; r < rowCount; r++) {
                if (r === headerRow) continue;
                const tr = document.createElement('tr');
                
                for (let c = 0; c < colCount; c++) {
                    if (c === headerCol) continue;

                    let content = grid[r][c];

                    // Handle merging
                    if (content === '^') {
                        let pr = r - 1;
                        while (pr >= 0 && (pr === headerRow || grid[pr][c] === '^')) pr--;
                        if (pr >= 0 && domGrid[pr] && domGrid[pr][c]) {
                            domGrid[pr][c].rowSpan = (domGrid[pr][c].rowSpan || 1) + 1;
                            domGrid[r][c] = { merged: true };
                            continue;
                        }
                    }

                    if (content === '<') {
                        let pc = c - 1;
                        while (pc >= 0 && (pc === headerCol || grid[r][pc] === '<')) pc--;
                        if (pc >= 0 && domGrid[r][pc]) {
                            domGrid[r][pc].colSpan = (domGrid[r][pc].colSpan || 1) + 1;
                            domGrid[r][c] = { merged: true };
                            continue;
                        }
                    }

                    const tag = (c < headerCol || r < headerRow) ? 'th' : 'td';
                    const cell = document.createElement(tag);
                    
                    // Parse styles ~.class{style}
                    let cellContent = content;
                    const styleSplit = content.split(/(?<![\\~])~(?!~)/);
                    if (styleSplit.length > 1) {
                        cellContent = styleSplit[0];
                        const styleStr = styleSplit[1];
                        const classes = styleStr.match(/(?<=^|\.)([a-zA-Z0-9_-]+)/g);
                        if (classes) classes.forEach(cls => cell.classList.add(cls));
                        const inlineStyles = styleStr.match(/\{(.*?)\}/);
                        if (inlineStyles) cell.style.cssText += inlineStyles[1];
                    }

                    cell.innerHTML = cellContent; 
                    domGrid[r][c] = cell;
                    tr.appendChild(cell);
                }
                if (tr.children.length > 0) table.appendChild(tr);
            }

            // Replace the pre/div wrapper
            // superfences often wraps in <div class="highlight"><pre><code>
            // Or with custom fence: <div class="sheet"><pre><code>
            const wrapper = pre.closest('.sheet') || pre.closest('.highlight') || pre;
            wrapper.parentNode.replaceChild(table, wrapper);
        });
        
        // Trigger KaTeX auto-render if available
        if (window.renderMathInElement) {
            window.renderMathInElement(document.body);
        }
    };

    renderSheets();
});
