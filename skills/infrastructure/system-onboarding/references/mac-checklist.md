# macOS checklist

1. Install command-line developer tools and a supported package manager before adding
   language runtimes. Verify the architecture and package prefix rather than assuming
   an Intel-specific location.
2. Install the requested Python and Node.js versions, then verify the executable path
   and version in a new shell session.
3. Install each agent runtime through its supported distribution and complete native
   authentication without copying credentials into a project or synchronization root.
4. Create provider-specific configuration directories under the user's home directory.
   Merge reviewed templates, preserve local overrides and restart desktop applications
   completely when required for configuration readback.
5. Keep virtual environments, dependency caches, keys and large runtime artifacts out
   of cloud-synchronized directories. Clear quarantine attributes only when the source
   is trusted and the operation is appropriate for the current security policy.
6. Verify rule loading, skill discovery, optional integrations and scheduler state on
   the target host. Record unsupported features as gaps rather than substituting an
   undocumented configuration edit.
