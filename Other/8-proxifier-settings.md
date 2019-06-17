# Shadowsocks 配合 Proxifier 實現客戶端代理

## 什麼是 Proxifier

Proxifier 是一款功能非常強大的 socks5 客戶端，可以讓不支持通過代理服務器工作的網絡程序能通過 HTTPS 或 SOCKS 代理或代理鏈。支持64位系統，支持 XP，Vista，Win7，macOS, 支持 socks4，socks5，http 代理協議，支持 TCP，UDP 協議，可以指定端口，指定 IP，指定域名,指定程序等運行模式，兼容性非常好，和 SOCKSCAP 屬於同類軟件，不過 SOCKSCAP 已經很久沒更新了，不支持64位系統。有許多網絡應用程序不支持通過代理服務器工作，Proxifier 解決了這些問題和所有限制，讓您有機會不受任何限制使用你喜愛的軟件。此外，它讓你獲得了額外的網絡安全控制，創建代理隧道，並添加使用更多網絡功能的權力。

## 使用方法

### Proxifier 下載

官網下載地址：[點擊這裏](http://www.proxifier.com/download.htm)

#### Windows 版本

軟件分為 Standard Edition 和 Portable Edition 版本，請自行購買註冊碼

#### macOS 版本

請自行購買註冊碼

若係統為 10.11，請下載[Beta版 ](https://www.proxifier.com/distr/ProxifierMacBeta.zip)

若 Yosemite 下 Proxifier 不能運行，打開 終端 應用，運行下面的命令然後重啟

```
sudo nvram boot-args="kext-dev-mode=1"
```

#### 詳細使用方法：

因為 Windows 和 macOS 的使用方式是一樣的，這裡就只演示 macOS 下的使用方法

首先點擊 `proxies` > `add`

在其中填寫 `socks5` 的代理地址 `127.0.0.1:1080` 請確保與圖中一致

![img](../files/images/565c75c39e2fa.jpg)
![img](../files/images/565c78968c9e6.jpg)

接下來填寫代理規則

![1549870860276](../files/images/1549870860276.png)

中最重要的就是請將 Shadowsocks 客戶端設置為全局模式

如圖，點擊*+* 添加 APP，再在 `Action` 中選擇 `Direct`

![1549870908639](../files/images/1549870908639.png)

此時就可以添加其他 APP 了，比如讓 Steam 和 CS:GO 走 Shadowsocks 以降低延遲，那麼如圖：

![1549870973407](../files/images/1549870973407.png)

確保選擇的是走 `socks5` 就可以了
