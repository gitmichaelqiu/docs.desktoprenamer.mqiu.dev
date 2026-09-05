# AppleScript

DesktopRenamer's scripting dictionary is available to Script Editor after the app is installed. AppleScript is convenient for one-off commands, shell scripts, and automation tools that already support macOS scripting.

Use the [structured records](structured-records.md) for typed read results. The commands on this page are the established text-command surface and remain available for compatibility. Window-specific commands are collected in [window automation](windows.md).

## Quick start

```applescript
tell application "DesktopRenamer"
    get api version
    get current space name
    get all spaces
end tell
```

`get all spaces` returns one line per space with fields separated by `~`:

```text
UUID~Name~DisplayName~Number~IsFullscreen~AppPath
```

The result is sorted by display and space number. Names and paths may be empty. Space identifiers are not guaranteed to survive display changes or Mission Control recreation, so use a fresh result before issuing a later command.

## Space commands

```applescript
tell application "DesktopRenamer"
    rename current space "Writing"
    switch to space "SPACE-ID"
    rename space "SPACE-ID" to "Research"
    rearrange space "SPACE-ID" direction "up"
end tell
```

The `direction` parameter for `rearrange space` must be `up` or `down`.

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
| `reload space labels` | — | Returns `true` after asking DesktopRenamer to reload its label windows. |

The toggle commands return a Boolean containing the resulting state. `toggle labels` returns `true` only when both the active and preview labels are enabled. `toggle desktop visibility` changes the **Keep visible on desktop** preference for the labels.

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

## Errors and timing

Commands that change spaces or move windows return before the operating-system action has necessarily finished. `execute window action` waits for DesktopRenamer's action routine and returns `true`, but clients should still refresh window data after a state-changing command.

Validation errors use standard script errors:

| Number | Meaning |
| --- | --- |
| `-1` | The API is disabled. |
| `-2` | An argument is missing or invalid. |
| `-3` | DesktopRenamer is not ready. |

Invalid rearrangement directions set the script error to `Direction must be up or down`. Clients should inspect the script error number and string rather than treating every missing result as success. When the API is disabled, commands set script error `-1` with `API Disabled`; read commands that have a text result also return that string, while Boolean commands return `false`.
