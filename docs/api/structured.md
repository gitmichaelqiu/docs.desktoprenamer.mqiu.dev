# Structured API

The structured SpaceAPI is the first formally versioned API contract. It is available from contract version **1.0.0** and uses JSON-RPC 2.0 as its message format. JSON-RPC 2.0 is the transport envelope and is versioned independently from the API contract.

The legacy SpaceAPI notifications, user-info keys, delimiter formats, and AppleScript commands remain supported. New integrations should prefer this page's structured protocol.

## Distributed notification channels

Structured messages use dedicated `DistributedNotificationCenter` channels:

| Channel | Direction | Purpose |
| --- | --- | --- |
| `com.michaelqiu.DesktopRenamer.RPCRequest` | Client → app | JSON-RPC requests. |
| `com.michaelqiu.DesktopRenamer.RPCResponse` | App → client | Correlated JSON-RPC responses. |
| `com.michaelqiu.DesktopRenamer.RPCEvent` | App → clients | JSON-RPC notifications for state changes. |

Every notification carries exactly one transport value in `userInfo`:

```swift
["payload": String]
```

`payload` is UTF-8 JSON encoded as a string. Do not put individual JSON fields beside `payload`; keeping one string value avoids Foundation bridging differences between Swift, JXA, and other clients. Register response observers before posting a request.

## JSON-RPC envelopes

Requests use a non-empty string ID. Named parameters are a JSON object, and may be omitted when the method has no parameters:

```json
{
  "jsonrpc": "2.0",
  "id": "9f3a8d40-2d38-4bf9-9c0c-790bd38f7598",
  "method": "getSpaceSnapshot"
}
```

An operation with parameters looks like this:

```json
{
  "jsonrpc": "2.0",
  "id": "4d72d2b4-c6b7-41ee-9aef-15fe1b8d9a9b",
  "method": "switchToSpace",
  "params": {
    "spaceID": "SPACE-ID"
  }
}
```

Successful responses contain exactly one `result`:

```json
{
  "jsonrpc": "2.0",
  "id": "4d72d2b4-c6b7-41ee-9aef-15fe1b8d9a9b",
  "result": {
    "accepted": true
  }
}
```

Errors contain exactly one `error`. Parameter errors include machine-readable metadata when available:

```json
{
  "jsonrpc": "2.0",
  "id": "4d72d2b4-c6b7-41ee-9aef-15fe1b8d9a9b",
  "error": {
    "code": -32602,
    "message": "Missing required parameter 'spaceID'.",
    "data": {
      "parameter": "spaceID",
      "expected": "string",
      "command": "switchToSpace"
    }
  }
}
```

Every response includes the `id` member. It is the request's non-empty string ID for a normal response, or explicit `null` when the server cannot recover an ID from a malformed request. Clients should accept the latter while matching normal responses only by their original request ID.

Events are JSON-RPC notifications and therefore have no ID or response. The current event is `stateChanged`:

```json
{
  "jsonrpc": "2.0",
  "method": "stateChanged",
  "params": {
    "reason": "activeSpaceChanged",
    "snapshot": {
      "apiVersion": "1.0.0",
      "revision": 18,
      "timestamp": "2026-08-31T07:00:00Z",
      "currentSpaceIDs": ["SPACE-ID"],
      "currentSpaceName": "Writing",
      "spaces": []
    }
  }
}
```

## Typed values

### Space

Each space object contains:

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Current Mission Control managed-space identifier. |
| `name` | string | User-facing name. |
| `displayID` | string | Display identifier. |
| `displayName` | string | Localized display name when available. |
| `number` | integer | Space number on its display. |
| `isFullscreen` | Boolean | Whether the space belongs to a full-screen app. |
| `appName` | string or `null` | Full-screen app name, when available. |
| `appPath` | string or `null` | Full-screen app path, when available. |
| `globalShortcutNumber` | integer or `null` | Configured global shortcut number, when available. |

