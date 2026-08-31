# API Versioning

The current external API contract version is **1.2.0**.

This version is intentionally independent from DesktopRenamer's marketing and build version. A client can therefore be compatible with an API contract even when the app receives an ordinary bug-fix release.

## Compatibility policy

- **Major** version changes indicate incompatible command, notification, or payload changes.
- **Minor** version changes add backwards-compatible commands or fields.
- **Patch** version changes represent compatible corrections or clarifications.

Contract `1.2.0` adds the structured JSON-RPC 2.0 transport, typed snapshots, typed AppleScript records, request validation, and revisioned state events. JSON-RPC `2.0` identifies the message envelope and is independent of the contract major version.

The legacy notification channels and delimiter payloads remain supported. They are not converted in place, so existing clients can migrate independently. See the [Structured API](structured.md) and [legacy SpaceAPI](space-api.md) guides.

Clients should accept unknown fields and should compare versions semantically rather than comparing app versions.

## Reading the version

AppleScript:

```applescript
tell application "DesktopRenamer"
    get api version
end tell
```

SpaceAPI clients can post the `com.michaelqiu.DesktopRenamer.GetAPIVersion` distributed notification and receive `com.michaelqiu.DesktopRenamer.ReturnAPIVersion` with an `apiVersion` user-info value.
