# Cudy TR3000 v1 · ImmortalWrt 25.12 云编译工程（V7 / ITB）

基于 [chasey-dev/immortalwrt-mt798x-rebase](https://github.com/chasey-dev/immortalwrt-mt798x-rebase) 的 `25.12` 分支，
用 GitHub Actions 交叉编译 Cudy TR3000 v1（MT7981B / 128MB NAND）固件。

## 本版目标

- 仅生成 OpenWrt U-Boot / ubootmod 布局的 `sysupgrade.itb`
- 闭源 mt_wifi + APCLI + 802.11k/v/r + 802.11w + HNAT/Fast-NAT
- iOS / Android / QMI / MBIM / Option USB 共享全栈
- `usbwan` Hotplug 自动接入 `wan` 防火墙区
- USB 3.0 + ext4/ntfs3/exfat/vfat/f2fs + automount + `kmod-mtd-rw`
- ksmbd + `ksmbd-hotplug` + `wsdd2`
- **Nikki + LuCI + Mihomo 内置**
- **PassWall 插件本体内置；Xray / Sing-box 单独 `.apk` 打包**
- **Clashoo 已移除**
- LAN `192.168.6.1/24`，root 密码 `password`

## 仓库结构

| 路径 | 说明 |
| --- | --- |
| `.github/workflows/build.yml` | 主流程：拉源码 → feeds → 第三方包 → 配置 → 编译 → 发 Release |
| `scripts/gen_config.py` | 从 `defconfig/mt7981-ax3000.config` 生成本项目 `.config` |
| `scripts/patch_sources.py` | 编译前微调（GOTOOLCHAIN=auto、ksmbd 共享可写） |
| `config/required.txt` | 必须命中的关键符号，缺一个就早停 |
| `overlay/etc/hotplug.d/net/99-usbwan` | USB 网卡 / 手机 / 模组即插即用，自动挂 wan 区 |
| `overlay/etc/uci-defaults/99-tr3000-defaults` | 首次启动：LAN 192.168.6.1/24、开 ksmbd+wsdd2 |
| `overlay/etc/shadow` | 预置 root 密码 `password` |
| `trigger/build.md` | 改这个文件并 push 即触发一次编译 |

## 产物

- `...cudy_tr3000-v1-ubootmod-squashfs-sysupgrade.itb`：主固件（OpenWrt U-Boot / ITB）
- `tr3000-passwall-cores-*.zip`：Xray + Sing-box 独立 `.apk`，不写进固件
- `manifest` / `sha256sums` / `config-built.txt`

## 触发编译

```bash
git clone https://github.com/wating9988/cudy-tr3000-immortalwrt.git
cd cudy-tr3000-immortalwrt
echo build >> trigger/build.md && git commit -am build && git push
```

也可以在 GitHub Actions 页面手动运行 `build-tr3000-v7`。

## 本地编译（可选）

```bash
git clone --depth 1 -b 25.12 https://github.com/chasey-dev/immortalwrt-mt798x-rebase.git openwrt
python3 scripts/gen_config.py openwrt/defconfig/mt7981-ax3000.config openwrt/.config
cd openwrt && make defconfig && make -j$(nproc)
```

## 默认参数

- 后台 `http://192.168.6.1`，root / `password`
- WiFi 首次启动不带密码，进后台自行配置

## 注意

本工程只出 ITB 固件，适用于已经刷了 OpenWrt U-Boot（ubootmod 布局）的 TR3000 v1。
Cudy 原厂 U-Boot 不要刷 ITB，否则可能变砖。
