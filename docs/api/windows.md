# Window Automation

Window commands use Core Graphics window IDs and owner process IDs. Obtain window information with `get windows` before issuing a targeted command.

## Inspect windows

```applescript
tell application "DesktopRenamer"
    get windows
end tell
```

The result is grouped by space and includes each visible application window. The exact text format is intended for the companion Raycast extension and may gain fields in future compatible API versions.

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
