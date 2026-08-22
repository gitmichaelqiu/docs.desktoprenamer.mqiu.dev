# Integration prerequisites

This page is for developers preparing a machine to run and integrate with DesktopRenamer.

## Runtime requirements

- macOS 13 Ventura or later.
- Mission Control spaces configured on at least one display.
- DesktopRenamer installed from [GitHub Releases](https://github.com/gitmichaelqiu/DesktopRenamer/releases) or Homebrew.

DesktopRenamer does not require disabling SIP. Unsigned releases may require confirmation in **System Settings → Privacy & Security → Open Anyway**.

## Homebrew

```bash
brew install --cask gitmichaelqiu/tap/desktoprenamer
```

## Companion clients

The [Raycast extension](https://www.raycast.com/michael_qiu/desktoprenamer) uses the external API for space and window operations. Other clients can use the same API surfaces without installing Raycast.

## Enable the API

Open **Settings → General → Advanced** and confirm that the API is enabled. Existing installations keep the API enabled by default unless it was explicitly disabled.
