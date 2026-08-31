# API Overview

DesktopRenamer exposes three automation surfaces:

1. **Structured SpaceAPI**, based on JSON-RPC 2.0 over `DistributedNotificationCenter`, for typed reads, operations, and state events.
2. **Legacy SpaceAPI**, based on `DistributedNotificationCenter`, for existing current-space and space-list integrations.
3. **AppleScript**, for commands that switch, rename, rearrange, inspect, and move windows.

The API is enabled by default for existing installations and can be controlled from **Settings → General → Advanced**. Clients should handle the API-disabled state and verify the [contract version](versioning.md). New integrations should start with the [Structured API](structured.md); the [legacy SpaceAPI](space-api.md) remains available for compatibility.

## Space identifiers

Use `get all spaces` through AppleScript or the `ReturnSpaceList` notification to obtain current identifiers. Do not persist a space ID indefinitely: macOS can replace identifiers after display or Mission Control changes.

## Main-thread behavior

Commands that change spaces or windows are asynchronous where required by AppKit and Accessibility APIs. A successful command dispatch means the operation was accepted; clients should observe subsequent space notifications before assuming the UI has settled.

## Compatibility

The API version is independent of the DesktopRenamer app version. See [API Versioning](versioning.md) before consuming new fields or commands. Contract `1.0.0` uses JSON-RPC `2.0` as its message envelope.

## Integration sequence

For a long-running client:

1. Confirm that the API is enabled.
2. Subscribe to response notifications before posting requests.
3. Request the API version, active-space snapshot, and space-list snapshot.
4. Treat each response as a complete snapshot and reconcile it by identifier.
5. Listen for subsequent broadcasts and refresh after display, sleep/wake, or fullscreen changes.

Space and window operations are not transactional. A command can be accepted before Mission Control finishes applying it, so clients should wait for a later notification or re-read the state before updating their UI.

## Error and permission model

Legacy SpaceAPI has no synchronous error response. A missing legacy response usually means that the API is disabled, the client subscribed after posting a request, or DesktopRenamer is still reconciling Mission Control. Structured SpaceAPI returns JSON-RPC errors, including an explicit API-disabled code. AppleScript reports `API Disabled` for commands with a defined return value; asynchronous commands can return before the requested operation succeeds.

Window and rearrangement operations additionally require Accessibility permission. Clients should surface a permission action instead of retrying indefinitely.
