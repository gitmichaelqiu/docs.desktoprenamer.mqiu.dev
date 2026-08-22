# Troubleshooting

## The launcher or shortcuts do nothing

Confirm that DesktopRenamer is enabled under **System Settings → Privacy & Security → Accessibility**. If the permission was recently changed, quit and reopen DesktopRenamer.

## A window move fails

Make sure the source and target spaces still exist, then refresh labels from the menu bar or API. Fullscreen applications may need to be active before macOS exposes their Accessibility window hierarchy.

## Space names or preview labels are stale

Use **Reload Space Labels** from the menu bar or AppleScript. Display changes, sleep/wake, and fullscreen transitions can temporarily invalidate Mission Control bindings; the app retries reconciliation after these events.

## Rearrangement is unavailable

Native rearrangement depends on private system behavior that can vary by macOS release. Verify Accessibility permission, ensure Mission Control is available, and wait for any current rearrangement to finish before starting another operation.

## API clients receive no notifications

Check that the API is enabled in **Settings → General → Advanced** and that the client subscribes to `DistributedNotificationCenter` before posting its request notification. Always request a fresh snapshot after reconnecting.
