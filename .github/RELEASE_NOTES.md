# Cudy TR3000 v1 (128MB) · ImmortalWrt 25.12 固件 · V6（ITB）

源码：`chasey-dev/immortalwrt-mt798x-rebase` @ `25.12`（内核 6.12 / MTK 闭源无线驱动）

## 本版重点

- **仅出 OpenWrt U-Boot / ubootmod 布局的 ITB 固件**，不再附带原厂 114m BIN。
- 保留联发科闭源 `mt_wifi`、APCLI、802.11k/v/r、802.11w、HNAT / Fast-NAT。
- 内置 iOS / Android / QMI / MBIM / Option USB 共享全栈。
- 内置 `usbwan` Hotplug：识别 `usb0` / `eth2` / `wwan0`，自动挂防火墙 `wan` 区，拔出自动释放。
- 内置 ksmbd + `ksmbd-hotplug` + `wsdd2`，U 盘/移动硬盘自动生成 SMB 共享。
- **内置 Clashoo + LuCI 面板**（Mihomo 内核随 clashoo）。
- **内置 PassWall 插件本体 + LuCI 页面 + 中文包**。
- **Xray / Sing-box 不进固件**，作为独立 `.apk` 内核包随 Release 提供，后续可单独升级。

## 资产说明

| 文件 | 用途 |
| --- | --- |
| `*cudy_tr3000-v1-ubootmod-squashfs-sysupgrade.itb` | **主固件（ITB）**：OpenWrt U-Boot（ubootmod）布局，U-Boot 网页直接上传 |
| `*.manifest` | 实际打包进固件的软件包清单 |
| `sha256sums` | 固件校验值 |
| `config-built.txt` | 最终编译配置 |
| `tr3000-passwall-cores-*.zip` | Xray + Sing-box 独立内核 `.apk`，不写进固件 |

> 本版不生成 Cudy 原厂 U-Boot 的 114m BIN。若你的机器不是 OpenWrt U-Boot，请勿刷本 ITB。

## 刷机

1. 断电，按住 RESET 上电，进入 OpenWrt U-Boot 网页（通常是 `192.168.1.1`）；
2. 上传 `...ubootmod-squashfs-sysupgrade.itb`；
3. 等待自动重启；
4. 浏览器打开 `http://192.168.6.1`，root / `password`。

> 刷机前备份 `Factory` 分区。不同 U-Boot 布局互刷可能变砖。

## 默认参数

- 后台：`http://192.168.6.1/24`（显式 `255.255.255.0`，避免 `/32` 导致 DHCP/IPv4 异常）
- root 密码：`password`
- WiFi：首次启动不预置密码，进后台自行设置
- ttyd：LuCI → 系统 → TTYD 终端（`http://192.168.6.1:7681`）

## 内置能力

- 闭源 `kmod-mt_wifi` + `mt7981` 固件，DBDC、MU-MIMO、WPA3
- APCLI 无线中继
- 802.11k / 11r / 11v 快速漫游
- 802.11w PMF 管理帧保护
- `kmod-mediatek_hnat` + `MTK_FAST_NAT_SUPPORT` 硬件加速
- iOS：`ipheth` + `usbmuxd` + `libimobiledevice`
- Android：RNDIS / CDC-NCM / CDC-ECM / EEM
- 4G/5G：QMI / MBIM / Option / ACM + `usb-modeswitch` + `uqmi` / `umbim` / `comgt`
- USB 3.0 + `ext4` / `ntfs3` / `exfat` / `vfat` / `f2fs` + automount
- `kmod-mtd-rw` 可解锁闪存写保护
- ksmbd（SMB2/3）+ `wsdd2` + U 盘自动共享
- WireGuard + DDNS（Cloudflare / 阿里云 / DNSPod / 华为云 / No-IP）
- 内核特性：`DEBUG_INFO_BTF`、`CGROUP_BPF`、`XDP_SOCKETS`、`nft-tproxy`

## PassWall 使用

1. PassWall 插件本体已内置，LuCI → 服务 → PassWall；
2. 解压 `tr3000-passwall-cores-*.zip`，把整个目录传到路由器 `/tmp/passwall/`；
3. SSH 执行：`cd /tmp/passwall && sh install.sh`；
4. 在 PassWall 中选择 `xray-core` 或 `sing-box` 内核。

## Clashoo

Clashoo 已内置，LuCI → 服务 → Clashoo。Mihomo 内核随 clashoo 包一起安装，不需要额外下载。
