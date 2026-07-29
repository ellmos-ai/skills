# Onboarding overview

The portable model separates local runtime state from shareable instructions. Keep
agent configuration, credentials, keys, caches and runtime logs on the target host.
Share only reviewed rules, portable skill definitions, sanitized configuration
templates and receipts that contain no secrets.

Before installation, define the target operating system, the required agent runtimes,
the selected rule and synchronization authorities, and the owner of each automation.
This prevents a copied workstation snapshot from becoming an accidental source of
truth. A synchronization surface may distribute approved artifacts, but it is not a
license to overwrite another host's configuration.

The safest sequence is bootstrap prerequisites, install runtimes, configure one
runtime at a time, verify local loading, add optional integrations, then establish
cross-host synchronization. Add automation last and keep it disabled until native
readback and its rollback path are proven.
