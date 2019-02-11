# Chrome + Proxy SwitchyOmega 设置

**这里假设您已经配置好 Shadowsocks 客户端，具体请参考**

* [Windows 下安装配置 Shadowsocks 使用教程](2-windows-setup-guide-cn.md)

* [macOS 下安装配置 Shadowsocks 使用教程](3-macos-setup-guide-cn.md)

* [Linux 下安装配置 Shadowsocks 使用教程](6-linux-setup-guide-cn.md)

## 安装扩展

* 您可以通过chrome商店安装 [Proxy SwitchyOmega](https://chrome.google.com/webstore/detail/padekgcemlokbadohgkifijomclgjgif) 扩展。

* 单击“添加至 CHROME” >  单击 “扩展应用程序”。

 ![安装到chrome](files/images/bro-chromeinstall.png)

**如果无法访问**

* 访问 `chrome://extensions/`，请使用 Chrome 浏览器复制粘贴输入地址栏并回车访问。

* 在 [Github](https://github.com/FelisCatus/SwitchyOmega/releases) 下载 SwitchyOmega.crx 文件并拖移入`chrome://extensions/` 。

![使用Guthub](files/images/bro-chrome-useGithub.png)

## 扩展的配置

**「推荐」** 可以直接使用本站提供的已经设置好的备份直接恢复配置。

通过下面链接下载 SwitchyOmega 的配置文件：

|Windows/Linux/macOS(ShadowsocksX)|macOS|
|:--------:|:--------:|
|[SwitchOmega + GFWList 自动切换配置文件(1080)](https://portal.shadowsocks.nu/dl.php?type=d&id=74)|[SwitchOmega + GFWList 自动切换配置文件(1086)](https://portal.shadowsocks.nu/dl.php?type=d&id=75)|
|适用于 Shadowsocks-Windows / Linux / ShadowsocksX(macOS) 等默认端口为 1080 的客户端。|适用于ShadowscoksX-NG， 默认本地端口为 1086|

* 点击 “Proxy SwitchyOmega” > "选项" > "导入/导出" > "从备份文件中恢复" 。

* 选择刚才下载的配置文件 > "打开"。
* 点击 "Switchyomega" 图标， 可以看到如下四个模式：


|连接方式|功能|
|--------|:--------:|
|直接连接|所有访问都不是使用代理。|
|系统代理|访问网站与系统的默认代理有关。|
|Shadowsocks|所有访问都使用代理。|
|自动切换|所有访问都使用代理。|


> 本站提供的配置使用了 "GFWList", 可以使大部分无法直接访问的网站默认使用代理，推荐日常使用， 在下文中会包含 "自定义配置规则"。

 ![从备份文件中恢复](files/images/bro-switchyomega.png)

## 自定义规则

* 点击"自动切换模式" > "添加条件"。

>* 条件类型选择： "域名通配符"。

>* 条件设置填写： "*.域名".

>* 情景模式： 选 "Shadowsocks" 则经过代理， 选 “直接连接” 则不经过代理。

![自定义规则](files/images/bro-swocustomize.png)
