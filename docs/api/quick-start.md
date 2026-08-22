# API Quick Start

This example shows the complete request flow for a Swift client using SpaceAPI.

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
