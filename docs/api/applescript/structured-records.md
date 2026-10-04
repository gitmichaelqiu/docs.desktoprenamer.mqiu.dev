# AppleScript structured records

DesktopRenamer's scripting dictionary is available to Script Editor after the app is installed. This page covers typed records introduced in contract `1.0.0`, Space Lock fields added in `1.1.0`, and persistent space IDs in `2.0.0`; see the [AppleScript overview](index.md) for common commands and the [window automation guide](windows.md) for window operations.

## Structured records

Contract `1.0.0` adds typed records alongside the existing commands. Contract `1.1.0` adds Space Lock state and restore-queue information. Contract `2.0.0` changes the structured `space.id` and window space references to DesktopRenamer-owned persistent IDs. The structured commands are:

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
- `space`: `id`, `name`, `display ID`, `display name`, `number`, `full screen`, `locked`, and optional `app name`, `app path`, and `global shortcut number` properties.
- `space snapshot`: `API version`, `revision`, `timestamp`, `current space IDs`, optional `current space ID`, `current display ID`, `current space name`, `moved windows count`, and `spaces`.
- `window`: `id`, `process ID`, `owner name`, optional `app path` and `title`, `space ID`, `space IDs`, `minimized`, and `hidden`.
- `window snapshot`: `API version`, `revision`, `timestamp`, `spaces`, and `windows`.

Optional app paths, titles, current space ID, and full-screen metadata can be unavailable when macOS does not expose them or the current space has not yet been reconciled. Structured snapshots include a revision and ISO 8601 timestamp so a client can identify the snapshot it read. The existing text commands remain available with their original command codes; their synchronous or asynchronous behavior is described in the [AppleScript overview](index.md) and [window automation guide](windows.md).

Structured record IDs are DesktopRenamer-owned. The legacy `get all spaces` and `get current space id` commands continue to return macOS ManagedSpaceIDs.

The JSON-RPC equivalents of mutating commands return an `operation result` object with an `accepted` Boolean. AppleScript mutating commands do not return that record: space and window movement commands return no value, while toggle commands and `reload space labels` return Booleans. A returned value does not imply that Mission Control or Accessibility has finished settling.
