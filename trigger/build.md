构建触发文件。改这个文件并 push 即触发一轮 GitHub Actions 编译。

第 1 次触发：2026-11-23 11:00 UTC（V1：含 clashoo 面板）
第 2 次触发：2026-11-23 12:55 UTC（V2：去掉 clashoo 面板 + 新增 ttyd）
第 3 次触发：2026-11-23 22:35 CST（V3：在 V2 基础上把 kmod-dummy / tun / inet-diag / nft-socket / nft-tproxy 显式编入固件，clashoo 可日后自装）
