# SpaceAPI legacy format

This page documents the legacy notification names and delimiter-based payloads that remain available for existing clients. It is a compatibility reference, not a recommendation for new integrations. For new integrations, use the [structured SpaceAPI protocol](structured.md).

SpaceAPI uses `DistributedNotificationCenter`. The notification prefix is:

```text
com.michaelqiu.DesktopRenamer
```

## Request and response notifications

| Request | Response | Purpose |
| --- | --- | --- |
| `GetActiveSpace` | `ReturnActiveSpace` | Read the currently tracked active space. |
| `GetSpaceList` | `ReturnSpaceList` | Read the known spaces and names. |
| `GetAPIVersion` | `ReturnAPIVersion` | Read the external API contract version. |
| `PerformCommand` | `CommandResult` | Execute a named legacy command and receive its result. |
| — | `ReturnAPIState` | Receive API enabled/disabled changes. |

All notification names use the prefix `com.michaelqiu.DesktopRenamer`. Requests should be posted only after response observers have been registered. Legacy request notifications do not use the structured `payload` key.

## Active-space payload

`ReturnActiveSpace` includes:

```text
apiVersion: String
spaceUUID: String
spaceName: String
spaceNumber: NSNumber
```

This payload contains one `spaceUUID`; it is not a per-display array. Use structured `getCurrentSpaceID` or AppleScript `get current space id` when a client needs all currently visible space IDs.

## Space-list payload

`ReturnSpaceList` includes an `apiVersion` value and a `spaces` array. Each entry contains:

```text
spaceUUID: String
spaceName: String
spaceNumber: NSNumber
displayID: String
```

The app broadcasts updates when the active space or stored names change. A client should request an initial snapshot after subscribing, then reconcile subsequent broadcasts by identifier.

The delimiter formats are not escaped. A space name, display name, path, owner name, or title containing `~`, `|`, or a newline can make positional parsing ambiguous; use the structured protocol when those values must round-trip exactly.

## Legacy command channel

Post `PerformCommand` with a `userInfo` dictionary containing a command name and, when needed, string arguments:

```swift
import Foundation

let center = DistributedNotificationCenter.default()
let requestID = UUID().uuidString
let arguments = try JSONSerialization.data(
    withJSONObject: ["spaceID": "SPACE-ID", "name": "Research"]
)
let argumentsJSON = String(decoding: arguments, as: UTF8.self)

center.post(
    name: Notification.Name("com.michaelqiu.DesktopRenamer.PerformCommand"),
    object: nil,
    userInfo: [
        "requestID": requestID,
        "command": "renameSpace",
        "argumentsJSON": argumentsJSON
    ],
    deliverImmediately: true
)
```

`argumentsJSON` must be a JSON object whose values are strings. The app also accepts an `arguments` dictionary containing only `String` values. The request ID is optional; when it is missing or empty, DesktopRenamer generates one for the response.

The command channel accepts the legacy command names supported by the app, including `getAPIVersion`, `getSpaceSnapshot`, `getCurrentSpaceName`, `getCurrentSpaceID`, `getAllSpaces`, `switchToSpace`, `renameCurrentSpace`, `renameSpace`, `rearrangeSpace`, `moveWindowNext`, `moveWindowPrevious`, `moveWindowToSpace`, `reloadSpaceLabels`, the six `toggle...` commands, `getWindows`, `focusWindow`, `executeWindowAction`, and `moveSpecificWindow`. `getAPIInfo` is only a structured-protocol method and is not implemented by `PerformCommand`.

Successful `result` strings use these legacy shapes:

- `getSpaceSnapshot` returns JSON with `apiVersion`, `currentSpaceIDs`, `currentSpaceName`, and `spaces`. It has no structured `revision` or `timestamp`; its space records contain `id`, `name`, `displayID`, `displayName`, `number`, `isFullscreen`, and an optional `appPath`.
- `getAllSpaces` returns newline-delimited `ID~Name~DisplayName~Number~IsFullscreen~AppPath` records, and `getWindows` returns the delimiter format described in [AppleScript window automation](../applescript/windows.md).
- `getCurrentSpaceID` returns comma-separated current space IDs. `getAPIVersion` and `getCurrentSpaceName` return text.
- Mutating commands return an empty string. The six toggle commands return the new Boolean state as the string `true` or `false`.

`CommandResult` always includes `requestID`, `apiVersion`, and `success`. Successful results also include a string `result` (which may be empty); failures include an `error` string instead:

```text
requestID: String
apiVersion: String
success: Bool
result: String         # success only
error: String          # failure only
```

The legacy command channel uses the same string command arguments as the structured method names: for example, `direction` is `up` or `down`, window IDs and process IDs are positive integer strings, and `action` is one of `close`, `minimize`, `hide`, `enterFullScreen`, `exitFullScreen`, `quit`, or `restore`. When SpaceAPI is disabled, legacy request listeners are not active and no legacy response is sent.

## Payload reference

| Notification | `userInfo` | Notes |
| --- | --- | --- |
| `ReturnActiveSpace` | `apiVersion`, `spaceUUID`, `spaceName`, `spaceNumber` | `spaceNumber` is `0` for the synthetic `FULLSCREEN` value. |
| `ReturnSpaceList` | `apiVersion`, `spaces` | `spaces` is an array of dictionaries using the four space fields above, including `displayID`. |
| `ReturnAPIVersion` | `apiVersion` | Sent in response to `GetAPIVersion`. |
| `CommandResult` | `requestID`, `apiVersion`, `success`, and either `result` or `error` | Sent in response to `PerformCommand`; `result` is a string and may be empty. |
| `ReturnAPIState` | `isEnabled` | A Boolean indicating whether the listener is active. |

Snapshot and version requests have no request ID or error response. If one of those responses is missing, check API state and request a fresh snapshot after subscribing. `PerformCommand` reports validation and execution failures through `CommandResult` when the legacy listener is active.

## Swift example

```swift
let center = DistributedNotificationCenter.default()
let name = Notification.Name("com.michaelqiu.DesktopRenamer.ReturnActiveSpace")

center.addObserver(forName: name, object: nil, queue: .main) { notification in
    let spaceID = notification.userInfo?["spaceUUID"] as? String
    let spaceName = notification.userInfo?["spaceName"] as? String
    print(spaceID ?? "", spaceName ?? "")
}

center.post(name: Notification.Name("com.michaelqiu.DesktopRenamer.GetActiveSpace"), object: nil)
```
