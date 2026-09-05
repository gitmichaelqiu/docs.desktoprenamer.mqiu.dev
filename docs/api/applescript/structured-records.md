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
- `space`: `id`, `name`, `display ID`, `display name`, `number`, `full screen`, and optional `app name`, `app path`, and `global shortcut number` properties.
- `space snapshot`: `API version`, `revision`, `timestamp`, `current space IDs`, `current space name`, and `spaces`.
- `window`: `id`, `process ID`, `owner name`, optional `app path` and `title`, `space ID`, `minimized`, and `hidden`.
- `window snapshot`: `API version`, `revision`, `timestamp`, `spaces`, and `windows`.

Optional app paths, titles, and full-screen metadata can be unavailable when macOS does not expose them. Structured snapshots include a revision and ISO 8601 timestamp so a client can identify the snapshot it read. The existing text commands remain available with their original command codes; their synchronous or asynchronous behavior is described in the [AppleScript overview](index.md) and [window automation guide](windows.md).

The JSON-RPC equivalents of mutating commands return an `operation result` object with an `accepted` Boolean. AppleScript mutating commands do not return that record: space and window movement commands return no value, while toggle commands and `reload space labels` return Booleans. A returned value does not imply that Mission Control or Accessibility has finished settling.
