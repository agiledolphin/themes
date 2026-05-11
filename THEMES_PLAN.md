# TokyoNight Themes — 整体方案计划

## 一、已完成

### Typora 主题

- Storm / Night / Moon / Day 四变体全部完成
- 含完整排版、代码高亮（hljs + CodeMirror）、PDF 导出
- 侧边栏分隔线修复（`.sidebar-tabs` / `.sidebar-footer`）
- 侧边栏文件面板：active/hover CSS 变量（`--active-file-*`、`--item-hover-*`）
- 大纲面板：active 加粗、hover 背景 + 文字色 + 下划线
- 同步脚本：`scripts/sync-typora.sh`

### Obsidian 主题（核心）

- 单一 `theme.css`，支持 Style Settings 插件
- 深色模式独立选择方案（Storm / Night / Moon / Day）
- 浅色模式独立选择方案（Storm / Night / Moon / Day）
- 系统深/浅模式自动切换，每个变体使用自身调色板
- Obsidian 变量完整映射（背景、文字、链接、代码、标题、标签、Callout 等）
- 工作区 UI 统一背景（编辑区、文件列表、Tab 栏、Ribbon、状态栏）
- 文件列表：文件夹着色、悬停渐变、活跃文件高亮
- 缩进线修复（`::before` + 堆叠上下文方案）
- Callout：全部 13 种官方类型语义化配色，背景区分无标题栏
- 任务清单：7 种状态（unchecked/checked/`/`/`-`/`>`/`?`/`!`），自定义圆形 checkbox；图标对齐修复
- 高亮文字与 inline code 阅读/编辑模式一致
- Unchecked checkbox 边框加深（`--tn-comment`）
- Notice/Toast 通知样式接入主题调色板
- 同步脚本：`scripts/sync-obsidian.sh`

---

## 二、待完成

### 阶段 1 — 样式补全

| 项目 | 说明 | 状态 |
|------|------|------|
| 搜索高亮 | 搜索结果匹配文字背景色 | ☐ |
| 右键菜单 | `.menu`、`.menu-item` 背景和悬停色 | ☐ |

### 阶段 2 — 多变体验证

- 切换全部 8 个组合（4×深色 + 4×浅色），截图对比
- 重点检查：可读性、对比度、代码高亮是否协调

### 阶段 3 — 文档与发布准备

| 项目 | 说明 | 状态 |
|------|------|------|
| 截图素材 | 各变体效果图（Typora + Obsidian） | ☐ |
| manifest.json | 补全 `authorUrl`（GitHub 地址） | ☐ |
| 社区提交 | 按 Obsidian 官方流程提 PR 到 obsidian-releases | ☐ |

### 阶段 4 — 可选扩展

- JetBrains / VS Code 配色方案移植
- Typora 主题提交到官方主题库

---

## 三、文件结构（目标态）

```
themes/
├── obsidian/tokyonight/
│   ├── theme.css          ✓
│   ├── manifest.json      ✓（需补 authorUrl）
│   └── README.md          ✓
├── typora/tokyonight/
│   ├── tokyonight-storm.css  ✓
│   ├── tokyonight-night.css  ✓
│   ├── tokyonight-moon.css   ✓
│   ├── tokyonight-day.css    ✓
│   └── README.md             ✓
└── scripts/
    ├── sync-typora.sh     ✓
    └── sync-obsidian.sh   ✓
```

---

## 四、调色板参考

| 变体 | 背景色 | 特点 |
|------|--------|------|
| Storm | `#24283b` | 标准深色，蓝灰调 |
| Night | `#1a1b26` | 最深，纯黑感 |
| Moon | `#222436` | 深色，蓝紫调 |
| Day | `#e1e2e7` | 浅色，低饱和 |
