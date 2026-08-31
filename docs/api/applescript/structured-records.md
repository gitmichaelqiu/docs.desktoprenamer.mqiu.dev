# AppleScript structured records

DesktopRenamer's scripting dictionary is available to Script Editor after the app is installed. This page covers the typed records added in contract `1.0.0`; see the [AppleScript overview](index.md) for common commands and the [window automation guide](windows.md) for window operations.

## Structured records

Contract `1.0.0` adds typed records alongside the existing commands. The new commands are:

```applescript
tell application "DesktopRenamer"
    get api information
    get structured spaces
    get structured snapshot
    get structured windows
end tell
```

The records use native scripting-dictionary properties rather than packed strings:

- `api information`: `contract version`, `JSON-RPC version`, `supported methods`, `legacy notifications`, `legacy compatibility`, `event notifications`, `event capabilities`, and `maximum payload bytes`.
- `space`: `id`, `name`, `display ID`, `display name`, `number`, `full screen`, and optional app/shortcut properties.
- `space snapshot`: `API version`, `revision`, `timestamp`, `current space IDs`, `current space name`, and `spaces`.
- `window`: `id`, `process ID`, `owner name`, optional `app path` and `title`, `space ID`, `minimized`, and `hidden`.
- `window snapshot`: `API version`, `revision`, `timestamp`, `spaces`, and `windows`.

Optional app paths and titles can be unavailable when macOS does not expose them. Structured snapshots include a revision and ISO 8601 timestamp so a client can identify the snapshot it read. The existing text commands remain compatibility aliases with their original command codes and asynchronous behavior.

For JSON-RPC operations, the equivalent structured result is an `operation result` object with an `accepted` Boolean. AppleScript operations that already return no value continue to return no value; acceptance does not imply that Mission Control or Accessibility has finished.
