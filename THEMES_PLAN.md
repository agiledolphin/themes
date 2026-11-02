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

#### Typora（v1.0.0）

- Underground / Office District / Lab 三个独立 CSS 文件，由同一模板生成，配色直接取自 Obsidian 版 `theme.css`，两个平台颜色完全一致
- 元素覆盖与 Catppuccin Mod Typora 版相同（选择器集合一致）；色彩角色与 Obsidian 版一致：H1 冷青、H2 黄铜、链接钢蓝、表头黄铜、代码高亮角色相同
- Blockquote 透明背景 + 黄铜竖线（嵌套为钢蓝）
- 与其他 Typora 主题保持一致的两处：inline code 为冷青文字、链接常驻淡下划线

### 通用

- 搜索高亮（三套主题，Obsidian + Typora）：每套主题一个专用搜索色，区别于 `==高亮==` 黄色与选区色——TokyoNight 橙、Catppuccin peach、Wonderland 冷青。所有命中 25% 淡底；Obsidian 阅读模式改为搜索色描边（高亮层盖在文字上方，不能填底）；Typora 当前命中为实色底（Latte 因 peach 亮度居中改用 55% 淡底 + 正文色，对比度 4.0）
- 右键菜单（Obsidian）：菜单底色改为 `bg-dark` 与编辑区区分；选中项沿用各主题文件列表的 hover 语言（TokyoNight 蓝色淡底、Catppuccin lavender 实色填充、Wonderland 黄铜淡底）；删除等危险项选中时为红色淡底。Typora 右键菜单是 macOS 原生菜单，主题无法修改
- 排版调整（三套主题，2026-10-24）：H1 字号 2em → 1.75em；表格字号统一为 14px（`--font-smaller`，与代码、标签、脚注同档），表格内行内代码与单元格同大；表格改为按内容宽度（不再撑满），单元格内边距统一为 6px / 12px（Obsidian 两种视图 + Typora）
- Obsidian 阅读视图与编辑视图（Live Preview）一致性：分隔线统一 1px（`--hr-*`）；代码块边框与 8px 圆角改由 `--code-border-width` / `--code-radius` 驱动，编辑视图也有边框圆角；编辑视图行内代码补上边框（原被 app.css 高优先级规则清零），圆角保持 4px；代码块字号统一为 `--code-size`（14px）、行高统一为 `--line-height-normal`（1.75）；代码字体改读 `--font-monospace`（尊重 Obsidian 设置里的等宽字体）；标签字号改用 Obsidian 默认（0.875em）。剩余差异：引用块与代码块的上下留白（编辑视图逐行渲染，无法整体加留白）、搜索高亮描边 vs 填底（有意）
- 主题命名统一加 "Mod" 后缀（`Catppuccin` → `Catppuccin Mod`，`TokyoNight` → `TokyoNight Mod`），Typora CSS 文件、Obsidian manifest、Style Settings YAML、README 全部同步改名
- 同步脚本：`scripts/sync-typora.sh`、`scripts/sync-obsidian.sh`（自动识别 `obsidian/` 下所有主题目录）

当前版本：

| Obsidian | 版本 |
|----------|------|
| Lamplit（含七套配色） | 1.6.1 |

| Typora（Lamplit + 配色，文件 `lamplit-<配色>-<变体>.css`） | 版本 |
|--------|------|
| Lamplit TokyoNight | 1.4.5 |
| Lamplit Catppuccin | 1.3.4 |
| Lamplit Wonderland | 1.1.6 |
| Lamplit Merino | 1.0.3 |
| Lamplit Big Wave | 1.0.1 |
| Lamplit Impression | 1.0.0 |
| Lamplit Bauhaus | 1.0.0 |

（合并前各 Obsidian 主题的最终版本：TokyoNight Mod 1.5.2、Catppuccin Mod 1.3.3、Wonderland Mod 1.1.3）

---

## 二、待完成

### 阶段 1 — 样式补全

| 项目 | 说明 | 状态 |
|------|------|------|
| Wonderland Mod 调色 | 已实际使用，当前满意；有问题再按需调整（观察点见下） | ☑ |

**Wonderland Mod 调色修正**（2026-10-24，Obsidian 1.1.3 / Typora 1.1.2）：对下列观察点逐一取满足约束（易混淆色 ΔE ≥ 16、文字对比度 ≥ 4.3）且离原色最近的值——Underground 青绿 `#6fa8a0→#6ca59d`；Office 黄色 `#e2c47a→#e9d184`、青绿 `#79ada3→#78a499`；Lab 黄色 `#8a6a0e→#6d5d00`、青绿 `#2d7a72→#2e7567`、冷青 `#1d7c88→#007784`、黄铜 `#8f6426→#885c20`。核验：三个变体两种视图 0 差异，Lab 的 H1 / 高亮 / 标签升至 4.63 / 4.45 / 4.36。当时未处理的两点已于 2026-10-26 处理（见下）。

**2026-10-26 处理遗留两点**（Lamplit 1.1.1；Typora：Wonderland 1.1.5，其余三套各升补丁版本）：

