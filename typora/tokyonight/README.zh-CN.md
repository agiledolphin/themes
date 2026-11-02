# Lamplit TokyoNight（Typora 主题）

[English](README.md) · 简体中文

基于 folke 的 [TokyoNight](https://github.com/folke/tokyonight.nvim) 配色。提供四个变体，各是一个独立的 CSS 文件，每个都有完整的配色。

---

## 截图

![Lamplit TokyoNight：深色和浅色](screenshot.png)

---

## 变体

| 文件 | 模式 | 背景 | 特点 |
|------|------|------|------|
| `lamplit-tokyonight-storm.css` | 深色 | `#24283b` | 蓝灰，标准深色 |
| `lamplit-tokyonight-night.css` | 深色 | `#1a1b26` | 深邃，接近纯黑 |
| `lamplit-tokyonight-moon.css` | 深色 | `#222436` | 带蓝紫色调 |
| `lamplit-tokyonight-day.css` | 浅色 | `#e1e2e7` | 低饱和浅色 |

---

## 特性

- **四个独立变体**：各有完整配色，不是近似调整出来的
- **标题层级**：H1–H6 用不同的点缀色（蓝 → 青 → 青绿 → 绿 → 黄 → 注释色）
- **中文优先的排版**：PingFang SC → Hiragino Sans GB → Noto Serif SC，行高舒适
- **代码块**：同时支持 highlight.js 和 CodeMirror 的语法高亮
- **元素覆盖完整**：引用、表格、任务列表、脚注、公式、Mermaid 图、YAML front matter、目录
- **侧边栏细节**：文件面板的当前项高亮和悬停色，大纲面板的当前项（加粗）和悬停（背景 + 下划线）状态
- **打印 / PDF 导出**：优化了版式和分页

---

## 安装

### 一行命令（macOS、Linux）

不需要克隆仓库，重新运行即可更新。

```bash
curl -fsSL https://raw.githubusercontent.com/agiledolphin/themes/main/install.sh | bash -s -- typora tokyonight
```

### 同步脚本

如果你已经克隆了仓库：

```bash
./scripts/sync-typora.sh tokyonight
```

### 手动安装

1. 找到 Typora 的主题文件夹：
   - **macOS**：`~/Library/Application Support/abnerworks.Typora/themes/`
   - **Windows**：`%APPDATA%\Typora\themes\`
   - **Linux**：`~/.config/Typora/themes/`
2. 把需要的文件复制到这个文件夹：
   - `lamplit-tokyonight-storm.css`
   - `lamplit-tokyonight-night.css`
   - `lamplit-tokyonight-moon.css`
   - `lamplit-tokyonight-day.css`
3. 打开 **Typora → 偏好设置 → 外观**，选择对应的主题

---

## 字体建议

- **正文**：PingFang SC / Hiragino Sans GB / Noto Serif SC / Georgia
- **等宽**：[JetBrains Mono](https://www.jetbrains.com/lp/mono/) 或 [Fira Code](https://github.com/tonsky/FiraCode)

---

## 致谢

- 配色：[@folke](https://github.com/folke) 的 [tokyonight.nvim](https://github.com/folke/tokyonight.nvim)

---

## 许可证

MIT
