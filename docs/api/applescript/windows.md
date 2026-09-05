# AppleScript window automation

Window commands use Core Graphics window IDs and owner process IDs. Obtain window information with `get windows` before issuing a targeted command.

## Inspect windows

```applescript
tell application "DesktopRenamer"
    get windows
end tell
```

The result is grouped by space and includes eligible regular-application windows assigned to known spaces. When macOS exposes the assignment, this includes windows on inactive spaces as well as the current spaces. The exact text format is intended for the companion Raycast extension and may gain fields in future compatible API versions.

The current format is newline-delimited:

```text
>spaceID~spaceName~displayName~number~isFullscreen~appPath
  windowID|pid|ownerName|appPath|title|isMinimized|isHidden
```

Each space begins with `>`. Its following window rows begin with two spaces. Fields are positional; split space rows on `~` and window rows on `|`. The formatter reserves empty fields, but the current enumerator emits only regular applications with a bundle path and a non-empty window title; background agents, invalid windows, and stale window records are filtered out. On active spaces, Accessibility window IDs are also used to reject stale records.

The fields are:

| Field | Meaning |
| --- | --- |
| `spaceID` | Managed space identifier. |
| `spaceName` | DesktopRenamer’s current name for the space. |
| `displayName` | macOS display name. |
| `number` | Space number on that display. |
| `isFullscreen` | `1` or `0`. |
| `appPath` | Full path of the fullscreen owner, when applicable. |
| `windowID` | Core Graphics window ID. |
| `pid` | Owner process ID. |
| `ownerName` | Application name. |
| `title` | Window title, when exposed by macOS. |
| `isMinimized` | `1` or `0`. |
| `isHidden` | `1` or `0`. |

## Move and focus windows

```applescript
tell application "DesktopRenamer"
    move window next
    move window previous
    move window to space "SPACE-ID"
    focus window "WINDOW-ID" pid "PROCESS-ID"
    move specific window "WINDOW-ID" pid "PROCESS-ID" from space "SOURCE-ID" to space "TARGET-ID"
end tell
```

The process ID is optional for `move specific window` when both space arguments are numeric ManagedSpaceIDs. Supplying it is recommended because the Accessibility path handles fullscreen and cross-display cases more reliably.

## Window actions

```applescript
tell application "DesktopRenamer"
    execute window action "WINDOW-ID" pid "PROCESS-ID" action "minimize"
end tell
```

Supported action names include `close`, `minimize`, `hide`, `enterFullScreen`, `exitFullScreen`, `quit`, and `restore`.

Actions that use Accessibility may first switch to the target space and wait for Mission Control to settle. `execute window action` waits for DesktopRenamer's action routine and returns `true`; the other movement and focus commands return without a result. Refresh window data afterward because the operating system may still be settling.
