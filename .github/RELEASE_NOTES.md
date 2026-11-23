# Cudy TR3000 v1 (128MB) · ImmortalWrt 25.12 固件

源码：`chasey-dev/immortalwrt-mt798x-rebase` @ `25.12`（内核 6.12 / MTK 闭源无线驱动）

## 资产说明

| 文件 | 用途 |
| --- | --- |
| `*cudy_tr3000-v1-ubootmod-squashfs-sysupgrade.itb` | **主固件（ITB）**：OpenWrt U-Boot（ubootmod）布局，U-Boot 网页 192.168.1.1 直接上传 |
| `*cudy_tr3000-v1-mtkuboot-squashfs-sysupgrade.bin` | 兜底：Cudy 原厂 U-Boot + **114m 大分区**布局（128M 机型刷机时选 114m） |
| `*ubootmod-preloader.bin` / `*ubootmod-bl31-uboot.fip` | 只有需要重刷 U-Boot 时才用，正常刷固件不要动 |
| `*.manifest` / `sha256sums` | 包清单与校验 |
| `tr3000-passwall-apk-*.zip` | PassWall 本体 + LuCI + xray 内核的 .apk 安装包（固件里不含，按需安装） |

> 25.12 分支包管理器已迁移到 apk，插件包是 `.apk` 而不是 `.ipk`。

## 刷机

**A. 已经是 OpenWrt U-Boot（ubootmod）**
1. 断电，按住 RESET 上电，进 `192.168.1.1` 的 U-Boot 网页；
2. 上传 `...ubootmod-squashfs-sysupgrade.itb`，等自动重启；
3. 浏览器打开 `http://192.168.6.1`，root / `password`。

**B. 官方（Cudy 原厂）U-Boot，128M 机型**
1. 断电，按住 RESET 上电，进 `192.168.1.1`；
2. 分区布局选 **114m**，上传 `...mtkuboot-squashfs-sysupgrade.bin`；
3. 浏览器打开 `http://192.168.6.1`，root / `password`。

> 不同布局互刷一定变砖，只能 TFTP/UART 救。刷前先备份 `Factory` 分区。

## 默认参数

- 后台：`http://192.168.6.1/24`（显式写死 255.255.255.0，避开 /32 把 DHCP 和 IPv4 搞挂）
- root 密码：`password`
- WiFi：不预置密码，首次进后台自己在「网络 → 无线」里设

## 内置能力

- 联发科闭源 `kmod-mt_wifi` 7.6.7.3 + `mt7981-fw-20260601`，DBDC 双频合一、MU-MIMO、WPA3
- APCLI 无线中继、802.11k / 11r / 11w(PMF)
- `kmod-mediatek_hnat` + `MTK_FAST_NAT_SUPPORT`（硬件 Fast-NAT，千兆满载 CPU 近零占用）
- USB 共享全栈：iOS（ipheth + usbmuxd）、Android（RNDIS / CDC-NCM / ECM / EEM）、4G-5G（QMI / MBIM / Option / ACM）+ usb-modeswitch + uqmi / umbim / comgt
- `/etc/hotplug.d/net/99-usbwan`：`usb*/wwan*/enx*`（含挂 USB 总线上的 `eth2`）出现就自动建 `usbwan` 并挂进防火墙 `wan` 区，拔掉自动释放
- USB 3.0 + `ext4 / ntfs3 / exfat / vfat / f2fs` + automount；`kmod-mtd-rw` 可解锁闪存写保护
- ksmbd（SMB2/3）+ `wsdd2`（Windows「网络」自动发现）+ ksmbd 自带热插共享：U 盘插上自动生成可写共享
- LuCI 文件管理（系统 → 文件浏览器）
- WireGuard + DDNS（cloudflare / 阿里云 / DNSPod / 华为云 / noip）
- Clashoo：内置 mihomo 1.19.34 + sing-box 双内核，LuCI 面板
- PassWall **依赖**已内置（chinadns-ng / dns2socks / microsocks / tcping / simple-obfs / ipt2socks / v2ray-geodata / dnsmasq-full / lyaml / luci-compat 等），本体走附件里的 apk
- 内核特性：`DEBUG_INFO` + `DEBUG_INFO_BTF`、`CGROUP_BPF`、`XDP_SOCKETS(_DIAG)`、`nft-tproxy`

## PassWall 安装

1. 解压 `tr3000-passwall-apk-*.zip`，整个目录传到路由器 `/tmp/passwall/`；
2. `cd /tmp/passwall && sh install.sh`；
3. LuCI → 服务 → PassWall。
