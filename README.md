# Cudy TR3000 v1 · ImmortalWrt 25.12 云编译工程

基于 [chasey-dev/immortalwrt-mt798x-rebase](https://github.com/chasey-dev/immortalwrt-mt798x-rebase) 的 `25.12` 分支，
用 GitHub Actions 交叉编译 Cudy TR3000 v1（MT7981B / 128MB NAND）固件。

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
| `trigger/` | 往这里推一个文件即触发一次编译 |

## 产物

- `...cudy_tr3000-v1-ubootmod-squashfs-sysupgrade.itb`：主固件（OpenWrt U-Boot / ITB）
- `...cudy_tr3000-v1-mtkuboot-squashfs-sysupgrade.bin`：原厂 U-Boot + 114m 大分区兜底
- `tr3000-passwall-apk-*.zip`：PassWall 本体 + LuCI + xray 的 `.apk` 包

## 触发编译

```bash
git clone https://github.com/wating9988/cudy-tr3000-immortalwrt.git
cd cudy-tr3000-immortalwrt
echo build >> trigger/build.md && git commit -am build && git push
```

## 本地编译（可选）

```bash
git clone --depth 1 -b 25.12 https://github.com/chasey-dev/immortalwrt-mt798x-rebase.git openwrt
python3 scripts/gen_config.py openwrt/defconfig/mt7981-ax3000.config openwrt/.config
cd openwrt && make defconfig && make -j$(nproc)
```

## 默认参数

- 后台 `http://192.168.6.1`，root / `password`
- WiFi 首次启动不带密码，进后台自行配置
