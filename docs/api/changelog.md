# API Changelog

This page records changes to the external contract, independently of DesktopRenamer’s app release version.

## 1.0.0

Added an additive structured API:

- JSON-RPC 2.0 messages on dedicated request, response, and event notifications.
- Typed space, window, snapshot, API-information, and operation-result values.
- UUID request correlation, strict parameter validation, stable error codes, and a 1 MiB payload limit.
- Revisioned and timestamped state-change snapshots for client re-synchronization after dropped distributed notifications.
- Typed AppleScript records and structured read commands.
- Continued support for all legacy SpaceAPI notifications, payload keys, delimiter formats, and AppleScript commands.

## Legacy (pre-1.0)

Initial documented contract:

- SpaceAPI active-space and space-list snapshots.
- API version discovery through SpaceAPI and AppleScript.
- Space naming, switching, and one-step rearrangement commands.
- Window inspection, focus, movement, and window actions through AppleScript.
- API enabled/disabled state notification.

Clients should ignore unknown dictionary fields and preserve their existing behavior when a newer compatible version adds fields or commands.
