#!/bin/bash
# Zensical Build & Optimization Script
# This script builds the site and then runs post-build optimizations
# to pre-render KaTeX and other components for better performance.

echo "* Starting Zensical build..."
export PYTHONPATH=.
zensical build

if [ $? -eq 0 ]; then
    echo "Build successful! Running optimizations..."
    python scripts/optimize_site.py
    echo "✔ Optimization complete! Your site is ready in the 'site' directory."
else
    echo "✘ Build failed. Skipping optimization."
    exit 1
fi
