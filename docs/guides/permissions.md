# Permissions and System Settings

DesktopRenamer uses macOS Accessibility APIs for operations that involve global input, windows, or Mission Control state.

Enable **System Settings → Privacy & Security → Accessibility → DesktopRenamer** for:

- Global keyboard shortcuts.
- Trackpad gesture switching.
- Reading the active application and its windows.
- Moving or focusing windows across spaces.
- Native space rearrangement through the system UI.

Some gesture configurations can conflict with macOS. If DesktopRenamer replaces a switching gesture, disable the corresponding **Swipe between full-screen applications** shortcut under **System Settings → Trackpad → More Gestures**, or choose a different finger count.

If permission is revoked while the app is running, re-enable it and restart DesktopRenamer so its accessibility clients are recreated.
