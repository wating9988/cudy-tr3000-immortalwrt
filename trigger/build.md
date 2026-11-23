构建触发文件。改这个文件并 push 即触发一轮 GitHub Actions 编译。

第 1 次触发：2026-11-23 11:00 UTC（V1：含 clashoo 面板 + mihomo）
第 2 次触发：2026-11-23 12:55 UTC（V2：去 clashoo 面板 + 加 ttyd）—— 已取消
第 3 次触发：2026-11-23 22:35 CST（V3：补 clashoo 内核模块）—— 已取消
第 4 次触发：2026-11-23 22:52 CST（V4：去 sing-box）—— 已取消
第 5 次触发（最终精简版）：2026-11-23 23:35 CST（V5：passwall 只留硬依赖，去掉 simple-obfs / v2ray-geodata，无 clashoo、无 sing-box，含 ttyd + 5 个 kmod）
