# DesktopRenamer

DesktopRenamer is a macOS menu bar application for naming, navigating, and automating Mission Control spaces.

It provides:

- Custom names for regular spaces and fullscreen spaces.
- Fast keyboard, gesture, launcher, and menu bar navigation.
- Window movement between spaces and displays.
- Native space rearrangement when macOS exposes the required operation.
- Space labels, preview labels, and window-management helpers.
- A versioned SpaceAPI and AppleScript automation surface.

## Documentation

Use **Getting Started** for installation, permissions, and space behavior. Use **API** when integrating DesktopRenamer with Raycast, AppleScript, or another automation tool.

## Requirements

- macOS 13 Ventura or later.
- Accessibility permission for global shortcuts, gestures, window inspection, and window movement.
- Mission Control spaces configured on at least one display.

The external API is disabled or enabled from the app's settings. Existing API clients should check the [API contract version](api/versioning.md) before relying on newer commands or fields.

<div class="grid cards" markdown>

-   :material-rocket-launch: **Start here**

    Install DesktopRenamer and configure the required macOS permissions.

    [Installation](guides/installation.md)

-   :material-api: **Integrate**

    Read the versioned SpaceAPI and AppleScript documentation.

    [API overview](api/index.md)

-   :material-monitor-screenshot: **Understand spaces**

    Learn how regular and fullscreen spaces are identified and rearranged.

    [Spaces and fullscreen apps](guides/spaces.md)

</div>
