# Live provider Limits repair — 2026-11-05

Source-mode daemon: reviewed source `07ba5e6b4d020e29acec8358fb655ecd29b84d6c`.
Existing installed desktop retains its earlier explicit artifact identity; its
ASAR hash and process were preserved. Production repository source was unchanged.

## Diagnosis and repair

The external quota collector was healthy and scheduled, but the local daemon was
stopped. The installed app therefore had no authenticated usage delivery and
showed dashes. Enabled only the existing private authenticated loopback daemon
under the user's login service manager: RunAtLoad and KeepAlive enabled, ten-
second restart throttle, existing wrapper/environment/credentials/state paths.
The disabled preparation template remains intact. No microphone or web backend
was enabled, and no authority/credential change or provider inference was needed.

Before activation, required executables/interpreter and existing desktop proof
were verified, no competing listener was present, optional assistant automatic
restoration was disabled, and all four SQLite stores were backed up consistently.
Private service/config/app preimages and rollback instructions are retained.

## Actual acceptance

- Installed daemon service is running with the same observed PID, bound only to
  loopback. Its source, wrapper, environment and installed desktop artifact hashes
  match their preimages. RunAtLoad/KeepAlive and owner-only service file verified.
- Anonymous protected reads are rejected. Existing desktop proof authenticates
  and receives a limits snapshot equal to the collector's real state.
- One existing read-only collector tick refreshed both providers successfully;
  observation ages meet each provider's configured freshness interval. The
  collector's existing ten-minute schedule and account setup remain unchanged.
- Actual installed desktop AX readback first recovered both provider values,
  including a real zero, and both existing conversation histories. After refresh,
  its changed value agrees with the current authenticated wire and state. Real
  percentages and account details remain private rather than in this record.
- No personal app restart/replacement, provider inference/login/trust acceptance,
  mic startup, credential rotation or authentication relaxation occurred.

## Observer recovery and limits

A post-refresh observer mistakenly applied a stricter unplanned 120-second age
threshold instead of the configured 600-second freshness contract. Healthy data
was within the configured interval; the corrected read-only observer verifies
that actual contract. No provider/service/data change was made for this error.

ScreenCaptureKit subsequently failed and exposed an old AX value. Resetting only
the CUA observer session restored fresh observation of the same already-running
app and matching current quota. The temporary user screen-status question became
unnecessary. This was observation recovery, not an app or daemon restart.

Runtime source-mode and installed-package identities are distinct and explicit.
No broad source gate was rerun for a private operational configuration repair.
Raw readings, database backups, paths and logs stay in the private
`usage-limits-20261105` bundle; the public index contains receipt digests only.

## Independent operational QA

Final ACCEPT. The reviewer independently verified all 16 receipt hashes,
installed/live service configuration and source/package identity, anonymous
rejection, the genuine existing-credential snapshot, matching state/wire/UI and
preserved histories. Its temporary subscriber was closed. Keep-alive/login
settings are verified configuration, not a deliberate crash or reboot test.
No permanent provider availability or inference qualification is claimed.
