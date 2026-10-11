# Themes — 整体方案计划

## 一、已完成

### TokyoNight Mod

#### Typora

- Storm / Night / Moon / Day 四变体全部完成
- 含完整排版、代码高亮（hljs + CodeMirror）、PDF 导出
- 侧边栏分隔线修复（`.sidebar-tabs` / `.sidebar-footer`）
- 侧边栏文件面板：active/hover CSS 变量（`--active-file-*`、`--item-hover-*`）
- 大纲面板：active 加粗、hover 背景 + 文字色 + 下划线
- 表格：圆角外框（border-collapse: separate + radius + overflow:hidden）、蓝色表头 + 蓝色行 hover，移除斑马纹

#### Obsidian（核心）

- 单一 `theme.css`，支持 Style Settings 插件
- 深色模式独立选择方案（Storm / Night / Moon，3 选 1）
- 浅色模式固定为 Day（Day 只作为浅色方案存在，非深浅通用）
- 系统深/浅模式自动切换，每个变体使用自身调色板
- Obsidian 变量完整映射（背景、文字、链接、代码、标题、标签、Callout 等）
- 工作区 UI 统一背景（编辑区、文件列表、Tab 栏、Ribbon、状态栏）
- 文件列表：文件夹着色、悬停渐变、活跃文件高亮（蓝色底 + 左侧强调条 inset shadow，不占布局）
- 缩进线修复（`::before` + 堆叠上下文方案）
- Callout：全部 13 种官方类型语义化配色，背景区分无标题栏；标题文字与图标按类型着色（`rgb(var(--callout-color))`，修复 RGB 三元组直接当 `color` 用导致的失效）
- Blockquote：Reading 与 Live Preview 共用 `--blockquote-background-color` / `--blockquote-color`，两种模式一致，背景透明
- 任务清单：7 种状态（unchecked/checked/`/`/`-`/`>`/`?`/`!`），自定义圆形 checkbox；图标对齐修复
- 高亮文字与 inline code 阅读/编辑模式一致
- Unchecked checkbox 边框加深（`--tn-comment`）
- Notice/Toast 通知样式接入主题调色板
- 导航悬停/激活填充色、tooltip（蓝色文字/边框）、链接下划线 hover 显现、文件夹图标（lucide mask）
- 表格：修复列斑马纹被 app.css 覆盖的问题（改用 Obsidian 原生变量驱动），圆角外框，蓝色表头 + 蓝色行 hover

### Catppuccin Mod

#### Typora

- Mocha / Macchiato / Frappé / Latte 四变体全部完成，排版、代码高亮、PDF 导出与 TokyoNight Mod 对齐
- 表格：与 TokyoNight Mod 同款圆角外框，mauve 表头文字 + 下划线、lavender 行 hover（保留 Catppuccin 自身色彩性格）

#### Obsidian（核心）

- 与 TokyoNight Mod 同等完整度：Style Settings 支持、Obsidian 变量全映射
- 深色模式独立选择方案（Mocha / Macchiato / Frappé，3 选 1）；浅色模式固定为 Latte（Latte 只作为浅色方案存在）
- 文件列表：hover = lavender、active = mauve、文字 = mantle；hover 优先级覆盖 active（匹配 app.css 特异性，绕过 Style Settings 切换时禁用 `.css-settings-manager` 的问题）
- 重命名文件/文件夹时文字颜色修复（`.is-being-renamed:focus-within` 复用了为 mauve 填充底设计的 mantle 色，导致几乎不可见）
- Tooltip：mantle 背景 + rosewater 文字/边框
- 表格：与 TokyoNight Mod 同款圆角外框，mauve 表头 + lavender hover
- Callout 标题/图标着色、Blockquote 两种模式一致（同 TokyoNight Mod）

### Wonderland Mod

灵感来自村上春树《世界尽头与冷酷仙境》中的「冷酷仙境」：克制的靛黑底色、冷灰白文字，唯一的暖色是黄铜（台灯 / 酒吧灯光），对比冷青 / 钢蓝的「数据」色调，不走霓虹赛博朋克路线。

#### Obsidian（v1.0.0）

- 基于 Catppuccin Mod 的结构，Style Settings 支持、Obsidian 变量全映射
- 深色模式 2 选 1：Underground（默认，地下水道，最暗最冷）/ Office District（地面东京夜，略亮略暖）；浅色模式固定为 Lab（系统实验室，冷白）
- 色彩角色：黄铜 = UI 强调（checkbox、标签、文件夹图标、活跃文件、光标、表头、H2）；冷青 = H1、属性键；钢蓝 = 链接、H3；血红 = 错误/危险；骨白 = tooltip（Lab 下改为石墨色）
- 文件列表沿用 TokyoNight Mod 的克制方案：黄铜渐变 hover + 活跃文件黄铜淡底 + 左侧强调条（不存在 Catppuccin 的重命名文字问题）
- 从一开始即包含 Callout 标题/图标着色、Blockquote 两种模式一致（透明背景）
- 已校验：三个变体变量定义完整、`-rgb` 三元组与 hex 一致；强调色对背景对比度 ≥ 4.3

### 通用

- 主题命名统一加 "Mod" 后缀（`Catppuccin` → `Catppuccin Mod`，`TokyoNight` → `TokyoNight Mod`），Typora CSS 文件、Obsidian manifest、Style Settings YAML、README 全部同步改名
- 同步脚本：`scripts/sync-typora.sh`、`scripts/sync-obsidian.sh`（自动识别 `obsidian/` 下所有主题目录）

