插件包重编触发文件（这个分支的任何 push 都会触发 build-addons 工作流）。

触发时间：2026-11-23 20:45 CST
原因：首轮 run #1 的 passwall 插件包只出了 6 个依赖 apk，缺少 luci-app-passwall / xray-core / v2ray-geodata。本轮改用官方 feeds 重新构建。
