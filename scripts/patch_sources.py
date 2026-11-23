#!/usr/bin/env python3
"""编译前的源码微调。

1) golang feeds：上游 xray-core / sing-box / mihomo 的 go.mod 可能要求比本树更高的
   go 版本，默认 GOTOOLCHAIN=local 会直接拒绝编译，改成 auto 让 go 自己拉工具链。
2) ksmbd 热插共享：feed 自带的 ksmbd.hotplug 默认 read_only=yes，改成可写。
"""
import glob
import sys

root = sys.argv[1]

for p in (glob.glob(root + "/feeds/packages/lang/golang/**/*.mk", recursive=True)
          + glob.glob(root + "/feeds/packages/lang/golang/**/*.sh", recursive=True)):
    try:
        s = open(p, encoding="utf-8").read()
    except Exception:
        continue
    if "GOTOOLCHAIN=local" in s:
        open(p, "w", encoding="utf-8").write(s.replace("GOTOOLCHAIN=local", "GOTOOLCHAIN=auto"))
        print("patched GOTOOLCHAIN=auto:", p)

hp = root + "/feeds/packages/net/ksmbd-tools/files/ksmbd.hotplug"
try:
    s = open(hp, encoding="utf-8").read()
    if 'read_only="yes"' in s:
        open(hp, "w", encoding="utf-8").write(s.replace('read_only="yes"', 'read_only="no"'))
        print("patched ksmbd.hotplug: read_only=no")
except FileNotFoundError:
    print("ksmbd.hotplug not found, skip")

print("patch_sources done")
