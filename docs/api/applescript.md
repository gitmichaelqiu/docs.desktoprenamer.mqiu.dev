# AppleScript

DesktopRenamer's scripting dictionary is available to Script Editor after the app is installed. Commands return immediately for operations that require Mission Control or Accessibility timing.

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

The `direction` parameter for `rearrange space` must be `up` or `down`.

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
