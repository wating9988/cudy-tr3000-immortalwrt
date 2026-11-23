# Cudy TR3000 v1 (128MB) · ImmortalWrt 25.12 固件 · V5（精简 final）

源码：`chasey-dev/immortalwrt-mt798x-rebase` @ `25.12`（内核 6.12 / MTK 闭源无线驱动）

> **V5 = V1 的全部硬件级能力，去掉 clashoo 三件套与 sing-box，passwall 只保留安装必需的硬依赖，新增 ttyd 网页终端。**
> V1（含 clashoo + mihomo）仍保留在 `fw-20261123-1103` 这个 release。

## V5 相对 V1 的差异

- ❌ 移除：`clashoo` / `luci-app-clashoo` / `luci-i18n-clashoo-zh-cn` / `sing-box`
- ❌ 移除可选件：`simple-obfs-client` / `simple-obfs-server` / `v2ray-geodata`（用时从插件包装或 PassWall 内下载）
- ✅ 新增：`ttyd` + `luci-app-ttyd`（LuCI → 系统 → TTYD 终端，默认端口 7681）
- ✅ 内置 clashoo 自装所需内核模块：`kmod-tun` / `kmod-dummy` / `kmod-inet-diag` / `kmod-nft-socket` / `kmod-nft-tproxy`
- ✅ 保留 passwall **硬依赖**（装 passwall 本体必需，从包定义逐条对齐）：`coreutils*`、`curl`、`chinadns-ng`、`dns2socks`、`ip-full`、`libuci-lua`、`lua`、`luci-compat`、`luci-lib-jsonc`、`microsocks`、`resolveip`、`tcping`、`lyaml`、`unzip`、`ipt2socks`、`kmod-nft-socket`、`kmod-nft-tproxy`、`kmod-nft-nat`、`kmod-nf-reject`、`kmod-nf-reject6`
- 其余与 V1 一致：闭源无线 / APCLI / 802.11k-r-w / HNAT / USB 全栈 / ksmbd+wsdd2 / 文件管理 / WireGuard / DDNS / BTF 内核特性

> xray-core / sing-box 这类代理内核**不进固件**，全部走插件包（按需安装，只装你用的那两个）。

## 资产说明

| 文件 | 用途 |
| --- | --- |
| `*cudy_tr3000-v1-ubootmod-squashfs-sysupgrade.itb` | **主固件（ITB）**：OpenWrt U-Boot（ubootmod）布局。U-Boot 网页 `192.168.1.1` 直接上传 |
| `*cudy_tr3000-v1-mtkuboot-squashfs-sysupgrade.bin` | 兜底：Cudy 原厂 U-Boot + **114m 大分区**布局（128M 机型刷机时选 `114m`） |
| `*ubootmod-preloader.bin` | 只有需要重刷 U-Boot 时才用，正常刷固件不要动 |
| `*.manifest` / `sha256sums` / `config-built.txt` | 包清单、校验值、最终配置 |

> 25.12 分支包管理器已迁移到 **apk**。

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

- 后台：`http://192.168.6.1/24`（写死 255.255.255.0，避开 /32 把 DHCP 和 IPv4 搞挂）
- root 密码：`password`
- WiFi：不预置密码，首次进后台自己设
- ttyd：LuCI → 系统 → TTYD 终端（`http://192.168.6.1:7681`）

## 内置能力

- 联发科闭源 `kmod-mt_wifi` 7.6.7.3 + `mt7981-fw-20260601`，DBDC 双频合一、MU-MIMO、WPA3
- APCLI 无线中继、802.11k / 11r / 11w(PMF)
- `kmod-mediatek_hnat` + `MTK_FAST_NAT_SUPPORT`（硬件 Fast-NAT，千兆满载 CPU 近零占用）
- USB 共享全栈：iOS（ipheth + usbmuxd）、Android（RNDIS / CDC-NCM / ECM / EEM）、4G-5G（QMI / MBIM / Option / ACM）+ usb-modeswitch + uqmi / umbim / comgt
- `/etc/hotplug.d/net/99-usbwan`：`usb*/wwan*/enx*`（含挂 USB 总线上的 `eth2`）出现就自动建 `usbwan` 并挂进防火墙 `wan` 区，拔掉自动释放
- USB 3.0 + `ext4 / ntfs3 / exfat / vfat / f2fs` + automount；`kmod-mtd-rw` 可解锁闪存写保护
- ksmbd（SMB2/3）+ `wsdd2`（Windows「网络」自动发现）+ U 盘插上自动生成共享
- LuCI 文件管理（系统 → 文件浏览器）+ ttyd 网页终端
- WireGuard + DDNS（cloudflare / 阿里云 / DNSPod / 华为云 / noip）
- 内核特性：`DEBUG_INFO` + `DEBUG_INFO_BTF`、`CGROUP_BPF`、`XDP_SOCKETS(_DIAG)`、`nft-tproxy`

## 插件安装

- **PassWall**：解压 `tr3000-passwall-full-*.zip` 传到 `/tmp/passwall/`，`cd /tmp/passwall && sh install.sh` → LuCI → 服务 → PassWall。插件包里只放 `luci-app-passwall` + 中文包 + `xray-core`（+ 需要时单独增 `sing-box`）。
- **clashoo（可选）**：装 `clashoo` + `luci-app-clashoo` + `luci-i18n-clashoo-zh-cn` 三个 apk，mihomo 内核在 clashoo 包内自带，固件依赖已备齐。
