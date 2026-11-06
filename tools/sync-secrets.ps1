# シリーズ共通の Android 署名鍵を、tools/repos.txt の全リポジトリの GitHub Secret に入れる（Windows）。
#   鍵ファイルから：  powershell -ExecutionPolicy Bypass -File tools\sync-secrets.ps1 -Keystore C:\path\meishiclaude-release.jks
#   1Password から：  powershell -ExecutionPolicy Bypass -File tools\sync-secrets.ps1 -OpKeystore "op://<保管庫>/<アイテム>/meishiclaude-release.jks" -OpPassword "op://<保管庫>/<アイテム>/password"
# 必要なもの：GitHub CLI（winget install GitHub.cli → gh auth login）。1Password から読むときは 1Password CLI（winget install AgileBits.1Password.CLI）。
# 詳しくは secrets/README.md
param(
    [string]$Keystore,
    [string]$OpKeystore,
    [string]$OpPassword,
    [string]$Alias = "meishiclaude",
    [string]$ExpectedSha1 = "A1:13:EA:34:83:60:56:32:E7:F5:94:4E:4E:8C:20:55:DD:AE:28:BA",
    [string]$Repos = (Join-Path $PSScriptRoot "repos.txt")
)
$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw "gh が見つかりません。winget install GitHub.cli のあと gh auth login" }

function Read-Plain([string]$prompt) {
    $s = Read-Host $prompt -AsSecureString
    [Runtime.InteropServices.Marshal]::PtrToStringBSTR([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))
}

# 鍵ファイルとパスワードを用意する（1Password からなら一時ファイルに取り出し、最後に消す）
$temp = $null
if ($OpKeystore) {
    if (-not (Get-Command op -ErrorAction SilentlyContinue)) { throw "op が見つかりません。winget install AgileBits.1Password.CLI のあと、1Password アプリの設定で CLI 連携をオン" }
    $temp = Join-Path ([IO.Path]::GetTempPath()) ("theta-" + [Guid]::NewGuid() + ".jks")
    op read --out-file $temp $OpKeystore | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "1Password から鍵ファイルを読めません: $OpKeystore" }
    $Keystore = $temp
}
if (-not $Keystore) { throw "-Keystore（鍵ファイルの場所）か -OpKeystore（1Password の参照）を指定してください" }
if (-not (Test-Path $Keystore)) { throw "鍵ファイルがありません: $Keystore" }

try {
    if ($OpPassword) {
        $storePass = (op read $OpPassword).Trim()
        if ($LASTEXITCODE -ne 0 -or -not $storePass) { throw "1Password からパスワードを読めません: $OpPassword" }
    } else {
        $storePass = Read-Plain "鍵ストアのパスワード"
    }
    # PKCS12 の鍵は、鍵のパスワード＝鍵ストアのパスワード
    $keyPass = $storePass

    # 配る前に、パスワード・別名・SHA-1 が合っているか確かめる
    $keytool = (Get-Command keytool -ErrorAction SilentlyContinue).Source
    if (-not $keytool) { $keytool = "C:\Program Files\Android\Android Studio\jbr\bin\keytool.exe" }
    if (Test-Path $keytool) {
        $out = & $keytool -list -v -keystore $Keystore -alias $Alias -storepass $storePass 2>&1
        if ($LASTEXITCODE -ne 0) { throw "keytool で開けません（パスワードか別名が違う）" }
        $sha1 = (($out | Select-String "SHA1:").Line -replace ".*SHA1:\s*", "").Trim()
        Write-Host "署名の SHA-1: $sha1"
        if ($ExpectedSha1 -and $sha1 -ne $ExpectedSha1) { throw "SHA-1 がシリーズ共通の鍵（$ExpectedSha1）と違います。配るのをやめました" }
    } else {
        Write-Warning "keytool が見つからないので、鍵の確認を飛ばします"
    }

    $b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes((Resolve-Path $Keystore)))
    $targets = Get-Content $Repos -Encoding UTF8 | ForEach-Object { ($_ -replace "#.*$", "").Trim() } | Where-Object { $_ }

    $failed = @()
    foreach ($repo in $targets) {
        Write-Host "== $repo"
        # パイプで渡すと PowerShell が末尾に改行を足すので --body で渡す
        $values = [ordered]@{ ANDROID_KEYSTORE_B64 = $b64; ANDROID_KEYSTORE_PASSWORD = $storePass; ANDROID_KEY_ALIAS = $Alias; ANDROID_KEY_PASSWORD = $keyPass }
        foreach ($name in $values.Keys) {
            gh secret set $name --repo $repo --body $values[$name]
            if ($LASTEXITCODE -ne 0) { $failed += "$repo ($name)"; break }
        }
    }
    if ($failed.Count) { Write-Warning ("登録できなかったもの：" + ($failed -join "、")) }
    Write-Host "完了：$($targets.Count - $failed.Count)/$($targets.Count) 個のリポジトリ"
} finally {
    if ($temp -and (Test-Path $temp)) { Remove-Item -Force $temp }
}
