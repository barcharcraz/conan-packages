param([string]$user)
Get-ChildItem -Directory | ForEach-Object {conan export $user/testing}