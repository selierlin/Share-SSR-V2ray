# Shadowsocks 设置方法 (Windows)

## 系统要求
**在安装之前，请始终确保您的系统满足最低系统要求。**

您需要具备 Windows 7 SP1 或更高版本才能运行 Shadowsocks。如果您的操作系统版本较旧， 则请先升级到  Windows 7 SP1 或更高版本。

**NET Framework**: 如果你的计算机未安装.NET Framework, 请点击 [这里](https://www.microsoft.com/zh-tw/download/details.aspx?id=53345) 下载最新版本的 .NET Framework。

## 安装 Shadowsocks

按照下面的说明在 Windows 中下载并安装 Shadowsocks。

#### 1. 下载客户端

访问 Shadowsocks Windows 客户端 [下载页面](https://github.com/shadowsocks/shadowsocks-windows/releases)。
下载最新版本的 `Shadowsocks-x.x.x.zip`  (`x.x.x`为版本号) 。

![下载页面](files/images/win-shadowsockDownload.png)

或是前往 [客户端中心](https://shadowsocks.org/en/download/clients.html) 下载

#### 2. 解压客户端

右键 `Shadowsocks-x.x.x.zip` 压缩文件 > "全部解压缩"。
点击 "浏览" 选择想要解压到的文件目录 > "完成时显示提取的文件" > "提取"。
双击运行 `Shadowsocks.exe`。

![解压 Shadowsocks.exe](files/images/win-unzipSS.png)

![解压 Shadowsocks.exe](files/images/win-unzipSS2.png)

![双击运行 Shadowsocks.exe](files/images/win-doubleClickSS.png)



## 配置 Shadowsocks 账号

>  在您的计算机上， 执行下列任一操作

#### 一、使用`gui-config.json`文件添加账号

* 将 `gui-config.json` 拖移到和 `Shadowsocks.exe` 同一个文件目录下。

![gui-config.json 拖到和 Shadowsocks.exe 同目录](files/images/win-together.png)

* 双击 `Shadowsocks.exe` > 右键状态栏 ![ss icon](files/images/win-icon.png) >  单击 “服务器”  > 即可看到服务器信息已自动填充完成。

![即可看到服务器信息已自动填充完成](files/images/win-autofill.png)



* 右键状态栏![ss icon](files/images/win-icon.png) > "启用系统代理”。

![右键图标](files/images/win-enable.png)

#### 二、通过二维码方式单独增加节点

**在分享节点的网站中一般都有查看二维码的功能。**

![1549868214348](files/images/1549868214348.png)

此二维码同样适用于其他客户端。

* 右键状态栏![ss icon](files/images/win-icon.png) > "服务器” > "扫描屏幕上的二维码"。
* 点击 "启用系统代理" 。

![QR](files/images/win-QR.png)



#### 三、手动配置账号

>  如果以上的功能都不存在的话，那么你可以选择此种方式来添加账号

从分享节点的网站中依次填入相应信息，确定即可

![1549868618888](files/images/1549868618888.png)





## 配置系统代理模式
* 右键状态栏![ss icon](files/images/win-icon.png) > "系统代理模式" > "PAC模式"。

* 如果使用 PAC 模式无法访问网站，请点击 [Pac文件下载](https://portal.shadowsocks.nu/dl.php?type=d&id=14) 下载 pac 配置文件，将  `pac.txt` 文件拖放在与 `Shadowsocks.exe` 相同的文件目录下。

![pac模式](files/images/win-pac.png)

![下载 pac](files/images/win-pact.png)

## 注意事项
- **PAC 模式** 表示可以实现自动代理， 及本来可以访问的网站不会经过代理，推荐日常使用。
- **全局模式** 表示计算机内大多数流量都会经过代理， 不推荐日常使用。

## 	配置 Firefox 的代理

**如需使用 Firefox 浏览器	通过代理浏览网页，请参考下面链接：**  
[Firefox上设置代理](7-1-firefox-setup-guide-cn.md)


## 配置 Chrome 的代理

**如需使用 Chrome 浏览器通过代理浏览网页，请参考下面链接：**  
[Chrome + Proxy SwitchyOmega 设置](7-2-chrome-setup-guide-cn.md)
