#!/usr/bin/env python3
"""从本树的 mt7981-ax3000 defconfig 生成 .config 种子。

保留 defconfig 里全部 MT7981 闭源无线 / HNAT / Fast-NAT 调优项，
只把设备收窄到 Cudy TR3000（默认 ubootmod / ITB 布局），再叠加本项目要的功能包。
"""
import sys

SRC = sys.argv[1]
DST = sys.argv[2]

DEVICES = [
    "cudy_tr3000-v1-ubootmod",   # OpenWrt U-Boot 布局 -> sysupgrade.itb
]

EXTRA = [
    # ---------- iOS 共享（ipheth + usbmuxd）----------
    "CONFIG_PACKAGE_kmod-usb-net=y",
    "CONFIG_PACKAGE_kmod-usb-net-ipheth=y",
    "CONFIG_PACKAGE_usbmuxd=y",
    "CONFIG_PACKAGE_libusbmuxd=y",
    "CONFIG_PACKAGE_libimobiledevice=y",
    "CONFIG_PACKAGE_libimobiledevice-glue=y",
    # ---------- Android 共享（RNDIS / CDC-NCM / CDC-ECM / EEM）----------
    "CONFIG_PACKAGE_kmod-usb-net-rndis=y",
    "CONFIG_PACKAGE_kmod-usb-net-cdc-ncm=y",
    "CONFIG_PACKAGE_kmod-usb-net-cdc-ether=y",
    "CONFIG_PACKAGE_kmod-usb-net-cdc-eem=y",
    "CONFIG_PACKAGE_kmod-usb-net-huawei-cdc-ncm=y",
    # ---------- 4G/5G 模组（QMI / MBIM / Option / ACM）----------
    "CONFIG_PACKAGE_kmod-usb-net-qmi-wwan=y",
    "CONFIG_PACKAGE_kmod-usb-net-qmi-wwan-dual=y",
    "CONFIG_PACKAGE_kmod-usb-net-cdc-mbim=y",
    "CONFIG_PACKAGE_kmod-usb-wdm=y",
    "CONFIG_PACKAGE_kmod-usb-serial=y",
    "CONFIG_PACKAGE_kmod-usb-serial-option=y",
    "CONFIG_PACKAGE_kmod-usb-serial-wwan=y",
    "CONFIG_PACKAGE_kmod-usb-acm=y",
    "CONFIG_PACKAGE_usb-modeswitch=y",
    "CONFIG_PACKAGE_usb-modeswitch-data=y",
    "CONFIG_PACKAGE_uqmi=y",
    "CONFIG_PACKAGE_umbim=y",
    "CONFIG_PACKAGE_comgt=y",
    "CONFIG_PACKAGE_usbutils=y",
    "CONFIG_PACKAGE_usbids=y",
    # ---------- USB 3.0 / 存储 / 文件系统 ----------
    "CONFIG_PACKAGE_kmod-usb3=y",
    "CONFIG_PACKAGE_kmod-usb-xhci-hcd=y",
    "CONFIG_PACKAGE_automount=y",
    "CONFIG_PACKAGE_kmod-usb-storage=y",
    "CONFIG_PACKAGE_kmod-usb-storage-uas=y",
    "CONFIG_PACKAGE_kmod-usb-storage-extras=y",
    "CONFIG_PACKAGE_kmod-fs-ext4=y",
    "CONFIG_PACKAGE_kmod-fs-exfat=y",
    "CONFIG_PACKAGE_kmod-fs-ntfs3=y",
    "CONFIG_PACKAGE_kmod-fs-vfat=y",
    "CONFIG_PACKAGE_kmod-fs-f2fs=y",
    "CONFIG_PACKAGE_kmod-nls-base=y",
    "CONFIG_PACKAGE_kmod-nls-cp437=y",
    "CONFIG_PACKAGE_kmod-nls-iso8859-1=y",
    "CONFIG_PACKAGE_kmod-nls-utf8=y",
    "CONFIG_PACKAGE_blockdev=y",
    "CONFIG_PACKAGE_mount-utils=y",
    "CONFIG_PACKAGE_e2fsprogs=y",
    # ---------- 闪存维护 ----------
    "CONFIG_PACKAGE_kmod-mtd-rw=y",
    # ---------- ksmbd（SMB2/3）+ wsdd2 ----------
    "CONFIG_PACKAGE_kmod-fs-ksmbd=y",
    "CONFIG_PACKAGE_ksmbd-server=y",
    "CONFIG_PACKAGE_wsdd2=y",
    "CONFIG_PACKAGE_luci-app-ksmbd=y",
    "CONFIG_PACKAGE_luci-i18n-ksmbd-zh-cn=y",
    # ---------- LuCI 内置文件管理 ----------
    "CONFIG_PACKAGE_luci-app-filebrowser=y",
    "CONFIG_PACKAGE_luci-i18n-filebrowser-zh-cn=y",
    # ---------- WireGuard ----------
    "CONFIG_PACKAGE_kmod-wireguard=y",
    "CONFIG_PACKAGE_wireguard-tools=y",
    "CONFIG_PACKAGE_luci-proto-wireguard=y",
    "CONFIG_PACKAGE_rpcd-mod-wireguard=y",
    "CONFIG_PACKAGE_qrencode=y",
    # ---------- DDNS ----------
    "CONFIG_PACKAGE_ddns-scripts=y",
    "CONFIG_PACKAGE_ddns-scripts-services=y",
    "CONFIG_PACKAGE_ddns-scripts-cloudflare=y",
    "CONFIG_PACKAGE_ddns-scripts-aliyun=y",
    "CONFIG_PACKAGE_ddns-scripts-dnspod=y",
    "CONFIG_PACKAGE_ddns-scripts-dnspod-v3=y",
    "CONFIG_PACKAGE_ddns-scripts-huaweicloud=y",
    "CONFIG_PACKAGE_ddns-scripts-noip=y",
    "CONFIG_PACKAGE_luci-app-ddns=y",
    "CONFIG_PACKAGE_luci-i18n-ddns-zh-cn=y",
    # ---------- clashoo：mihomo 内核 + sing-box 内核一起烧进固件 ----------
    "CONFIG_PACKAGE_clashoo=y",
    "CONFIG_PACKAGE_luci-app-clashoo=y",
    "CONFIG_PACKAGE_luci-i18n-clashoo-zh-cn=y",
    "CONFIG_PACKAGE_sing-box=y",
    "CONFIG_PACKAGE_yq=y",
    "CONFIG_PACKAGE_unzip=y",
    # ---------- passwall 依赖（不含 passwall 本体）----------
    "CONFIG_PACKAGE_dnsmasq-full=y",
    "# CONFIG_PACKAGE_dnsmasq is not set",
    "CONFIG_PACKAGE_chinadns-ng=y",
    "CONFIG_PACKAGE_dns2socks=y",
    "CONFIG_PACKAGE_microsocks=y",
    "CONFIG_PACKAGE_tcping=y",
    "CONFIG_PACKAGE_simple-obfs-client=y",
    "CONFIG_PACKAGE_simple-obfs-server=y",
    "CONFIG_PACKAGE_ipt2socks=y",
    "CONFIG_PACKAGE_v2ray-geodata=y",
    "CONFIG_PACKAGE_lyaml=y",
    "CONFIG_PACKAGE_luci-compat=y",
    "CONFIG_PACKAGE_luci-lib-jsonc=y",
    "CONFIG_PACKAGE_libuci-lua=y",
    "CONFIG_PACKAGE_coreutils-base64=y",
    "CONFIG_PACKAGE_coreutils-nohup=y",
    "CONFIG_PACKAGE_coreutils-timeout=y",
    "CONFIG_PACKAGE_resolveip=y",
    "CONFIG_PACKAGE_lua=y",
    # ---------- 内核特性 ----------
    "CONFIG_KERNEL_DEBUG_INFO=y",
    "# CONFIG_KERNEL_DEBUG_INFO_REDUCED is not set",
    "CONFIG_KERNEL_DEBUG_INFO_BTF=y",
    "CONFIG_KERNEL_CGROUP_BPF=y",
    "CONFIG_KERNEL_XDP_SOCKETS=y",
    "CONFIG_KERNEL_XDP_SOCKETS_DIAG=y",
    # ---------- 明确不烧进固件 ----------
    "# CONFIG_PACKAGE_luci-app-passwall is not set",
    "# CONFIG_PACKAGE_luci-i18n-passwall-zh-cn is not set",
]

