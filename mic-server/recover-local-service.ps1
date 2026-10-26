# Native Windows cannot enforce the backend's POSIX owner/mode credential contract.
# Run the mic backend, web host and recovery helper inside WSL.
$ErrorActionPreference = 'Stop'
throw 'Native Windows microphone recovery is unsupported. Run the authenticated mic service and web host in WSL; see mic-server/README.md.'