- 深色背景区分：Office 原背景其实偏冷（Lab b* -4，与 Underground 同向），只是略亮。表面五层（bg / bg-dark / bg-hl / gutter / selection）保持亮度、改为偏暖（b* +5，与正文的暖色同向）：`#1a1a20→#1f1a14`、`#141418→#1a130b`、`#26262e→#2d251e`、`#36363f→#3e352d`、`#3a3a44→#423931`。与 Underground 背景的 ΔE 3.9 → 9.7；亮度不变，所有文字对比度不变（血红 4.31，无需调整）。三档候选（b* +2.5 / +5 / +8）做了预览，用户选中间档。
- 搜索命中对比度：测算发现与色相无关（换成任何色相，Lab 的 H1 都在 3.1–3.3），是 25% 底色压暗浅色背景、提亮深色背景所致，所有配色都有（深色变体正文/链接最低 3.3–3.7）。模板中搜索底色统一降为 18%（Obsidian 编辑器 Cmd+F 与搜索面板、Typora 搜索命中；高亮文字内的命中 35% → 25%）：深色变体正文/链接最低约 3.8–4.1，Lab 正文/链接 4.50、H1 3.63（大字号，WCAG 要求 3:1）。TokyoNight Day / Catppuccin Latte 受上游配色所限仍偏低。
- 同日修订（Lamplit 1.1.2 / Typora Wonderland 1.1.6）：用户实看后觉得 b* +5 的暖色偏脏、不够清爽。四组候选（中性炭灰 / 中性略亮 / 冷而亮 / 极微暖）预览后先选极微暖（b* +1.5，`#1f1d1b`），实看仍不舒服，改为中性炭灰：`#1d1d1d` / `#171717` / `#2a2a2a` / `#3a3a3a` / `#3e3e3e`（亮度比原先 +1.5），与 Underground ΔE 6.5；背景提亮后血红 `#c95f53→#cc6155`（4.34；与锈红 ΔE 22.4），注释 3.57、正文 10.51。核验：与上一基线的差异只在 Wonderland Office；阅读/编辑视图 0 不一致（完整运行末尾 Wonderland Lab 的编辑视图标签一节因窗口被遮挡漏测，单独重跑 Lab 后数值与之前一致，结果已并入 `.verify`）。
- 核验：与 2026-10-26 完整基线对比 122 处差异，全部在预期内——Wonderland Office 86 处（表面颜色），其余 12 个变体各 3 处（搜索高亮透明度）；阅读/编辑视图 0 不一致。

原始观察点（2026-10-12）：

- 黄铜 vs 黄色接近：Office ΔE 11、Lab ΔE 12（Underground 16）——H2 / 标签 / 表头 与 `==高亮==` / question callout 可能混淆
- 冷青 vs 青绿接近：Office ΔE 13、Lab ΔE 12（Underground 15）——H1 与 H4、tip 与 abstract callout
- Underground 与 Office District 背景几乎相同（ΔE 3.9），区别主要在正文冷暖（ΔE 11.9）
- Lab 下搜索命中落在冷青文字上（H1、Typora 行内代码）对比度仅 3.1
- Lab 注释色对比度 3.3，三个变体中最低

### 阶段 2 — 多变体验证（Obsidian 已完成 2026-10-24；Typora 暂不验证）

通过 Obsidian 远程调试端口自动执行（工具已收入仓库 `scripts/verify-obsidian/`，用法见 CLAUDE.md）：三套主题 11 个变体 × 阅读视图 / 编辑视图（Live Preview），对测试笔记 `obsidian-theme-sample.md` 各章节截图（132 张，整理在核验页 artifact 中），并读取实际渲染样式逐项比对、计算对比度。

| 项目 | 结果 | 状态 |
|------|------|------|
| 两种视图样式一致性 | H1–H6、分隔线、代码块（边框/圆角/字号/字体/行高）、行内代码、表格（宽度/字号/内边距/表格内代码）、引用、高亮、链接、Callout、标签：11 个变体全部一致 | ☑ |
| 回归：阅读视图标签变成链接色 | 模板化提交引入（链接规则 `.markdown-rendered a` 与 app.css 的 `a.tag` 同优先级且在后）；改为 `a:not(.tag)` 后修复并重新验证（Obsidian 1.5.2 / 1.3.3 / 1.1.2） | ☑ |
| 行内代码内边距 | 主题的 `0.1em 0.4em` 只在阅读视图生效；改为使用 Obsidian 默认 `0.15em 0.3em`，两种视图一致 | ☑ |
| 编辑视图表格手柄 / 加行加列按钮 | 自动化截不到（DOM 中存在）；2026-10-24 手动确认：行列手柄、加行/加列按钮、单元格选中框（含圆角处）均正常 | ☑ |
| Typora 多变体验证 | 暂不进行 | — |

**对比度观察点**（阅读视图，文字对实际背景；正文类 < 4.3、弱化文字 < 3.0 视为偏低）——深色变体基本达标。TokyoNight 与 Catppuccin 的偏低项来自上游官方配色，**决定保持官方配色、不调整**（2026-10-24）：

- TokyoNight Day：多处约 3:1（H1 / 链接 3.1、H3 3.2、行内代码 3.5、高亮 3.2、标签 2.7）
- Catppuccin Latte：高亮文字 2.1、H1 2.8、H5 3.0、Note 标题 2.5
- TokyoNight Storm / Night：H6 与失效链接（注释色）2.4 / 2.8
- Wonderland Lab：H1 4.3、高亮 3.5 → 已随 Wonderland 调色修正（见阶段 1）

### 阶段 3 — 结构改进：模板化生成（已完成 2026-10-12）

全部 14 个主题 CSS 和 3 个 `manifest.json` 改由 `scripts/gen-themes.py` 生成，数据源为 `shared/palettes/<theme>.toml`（调色板、颜色角色、`nav_style` / `menu_style` 风格开关、版本号），模板为 `scripts/templates/{obsidian,typora}.css.tmpl`；`--check` 检查产物是否过期。取代原 `gen-wonderland-typora.py`。

| 项目 | 说明 | 状态 |
|------|------|------|
| 梳理有意保留的差异 | 颜色角色映射（Obsidian 76 处 / Typora 44 处）、导航与菜单的实色填充 vs 淡底两种风格、tooltip 参数 | ☑ |
| Typora 模板化 | 一个模板生成 11 个文件 | ☑ |
| Obsidian 模板化 | 一个模板生成 3 个 `theme.css`，Style Settings 块与 manifest 逐字节一致 | ☑ |
| 等价性验证 | 按变体解析变量后逐条对比选择器/属性/值与规则顺序：除下列有意修正外渲染完全一致 | ☑ |

梳理中发现并修正的不一致：

- Catppuccin 标签：阅读模式蓝色、Live Preview magenta（`.tag` 规则写死颜色只作用于阅读模式）→ 统一为 magenta，标签颜色改由 `--tag-*` 变量驱动（Obsidian 1.3.1）
- TokyoNight 的 4 个 Typora 文件初版遗留漂移 → 统一：Moon 引用竖线改蓝、Night 的 H4 改绿、Day/Moon 的代码内建函数与目录悬停改冷青（原为 2:2 平局，选冷青以与另两套主题一致）（Typora 1.4.1）

