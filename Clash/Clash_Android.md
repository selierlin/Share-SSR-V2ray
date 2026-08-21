# Clash Meta for Android 使用教程

Clash Party 目前没有 Android 版。本教程推荐使用 **Clash Meta for Android（CMFA）**：它是基于 Mihomo 内核的 Android 客户端，适合导入 Clash / Mihomo 订阅并通过 Android VPN 服务代理流量。

> 原 Clash for Android 已停止维护，不建议新用户继续使用。本教程不再适用于 Clash for Android 或第三方修改版。

## 1. 下载与安装

1. 前往 [Clash Meta for Android 官方发布页](https://github.com/MetaCubeX/ClashMetaForAndroid/releases)。
2. 下载适合自己设备架构的 APK；不确定架构时，优先查看发布页的说明或选择通用版本（如发布页提供）。
3. 在 Android 的下载目录中打开 APK 并完成安装；如果系统阻止安装，请仅为当前浏览器或文件管理器授予“允许安装未知应用”的权限。
4. 安装完成后打开 Clash Meta for Android。

> 请只从 MetaCubeX 官方 GitHub Release 下载，不要安装名称相近的第三方 APK。

## 2. 导入订阅

1. 在机场或服务商后台复制 **Clash / Mihomo 订阅地址**。
2. 打开应用，进入「配置（Profiles）」页面，点击右上角或右下角的「+」。
3. 选择「从 URL 导入（Import from URL）」。
4. 粘贴订阅地址，填写便于识别的名称后保存或创建配置。
5. 等待配置下载完成，在配置列表中选中刚导入的配置使其生效。

> 请不要把订阅地址分享给他人；它通常相当于账号凭证。若地址泄露，请及时在服务商后台重置。

## 3. 选择节点并启动代理

1. 进入「代理（Proxies）」页面，在对应的策略组中选择节点；通常可先选择「自动选择」或延迟较低的节点。
2. 返回主页，模式保持为「规则（Rule）」。
3. 点击「已停止（Stopped）」或启动按钮。
4. 第一次启动时，Android 会请求创建 VPN 连接，点击「允许」。状态显示为运行中后，代理即已开启。

## 4. 选择代理模式

- **规则（Rule）**：按订阅配置中的规则分流；通常推荐日常使用。
- **全局（Global）**：所有流量都通过所选代理节点。
- **直连（Direct）**：所有流量直接连接，不使用代理。
- **脚本（Script）**：仅适用于包含自定义脚本的高级配置，普通用户通常不需要使用。

## 5. 更新订阅与常见问题

- **更新订阅**：进入「配置」页面，找到对应配置并点击更新或刷新图标；更新后确认该配置仍处于选中状态。
- **无法启动**：确认已允许 VPN 连接；如系统中已有其它 VPN 或代理应用，先关闭它们再重试。
- **网页或应用无法连接**：先切换到其它节点；仍无效时更新订阅，并检查服务商后台的订阅是否有效。
- **订阅导入失败**：确认复制的是完整的 Clash / Mihomo 订阅地址，而不是单个节点链接或其它客户端专用链接。

## 参考

- [Clash Meta for Android 官方 GitHub 仓库](https://github.com/MetaCubeX/ClashMetaForAndroid)
- [Clash Meta for Android 官方发布页](https://github.com/MetaCubeX/ClashMetaForAndroid/releases)
