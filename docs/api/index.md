# API Overview

DesktopRenamer exposes two automation surfaces:

1. **SpaceAPI**, based on `DistributedNotificationCenter`, for observing current-space and space-list changes.
2. **AppleScript**, for commands that switch, rename, rearrange, inspect, and move windows.

The API is enabled by default for existing installations and can be controlled from **Settings → General → Advanced**. Clients should handle the API-disabled state and verify the [contract version](versioning.md).

## Space identifiers

Use `get all spaces` through AppleScript or the `ReturnSpaceList` notification to obtain current identifiers. Do not persist a space ID indefinitely: macOS can replace identifiers after display or Mission Control changes.

## Main-thread behavior

Commands that change spaces or windows are asynchronous where required by AppKit and Accessibility APIs. A successful command dispatch means the operation was accepted; clients should observe subsequent space notifications before assuming the UI has settled.

## Compatibility

The API version is independent of the DesktopRenamer app version. See [API Versioning](versioning.md) before consuming new fields or commands.
