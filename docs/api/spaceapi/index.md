# SpaceAPI

SpaceAPI is DesktopRenamer's distributed-notification interface. It is useful for integrations that need to observe spaces or issue commands without launching AppleScript.

There are two SpaceAPI formats:

| Format | Use it when | Data shape |
| --- | --- | --- |
| [Structured protocol](structured.md) | Building a new integration. | JSON-RPC 2.0 messages containing typed JSON values. |
| [Legacy format](legacy-format.md) | Supporting an existing client. | Distributed notifications with the original user-info keys and delimiter-based strings. |

The structured protocol is the first formally versioned contract and should be the default for new clients. The legacy format remains supported but is not changed in place, so existing integrations can migrate on their own schedule.

## Common request flow

1. Register response observers before posting a request.
2. Confirm that the API is enabled.
3. Request an initial snapshot.
4. Reconcile updates by space identifier, not by array position.
5. Re-fetch after reconnecting or after a display, sleep/wake, or fullscreen change.

Distributed notifications are broadcasts and can be dropped. The structured protocol includes snapshot revisions so clients can detect a gap and fetch a complete snapshot again.

## Requirements

SpaceAPI is available when **Settings → General → Advanced → API** is enabled. A client does not need to activate or bring DesktopRenamer to the front. Requests that switch or rearrange spaces are asynchronous; observe a later state update before assuming Mission Control has settled.

For a typed contract, transport details, methods, and error handling, see the [structured protocol](structured.md). For existing notification names and payload keys, see the [legacy format](legacy-format.md).
