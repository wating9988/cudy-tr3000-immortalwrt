#!/usr/bin/env python3
"""从本树的 mt7981-ax3000 defconfig 生成 .config 种子。

V7（本次确认版）：
  - 设备固定为 Cudy TR3000 v1（128MB）OpenWrt U-Boot / ubootmod 布局，产出 sysupgrade.itb
  - 闭源 mt_wifi / APCLI / 802.11k-v-r-w / HNAT / Fast-NAT 全保留
  - iOS / Android / QMI / MBIM / Option USB 共享全栈
  - USB 存储 + ext4/ntfs3/exfat/vfat/f2fs + automount + kmod-mtd-rw
  - ksmbd + ksmbd-hotplug + wsdd2 + LuCI 网络存储
  - 移除 Clashoo；新增 Nikki + LuCI + Mihomo 内核
  - PassWall 插件本体写进固件，但关闭 PassWall 自带的可选内核/可选依赖
  - Xray / Sing-box 不进固件，由 Actions 单独编译为 .apk 附件
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
    # ---------- ksmbd（SMB2/3）+ 热插共享 + wsdd2 ----------
    "CONFIG_PACKAGE_kmod-fs-ksmbd=y",
    "CONFIG_PACKAGE_ksmbd-server=y",
    "CONFIG_PACKAGE_ksmbd-hotplug=y",
    "CONFIG_PACKAGE_wsdd2=y",
    "CONFIG_PACKAGE_luci-app-ksmbd=y",
    "CONFIG_PACKAGE_luci-i18n-ksmbd-zh-cn=y",
    # ---------- LuCI 内置文件管理 / 网页终端 ----------
    "CONFIG_PACKAGE_luci-app-filebrowser=y",
    "CONFIG_PACKAGE_luci-i18n-filebrowser-zh-cn=y",
    "CONFIG_PACKAGE_ttyd=y",
    "CONFIG_PACKAGE_luci-app-ttyd=y",
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
    # ---------- Nikki（Mihomo 透明代理）----------
    "CONFIG_PACKAGE_nikki=y",
    "CONFIG_PACKAGE_luci-app-nikki=y",
    "CONFIG_PACKAGE_luci-i18n-nikki-zh-cn=y",
    "CONFIG_PACKAGE_mihomo-meta=y",
    "# CONFIG_PACKAGE_mihomo-alpha is not set",
    "CONFIG_PACKAGE_yq=y",
    "CONFIG_PACKAGE_curl=y",
    "CONFIG_PACKAGE_ca-bundle=y",
    "CONFIG_PACKAGE_ip-full=y",
    "CONFIG_PACKAGE_firewall4=y",
    "CONFIG_PACKAGE_nftables=y",
    "CONFIG_PACKAGE_kmod-dummy=y",
    "CONFIG_PACKAGE_kmod-tun=y",
    "CONFIG_PACKAGE_kmod-inet-diag=y",
    "CONFIG_PACKAGE_kmod-nft-socket=y",
    "CONFIG_PACKAGE_kmod-nft-tproxy=y",
    "CONFIG_PACKAGE_kmod-nft-nat=y",
    "CONFIG_PACKAGE_kmod-nf-reject=y",
    "CONFIG_PACKAGE_kmod-nf-reject6=y",
    "CONFIG_PACKAGE_unzip=y",
    # ---------- 移除 Clashoo ----------
    "# CONFIG_PACKAGE_clashoo is not set",
    "# CONFIG_PACKAGE_luci-app-clashoo is not set",
    "# CONFIG_PACKAGE_luci-i18n-clashoo-zh-cn is not set",
    # ---------- PassWall 插件本体（关闭所有可选内核/可选依赖）----------
    "CONFIG_PACKAGE_luci-app-passwall=y",
    "CONFIG_PACKAGE_luci-i18n-passwall-zh-cn=y",
    "CONFIG_PACKAGE_luci-app-passwall_Nftables_Transparent_Proxy=y",
    "# CONFIG_PACKAGE_luci-app-passwall_Iptables_Transparent_Proxy is not set",
    "# CONFIG_PACKAGE_luci-app-passwall_INCLUDE_Geoview is not set",
    "# CONFIG_PACKAGE_luci-app-passwall_INCLUDE_SmartDNS is not set",
    "# CONFIG_PACKAGE_luci-app-passwall_INCLUDE_Haproxy is not set",
    "# CONFIG_PACKAGE_luci-app-passwall_INCLUDE_Hysteria is not set",
    "# CONFIG_PACKAGE_luci-app-passwall_INCLUDE_NaiveProxy is not set",
    "# CONFIG_PACKAGE_luci-app-passwall_INCLUDE_Shadowsocks_Rust_Client is not set",
    "# CONFIG_PACKAGE_luci-app-passwall_INCLUDE_Shadowsocks_Rust_Server is not set",
    "# CONFIG_PACKAGE_luci-app-passwall_INCLUDE_ShadowsocksR_Libev_Client is not set",
    "# CONFIG_PACKAGE_luci-app-passwall_INCLUDE_ShadowsocksR_Libev_Server is not set",
    "# CONFIG_PACKAGE_luci-app-passwall_INCLUDE_Shadow_TLS is not set",
    "# CONFIG_PACKAGE_luci-app-passwall_INCLUDE_Simple_Obfs is not set",
    "# CONFIG_PACKAGE_luci-app-passwall_INCLUDE_SingBox is not set",
    "# CONFIG_PACKAGE_luci-app-passwall_INCLUDE_V2ray_Geodata is not set",
    "# CONFIG_PACKAGE_luci-app-passwall_INCLUDE_V2ray_Plugin is not set",
    "# CONFIG_PACKAGE_luci-app-passwall_INCLUDE_Xray is not set",
    "# CONFIG_PACKAGE_luci-app-passwall_INCLUDE_Xray_Plugin is not set",
    # PassWall 安装必需依赖
    "CONFIG_PACKAGE_dnsmasq-full=y",
    "# CONFIG_PACKAGE_dnsmasq is not set",
    "CONFIG_PACKAGE_chinadns-ng=y",
    "CONFIG_PACKAGE_dns2socks=y",
    "CONFIG_PACKAGE_microsocks=y",
    "CONFIG_PACKAGE_tcping=y",
    "CONFIG_PACKAGE_ipt2socks=y",
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
    # ---------- 明确不烧进固件（内核单独打包）----------
    "# CONFIG_PACKAGE_sing-box is not set",
    "# CONFIG_PACKAGE_xray-core is not set",
    "# CONFIG_PACKAGE_pikvm is not set",
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