device_lines = ["CONFIG_TARGET_DEVICE_mediatek_filogic_DEVICE_%s=y" % d for d in DEVICES]

drop_prefix = (
    "CONFIG_TARGET_DEVICE_",
    "CONFIG_TARGET_DEVICE_PACKAGES_",
    "CONFIG_TARGET_PROFILE",
    "CONFIG_TARGET_ARCH",
    "CONFIG_TARGET_BOARD",
    "CONFIG_TARGET_SUBTARGET",
    "CONFIG_TARGET_MULTI_PROFILE",
)

kept, keys = [], set()
with open(SRC, encoding="utf-8") as f:
    for raw in f:
        line = raw.rstrip("\n")
        if line.startswith(drop_prefix):
            continue
        if not line.strip() or line.lstrip().startswith("#"):
            kept.append(line)
            continue
        key = line.split("=", 1)[0]
        if key in keys:
            continue
        keys.add(key)
        kept.append(line)

extra_keys = set(l.split("=", 1)[0] for l in EXTRA if not l.startswith("#"))
neg_keys = set(l[2:-len(" is not set")] for l in EXTRA if l.startswith("# CONFIG_") and l.endswith(" is not set"))
kept = [l for l in kept if l.split("=", 1)[0] not in extra_keys and l.split("=", 1)[0] not in neg_keys]

with open(DST, "w", encoding="utf-8") as f:
    f.write("\n".join(kept) + "\n")
    f.write("\n".join([
        "CONFIG_TARGET_mediatek=y",
        "CONFIG_TARGET_mediatek_filogic=y",
        "CONFIG_TARGET_MULTI_PROFILE=y",
        "CONFIG_TARGET_PER_DEVICE_ROOTFS=y",
    ]) + "\n")
    f.write("\n".join(device_lines) + "\n")
    f.write("\n".join(EXTRA) + "\n")

print("wrote %s (%d lines), devices=%s" % (DST, len(kept) + len(EXTRA) + len(device_lines) + 4, ",".join(DEVICES)))
