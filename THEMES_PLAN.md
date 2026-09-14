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
- Callout：全部 13 种官方类型语义化配色，背景区分无标题栏
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
- Tooltip：mantle 背景 + rosewater 文字/边框
- 表格：与 TokyoNight Mod 同款圆角外框，mauve 表头 + lavender hover

### 通用

- 主题命名统一加 "Mod" 后缀（`Catppuccin` → `Catppuccin Mod`，`TokyoNight` → `TokyoNight Mod`），Typora CSS 文件、Obsidian manifest、Style Settings YAML、README 全部同步改名
- 同步脚本：`scripts/sync-typora.sh`、`scripts/sync-obsidian.sh`

---

## 二、待完成

### 阶段 1 — 样式补全

| 项目 | 说明 | 状态 |
|------|------|------|
| 搜索高亮 | 搜索结果匹配文字背景色 | ☐ |
| 右键菜单 | `.menu`、`.menu-item` 背景和悬停色 | ☐ |

### 阶段 2 — 多变体验证

- TokyoNight Mod：验证全部 3 种有效组合（深色 Storm/Night/Moon 各配浅色 Day），截图对比
- Catppuccin Mod：验证全部 3 种有效组合（深色 Mocha/Macchiato/Frappé 各配浅色 Latte），截图对比
- 重点检查：可读性、对比度、代码高亮与新表格样式是否协调

### 阶段 3 — 文档与发布准备

| 项目 | 说明 | 状态 |
|------|------|------|
| 截图素材 | 各变体效果图（Typora + Obsidian，两套主题） | ☐ |
| manifest.json | 补全 `authorUrl`（GitHub 地址）— TokyoNight Mod、Catppuccin Mod 均为空 | ☐ |
| 社区提交 | 按 Obsidian 官方流程提 PR 到 obsidian-releases（两套主题） | ☐ |

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
│   └── catppuccin/
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
│   └── catppuccin/
│       ├── catppuccin-mod-mocha.css      ✓
│       ├── catppuccin-mod-macchiato.css  ✓
│       ├── catppuccin-mod-frappe.css     ✓
│       ├── catppuccin-mod-latte.css      ✓
│       └── README.md                     ✓
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
