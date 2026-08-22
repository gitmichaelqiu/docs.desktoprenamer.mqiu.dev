# SpaceAPI

SpaceAPI uses `DistributedNotificationCenter`. The notification prefix is:

```text
com.michaelqiu.DesktopRenamer
```

## Request and response notifications

| Request | Response | Purpose |
| --- | --- | --- |
| `GetActiveSpace` | `ReturnActiveSpace` | Read the currently visible space on each display. |
| `GetSpaceList` | `ReturnSpaceList` | Read the known spaces and names. |
| `GetAPIVersion` | `ReturnAPIVersion` | Read the external API contract version. |
| — | `ReturnAPIState` | Receive API enabled/disabled changes. |

## Active-space payload

`ReturnActiveSpace` includes:

```text
apiVersion: String
spaceUUID: String
spaceName: String
spaceNumber: NSNumber
```

## Space-list payload

`ReturnSpaceList` includes an `apiVersion` value and a `spaces` array. Each entry contains:

```text
spaceUUID: String
spaceName: String
spaceNumber: NSNumber
```

The app broadcasts updates when the active space or stored names change. A client should request an initial snapshot after subscribing, then reconcile subsequent broadcasts by identifier.

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
