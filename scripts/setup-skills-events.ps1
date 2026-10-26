param(
    [Parameter(Mandatory=$true)][string]$Endpoint,
    [Parameter(Mandatory=$true)][string]$RepositoryRoot,
    [string]$Invitation,
    [switch]$Uninstall
)
$ErrorActionPreference='Stop'
$profileRoot=[Environment]::GetFolderPath('UserProfile')
$stateDir=Join-Path $profileRoot '.codex\hub\skills-events'
$taskName='Redoma-Skills-Events'
if($Uninstall){
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Output 'Receiver startup removed. Local config and logs preserved.'
    exit 0
}
$uri=[Uri]$Endpoint
if($uri.Scheme -ne 'https' -or $uri.AbsolutePath -ne '/' -or $uri.Query -or $uri.UserInfo){throw 'Use the HTTPS service origin only.'}
$repoRoot=(Resolve-Path -LiteralPath $RepositoryRoot).Path
$parent=Split-Path -Parent $repoRoot
$repoPaths=@{}
foreach($name in @('skills-redoma','skills-equipe')){
    $repo=Join-Path $parent $name
    $remote=& git -C $repo remote get-url origin
    if($LASTEXITCODE -ne 0 -or $remote -ne "https://github.com/ARedomaDigital/$name.git"){throw "Clone not ready: $name"}
    $repoPaths[$name]=$repo
}
$python=(Get-Command python -ErrorAction Stop).Source
New-Item -ItemType Directory -Path $stateDir -Force | Out-Null
$configPath=Join-Path $stateDir 'config.json'
$secretPath=Join-Path $stateDir 'device.dpapi'
if(-not (Test-Path -LiteralPath $configPath)){
    if(-not $Invitation){$Invitation=Read-Host 'Convite de uso unico da Redoma'}
    if(-not $Invitation){throw 'Invitation required. Nothing was enrolled.'}
    $body=@{code=$Invitation;name=$env:COMPUTERNAME} | ConvertTo-Json -Compress
    $enrolled=Invoke-RestMethod -Uri ($Endpoint.TrimEnd('/')+'/enroll') -Method Post -ContentType 'application/json' -UserAgent 'Redoma-Skills-Events/1.0' -Body $body
    Add-Type -AssemblyName System.Security
    $plain=[Text.Encoding]::UTF8.GetBytes($enrolled.token)
    $encrypted=[Security.Cryptography.ProtectedData]::Protect($plain,$null,[Security.Cryptography.DataProtectionScope]::CurrentUser)
    [IO.File]::WriteAllText($secretPath,[Convert]::ToBase64String($encrypted))
    [Array]::Clear($plain,0,$plain.Length)
    $configuration=@{schema_version=1;home=$profileRoot;endpoint=$Endpoint.TrimEnd('/');device_id=$enrolled.id;python=$python;repositories=$repoPaths}
    $configuration | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $configPath -Encoding utf8
    $enrolled=$null;$Invitation=$null
}else{
    $existing=Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
    if($existing.endpoint -ne $Endpoint.TrimEnd('/')){throw 'Existing enrollment uses another endpoint; reconcile explicitly.'}
    if(-not (Test-Path -LiteralPath $secretPath)){throw 'Local device credential missing; revoke and enroll again.'}
}
# Pin runtime locally. New pushes update skills only, never replace the running client code.
$runtime=Join-Path $stateDir 'runtime'
New-Item -ItemType Directory -Path $runtime -Force | Out-Null
foreach($name in @('receive-skills-events.ps1','update_skills_event.py','install.py','release_approval.py','configure_hub.py','events_install.py')){
    $source=Join-Path (Split-Path -Parent $PSCommandPath) $name
    Copy-Item -LiteralPath $source -Destination (Join-Path $runtime $name) -Force
}
$receiver=Join-Path $runtime 'receive-skills-events.ps1'
$arguments='-NoProfile -NonInteractive -WindowStyle Hidden -File "'+$receiver+'" -ConfigPath "'+$configPath+'"'
$action=New-ScheduledTaskAction -Execute 'powershell.exe' -Argument $arguments
$trigger=New-ScheduledTaskTrigger -AtLogOn -User ([Security.Principal.WindowsIdentity]::GetCurrent().Name)
$settings=New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit ([TimeSpan]::Zero) -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1) -MultipleInstances IgnoreNew
$principal=New-ScheduledTaskPrincipal -UserId ([Security.Principal.WindowsIdentity]::GetCurrent().Name) -LogonType Interactive -RunLevel Limited
$task=New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal
Register-ScheduledTask -TaskName $taskName -InputObject $task -Force | Out-Null
Start-ScheduledTask -TaskName $taskName
Write-Output 'Receiver enrolled and started. Check status.json after the first connection.'
