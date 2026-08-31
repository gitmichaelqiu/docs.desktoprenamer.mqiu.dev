# SpaceAPI legacy format

This page documents the legacy notification names and delimiter-based payloads that remain available for existing clients. It is a compatibility reference, not a recommendation for new integrations. For new integrations, use the [structured SpaceAPI protocol](structured.md).

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

All notification names use the prefix `com.michaelqiu.DesktopRenamer`. Requests should be posted only after response observers have been registered.

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
displayID: String
```

The app broadcasts updates when the active space or stored names change. A client should request an initial snapshot after subscribing, then reconcile subsequent broadcasts by identifier.

## Payload reference

| Notification | `userInfo` | Notes |
| --- | --- | --- |
| `ReturnActiveSpace` | `apiVersion`, `spaceUUID`, `spaceName`, `spaceNumber` | `spaceNumber` is `0` for the synthetic `FULLSCREEN` value. |
| `ReturnSpaceList` | `apiVersion`, `spaces` | `spaces` is an array of dictionaries using the four space fields above, including `displayID`. |
| `ReturnAPIVersion` | `apiVersion` | Sent in response to `GetAPIVersion`. |
| `ReturnAPIState` | `isEnabled` | A Boolean indicating whether the listener is active. |

The notification center does not provide a request error callback. If a response is missing, check API state and request a fresh snapshot after subscribing.

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
