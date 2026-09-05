# API overview

DesktopRenamer exposes three automation surfaces:

1. **SpaceAPI**, based on `DistributedNotificationCenter`. New integrations should use its [structured protocol](spaceapi/structured.md); existing clients can continue using the [legacy format](spaceapi/legacy-format.md).
2. **AppleScript**, for commands that switch, rename, rearrange, inspect, and move windows. Start with the [AppleScript overview](applescript/index.md).

The API is enabled by default for existing installations and can be controlled from **Settings → General → Advanced → Enable SpaceAPI**. Clients should handle the API-disabled state and verify the [contract version](versioning.md). Choose the [structured SpaceAPI protocol](spaceapi/structured.md) for new integrations, or the [legacy format](spaceapi/legacy-format.md) when maintaining an existing client.

Use the navigation to choose the integration surface first. The same concepts—spaces, windows, asynchronous operations, and API availability—are described separately for each calling method.

## Space identifiers

Use the SpaceAPI space snapshot or AppleScript's `get all spaces` command to obtain current identifiers. Do not persist a space ID indefinitely: macOS can replace identifiers after display or Mission Control changes.

## Main-thread behavior

Commands that change spaces or windows are asynchronous where required by AppKit and Accessibility APIs. A successful command dispatch means the operation was accepted; clients should observe subsequent space notifications before assuming the UI has settled.

## Compatibility

The API version is independent of the DesktopRenamer app version. See [API Versioning](versioning.md) before consuming new fields or commands. Contract `1.0.0` uses JSON-RPC `2.0` as its message envelope.

## Integration sequence

For a long-running client:

1. Confirm that the API is enabled.
2. Subscribe to response notifications before posting requests.
3. Request the API version and a complete space snapshot; if you use the legacy notifications, request the active-space and space-list snapshots instead.
4. Treat each response as a complete snapshot and reconcile it by identifier.
5. Listen for subsequent broadcasts and refresh after display, sleep/wake, or fullscreen changes.

Space and window operations are not transactional. A command can be accepted before Mission Control finishes applying it, so clients should wait for a later notification or re-read the state before updating their UI.

## Error and permission model

Legacy snapshot and version requests have no synchronous error response. A missing response usually means that the API is disabled, the client subscribed after posting a request, or DesktopRenamer is still reconciling Mission Control. The legacy `PerformCommand` channel reports failures through `CommandResult`. Structured SpaceAPI returns JSON-RPC errors, including an explicit API-disabled code. AppleScript reports `API Disabled` for commands with a defined return value; asynchronous commands can return before the requested operation succeeds.

Window inspection and control operations require Accessibility permission. Space rearrangement uses macOS's native space-management operation and can also fail when that backend is unavailable or another rearrangement is already in progress. Clients should surface a permission or retry action instead of retrying indefinitely.
