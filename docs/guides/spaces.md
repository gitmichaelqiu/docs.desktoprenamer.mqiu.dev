# Spaces and Full-Screen Apps

DesktopRenamer distinguishes regular Mission Control spaces from fullscreen application spaces.

Regular spaces can be named and manually reordered from **Settings → Spaces**. Drag a row to a new position, or use the launcher and AppleScript rearrangement commands.

Fullscreen spaces are owned by the application that created them. Their displayed names are derived from that application, and macOS may recreate or reposition them during fullscreen transitions.

## Automatic fullscreen placement

When **Keep full-screen spaces next to source desktop** is enabled, DesktopRenamer attempts to place a newly created fullscreen space immediately after the desktop from which the app entered fullscreen. The operation is asynchronous because Mission Control state is not stable during the transition.

## Limitations

- Space identifiers are system-managed and can change after display changes, sleep/wake, or Mission Control updates.
- Rearrangement requires a macOS version that exposes the native operation.
- Window movement across fullscreen spaces may temporarily enter or exit fullscreen to complete the operation.
- Multiple displays have independent space sequences.