### 阶段 4 — 文档与发布准备（2026-11-02 启动）

官方流程已改为在 community.obsidian.md 提交并自动审核，不再向 obsidian-releases 提 PR。

| 项目 | 说明 | 状态 |
|------|------|------|
| 独立发布仓库 | `agiledolphin/lamplit`：根目录放主题文件，`scripts/publish-lamplit.sh` 从本仓库同步并发版（tag 与 manifest 版本相同，无 `v`）；已发布 `1.6.0` | ☑ |
| 截图素材 | `obsidian/lamplit/screenshot.png`：Wonderland Underground + Lab 对半，1024×576（16:9），只用示例笔记，不含 vault 文件列表 | ☑ |
| manifest.json | `authorUrl` 已填 | ☑ |
| LICENSE / README | 本仓库已补；发布仓库的 README 取自 `obsidian/lamplit/README.md` | ☑ |
| 社区提交 | 用户本人登录 community.obsidian.md 提交并发布，已上架 | ☑ |
| Typora 截图 | 各 Typora README 中的 *coming soon* | ☐ |

**社区目录自动审核**（Lamplit 1.6.0，页面 Scorecard）：0 错误、101 条警告（警告不阻止发布），Health Excellent、Review Caution。

| 数量 | 警告 | 处理 |
|------|------|------|
| 68 | 避免 `!important` | 待逐条判断，能改变量的改，每批跑完整核验，不追求清零 |
| 28 | `text-decoration` 14、`css-masks` 12、`css-boxdecorationbreak` 2 在 Obsidian 1.4.5 上部分支持 | 1.6.1 把 `minAppVersion` 从 1.0.0 提到 1.5.0 试验；扫描器不公开，效果待发布后确认 |
| 4 | 避免 `:has` | 1.6.1 已清除：H1 行改用 `.HyperMD-header-1`，任务行改用 `data-task` 属性 |
| 1 | CSS 文件超过建议大小（112KB，19 个方案） | 不处理 |

1.6.1 扫描结果：97 条。`:has` 已清除；提高 `minAppVersion` 对兼容性警告没有作用（仍为 28 条），保留 1.5.0，因 1.0.0 本来不准确（Color Folders 用到较新的 CSS）。

逐条检查（2026-11-02）：`text-decoration` 14 条与 `css-masks` 12 条保留（基本写法 / 图标实现，app.css 同样使用）。`box-decoration-break` 2 条多余，已删除模板规则（app.css 的 `.cm-s-obsidian span.cm-inline-code` 已设置），待下次发版生效。`!important`：临时全部去掉后测 3 个方案，只有高亮（`mark` 2 行及高亮内搜索命中 3 行）变化，这 5 行必须保留；其余未证明可删，因核验不测边距、flex、`mix-blend-mode`、复选框悬停与编辑视图，要先补探针再分组处理。

1.6.1 核验：`:has` 替换前后，编辑视图 H1 与 4 种任务行在光标离开 / 落在行上共 10 个状态样式 0 差异；19 个变体阅读/编辑视图 0 不一致，与基线 0 差异。

### 阶段 5 — 可选扩展

- JetBrains / VS Code 配色方案移植
- Typora 主题提交到官方主题库


### 阶段 6 — Obsidian 主题合并为 Lamplit（2026-10-25 完成）

名称 **Lamplit**（青灯夜读）。Obsidian 侧三套主题合并为一个，TokyoNight / Catppuccin / Wonderland 作为配色方案在 Style Settings 里选择；Typora 不变。

- 设置：深色方案 8 选 1、浅色方案 3 选 1（选项形如「Wonderland · Underground」，顺序 Wonderland → TokyoNight → Catppuccin），默认 Underground + Lab（与当前使用一致，无需迁移）；隐藏文件夹图标开关
- 差异处理：颜色角色与按风格变化的变量 → 每个变体块输出语义颜色（`--ll-accent`、`--ll-h2` …）；按风格变化的整条规则（文件列表 / 菜单的实色填充 vs 淡底）→ 两套都输出，用 `:where()` 限定作用域（不改变优先级）；未装 Style Settings 时默认走淡底风格
- 配置：新增 `shared/lamplit.toml`（名称、前缀 `ll`、Obsidian 版本、默认、顺序）；三个配色 toml 保留 `typora_version`，`obsidian_version` 移入 lamplit.toml
- 验证：先给核验工具补上文件列表 / 菜单 / tooltip / 搜索 / Obsidian 变量的测量，用现有三主题建立基线，再与 Lamplit 逐项对比，要求完全一致；另测深浅混搭

| 步骤 | 状态 |
|------|------|
| 1. 核验工具补测量项 + 基线（现有三主题 × 11 变体） | ☑ 补测 Obsidian 变量 122 个、UI 探针 72 个、5 种强制 hover/focus 状态；`--baseline` 逐项对比。修正测量不稳定：探针禁用过渡动画、每项只在所属章节取可见元素（全量与部分重跑 0 差异）；Obsidian 窗口隐藏时渲染暂停，工具改为先检查、不可见则拒绝运行 |
| 2. 生成器与模板改造，生成 `obsidian/lamplit/` | ☑ 静态检查：各变体变量定义完整 |
| 3. 与基线逐项对比、混搭测试 | ☑ 11 个变体共 13,519 项与旧三主题完全一致；阅读/编辑视图 0 差异；深色 Catppuccin Mocha + 浅色 Wonderland Lab 混搭各自与单独选择时一致 |
| 4. vault 切换到 Lamplit；删除仓库中三个旧 Obsidian 目录；README / CLAUDE.md 更新 | ☑ 2026-10-25 切换（深色方案设为 Wonderland · Office District，沿用用户当时的选择）；生成器与核验工具移除旧的每配色一主题模式 |
| 5. vault 中旧主题文件夹（用户确认后删除） | ☑ 已删除 TokyoNight Mod / Catppuccin Mod / Wonderland Mod 三个文件夹，保留 Lamplit 与用户自装的 Minimal |


