# Post-install verification

Verify each selected runtime with a version check and a minimal, non-sensitive task.
Confirm that the intended rule surface is loaded, the explicitly deployed skills are
discoverable and every requested integration appears through the provider's supported
status or user interface.

For desktop applications, distinguish a changed configuration file from a configuration
the application has actually loaded. For command-line tools, distinguish successful
installation from authenticated operation. For schedulers, distinguish task definition,
native registration, execution and successful outcome.

Inspect synchronization destinations for credentials, private prompts and raw logs before
publishing any receipt. If a secret is found, revoke or rotate it through the owning
provider, remove it from the shared surface according to the applicable policy and repeat
the check. Completion is a local, evidence-backed state, not a claim inferred from a
copied template.
