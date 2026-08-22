# Raycast Integration

The official [DesktopRenamer Raycast extension](https://www.raycast.com/michael_qiu/desktoprenamer) is a reference client for both API surfaces.

## Setup

1. Install DesktopRenamer and the Raycast extension.
2. Enable the API in **Settings → General → Advanced**.
3. Grant DesktopRenamer Accessibility permission in **System Settings → Privacy & Security → Accessibility**.
4. Open the extension and refresh its space and window data.

The extension uses SpaceAPI for live space updates and AppleScript for commands that require arguments or window automation. It should be treated as an example of the integration sequence rather than a required dependency.

## Full-screen windows

Full-screen spaces are managed differently from regular desktops. Some Accessibility operations require the target application to become active first, and DesktopRenamer may temporarily switch spaces or exit full screen before completing a window action. The command may therefore take longer than a regular desktop operation.

After any move, rearrangement, or full-screen transition, wait for the next SpaceAPI update before refreshing the Raycast UI. Do not cache space identifiers indefinitely.

## Diagnosing a missing result

- Confirm that DesktopRenamer’s API is enabled.
- Confirm Accessibility permission and restart DesktopRenamer after changing it.
- Ensure the extension subscribes before posting SpaceAPI requests.
- Re-request `GetSpaceList` after displays or full-screen applications change.
- Use `osascript` to test the AppleScript surface independently of Raycast.
