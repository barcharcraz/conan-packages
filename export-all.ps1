param([string]$user)
Get-ChildItem -Directory | ForEach-Object {conan export -p $_.FullName $user}