### Space snapshot

`getSpaceSnapshot` returns a versioned snapshot:

```json
{
  "apiVersion": "1.0.0",
  "revision": 18,
  "timestamp": "2026-08-31T07:00:00Z",
  "currentSpaceIDs": ["SPACE-ID"],
  "currentSpaceName": "Writing",
  "spaces": [/* space objects */]
}
```

`getAllSpaces` returns an array of space objects. Use `getSpaceSnapshot` when the current-space values, revision, and timestamp are also needed.

### Window snapshot

`getWindows` returns a versioned snapshot containing `spaces` and `windows`:

```json
{
  "apiVersion": "1.0.0",
  "revision": 18,
  "timestamp": "2026-08-31T07:00:00Z",
  "spaces": [/* space objects */],
  "windows": [
    {
      "id": 1234,
      "pid": 5678,
      "ownerName": "Example",
      "appPath": "/Applications/Example.app",
      "title": "Document | Notes",
      "spaceID": "SPACE-ID",
      "isMinimized": false,
      "isHidden": false
    }
  ]
}
```

`appPath` and `title` are nullable because macOS may not expose them. Structured JSON responses include these keys with `null` when unavailable; a non-JSON representation such as an AppleScript record may omit the corresponding property. Titles, names, paths, Unicode, quotes, newlines, and delimiter characters are ordinary string values in this protocol and require no escaping beyond JSON encoding.

### Operation result

Accepted asynchronous operations return:

```json
{
  "accepted": true
}
```

`accepted` means that DesktopRenamer accepted the operation for processing. It does not mean that Mission Control or Accessibility has finished applying it. Re-read a snapshot or wait for a later state event before updating a client UI. Toggle methods return a Boolean containing the new state.

## Method catalog

| Method | Parameters | Result |
| --- | --- | --- |
| `getAPIInfo` | — | API information object. |
| `getAPIVersion` | — | Contract version string. |
| `getSpaceSnapshot` | — | Space snapshot. |
| `getCurrentSpaceName` | — | String. |
| `getCurrentSpaceID` | — | Array of current space IDs. |
| `getAllSpaces` | — | Array of space objects. |
| `getWindows` | — | Window snapshot. |
| `switchToSpace` | `spaceID` | Operation result. |
| `renameCurrentSpace` | `name` | Operation result. |
| `renameSpace` | `spaceID`, `name` | Operation result. |
| `rearrangeSpace` | `spaceID`, `direction` (`up` or `down`) | Operation result. |
| `moveWindowNext` / `moveWindowPrevious` | — | Operation result. |
| `moveWindowToSpace` | `spaceID` | Operation result. |
| `reloadSpaceLabels` | — | Operation result. |
| `toggleMenubar` / `toggleLauncher` | — | New visibility Boolean. |
| `toggleLabels` / `toggleActiveLabel` / `togglePreviewLabel` | — | New label-state Boolean. |
| `toggleDesktopVisibility` | — | New desktop-visibility Boolean. |
| `focusWindow` | `windowID`, `pid` | Operation result. |
| `executeWindowAction` | `windowID`, `pid`, `action` | Operation result. |
| `moveSpecificWindow` | `windowID`, optional `pid`, `fromSpaceID`, `targetSpaceID` | Operation result. |

`windowID` and `pid` are integers. The optional `pid` in `moveSpecificWindow` can be omitted only when both space IDs are numeric values usable by the low-level move operation. Unknown method parameters are rejected rather than silently ignored.

## API information

`getAPIInfo` reports the capabilities needed for negotiation:

```json
{
  "contractVersion": "1.0.0",
  "jsonRPCVersion": "2.0",
  "supportedMethods": ["getAPIInfo", "getSpaceSnapshot"],
  "legacyNotifications": true,
  "legacyCompatibility": "supported",
  "eventNotifications": true,
  "eventCapabilities": ["stateChanged"],
  "maxPayloadBytes": 1048576
}
```

