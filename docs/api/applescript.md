# AppleScript

DesktopRenamer's scripting dictionary is available to Script Editor after the app is installed. Commands return immediately for operations that require Mission Control or Accessibility timing.

## Structured records

Contract `1.2.0` adds typed records alongside the existing commands. The new commands are:

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

Optional app paths and titles can be unavailable when macOS does not expose them. Structured snapshots include a revision and ISO 8601 timestamp so a client can identify the snapshot it read. The existing text commands below remain compatibility aliases with their original command codes and asynchronous behavior.

For JSON-RPC operations, the equivalent structured result is an `operation result` object with an `accepted` Boolean. AppleScript operations that already return no value continue to return no value; acceptance does not imply that Mission Control or Accessibility has finished.

## Space commands

```applescript
tell application "DesktopRenamer"
    get api version
    get current space name
    get current space id
    get all spaces
    rename current space to "Writing"
    switch to space "SPACE-ID"
    rename space "SPACE-ID" to "Research"
    rearrange space "SPACE-ID" direction "up"
end tell
```

`get all spaces` returns one line per space with fields separated by `~`:

```text
UUID~Name~DisplayName~Number~IsFullscreen~AppPath
```

`get all spaces` is sorted by display and space number. Names and paths may be empty. Space identifiers are not guaranteed to survive display changes or Mission Control recreation.

The `direction` parameter for `rearrange space` must be `up` or `down`.

## Command reference

| Command | Parameters | Return / timing |
| --- | --- | --- |
| `get api version` | — | Returns the API contract version immediately. |
| `get current space name` | — | Returns a string immediately. |
| `get current space id` | — | Returns current ManagedSpaceID values, comma-separated for multiple displays. |
| `get all spaces` | — | Returns the multiline space record described above. |
| `rename current space` | Text | Asynchronous; returns no value. |
| `rename space` | Space ID, `to` text | Asynchronous; returns no value. |
| `switch to space` | Space ID | Asynchronous; returns no value. |
| `rearrange space` | Space ID, `direction` | Asynchronous; moves one position. |

Invalid rearrangement directions set the script error to `Direction must be up or down`. The API-disabled error is `API Disabled`.

Validation errors use standard script errors: `-1` means the API is disabled, `-2` means an argument is missing or invalid, and `-3` means DesktopRenamer is not ready. Clients should inspect the script error number and string instead of treating every missing result as success.

## Label and launcher commands

```applescript
tell application "DesktopRenamer"
    toggle menubar
    toggle launcher
    toggle labels
    toggle active label
    toggle preview label
    toggle desktop visibility
    reload space labels
end tell
```

## API-disabled behavior

When the API is disabled, commands return `API Disabled` where a result is defined, or do nothing for asynchronous commands. Automation clients should treat this as a recoverable configuration state.
