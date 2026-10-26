param([Parameter(Mandatory=$true)][string]$ConfigPath)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Security
$config=Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json
$runtime=Split-Path -Parent $PSCommandPath
$stateDir=Split-Path -Parent $ConfigPath
$logPath=Join-Path $stateDir 'receiver.jsonl'
function Write-ReceiverLog([string]$message) {
    @{at=[DateTime]::UtcNow.ToString('o');message=$message} | ConvertTo-Json -Compress | Add-Content -LiteralPath $logPath -Encoding utf8
}
function Notify-User([string]$message) {
    Add-Type -AssemblyName System.Windows.Forms
    $icon=New-Object System.Windows.Forms.NotifyIcon
    $icon.Icon=[System.Drawing.SystemIcons]::Information
    $icon.Visible=$true;$icon.BalloonTipTitle='Skills Redoma';$icon.BalloonTipText=$message
    $icon.ShowBalloonTip(6000)
    Start-Sleep -Seconds 7
    $icon.Dispose()
}
# Per-user mutex prevents duplicate receivers after setup or manual restart.
$mutexName='Local\RedomaSkillsEvents-'+$config.device_id
$created=$false
$mutex=[System.Threading.Mutex]::new($true,$mutexName,[ref]$created)
if(-not $created){$mutex.Dispose();exit 0}
$delay=2
try {
    while($true) {
        $socket=New-Object System.Net.WebSockets.ClientWebSocket
        try {
            $encrypted=[Convert]::FromBase64String((Get-Content -LiteralPath (Join-Path $stateDir 'device.dpapi') -Raw).Trim())
            $clear=[System.Security.Cryptography.ProtectedData]::Unprotect($encrypted,$null,[System.Security.Cryptography.DataProtectionScope]::CurrentUser)
            $token=[System.Text.Encoding]::UTF8.GetString($clear)
            $socket.Options.SetRequestHeader('Authorization','Bearer '+$token)
            $socket.Options.SetRequestHeader('X-Device-Id',$config.device_id)
            $socket.Options.KeepAliveInterval=[TimeSpan]::FromSeconds(30)
            $uri=[Uri]($config.endpoint.Replace('https://','wss://').TrimEnd('/')+'/connect')
            $socket.ConnectAsync($uri,[Threading.CancellationToken]::None).GetAwaiter().GetResult()
            $delay=2;Write-ReceiverLog 'Connected'
            $token=$null;[Array]::Clear($clear,0,$clear.Length)
            while($socket.State -eq [System.Net.WebSockets.WebSocketState]::Open) {
                $buffer=New-Object byte[] 8192
                $stream=New-Object IO.MemoryStream
                do {
                    $segment=New-Object 'ArraySegment[byte]' -ArgumentList @(,$buffer)
                    $result=$socket.ReceiveAsync($segment,[Threading.CancellationToken]::None).GetAwaiter().GetResult()
                    if($result.MessageType -eq [Net.WebSockets.WebSocketMessageType]::Close){throw 'Disconnected'}
                    $stream.Write($buffer,0,$result.Count)
                    if($stream.Length -gt 65536){throw 'Event too large'}
                }while(-not $result.EndOfMessage)
                $message=[Text.Encoding]::UTF8.GetString($stream.ToArray()) | ConvertFrom-Json
                $stream.Dispose()
                if($message.type -notin @('snapshot','update')){continue}
                # Input supplies only a wake-up signal; repository paths and commands are local.
                $answer=& $config.python -B (Join-Path $runtime 'update_skills_event.py') $ConfigPath
                $update=$answer | ConvertFrom-Json
                $ack=@{type='ack';ok=($update.ok -eq $true);heads=$update.heads;conflicts=($update.conflicts -eq $true)} | ConvertTo-Json -Compress -Depth 5
                $bytes=[Text.Encoding]::UTF8.GetBytes($ack)
                $socket.SendAsync((New-Object 'ArraySegment[byte]' -ArgumentList @(,$bytes)),[Net.WebSockets.WebSocketMessageType]::Text,$true,[Threading.CancellationToken]::None).GetAwaiter().GetResult()
                if($update.ok -and $update.changed){Notify-User 'Skills atualizadas e verificadas.'}
                elseif(-not $update.ok){Notify-User 'Atualizacao pausada. Confira o status local; seus arquivos foram preservados.'}
            }
        }catch {
            $detail=$_.Exception.Message -replace '(?i)Bearer\s+\S+','Bearer [REDACTED]'
            Write-ReceiverLog ('Connection ended: '+$_.Exception.GetType().Name+'; '+$detail)
        }finally{$socket.Dispose()}
        # Reconnect only after failure, not periodic repository polling.
        Start-Sleep -Seconds ($delay+(Get-Random -Minimum 0 -Maximum 3))
        $delay=[Math]::Min(120,$delay*2)
    }
}finally{$mutex.ReleaseMutex();$mutex.Dispose()}
