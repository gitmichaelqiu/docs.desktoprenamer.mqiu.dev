# DesktopRenamer Documentation Contributor Guide

## Scope

This repository contains the Zensical source for `docs.desktoprenamer.mqiu.dev`. Keep documentation accurate against the DesktopRenamer app and its external API contract.

## Writing style

- Use clear, direct English and prefer short sections.
- Use sentence-case headings.
- Keep code examples executable or explicitly label them as pseudocode.
- Document user-visible behavior, permissions, platform assumptions, and failure states.
- Do not claim support for an API command or payload that is not present in the app's scripting dictionary or API implementation.
- Keep the footer label as `docs.desktoprenamer.mqiu.dev`.

## Change workflow

1. Check the current DesktopRenamer implementation before documenting behavior.
2. Make the smallest coherent documentation change.
3. Run the Zensical build, preferably with `--strict`.
4. Review generated navigation and links for broken pages.
5. Commit with a Conventional Commit message such as `docs: add SpaceAPI guide` or `fix: correct AppleScript example`.

Do not commit generated `site/`, dependency directories, virtual environments, `.env` files, or caches. Do not push changes unless explicitly requested.