### 阶段 7 — 新增 Merino 配色（2026-10-25）

按用户提供的 Merino Light / Merino Dark 终端配色截图设计（GitHub Primer 配色）。截图里的颜色原样采用；终端配色没有青绿和橙：青绿取其青与绿的中点，橙用 Primer 的橙。背景层级（bg-dark / bg-hl / gutter）取 Primer 的中性色，选区为蓝色淡底。

- 变体：**Light**（`#ffffff` / 文字 `#1f2328`）、**Dark**（`#0d1117` / 文字 `#e6edf3`）
- 强调色蓝（链接、H1、复选框、光标）；紫为第二声部（H2、表头）；标签青绿（浅色下对比度 5.1，紫只有 4.29）；搜索色橙；淡底风格
- 约束：点缀色对比度 ≥ 4.5、易混淆色 ΔE ≥ 16（最近一对 20），浅色高亮底透明度降为 0.15（高亮文字 4.32）
- 接入：`shared/palettes/merino.toml`；schemes 顺序 Wonderland → Merino → TokyoNight → Catppuccin；Lamplit 1.1.0，Typora Merino Mod 1.0.0；生成器修正新配色目录不存在时的写入错误

| 步骤 | 状态 |
|------|------|
| 配色与约束检查 | ☑ |
| 生成（Lamplit + Typora）并同步 | ☑ |
| Typora 实际效果（Light / Dark） | ☑ 用户手动确认 |
| Obsidian 自动核验：Merino 两变体 + 原 11 变体与上次 `.verify` 逐项对比（应 0 差异） | ☑ 13 个变体阅读/编辑视图 0 不一致；Merino 对比度全部达标（Light 最低为高亮 4.31，Dark 最低为 H6 4.12）。原 11 变体只有 `table.parentWidth` 不同，查明是基线测量偏差：基线 10 个变体的阅读视图记成 0px，本次全部 700px，表格宽度两次一致，实际渲染无变化。`analyze.py --baseline` 改为跳过基线里没有的变体并列出名称 |

### 阶段 8 — Mermaid 图（2026-10-25）

机制（查自两个应用的源码，Mermaid 均为 11.13.0）：

- **Obsidian**：初始化 Mermaid 时不指定主题，一律用默认浅色主题；只有字体读主题（`--font-mermaid` → `--font-text`）。深色模式下 app.css 给整张图加 `filter: invert(100%) hue-rotate(180deg) saturate(1.25)` 反相。Lamplit 不改：图的颜色与配色方案无关，但各方案都能看清。若要随配色走，需去掉反相滤镜，并按图表类型用 `!important` 覆盖 Mermaid 内嵌、以图 id 限定的样式，没有变量可用，不做。
- **Typora**：读主题的 `--mermaid-theme`（基础样式设为 `default`）。`default` / `dark` / `forest` / `neutral` / `base` 直接用 Mermaid 同名主题；`night` 用 Mermaid 的 `dark` 主题；值为空时走自定义方式：Mermaid `base` 主题，以 `--node-fill` 为主色推导整套颜色，另读 `--node-text-color`、`--cluster-fill`（备注底色）、`--text-color`（备注文字）、`--bg-color`、`--mermaid-font-family`。深浅判断：`--node-fill` 是十六进制时用一个读错蓝色分量的公式（如 `#161b22` 被判成浅色），否则按页面背景判断。
- Mermaid 自带的 `dark` 主题按 `#333` 灰底设计，饼图等配色里有 `#0b0000` 这类近黑色，放在我们接近纯黑的底上看不见（Night 方式试过，用户截图确认此问题）。

| 项目 | 状态 |
|------|------|
| Typora 深色变体：`--mermaid-theme` 置空走自定义方式，`--node-fill` 为强调色 30% 叠在背景上（写成 `rgb()`，绕开深浅判断的 bug），节点文字为正文色，备注底色为 bg-hl；浅色变体保持 `default` | ☑ 用 Typora 自己的配置函数 + Mermaid 库在无头浏览器中渲染确认（theme=base、darkMode=true）；用户在 Typora 中确认 |
| Typora 浅色变体（2026-10-26）：同样走自定义方式，`--node-fill` 为强调色 20% 叠在背景上（深色 30%），四套浅色主题的图表随配色带色调；原先为 Mermaid 默认主题（淡紫节点、黄色备注），与配色无关（Typora：TokyoNight 1.4.4 / Catppuccin 1.3.3 / Wonderland 1.1.4 / Merino 1.0.2） | ☑ 无头浏览器渲染确认（theme=base、darkMode=false）；用户在 Typora 中确认 |
| Typora 图表外框：未编辑的图表恢复 Typora 默认的无框无底（原先代码块样式的 `!important` 底色与内边距盖掉了 Typora 的设置，面板又加了一圈边框）；编辑时保留代码块外观，预览上方加一条分隔线；子图框改用 bg-hl 底、gutter 边 | ☑ 同上 |
| Typora `--text-color`：基础样式为 `#333333`，主题从未设置，深色变体里下拉菜单、输入框、专注模式等处文字发暗；改为正文色 | ☑ |
| 版本：TokyoNight 1.4.3 / Catppuccin 1.3.2 / Wonderland 1.1.3 / Merino 1.0.1（Typora） | ☑ |
| 核验工具：示例笔记的 Mermaid 一节加入截图（等图渲染出来再截），报告页增加「Mermaid 图」 | ☑ Merino 两变体试跑正常 |

### 阶段 9 — Typora 主题改用 Lamplit 前缀（2026-10-26）

Typora 菜单里的主题名取自文件名。原先 `tokyonight-mod-storm.css` 显示为「Tokyonight Mod Storm」；Mod 对原创的 Wonderland、按终端配色设计的 Merino 并不贴切，而 TokyoNight / Catppuccin 直接去掉 Mod 又容易被当成官方移植、或与同名文件互相覆盖。改为统一前缀 `lamplit-<配色>-<变体>.css`（菜单显示「Lamplit Tokyonight Storm」等），与 Obsidian 的 Lamplit 同名、13 个主题在菜单中排在一起。

