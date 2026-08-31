# API Quick Start

This example shows the preferred request flow for a Swift client using the [structured JSON-RPC API](structured.md). The legacy example below remains useful for existing integrations and continues to work unchanged.

## Structured request

Register the response observer before posting the request. Every structured response is carried as a JSON string in the `payload` user-info key and must be matched by its request ID.

```swift
import Foundation

let center = DistributedNotificationCenter.default()
let requestID = UUID().uuidString
let responseName = Notification.Name("com.michaelqiu.DesktopRenamer.RPCResponse")
let requestName = Notification.Name("com.michaelqiu.DesktopRenamer.RPCRequest")

var observer: NSObjectProtocol?
observer = center.addObserver(forName: responseName, object: nil, queue: .main) { notification in
    guard let payload = notification.userInfo?["payload"] as? String,
          let data = payload.data(using: .utf8),
          let response = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
          response["id"] as? String == requestID
    else { return }

    print(response)
    if let observer { center.removeObserver(observer) }
}

let request: [String: Any] = [
    "jsonrpc": "2.0",
    "id": requestID,
    "method": "getSpaceSnapshot"
]
if let requestData = try? JSONSerialization.data(withJSONObject: request),
   let payload = String(data: requestData, encoding: .utf8) {
    center.post(
        name: requestName,
        object: nil,
        userInfo: ["payload": payload],
        deliverImmediately: true
    )
} else {
    print("Could not encode SpaceAPI request")
}
```

For production code, replace the compact `JSONSerialization` handling with a Codable model and keep the observer alive until the matching response or a timeout is received.

```swift
import Foundation

let center = DistributedNotificationCenter.default()
let prefix = "com.michaelqiu.DesktopRenamer"

let activeName = Notification.Name("\(prefix).ReturnActiveSpace")
let listName = Notification.Name("\(prefix).ReturnSpaceList")

center.addObserver(forName: activeName, object: nil, queue: .main) { notification in
    let values = notification.userInfo ?? [:]
    print("Active:", values["spaceName"] ?? "Unknown")
}

center.addObserver(forName: listName, object: nil, queue: .main) { notification in
    let values = notification.userInfo ?? [:]
    let spaces = values["spaces"] as? [[String: Any]] ?? []
    print("Known spaces:", spaces.count)
}

// Subscribe before requesting snapshots.
center.post(name: Notification.Name("\(prefix).GetActiveSpace"), object: nil)
center.post(name: Notification.Name("\(prefix).GetSpaceList"), object: nil)

RunLoop.main.run()
```

The request notifications do not carry a payload. The response arrives through `userInfo`. Keep the observers alive for the lifetime of the client, and request fresh snapshots after reconnecting or receiving `ReturnAPIState` with `isEnabled == false` followed by `true`.

For a one-off command, AppleScript is usually simpler:

```bash
osascript -e 'tell application "DesktopRenamer" to get all spaces'
```

Use the returned identifiers for later commands rather than assuming that space numbers or identifiers remain stable.
