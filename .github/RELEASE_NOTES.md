# Cudy TR3000 v1 (128MB) · ImmortalWrt 25.12 固件 · V2（无 clashoo / 含 ttyd）

源码：`chasey-dev/immortalwrt-mt798x-rebase` @ `25.12`（内核 6.12 / MTK 闭源无线驱动）

> **本版本 = V1 的全部功能，去掉 clashoo（clashoo + luci-app-clashoo + 中文语言包），新增 ttyd 网页终端。**
> V1（含 clashoo 面板）仍保留在 `fw-20261123-1103` 这个 release 里。

## V2 差异

- ❌ 移除：`clashoo`、`luci-app-clashoo`、`luci-i18n-clashoo-zh-cn`（mihomo 面板不再内置）
- ✅ 新增：`ttyd` + `luci-app-ttyd`（LuCI → 系统 → TTYD 终端，默认端口 7681）
- ✅ 保留：`sing-box` 内核 + `yq` / `unzip`（日后想装回 clashoo 或给 passwall 用都现成）
- 其余与 V1 完全一致：闭源无线 / APCLI / 802.11k-r-w / HNAT / USB 全栈 / ksmbd+wsdd2 / 文件管理 / WireGuard / DDNS / passwall 依赖 / BTF 内核特性

## 资产说明

| 文件 | 用途 |
| --- | --- |
| `*cudy_tr3000-v1-ubootmod-squashfs-sysupgrade.itb` | **主固件（ITB）**：OpenWrt U-Boot（ubootmod）布局。U-Boot 网页 `192.168.1.1` 直接上传 |
| `*cudy_tr3000-v1-mtkuboot-squashfs-sysupgrade.bin` | 兜底：Cudy 原厂 U-Boot + **114m 大分区**布局（128M 机型刷机时选 `114m`） |
| `*ubootmod-preloader.bin` | 只有需要重刷 U-Boot 时才用，正常刷固件不要动 |
| `*.manifest` / `sha256sums` / `config-built.txt` | 包清单、校验值、最终配置 |

> 25.12 分支包管理器已迁移到 **apk**，插件包是 `.apk` 而不是 `.ipk`。

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

- 后台：`http://192.168.6.1/24`（显式写死 255.255.255.0，避免 /32 把 DHCP 和 IPv4 搞挂）
- root 密码：`password`
- WiFi：不预置密码，首次进后台自己在「网络 → 无线」里设
- ttyd：LuCI → 系统 → TTYD 终端（`http://192.168.6.1:7681`）

## 内置能力

- 联发科闭源 `kmod-mt_wifi` 7.6.7.3 + `mt7981-fw-20260601`，DBDC 双频合一、MU-MIMO、WPA3
- APCLI 无线中继、802.11k / 11r / 11w(PMF)
- `kmod-mediatek_hnat` + `MTK_FAST_NAT_SUPPORT`（硬件 Fast-NAT，千兆满载 CPU 近零占用）
- USB 共享全栈：iOS（ipheth + usbmuxd）、Android（RNDIS / CDC-NCM / ECM / EEM）、4G-5G（QMI / MBIM / Option / ACM）+ usb-modeswitch + uqmi / umbim / comgt
- `/etc/hotplug.d/net/99-usbwan`：`usb*/wwan*/enx*`（含挂 USB 总线上的 `eth2`）出现就自动建 `usbwan` 并挂进防火墙 `wan` 区，拔掉自动释放
- USB 3.0 + `ext4 / ntfs3 / exfat / vfat / f2fs` + automount；`kmod-mtd-rw` 可解锁闪存写保护
- ksmbd（SMB2/3）+ `wsdd2`（Windows「网络」自动发现）+ ksmbd 自带热插共享：U 盘插上自动生成可写共享
- LuCI 文件管理（系统 → 文件浏览器）+ ttyd 网页终端
- WireGuard + DDNS（cloudflare / 阿里云 / DNSPod / 华为云 / noip）
- PassWall **依赖**已内置（chinadns-ng / dns2socks / microsocks / tcping / ipt2socks / dnsmasq-full / lyaml / luci-compat 等），本体走独立的插件包
- 内核特性：`DEBUG_INFO` + `DEBUG_INFO_BTF`、`CGROUP_BPF`、`XDP_SOCKETS(_DIAG)`、`nft-tproxy`

## PassWall / clashoo 安装

- PassWall：解压 `tr3000-passwall-full-*.zip` 传到 `/tmp/passwall/`，`cd /tmp/passwall && sh install.sh`，然后 LuCI → 服务 → PassWall。
- clashoo（可选）：`sing-box` / `yq` / `unzip` 已在固件里，装上 `clashoo` 的 apk 即可恢复面板。