- 生成器：文件名前缀与文件头标题取自 `shared/lamplit.toml` 的 `name` + 各配色的 `short_name`；配色 TOML 删去 `name`（"… Mod"）
- 各 Typora README、CLAUDE.md、本文件同步改名；`analyze.py` 报告标题改为「Lamplit 渲染核验」
- Typora 主题目录：删除旧的 `*-mod-*.css`，同步新文件；用户需在 Typora 中重新选一次主题（用户已确认）
- 不另升版本（与阶段 8 浅色 Mermaid 同一批提交）
- 遗漏修正（2026-10-26）：核验工具 `run.mjs` 仍读取配色 TOML 已删除的 `name`，启动即报错（未连接 Obsidian、未改动任何东西）；该值本未使用，删去读取。随后完整核验 13 个变体建立新基线：阅读/编辑视图 0 不一致，对比度与此前一致，表格父容器宽度全部 700px，Mermaid 截图 26 张


### 阶段 10 — 新增 Big Wave 配色（2026-10-27）

参考山下达郎专辑《Big Wave》（1984）封面：浪管内侧的深海军蓝、浪花白、天空钴蓝、标题的珊瑚粉手写字、黄色冲浪板。封面只有蓝、白、珊瑚、黄四种颜色，代码高亮所需的绿、橙、红按 80 年代 City Pop 的夏日色补齐（棕榈绿、晚霞橙）。

- 变体：**Pipeline**（深色，`#0e1a30` / 文字 `#dbe5f2`）、**Spray**（浅色，`#f4f7fb` / 文字 `#18264a`）；用户选定一深一浅
- 角色：H1、表头、嵌套引用、关键字为珊瑚粉（专辑标题色，用户选定）；强调色钴蓝（链接、H2、光标、当前文件）；水青为 H3、行内代码、标签；冲浪板黄为 `==高亮==` 与 H5；搜索为晚霞橙；淡底风格
- 约束：初稿深色全部达标；浅色校正三处，均只降亮度：黄 `#8a6d00→#7e6200`（高亮 4.39，透明度 0.15 同 Merino Light）、水青 `#00798a→#007283`（标签 4.43）、珊瑚 `#c04a64→#bd4762`（4.61）。所有点缀色 ≥ 4.6，易混淆色 ΔE ≥ 21（最近：浅色珊瑚/红 21.3）
- 接入：`shared/palettes/big-wave.toml`（文件名带连字符，Typora 菜单显示「Lamplit Big Wave …」；CSS 前缀 `bw`）；schemes 顺序 Wonderland → Merino → Big Wave → TokyoNight → Catppuccin；Lamplit 1.2.0，Typora Big Wave 1.0.0
- 核验：15 个变体阅读/编辑视图 0 不一致；原 13 个变体与基线 0 差异；Big Wave 正文 13.65 / 13.81，最低 H6 4.28 / 4.03
- 2026-10-27 修订（Lamplit 1.2.1 / Typora Big Wave 1.0.1）：用户觉得 Pipeline 的高亮太黄、突兀。柠檬黄 `#f2d94e`（色度 69）是全页最亮最饱和的颜色，改为柔沙黄 `#e6cf7e`（色度 43）：文字 11.24、高亮 7.36，与晚霞橙 ΔE 34、棕榈绿 35。五组候选（柔沙黄 / 暖奶油 / 日晒板黄 / 淡金 / 柔沙黄 + 底色 14%）预览后用户选柔沙黄；影响高亮、H5、代码属性名，以及同样用黄色的 question callout、两种任务状态复选框和 `--text-warning`。Spray 不变。核验：与基线 33 处差异全部在 Big Wave Pipeline 的上述黄色用处；15 个变体阅读/编辑视图 0 不一致


### 阶段 11 — 新增 Impression 配色（2026-10-29）

参考莫奈《印象·日出》（1872）：勒阿弗尔港的清晨，大片冷灰蓝、灰绿的晨雾里只有一轮橙红的太阳和水中倒影是暖的。配色沿用这个结构——太阳是唯一的暖色与高饱和色，其余颜色偏冷、低饱和。用户要求覆盖深浅两种模式、浅色要通透；变体名、浅色太阳色统一为深朱红、深色底色（灰绿石板蓝）按建议默认。

- 变体：**Havre**（深色，`#1c272c` / 文字 `#d6dfe2`）、**Brume**（浅色，`#f4f6f5` / 文字 `#2a3842`）
- 角色：太阳 H1、表头、强调色（光标、当前文件、引用竖线）；港湾灰蓝为链接与 H2；海水青为 H3、行内代码、标签；淡紫雾为 H4、关键字、搜索命中、嵌套引用；赭黄光晕为高亮与 H5；岸边灰绿为字符串；茜红为错误；淡底风格
- 浅色「通透」：灰绿近白底，侧栏 / 代码块 / 边框之间只差一层雾色（`#ebf0ef` / `#e0e7e7` / `#cfd9da`），正文为深石板蓝而非纯黑，高亮底色透明度 0.15
- 约束：深色初稿全部达标；浅色校正三处——茜红转 5°（`#b03a34→#b2373b`，与太阳 ΔE 15.5→20.1）、青绿转 5°（`#2a6e5c→#2f6e58`，与海水青 ΔE 18.0→20.3）、赭黄略压暗（`#86601f→#835e1d`，高亮 4.30→4.40）。点缀色 ≥ 5.0（深色最低茜红 4.56），易混淆色 ΔE ≥ 20
- 已知：Brume 底色与 Wonderland Lab、Big Wave Spray 的 ΔE 仅约 2.5（近白底难以拉开，区别在点缀色）；Brume 太阳为作文字压成深朱红 `#b4471f`，发光感弱于 Havre
- 接入：`shared/palettes/impression.toml`（CSS 前缀 `im`）；schemes 顺序 Wonderland → Merino → Big Wave → Impression → TokyoNight → Catppuccin；Lamplit 1.3.0，Typora Impression 1.0.0
- 核验：17 个变体阅读/编辑视图 0 不一致；原 15 个变体与基线 0 差异；Impression 正文 11.27 / 11.1，最低 H6 3.87 / 3.88


