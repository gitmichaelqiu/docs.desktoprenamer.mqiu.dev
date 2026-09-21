# API versioning

The current external API contract version is **1.1.0**.

This version is intentionally independent from DesktopRenamer's marketing and build version. A client can therefore be compatible with an API contract even when the app receives an ordinary bug-fix release.

## Compatibility policy

- **Major** version changes indicate incompatible command, notification, or payload changes.
- **Minor** version changes add backwards-compatible commands or fields.
- **Patch** version changes represent compatible corrections or clarifications.

The legacy notification and delimiter-based APIs predate formal API versioning and are treated as **pre-1.0.0 compatibility surfaces**. Their existing names, payloads, and behavior remain supported.

Contract `1.0.0` was the first formally versioned API contract. It added the structured JSON-RPC 2.0 transport, typed snapshots, typed AppleScript records, request validation, and revisioned state events. Contract `1.1.0` adds Space Lock capabilities without changing legacy delimiter shapes or the JSON-RPC envelope; the legacy JSON snapshot receives additive fields. JSON-RPC `2.0` identifies the message envelope and is independent of the contract major version.

The legacy notification channels, `PerformCommand`/`CommandResult` transport, and delimiter payloads remain supported. They are not converted in place, so existing clients can migrate independently. The preferred distributed-notification namespace is `dev.mqiu.DesktopRenamer`, matching the current app bundle identifier. DesktopRenamer also accepts and emits the `com.michaelqiu.DesktopRenamer` namespace solely for compatibility with existing integrations; new clients should use `dev.mqiu.DesktopRenamer`. A legacy response's `apiVersion` identifies the app's current contract marker; it does not prove that the structured JSON-RPC channels are available. Use `getAPIInfo` to negotiate structured capabilities. See the [structured SpaceAPI](spaceapi/structured.md) and [legacy format](spaceapi/legacy-format.md) guides.

Clients should accept unknown fields and should compare versions semantically rather than comparing app versions.

## Reading the version

AppleScript:

```applescript
tell application "DesktopRenamer"
    get api version
end tell
```

SpaceAPI clients can post the preferred `dev.mqiu.DesktopRenamer.GetAPIVersion` distributed notification and receive `dev.mqiu.DesktopRenamer.ReturnAPIVersion` with an `apiVersion` user-info value. The corresponding `com.michaelqiu.DesktopRenamer` names remain accepted only for compatibility.
