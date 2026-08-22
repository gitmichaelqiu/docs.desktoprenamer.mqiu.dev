# DesktopRenamer

DesktopRenamer is a macOS menu bar application with a versioned automation interface for Mission Control spaces.

It provides:

- A versioned SpaceAPI and AppleScript automation surface.
- Stable space identifiers, names, display associations, and fullscreen metadata.
- Window inspection, focus, movement, and control actions.
- Native space switching and rearrangement operations.

## Documentation

This site is for developers integrating DesktopRenamer with Raycast, AppleScript, SpaceAPI, or another automation tool. **Integration Setup** covers platform prerequisites and the Mission Control state that affects integrations. **API** defines the stable contract.

## Requirements

- macOS 13 Ventura or later.
- Accessibility permission for global shortcuts, gestures, window inspection, and window movement.
- Mission Control spaces configured on at least one display.

The external API is disabled or enabled from the app's settings. Existing API clients should check the [API contract version](api/versioning.md) before relying on newer commands or fields.

<div class="grid cards" markdown>

-   :material-rocket-launch: **Start here**

    Verify the macOS version, API setting, and Accessibility requirements for automation.

    [Prerequisites](guides/installation.md)

-   :material-api: **Integrate**

    Read the versioned SpaceAPI and AppleScript documentation.

    [API overview](api/index.md)

-   :material-monitor-screenshot: **Understand spaces**

    Learn how regular and fullscreen spaces affect integrations.

    [Spaces model](guides/spaces.md)

</div>