### 阶段 12 — 新增 Bauhaus 配色与两个模板开关（2026-11-01）

参考包豪斯（1919–1933）：三原色加黑白灰、平涂色块、几何直角。正文只用红黄蓝与黑白灰；代码高亮所需的橙、绿、紫、青取伊顿色环的二次色（伊顿是包豪斯基础课教师），只出现在代码里。用户选定：加「实色高亮」与「直角」两个模板开关、浅色用暖纸白、变体名 Dessau / Weimar。

- 变体：**Weimar**（深色，`#161616` / 文字 `#ece8de`）、**Dessau**（浅色，暖纸白 `#f3f0e7` / 文字 `#1c1c1c`）
- 角色：H1、强调色为红；链接、H2、标签、表头为蓝；H3 在 Weimar 为黄、在 Dessau 为近黑加粗（黄色当不了浅色文字）；高亮为实心黄块；搜索为橙；导航与菜单用实色填充（悬停蓝、当前文件红）
- 两种黄：`yellow` 供文字用途（代码属性、警告，Dessau 压暗为 `#876700`），`signal` 为高亮色块的亮黄 `#f2c014`
- 约束：深色初稿全部达标；浅色橙 `#b85a12→#ad5106`、黄 `#8a6a00→#876700` 只降亮度至 4.6。文字点缀色 ≥ 4.6，易混淆色 ΔE ≥ 26，红 / 蓝实色填充上的导航文字 ≥ 4.5
- 已知：Weimar 底色与 Wonderland Office 的 ΔE 3.5（同为中性炭黑，区别在点缀色）

**模板开关**（配色 TOML 的 `[roles]`；不写即原样，其他配色输出不变）：

- `corners = "square"`：两个模板中所有圆角（2/3/4/6/8px）改由角色 `radius_2 … radius_8` 提供，直角时为 0；Obsidian 侧另把界面圆角变量 `--radius-s/m/l/xl`、`--input-radius`、`--tab-radius-active` 归零。任务复选框的圆形保留
- `mark_style = "solid"`：`==高亮==` 为实心色块（`mark_fill`，默认黄色）加深色字（`mark_text`，深色模式取 bg、浅色取 fg）。Obsidian 复用的 `--text-highlight-bg`（链接跳转闪烁、搜索等）仍为淡色，避免浅色正文压在亮黄上；高亮中的搜索命中保留黄底再叠搜索色
- 生成器：Lamplit 的 rule group 若无方案使用即不输出（避免空 `:where()`）；经角色间接指向 `mark-bg` 的颜色也能正确展开
- 等价性验证：原 17 个变体的 Typora 文件逐字节不变；Obsidian 与基线对比仅多出 6 个新记录的界面圆角变量（`--radius-*` 等），测到的均为 Obsidian 默认值，其余样式全部一致

- 接入：`shared/palettes/bauhaus.toml`（CSS 前缀 `bh`）；schemes 顺序 Wonderland → Merino → Big Wave → Impression → Bauhaus → TokyoNight → Catppuccin；Lamplit 1.4.0，Typora Bauhaus 1.0.0（其余 Typora 主题输出不变，不升版本）
- 核验：19 个变体阅读/编辑视图 0 不一致；Bauhaus 正文 14.79 / 14.96，最低 H6 4.98 / 4.72


### 修复：另一台 Mac 上找不到 Lamplit（2026-11-02）

Obsidian 列主题时要求 `manifest.json` 的 `name` 与文件夹名完全一致（`f.name === 文件夹名`，区分大小写），否则静默跳过、不报错。`sync-obsidian.sh` 原先靠 uv 读主题名，没有 uv 时退回仓库目录名，生成小写的 `themes/lamplit/`，主题因此不出现（用户在那台机器上确认文件夹确为小写，改名后恢复正常）。手动复制仓库的 `lamplit` 目录也有同样的问题。

- 脚本：主题名改用 sed 直接从 `manifest.json` 读取，不再依赖 uv；已存在只有大小写不同的文件夹时自动改名（macOS 磁盘默认不区分大小写，`mkdir -p Lamplit` 不会改变已有的 `lamplit`）
- 测试（无 uv、系统 bash 3.2）：全新 vault、已有小写文件夹、已是正确文件夹且另有其他主题、空主题目录，四种情况均生成 `Lamplit/`，其他主题不受影响
- README（根目录与 Lamplit）说明文件夹名必须完全一致，根 README 增加「Lamplit does not show up?」排查说明；CLAUDE.md 记录此规则


### 阶段 13 — 不用 clone 的安装方式（2026-11-02）

提供两种方式，共用一份发布文件：GitHub Release 压缩包，以及从最新 Release 下载安装的一行脚本。

- `scripts/package-release.sh`：先跑 `gen-themes.py --check`，打出 `dist/Lamplit-obsidian.zip`（`Lamplit/` 文件夹，名称取自 manifest，含 LICENSE）和 `dist/Lamplit-typora.zip`（19 个主题 + LICENSE），并打印 `gh release create` 命令
- `install.sh`（根目录）：`obsidian <vault>` / `typora [palette …]`，只需 bash、curl、unzip；支持 macOS 与 Linux，兼容系统 bash 3.2；重复运行即更新；自动修正只差大小写的文件夹；整个脚本包在 `main` 里，下载被截断时不会执行半截
- 测试（管道交给 bash、无 uv、假 HOME、`dist/` 代替 Release）：路径带空格、重复运行、小写文件夹、不影响其他主题、非 vault、缺参数、Typora 目录不存在、全部 / 指定配色、未知配色、下载失败、脚本被截断，共 11 项符合预期
- README 安装部分改为三种方式（一行命令 / 下载 Release / clone）；CLAUDE.md 记录发版流程。Release 的 tag 跟随 Lamplit 版本；只改 Typora 时用 `gh release upload --clobber` 替换当前 Release 的文件
- 首个 Release：`v1.4.0`（2026-11-02）。真实链接验证（macOS，无 uv，假 HOME）：一行命令装到临时 vault 与 Typora 目录，Obsidian 2 个文件与 Typora 19 个文件均与仓库逐字节一致；Linux 未实测


