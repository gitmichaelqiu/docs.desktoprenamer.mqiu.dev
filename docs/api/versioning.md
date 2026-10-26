# API versioning

The current external API contract version is **1.3.1**.

This version is intentionally independent from DesktopRenamer's marketing and build version. A client can therefore be compatible with an API contract even when the app receives an ordinary bug-fix release.

## Compatibility policy

- **Major** version changes indicate incompatible commands, notification changes, payload shape/type changes, or behavior changes without a compatibility path.
- **Minor** version changes add backwards-compatible capabilities or behavior. Opaque identifier values may evolve when clients can keep treating them as strings, passing them through unchanged, and old identifiers remain accepted while still valid.
- **Patch** version changes represent compatible corrections or clarifications.

The legacy notification and delimiter-based APIs predate formal API versioning and are treated as **pre-1.0.0 compatibility surfaces**. Their existing names, payloads, and behavior remain supported.

Contract `1.0.0` was the first formally versioned API contract. It added the structured JSON-RPC 2.0 transport, typed snapshots, typed AppleScript records, request validation, and revisioned state events. Contract `1.1.0` added Space Lock capabilities without changing legacy delimiter shapes or the JSON-RPC envelope. Contract `1.2.0` exposes persistent DesktopRenamer-owned IDs in structured space records, current-space IDs, window space references, and operation parameters. Structured operations continue to accept a currently valid ManagedSpaceID for migration compatibility. JSON-RPC `2.0` identifies the message envelope and is independent of the API contract version.

Contract `1.3.0` adds an authenticated Unix-domain socket transport and opt-in SpaceAPI access restriction. The existing DNC transport remains available when restriction is off. When restriction is on, only approved app code identities can use the socket; legacy DNC requests and broadcasts are disabled. See [SpaceAPI permissions](spaceapi/structured.md#access-control) for client approval and compatibility behavior.

The released 1.3.0 implementation reports `returnToOriginalSpace` in `getAPIInfo` and supports the optional `deferAutomaticReturn` parameter on window moves and actions. When automatic return is enabled, these operations return to the spaces that were active before the operation; clients can defer that behavior while batching operations.

When no saved access policy exists, the released implementation enables SpaceAPI access restriction by default and preserves an existing saved choice. DNC-only clients require restriction to be turned off.

Contract `1.3.1` adds the optional `managedSpaceID` field to structured SpaceAPI and AppleScript space records. It maps each stable DesktopRenamer `id` to the current macOS ManagedSpaceID, allowing clients to make OS-specific calls without deriving the mapping from order, number, or name. Older 1.3.0 builds omit the field. The ManagedSpaceID can change and is suitable only for immediate macOS API calls; continue using `id` for saved references.

The legacy notification channels, `PerformCommand`/`CommandResult` transport, and delimiter payloads remain supported and keep their ManagedSpaceID semantics; they are not converted in place, so existing clients can migrate independently. The preferred distributed-notification namespace is `dev.mqiu.DesktopRenamer`, matching the current app bundle identifier. DesktopRenamer also accepts and emits the `com.michaelqiu.DesktopRenamer` namespace solely for compatibility with existing integrations; new clients should use `dev.mqiu.DesktopRenamer`. A legacy response's `apiVersion` identifies the app's current contract marker; it does not prove that the structured JSON-RPC channels are available. Use `getAPIInfo` to negotiate structured capabilities. See the [structured SpaceAPI](spaceapi/structured.md) and [legacy format](spaceapi/legacy-format.md) guides.

Clients should accept unknown fields and should compare versions semantically rather than comparing app versions.

## Reading the version

AppleScript:

```applescript
tell application "DesktopRenamer"
    get api version
end tell
```

SpaceAPI clients can request `getAPIInfo` over the authenticated socket or, when using the compatibility transport, post the preferred `dev.mqiu.DesktopRenamer.GetAPIVersion` distributed notification and receive `dev.mqiu.DesktopRenamer.ReturnAPIVersion` with an `apiVersion` user-info value. The corresponding `com.michaelqiu.DesktopRenamer` names remain accepted only for compatibility.
