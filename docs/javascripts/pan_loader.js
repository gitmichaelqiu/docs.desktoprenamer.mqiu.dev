/**
 * pan_loader.js
 * Handles lazy-loading and initializing pan-zoom for SVG mindmaps.
 */

(function() {
    function initializeWrapper(wrapper) {
        const linkEl = wrapper.querySelector('link');
        const svgSrc = linkEl ? linkEl.getAttribute('href') : null;
        if (!svgSrc) return;

        // Skip if already has an embed
        if (wrapper.querySelector('embed')) return;

        const embed = document.createElement('embed');
        embed.setAttribute('class', 'pan-zoom-svg');
        embed.setAttribute('type', 'image/svg+xml');
        embed.setAttribute('src', svgSrc);
        embed.style.width = '100%';
        embed.style.height = '100%';

        const tryInit = () => {
            if (!window.svgPanZoom) {
                console.warn('svgPanZoom not loaded yet, retrying...');
                setTimeout(tryInit, 100);
                return;
            }

            try {
                window.svgPanZoom(embed, {
                    zoomEnabled: true,
                    controlIconsEnabled: true,
                    fit: true,
                    center: true,
                    minZoom: 0.1,
                    maxZoom: 10
                });
            } catch (e) {
                console.error('Failed to initialize svgPanZoom:', e);
            }
        };

        const stopScroll = (e) => {
            e.preventDefault();
            e.stopPropagation();
        };

        // Attach scroll suppression to both the wrapper and the embed itself
        wrapper.addEventListener('wheel', stopScroll, { passive: false });
        embed.addEventListener('wheel', stopScroll, { passive: false });

        embed.addEventListener('load', () => {
            tryInit();
            // Try to attach to the inner document as well
            try {
                const svgDoc = embed.getSVGDocument();
                if (svgDoc) {
                    svgDoc.addEventListener('wheel', stopScroll, { passive: false });
                }
            } catch (e) {
                console.warn('Could not attach scroll listener to inner SVG document');
            }
        });
        
        wrapper.appendChild(embed);
    }

    function scanAndInit() {
        // Look for any div with id="map-wrapper"
        const mapWrappers = document.querySelectorAll('#map-wrapper');
        mapWrappers.forEach(initializeWrapper);
    }

    // Initial check
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', scanAndInit);
    } else {
        scanAndInit();
    }

    // Observe for dynamic content changes (SPA transitions)
    const observer = new MutationObserver((mutations) => {
        let shouldScan = false;
        for (const mutation of mutations) {
            if (mutation.addedNodes.length) {
                shouldScan = true;
                break;
            }
        }
        if (shouldScan) scanAndInit();
    });

    observer.observe(document.documentElement, { childList: true, subtree: true });
})();
