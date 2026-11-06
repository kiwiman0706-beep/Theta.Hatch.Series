#!/usr/bin/env bash
# シリーズ共通の Android 署名鍵を、tools/repos.txt の全リポジトリの GitHub Secret に入れる（Mac / Linux）。
#   bash tools/sync-secrets.sh ~/path/theta-hatch-release.jks [別名]
# 必要なもの：GitHub CLI（brew install gh → gh auth login）。詳しくは secrets/README.md
set -euo pipefail

keystore="${1:?鍵ファイル（.jks）を指定してください}"
alias_name="${2:-thetahatch}"
repos="$(dirname "$0")/repos.txt"

command -v gh >/dev/null || { echo "gh が見つかりません。brew install gh のあと gh auth login" >&2; exit 1; }
[ -f "$keystore" ] || { echo "鍵ファイルがありません: $keystore" >&2; exit 1; }

read -rsp "鍵ストアのパスワード: " store_pass; echo
read -rsp "鍵のパスワード（同じなら Enter）: " key_pass; echo
key_pass="${key_pass:-$store_pass}"

# 配る前に、パスワードと別名が合っているか確かめる（keytool があれば）
if command -v keytool >/dev/null; then
  if ! out="$(keytool -list -v -keystore "$keystore" -alias "$alias_name" -storepass "$store_pass" 2>&1)"; then
    echo "keytool で開けません（パスワードか別名が違う）:" >&2; echo "$out" >&2; exit 1
  fi
  echo "署名の $(echo "$out" | grep -m1 'SHA1:' | sed 's/^[[:space:]]*//')"
fi

b64="$(base64 < "$keystore" | tr -d '\n')"
count=0
while IFS= read -r line; do
  repo="$(echo "${line%%#*}" | xargs)"
  [ -z "$repo" ] && continue
  echo "== $repo"
  printf '%s' "$b64" | gh secret set ANDROID_KEYSTORE_B64 --repo "$repo"
  printf '%s' "$store_pass" | gh secret set ANDROID_KEYSTORE_PASSWORD --repo "$repo"
  printf '%s' "$alias_name" | gh secret set ANDROID_KEY_ALIAS --repo "$repo"
  printf '%s' "$key_pass" | gh secret set ANDROID_KEY_PASSWORD --repo "$repo"
  count=$((count + 1))
done < "$repos"
echo "完了：$count 個のリポジトリ"
