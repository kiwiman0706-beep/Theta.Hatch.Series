# シリーズ共通の Android 署名鍵を、tools/repos.txt の全リポジトリの GitHub Secret に入れる（Windows）。
#   powershell -ExecutionPolicy Bypass -File tools\sync-secrets.ps1 -Keystore C:\path\meishiclaude-release.jks
# 必要なもの：GitHub CLI（winget install GitHub.cli → gh auth login）。詳しくは secrets/README.md
param(
    [Parameter(Mandatory = $true)][string]$Keystore,
    [string]$Alias = "meishiclaude",
    [string]$Repos = (Join-Path $PSScriptRoot "repos.txt")
)
$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw "gh が見つかりません。winget install GitHub.cli のあと gh auth login" }
if (-not (Test-Path $Keystore)) { throw "鍵ファイルがありません: $Keystore" }

function Read-Plain([string]$prompt) {
    $s = Read-Host $prompt -AsSecureString
    [Runtime.InteropServices.Marshal]::PtrToStringBSTR([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))
}
$storePass = Read-Plain "鍵ストアのパスワード"
$keyPass = Read-Plain "鍵のパスワード（同じなら Enter）"
if ([string]::IsNullOrEmpty($keyPass)) { $keyPass = $storePass }

# 配る前に、パスワードと別名が合っているか確かめる（keytool があれば）
if (Get-Command keytool -ErrorAction SilentlyContinue) {
    $out = & keytool -list -v -keystore $Keystore -alias $Alias -storepass $storePass 2>&1
    if ($LASTEXITCODE -ne 0) { throw "keytool で開けません（パスワードか別名が違う）:`n$out" }
    ($out | Select-String "SHA1:") | ForEach-Object { Write-Host "署名の $($_.Line.Trim())" }
}

$b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes((Resolve-Path $Keystore)))
$targets = Get-Content $Repos -Encoding UTF8 | ForEach-Object { ($_ -replace "#.*$", "").Trim() } | Where-Object { $_ }

foreach ($repo in $targets) {
    Write-Host "== $repo"
    # パイプで渡すと PowerShell が末尾に改行を足すので --body で渡す
    gh secret set ANDROID_KEYSTORE_B64 --repo $repo --body $b64
    gh secret set ANDROID_KEYSTORE_PASSWORD --repo $repo --body $storePass
    gh secret set ANDROID_KEY_ALIAS --repo $repo --body $Alias
    gh secret set ANDROID_KEY_PASSWORD --repo $repo --body $keyPass
    if ($LASTEXITCODE -ne 0) { throw "$repo への登録に失敗しました" }
}
Write-Host "完了：$($targets.Count) 個のリポジトリ"