Clients should inspect the complete `supportedMethods` array rather than assuming that a future minor version supports every method. Unknown response fields must be ignored so compatible clients can survive additive fields.

## Validation and errors

Requests are rejected when the payload is not valid UTF-8 JSON, is not a JSON object, uses a different JSON-RPC version, has no non-empty string ID, contains an unknown parameter, supplies the wrong parameter type, or exceeds **1 MiB (1,048,576 bytes)**. The server does not execute a partially valid request.

| Code | Meaning |
| --- | --- |
| `-32700` | Invalid JSON. |
| `-32600` | Invalid JSON-RPC request or response shape. |
| `-32601` | Unsupported method. |
| `-32602` | Invalid or missing parameters. |
| `-32603` | Unexpected server-side failure. |
| `-32001` | SpaceAPI is disabled. |
| `-32002` | DesktopRenamer is not ready. |
| `-32004` | Requested operation failed. |
| `-32006` | Payload exceeds the size limit. |

The `data` object is optional. When present, `parameter`, `expected`, and `command` identify the validation failure without requiring clients to parse the human-readable message.

## Re-synchronizing after events

Distributed notifications are broadcasts and can be dropped while a client is suspended or disconnected. Track the `revision` in every snapshot and event:

1. Subscribe to `RPCEvent`.
2. Request `getSpaceSnapshot` and record its revision.
3. Ignore an event whose revision is not newer than the last applied revision.
4. If the next revision is not greater by one, request a fresh `getSpaceSnapshot` before applying later UI state.
5. Re-fetch after reconnecting, display changes, sleep/wake, or an API enabled transition.

Revisions are monotonic during an app process lifetime. A newly launched app can start a new revision sequence, so clients should treat a new process or API version response as a resynchronization boundary. Timestamps are ISO 8601 strings for diagnostics and ordering context; revision remains the authoritative state sequence.

## Swift client example

```swift
import Foundation

let center = DistributedNotificationCenter.default()
let requestID = UUID().uuidString
var receivedResponse = false

let observer = center.addObserver(
    forName: Notification.Name("com.michaelqiu.DesktopRenamer.RPCResponse"),
    object: nil,
    queue: .main
) { notification in
    guard let payload = notification.userInfo?["payload"] as? String,
          let data = payload.data(using: .utf8),
          let object = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
          object["id"] as? String == requestID else {
        return
    }
    receivedResponse = true
    print(object)
}

let request: [String: Any] = [
    "jsonrpc": "2.0",
    "id": requestID,
    "method": "getSpaceSnapshot"
]
do {
    let data = try JSONSerialization.data(withJSONObject: request)
    guard let payload = String(data: data, encoding: .utf8) else { throw CocoaError(.fileReadCorruptFile) }
    center.post(
        name: Notification.Name("com.michaelqiu.DesktopRenamer.RPCRequest"),
        object: nil,
        userInfo: ["payload": payload],
        deliverImmediately: true
    )
} catch {
    print("Could not encode request:", error)
}

let deadline = Date().addingTimeInterval(3)
while !receivedResponse && Date() < deadline {
    RunLoop.main.run(until: Date(timeIntervalSinceNow: 0.01))
}
center.removeObserver(observer)
```

The example demonstrates correlation only; production clients should decode and validate the complete response, handle the documented error codes, and keep the observer alive until the response or timeout is received.

## Legacy migration

Existing clients can continue using [legacy SpaceAPI](space-api.md) without changes. To migrate incrementally:

1. Keep the legacy listener as a fallback.
2. Request `getAPIInfo` on `RPCRequest`.
3. Use structured snapshots and UUID request IDs when the reported contract is `1.0.0` or newer.
4. Fall back to the legacy notification and delimiter protocol only when the structured channel is unavailable or the client explicitly targets an older app.
5. Do not split structured names or titles on `~`, `|`, or newlines.