### 阶段 14 — 文件列表的文件类型图标（2026-11-02，Lamplit 1.5.0）

文件列表每个文件都带图标（`md` 也有，用户要求），默认显示，Style Settings 的「Hide File Icons」（`ll-hide-file-icons`）可隐藏。

- 按扩展名选图标（大小写不敏感），格式列表取自 Obsidian 程序代码：笔记 `md`、图片 8 种、白板 `canvas`、数据库 `base`、`pdf`、音频 8 种、视频 5 种；其余为普通文件图标。图标数据取自 Obsidian 内置的 Lucide 图标（file-text / image / layout-dashboard / table / file-type / music / film / file）
- 颜色用 `currentColor` 跟随文字，平时 65% 透明度，悬停与当前文件全色，因此实色填充风格无需单独规则；扩展名小标签保留不动。Typora 不涉及，Typora 主题版本不变
- 核验工具增加文件图标探针（普通、当前、悬停、重命名状态）
- 核验：每种扩展名含大写形式在 Obsidian 中实测映射正确，8 种图标互不相同；开关实测可隐藏文件图标且不影响文件夹图标；19 个变体阅读/编辑视图 0 不一致；与基线 95 处差异全部是新增探针（19 × 5，无 → 有值），原有内容 0 变化；悬停与当前文件时图标颜色在 19 个变体中都与文字一致
- 用户在 Obsidian 中确认显示效果，并手动测试了重命名


### 阶段 15 — 目录按顺序循环上色（2026-11-02，Lamplit 1.6.0）

Style Settings 的「Color Folders」（`ll-color-folders`，默认关闭）：顶层目录按排列顺序循环 8 种颜色，子目录图标与竖线继承，文件图标保持中性。

- 颜色取各方案现有的点缀色，按冷暖交替排序（蓝、橙、青绿、红、绿、紫、黄、青），相邻色差 22–68，深浅模式随方案自动切换。Bauhaus 的青与青绿同色，循环中有一色重复；用户决定不为此加特例（Bauhaus 一般不开此开关）
- 对比度：除 Catppuccin Latte 外对背景 ≥ 3:1（TokyoNight Day 最低 3.11）。Latte 的黄 2.31、青 2.47、橙 2.64、绿 2.96 来自官方配色且无更深的替代色，保持不变
- 实现：`:nth-child(8n + k of .nav-folder)` 设 `--ll-folder-color`，跳过占位元素与根目录文件；开关关闭时图标取原来的 `--text-accent`
- 已知限制（实测，无 CSS 解法）：颜色跟随位置，新增顶层目录会使后面的目录变色；列表较长时 Obsidian 把滚出屏幕的顶层目录移出页面，其余目录序号改变，滚动中颜色错位。展开全部目录（约 27000px）后在 50%–100% 滚动位置复现；Blue Topaz `2026102001` 的「按顺序」模式同样复现
- 考虑过的替代：按目录名首字符（用户的 article/attachments 等相邻目录同色）、脚本生成 vault 片段并记录对应关系、小插件。主题本身是纯 CSS，无法运行程序或保存记录。用户选择保留按顺序并写明限制
- 测试：19 个方案逐一开启开关，顶层颜色顺序、子目录继承、关闭后还原均正确（Wonderland Lab 首次因测试时序失败，单独重测通过）
- 核验：19 个变体阅读/编辑视图 0 不一致。开关开启时，与基线的差异只有目录竖线颜色（预期效果）；关闭时竖线恢复原值，其余全部一致
- 观察：一次完整核验中用户看到 `ideas` 下的文件图标与 `ideas` 图标对齐，切换主题后恢复。Obsidian 虚拟滚动把每行缩进缓存为行内 `margin` / `padding`，疑与此有关；切换 19 个方案、折叠展开、切换模式、重载主题、展开全部并滚动均未复现，原因未确认
- 核验工具：`run.mjs` 运行期间关闭 3 个可选开关、结束后恢复，结果与基线不再受用户当前设置影响（此前用户开着 Color Folders 时测量值混入了开启状态）

---

## 三、文件结构（现状）

```
themes/
├── shared/
│   ├── lamplit.toml           # Lamplit（Obsidian）设置：名称、前缀、版本、默认方案、顺序
│   ├── palettes/              # 每套配色的唯一数据源（.toml）
│   │   ├── tokyonight.toml
│   │   ├── catppuccin.toml
│   │   ├── wonderland.toml
│   │   ├── merino.toml
│   │   ├── big-wave.toml
│   │   ├── impression.toml
│   │   └── bauhaus.toml
│   └── tokens/base.css        # 仅参考，未被导入
├── obsidian/
│   └── lamplit/
│       ├── theme.css          ✓（生成）
│       ├── manifest.json      ✓（生成，需补 authorUrl）
│       └── README.md          ✓
├── install.sh                 # 从最新 Release 安装，无需 clone
├── README.md / README.zh-CN.md / LICENSE   # 总览与安装（英文 / 中文）/ MIT
├── typora/
│   ├── tokyonight/            # 各配色目录：lamplit-<配色>-<变体>.css（生成）+ README.md
│   │   ├── lamplit-tokyonight-{storm,night,moon,day}.css
│   │   └── README.md
│   ├── catppuccin/
│   │   ├── lamplit-catppuccin-{mocha,macchiato,frappe,latte}.css
│   │   └── README.md
│   ├── wonderland/
│   │   ├── lamplit-wonderland-{underground,office-district,lab}.css
│   │   └── README.md
│   ├── merino/
│   │   ├── lamplit-merino-{light,dark}.css
│   │   └── README.md
│   ├── big-wave/
│   │   ├── lamplit-big-wave-{pipeline,spray}.css
│   │   └── README.md
│   ├── impression/
│   │   ├── lamplit-impression-{havre,brume}.css
│   │   └── README.md
│   └── bauhaus/
│       ├── lamplit-bauhaus-{weimar,dessau}.css
│       └── README.md
└── scripts/
    ├── gen-themes.py      ✓  # 生成全部主题文件
    ├── templates/         ✓  # obsidian.css.tmpl, typora.css.tmpl
    ├── sync-typora.sh     ✓
    └── sync-obsidian.sh   ✓
```

