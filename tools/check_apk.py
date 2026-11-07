"""APK を開いて、パッケージ名・版・署名の SHA-256 を出す（Android SDK が無くても動く）。

    python tools/check_apk.py <APK> [<APK> ...]

ハブ（Home・KidsHome）が入れるための条件のうち、APK の中身にかかわるもの
（パッケージ名が catalog の target、署名がシリーズ共通の鍵）を確かめるのに使う。
署名は APK Signature Scheme v2/v3 のブロックから、無ければ META-INF の証明書から読む。
"""
import hashlib
import struct
import sys
import zipfile

SERIES_SHA256 = "F4:77:40:D8:54:9B:C1:C3:7F:EB:00:B1:87:80:D8:0B:52:75:8B:60:25:2B:A0:D2:21:7D:83:AB:3F:01:2A:23"
V2, V3 = 0x7109871A, 0xF05368C0


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def signing_block(data):
    """ZIP の中央ディレクトリの直前にある APK Signing Block を返す（無ければ None）。"""
    eocd = data.rfind(b"PK\x05\x06")
    if eocd < 0:
        return None
    cd = u32(data, eocd + 16)
    if data[cd - 16:cd] != b"APK Sig Block 42":
        return None
    size = struct.unpack_from("<Q", data, cd - 24)[0]
    start = cd - size - 8
    return data[start + 8:cd - 24]


def certs_from_block(block):
    """v2/v3 の最初の署名者の証明書（DER）を返す。"""
    o = 0
    while o < len(block):
        ln = struct.unpack_from("<Q", block, o)[0]
        bid = u32(block, o + 8)
        val = block[o + 12:o + 8 + ln]
        o += 8 + ln
        if bid not in (V2, V3):
            continue
        # signers(len) > signer(len) > signed data(len) > digests(len) ... certificates(len) > cert(len)
        p = 4          # signers の長さ
        p += 4         # 最初の signer の長さ
        p += 4         # signed data の長さ
        dl = u32(val, p)
        p += 4 + dl    # digests を飛ばす
        p += 4         # certificates の長さ
        cl = u32(val, p)
        return val[p + 4:p + 4 + cl]
    return None


def cert_from_meta_inf(z):
    """v1 署名（META-INF/*.RSA など）の PKCS#7 から最初の証明書を取り出す（簡易版）。"""
    for n in z.namelist():
        if n.startswith("META-INF/") and n.rsplit(".", 1)[-1] in ("RSA", "DSA", "EC"):
            der = z.read(n)
            i = der.find(b"\x30\x82", 40)
            while i >= 0:
                ln = struct.unpack(">H", der[i + 2:i + 4])[0]
                cand = der[i:i + 4 + ln]
                if b"\xa0\x03\x02\x01\x02" in cand[:20]:
                    return cand
                i = der.find(b"\x30\x82", i + 1)
    return None


def manifest_info(axml):
    """バイナリの AndroidManifest.xml から package と versionName を読む。"""
    strings = []
    o = 8
    out = {}
    while o < len(axml):
        ctype, hsize, csize = struct.unpack_from("<HHI", axml, o)
        if ctype == 0x0001:  # 文字列プール
            count = u32(axml, o + 8)
            flags = u32(axml, o + 16)
            sstart = u32(axml, o + 20)
            utf8 = flags & (1 << 8)
            for i in range(count):
                so = o + sstart + u32(axml, o + hsize + i * 4)
                if utf8:
                    n = axml[so]
                    so += 2 if n & 0x80 else 1
                    n = axml[so]
                    if n & 0x80:
                        n = ((n & 0x7F) << 8) | axml[so + 1]
                        so += 2
                    else:
                        so += 1
                    strings.append(axml[so:so + n].decode("utf-8", "replace"))
                else:
                    n = struct.unpack_from("<H", axml, so)[0]
                    strings.append(axml[so + 2:so + 2 + n * 2].decode("utf-16le", "replace"))
        elif ctype == 0x0102:  # 要素の始まり
            name = strings[u32(axml, o + 20)]
            if name == "manifest":
                acount = struct.unpack_from("<H", axml, o + 28)[0]
                ao = o + 36
                for _ in range(acount):
                    aname = strings[u32(axml, ao + 4)]
                    raw = u32(axml, ao + 8)
                    if raw != 0xFFFFFFFF and aname in ("package", "versionName"):
                        out[aname] = strings[raw]
                    elif aname == "versionCode":
                        out[aname] = u32(axml, ao + 16)
                    ao += 20
                return out
        o += csize
    return out


def inspect(path):
    data = open(path, "rb").read()
    z = zipfile.ZipFile(path)
    info = manifest_info(z.read("AndroidManifest.xml"))
    block = signing_block(data)
    cert = certs_from_block(block) if block else None
    scheme = "v2/v3" if cert else "v1"
    if cert is None:
        cert = cert_from_meta_inf(z)
    sha = ":".join(f"{b:02X}" for b in hashlib.sha256(cert).digest()) if cert else ""
    return {"file": path.rsplit("/", 1)[-1], "package": info.get("package", "?"), "versionName": info.get("versionName", "?"),
            "scheme": scheme, "sha256": sha, "seriesKey": sha == SERIES_SHA256}


if __name__ == "__main__":
    for p in sys.argv[1:]:
        r = inspect(p)
        print(f"{r['file']}: {r['package']} {r['versionName']}  署名 {r['scheme']} {'シリーズ共通の鍵' if r['seriesKey'] else '別の鍵 ' + r['sha256'][:23]}")
