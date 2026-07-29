# Windows checklist

1. Install current operating-system updates, Git and the required supported runtimes.
   Confirm each executable with its native version command.
2. Install Python from an official distribution, enable UTF-8 behaviour where the
   runtime requires it, and update the package installer in the user environment.
3. Install Node.js LTS only when a selected runtime requires it. Verify the selected
   package manager before installing global command-line clients.
4. Install each agent application through its supported installer and complete login
   through the provider's native flow. Do not save tokens in a shared folder.
5. Create only the configuration directories required by that provider. Merge a
   reviewed template with existing state, then restart the application when its
   documentation requires a full quit.
6. Keep virtual environments, dependency caches and large binary artifacts outside
   cloud-synchronized work trees. Use normal PowerShell path handling rather than
   shell-specific redirection conventions that can create reserved device files.
7. Verify the rule loader, skill discovery, MCP connectivity and any requested
   scheduler registration with native readback before recording completion.
