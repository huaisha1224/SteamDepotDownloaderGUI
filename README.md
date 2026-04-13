# Steam Depot Downloader GUI

<div align="center">
**一款用于下载 Steam 游戏历史版本的图形化工具**
[⬇️ 下载安装](#-安装) | [📖 使用文档](使用教程.md) | [💬 问题反馈](../../issues)

</div>

---
## 📸 界面预览

![软件界面截图](screenshots/main_interface.png)

> 简洁直观的图形界面，让版本下载变得简单

---

## 🌟 简介

**Steam Depot Downloader GUI** 是一款基于 Python 和 ttkbootstrap 开发的桌面应用程序，通过调用 [DepotDownloader](https://github.com/SteamRE/DepotDownloader) 实现 Steam 游戏历史版本的下载功能。

### ✨ 为什么需要这个工具？

- 🎮 **回退游戏版本** - Steam 客户端不支持的游戏，可以用此工具下载旧版本
- 🔧 **Mod 开发** - 获取特定版本的游戏文件进行 Mod 制作
- 📚 **版本研究** - 分析游戏的历史更新变化
- 💾 **备份收藏** - 保存喜欢的版本防止更新丢失

### 🔥 核心特性

- ✅ **图形化界面** - 无需记忆复杂的命令行参数
- ✅ **实时日志** - 下载进度一目了然
- ✅ **安全可靠** - 密码加密显示，不保存账号信息
- ✅ **自动更新** - 启动时自动检查新版本
- ✅ **完全开源** - 代码透明，安全可信

---

## 🚀 快速开始

### 方法一：使用预编译版本（推荐）

#### 1. 下载安装包

从 [Releases](../../releases) 页面下载最新版本的压缩包。

### 方法二：从源码运行

#### 1. 环境要求

- Python 3.8 或更高版本
- Windows 10/11 (64位)

#### 2. 克隆仓库

```bash
git clone https://github.com/huaisha1224/SteamDepotDownloaderGUI.git
cd SteamDepotDownloaderGUI
```

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

#### 4. 运行程序

```bash
python main.py
```

---

## 📖 使用说明

### 基本操作流程

1. **首次运行** - 完成B站授权验证（仅需一次，缓存30天）
2. **填写信息** - 输入Steam账号、游戏ID等信息
3. **选择路径** - 指定下载文件保存位置
4. **开始下载** - 点击按钮等待完成

### 参数获取指南

#### 如何获取 App ID、Depot ID、Manifest ID？

1. 访问 [SteamDB](https://steamdb.info/)
2. 搜索目标游戏
3. 查看 App ID（应用ID）
4. 进入 Depots 标签页查看 Depot ID
5. 点击具体 Depot 查看历史 Manifest ID

**示例：**
```
游戏: Counter-Strike 2
App ID: 730
Depot ID: 731 (Windows Content)
Manifest ID: 5859084079696781234 (某个历史版本)
```

### 详细教程

📚 完整的使用教程请查看：[使用教程.md](使用教程.md)

📺 视频教程：[B站视频链接]（待添加）



## 🔗 相关链接

### 核心依赖
- [DepotDownloader](https://github.com/SteamRE/DepotDownloader) - Steam depot 下载工具
- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap) - 现代化 tkinter 主题库
- [SteamDB](https://steamdb.info/) - Steam 数据库查询

### 作者相关
- [B站主页 - 怀沙2049](https://space.bilibili.com/37443749)
- [GitHub - huaisha1224](https://github.com/huaisha1224)


---

## 📝 更新日志

### v1.0.0 (2026-04-13)

**首次发布**

✨ **新功能**
- 基于 Python + ttkbootstrap 重构
- 现代化深色主题UI
- 自动更新检查功能
- 实时下载日志显示
- 密码安全保护
- 智能路径管理

---

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## ⚠️ 免责声明

1. **合法使用**: 本工具仅供学习和研究使用
2. **版权尊重**: 请尊重游戏开发商的知识产权
3. **账号安全**: 使用自己的账号，后果自负
4. **商业用途**: 禁止用于商业目的
5. **法律责任**: 使用者需自行承担法律责任

**建议**:
- ✅ 仅下载自己拥有的游戏
- ✅ 用于个人备份和学习研究
- ✅ 支持正版游戏
- ❌ 不要用于盗版分发
- ❌ 不要用于作弊行为

---

## 💖 支持项目

如果这个工具对你有帮助，欢迎：

- ⭐ 给项目点个 Star
- 📢 分享给需要的朋友
- 🎬 观看[B站视频教程]()
- 💬 在评论区分享使用体验

你的支持是我持续更新的动力！

---

## 📞 联系方式

- 💬 B站私信: [https://space.bilibili.com/37443749](https://space.bilibili.com/37443749)
- 🐛 GitHub Issues: [https://github.com/huaisha1224/SteamDepotDownloaderGUI/issues](../../issues)

---
<div align="center">

**Made with ❤️ by 怀沙2049**

如果这个项目对你有帮助，请考虑给它一个 ⭐️ Star！

[⬆ 回到顶部](#steam-depot-downloader-gui)

</div>