当前版本：

| 主题 | Obsidian | Typora |
|------|----------|--------|
| TokyoNight Mod | 1.4.1 | 1.3.0 |
| Catppuccin Mod | 1.2.1 | 1.2.0 |
| Wonderland Mod | 1.0.0 | — |

---

## 二、待完成

### 阶段 1 — 样式补全

| 项目 | 说明 | 状态 |
|------|------|------|
| 搜索高亮 | 搜索结果匹配文字背景色（三套主题） | ☐ |
| 右键菜单 | `.menu`、`.menu-item` 背景和悬停色（三套主题） | ☐ |
| Wonderland Mod Typora | 按 Obsidian 版配色移植 Underground / Office District / Lab 三个 CSS 文件 + README | ☐ |
| Wonderland Mod 调色 | 在 Obsidian 中实际查看后微调（黄铜强度、Office District 与 Underground 的区分度） | ☐ |
| sync-obsidian.sh 提示语 | 结束提示固定写着「select TokyoNight」，应改为通用文案 | ☐ |

### 阶段 2 — 多变体验证

- TokyoNight Mod：验证全部 3 种有效组合（深色 Storm/Night/Moon 各配浅色 Day），截图对比
- Catppuccin Mod：验证全部 3 种有效组合（深色 Mocha/Macchiato/Frappé 各配浅色 Latte），截图对比
- Wonderland Mod：验证全部 2 种有效组合（深色 Underground/Office District 各配浅色 Lab），截图对比
- 重点检查：可读性、对比度、代码高亮与新表格样式是否协调

### 阶段 3 — 文档与发布准备

| 项目 | 说明 | 状态 |
|------|------|------|
| 截图素材 | 各变体效果图（Typora + Obsidian，三套主题） | ☐ |
| manifest.json | 补全 `authorUrl`（GitHub 地址）— 三套主题均为空 | ☐ |
| 社区提交 | 按 Obsidian 官方流程提 PR 到 obsidian-releases（三套主题） | ☐ |

### 阶段 4 — 可选扩展

- JetBrains / VS Code 配色方案移植
- Typora 主题提交到官方主题库

---

## 三、文件结构（现状）

```
themes/
├── shared/
│   ├── tokens/base.css
│   └── palettes/
├── obsidian/
│   ├── tokyonight/
│   │   ├── theme.css          ✓
│   │   ├── manifest.json      ✓（需补 authorUrl）
│   │   └── README.md          ✓
│   ├── catppuccin/
│   │   ├── theme.css          ✓
│   │   ├── manifest.json      ✓（需补 authorUrl）
│   │   └── README.md          ✓
│   └── wonderland/
│       ├── theme.css          ✓
│       ├── manifest.json      ✓（需补 authorUrl）
│       └── README.md          ✓
├── typora/
│   ├── tokyonight/
│   │   ├── tokyonight-mod-storm.css  ✓
│   │   ├── tokyonight-mod-night.css  ✓
│   │   ├── tokyonight-mod-moon.css   ✓
│   │   ├── tokyonight-mod-day.css    ✓
│   │   └── README.md                 ✓
│   ├── catppuccin/
│   │   ├── catppuccin-mod-mocha.css      ✓
│   │   ├── catppuccin-mod-macchiato.css  ✓
│   │   ├── catppuccin-mod-frappe.css     ✓
│   │   ├── catppuccin-mod-latte.css      ✓
│   │   └── README.md                     ✓
│   └── wonderland/                       ☐ 待建
└── scripts/
    ├── sync-typora.sh     ✓
    └── sync-obsidian.sh   ✓
```

---

## 四、调色板参考

### TokyoNight Mod

| 变体 | 背景色 | 特点 |
|------|--------|------|
| Storm | `#24283b` | 标准深色，蓝灰调 |
| Night | `#1a1b26` | 最深，纯黑感 |
| Moon | `#222436` | 深色，蓝紫调 |
| Day | `#e1e2e7` | 浅色，低饱和 |

### Catppuccin Mod

| 变体 | 背景色 | 特点 |
|------|--------|------|
| Mocha | `#1e1e2e` | 最深，深海军蓝 |
| Macchiato | `#24273a` | 略浅海军蓝 |
| Frappé | `#303446` | 冷灰蓝调 |
| Latte | `#eff1f5` | 浅色，暖白 |

### Wonderland Mod

| 变体 | 背景色 | 特点 |
|------|--------|------|
| Underground | `#121218` | 最深最冷，地下水道 |
| Office District | `#1a1a20` | 略亮略暖，地面东京夜 |
| Lab | `#eef0f2` | 浅色，冷白实验室 |

| 角色 | Underground | Office District | Lab | 用途 |
|------|-------------|-----------------|-----|------|
| 黄铜 brass | `#c39a5f` | `#d4a85e` | `#8f6426` | UI 强调、H2 |
| 冷青 cyan | `#7fcfcf` | `#86cccb` | `#1d7c88` | H1、属性键 |
| 钢蓝 steel | `#7d9ac4` | `#8aa0c4` | `#3a5e94` | 链接、H3 |
| 血红 blood | `#c25a50` | `#c95f53` | `#a8323a` | 错误、危险 |
| 骨白 bone | `#e6e1d3` | `#ece5d4` | `#5a5446`（石墨） | tooltip |
