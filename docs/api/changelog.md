# API changelog

This page records changes to the external contract, independently of DesktopRenamer’s app release version.

## 1.2.0

Changed structured space identity semantics:

- The `id` field in structured space records is now an opaque ID generated and persisted by DesktopRenamer rather than the current macOS ManagedSpaceID. Clients should treat it as a string and pass it through unchanged.
- Structured current-space IDs, window `spaceID`/`spaceIDs`, and space-operation parameters use the DesktopRenamer-owned ID.
- Structured operations also accept a ManagedSpaceID while it still identifies a current space, to ease migration for clients that cached IDs before upgrading. New integrations should use the stable IDs from structured responses.
- Structured AppleScript records use the same persistent IDs. Legacy notifications, delimiter payloads, and AppleScript's `get all spaces` continue to expose ManagedSpaceIDs for compatibility.
- IDs are retained across app and system restarts, reordering, and display changes while macOS continues to report the same persistent space UUID. A deleted and recreated space gets a new ID when macOS reports its new persistent identity or DesktopRenamer observes it as distinct. For spaces without a persistent UUID, the ID is guaranteed only during the current boot and is renewed after reboot rather than guessing by position.

## 1.1.0

Added additive Space Lock capabilities to the structured contract:

- `isLocked` on structured space records, including structured AppleScript records.
- `movedWindowsCount` on space snapshots so clients can show the pending restore queue.
- `toggleLockSpace` and `restoreMovedWindows` JSON-RPC methods.
- `lockStateChanged` and `movedWindowsChanged` state-event reasons.
- Fullscreen spaces remain in the space list but cannot be locked.
- Preferred all SpaceAPI distributed-notification names under `dev.mqiu.DesktopRenamer`, matching the current bundle identifier. The previous `com.michaelqiu.DesktopRenamer` namespace remains accepted and emitted only for compatibility.

The legacy `getAllSpaces` delimiter payload remains unchanged and still returns six `~`-separated fields. The legacy JSON `getSpaceSnapshot` gains the additive `movedWindowsCount` and `isLocked` fields. Use structured JSON-RPC `getAllSpaces` or `get structured spaces` when you need typed records with lock state.

## 1.0.0

Added an additive structured API:

- JSON-RPC 2.0 messages on dedicated request, response, and event notifications.
- Typed space, window, snapshot, API-information, and operation-result values.
- UUID request correlation, strict parameter validation, stable error codes, and a 1 MiB payload limit.
- Revisioned and timestamped state-change snapshots for client re-synchronization after dropped distributed notifications.
- Typed AppleScript records and structured read commands.
- Continued support for all legacy SpaceAPI notifications, including the `PerformCommand`/`CommandResult` channel, payload keys, delimiter formats, and AppleScript commands.

## Legacy format (pre-1.0.0)

Initial compatibility contract, before formal API versioning:

- SpaceAPI active-space and space-list snapshots.
- API version discovery through SpaceAPI and AppleScript.
- Space naming, switching, and one-step rearrangement commands.
- Window inspection, focus, movement, and window actions through AppleScript.
- API enabled/disabled state notification.

Clients should ignore unknown dictionary fields and preserve their existing behavior when a newer compatible version adds fields or commands.