---

## 四、调色板参考

### TokyoNight

| 变体 | 背景色 | 特点 |
|------|--------|------|
| Storm | `#24283b` | 标准深色，蓝灰调 |
| Night | `#1a1b26` | 最深，纯黑感 |
| Moon | `#222436` | 深色，蓝紫调 |
| Day | `#e1e2e7` | 浅色，低饱和 |

### Catppuccin

| 变体 | 背景色 | 特点 |
|------|--------|------|
| Mocha | `#1e1e2e` | 最深，深海军蓝 |
| Macchiato | `#24273a` | 略浅海军蓝 |
| Frappé | `#303446` | 冷灰蓝调 |
| Latte | `#eff1f5` | 浅色，暖白 |

### Wonderland

| 变体 | 背景色 | 特点 |
|------|--------|------|
| Underground | `#121218` | 最深最冷，地下水道 |
| Office District | `#1d1d1d` | 略亮、中性炭灰（不带色相），地面东京夜 |
| Lab | `#eef0f2` | 浅色，冷白实验室 |

| 角色 | Underground | Office District | Lab | 用途 |
|------|-------------|-----------------|-----|------|
| 黄铜 brass | `#c39a5f` | `#d4a85e` | `#885c20` | UI 强调、H2 |
| 冷青 cyan | `#7fcfcf` | `#86cccb` | `#007784` | H1、属性键、搜索 |
| 钢蓝 steel | `#7d9ac4` | `#8aa0c4` | `#3a5e94` | 链接、H3 |
| 血红 blood | `#c25a50` | `#cc6155` | `#a8323a` | 错误、危险 |
| 骨白 bone | `#e6e1d3` | `#ece5d4` | `#5a5446`（石墨） | tooltip |

### Merino

| 变体 | 背景色 | 文字 |
|------|--------|------|
| Light | `#ffffff` | `#1f2328` |
| Dark | `#0d1117` | `#e6edf3` |

| 角色 | Light | Dark | 用途 |
|------|-------|------|------|
| 蓝 blue | `#0969da` | `#58a6ff` | 强调色、链接、H1 |
| 紫 magenta | `#8250df` | `#bc8cff` | H2、表头、关键字 |
| 青 cyan | `#1b7c83` | `#39c5cf` | H3、行内代码 |
| 青绿 teal | `#167056` | `#3cbf90` | 标签 |
| 橙 orange | `#bc4c00` | `#f0883e` | 搜索、数字 |
| 红 red | `#cf222e` | `#ff7b72` | 错误、危险 |

### Big Wave

| 变体 | 背景色 | 文字 |
|------|--------|------|
| Pipeline | `#0e1a30` | `#dbe5f2` |
| Spray | `#f4f7fb` | `#18264a` |

| 角色 | Pipeline | Spray | 用途 |
|------|----------|-------|------|
| 珊瑚 coral | `#ff8fa3` | `#bd4762` | H1、表头、嵌套引用、关键字 |
| 钴蓝 cobalt | `#6ea0ff` | `#1f4fbf` | 强调色、链接、H2 |
| 水青 aqua | `#5fd4e0` | `#007283` | H3、行内代码、标签 |
| 冲浪板黄 board | `#e6cf7e` | `#7e6200` | 高亮、H5 |
| 晚霞橙 sunset | `#ff9f5a` | `#b8500f` | 搜索、数字 |
| 棕榈绿 palm | `#8fd18a` | `#2f7a2a` | 字符串、H4 |
| 红 red | `#ff6b6b` | `#c0303a` | 错误、危险 |

### Impression

| 变体 | 背景色 | 文字 |
|------|--------|------|
| Havre | `#1c272c` | `#d6dfe2` |
| Brume | `#f4f6f5` | `#2a3842` |

| 角色 | Havre | Brume | 用途 |
|------|-------|-------|------|
| 太阳 sun | `#f07a45` | `#b4471f` | 强调色、H1、表头 |
| 港湾灰蓝 harbor | `#82a3c8` | `#355f86` | 链接、H2 |
| 海水青 water | `#6cbcc4` | `#1f6f7a` | H3、行内代码、标签 |
| 淡紫雾 lilac | `#aa9ad6` | `#62538f` | H4、关键字、搜索 |
| 赭黄 ochre | `#dcb27a` | `#835e1d` | 高亮、H5 |
| 岸边灰绿 shore | `#a6bd7e` | `#4f6b2c` | 字符串 |
| 青绿 jade | `#6dbb9c` | `#2f6e58` | 代码中的 teal 角色 |
| 茜红 madder | `#e86060` | `#b2373b` | 错误、危险 |

### Bauhaus

| 变体 | 背景色 | 文字 |
|------|--------|------|
| Weimar | `#161616` | `#ece8de` |
| Dessau | `#f3f0e7` | `#1c1c1c` |

| 角色 | Weimar | Dessau | 用途 |
|------|--------|--------|------|
| 红 red | `#ff5a4e` | `#c4262e` | 强调色、H1、当前文件 |
| 蓝 blue | `#6f9dff` | `#1f4f9c` | 链接、H2、标签、表头 |
| 信号黄 signal | `#ffd23f` | `#f2c014` | 实色高亮块 |
| 黄 yellow | `#ffd23f` | `#876700` | H3（Weimar）、代码属性、警告 |
| 橙 orange | `#ff9a3c` | `#ad5106` | 搜索、数字 |
| 绿 green | `#6cc070` | `#2e7d32` | 字符串 |
| 紫 violet | `#b48cff` | `#6a3fa0` | 关键字 |
| 青 teal | `#4fc1b8` | `#00756e` | 行内代码 |
