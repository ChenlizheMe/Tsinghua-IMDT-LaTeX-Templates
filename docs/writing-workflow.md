# 配置指令与正式写作

日常只编辑 `config/user.tex`、`chapters/` 和 `bib/references.bib`。两个主入口不需要改排版。`config/metadata.tex`、`work-plan-fields.tex`、`project-options.tex` 是内部存储与初始化，不再作为用户填写入口。

## 元信息

在 `\imdtsetup{...}` 中使用下列键，值含逗号或多段内容时放在花括号内。后写的键覆盖前写的键；可分成多个 `\imdtsetup`。

| 键 | 内容 |
| --- | --- |
| `title` | 论文题目，最多 25 个汉字（符） |
| `author` / `student-id` | 姓名 / 学号；保留为文本，前导零不会丢失 |
| `school` / `major` | 培养单位 / 专业；已有 IMDT 默认值 |
| `supervisor` / `supervisor-rank` | 学籍系统导师 / 职称；不代填亲笔签名 |
| `enrollment-date` | 计划表入学年月 |
| `report-date` / `form-date` | 报告日期 / 表格封面日期 |
| `defense-date` | 预计答辩年月 |
| `chapters` | 章节文件顺序，以逗号分隔，不带 `.tex` |
| `bibliography` | BibTeX 库路径，不带 `.bib`；默认 `bib/references` |

```latex
\imdtsetup{author={张三}, student-id={2026123456}}
```

## 开关指令

| 配置 | 值 | 默认 |
| --- | --- | --- |
| `mode` | `writing` 实际写作；`reference` 完整 12 页原件对照 | writing |
| `hints` | `show` / `hide`：红色和灰色提示 | show |
| `examples` | `show` / `hide`：演示段落、图、表、公式与引文 | show |
| `fonts` | `auto` 自动识别私人字库；`windows` 强制真实字库；`portable` 便携预览 | auto |
| `output` | `electronic` / `print`；打印模式按指南处理右页起始 | electronic |
| `lists` | `show` / `hide`：插图与附表清单 | hide |
| `symbols` | `show` / `hide`：术语符号表 | hide |
| `appendix` | `show` / `hide`：可选排版示例附录，同时要求 examples=show | hide |

便利命令：`\imdtshowhints`、`\imdthidehints`、`\imdtshowexamples`、`\imdthideexamples`。提交命令 `\imdtsubmission` 等价于：

```latex
\imdtsetup{mode=writing,hints=hide,examples=hide,appendix=hide}
```

这些配置在 `config/user.tex` 内设置，再重新编译。不要在正文中切换文档类或字体配置。

## 正式正文、提示和演示的区别

```latex
\section{研究方法}
\imdthint{提示：说明实验设计。这条内容可关闭。}

这里写你的正式正文，直接写在普通段落中，关闭提示后仍然保留。
实际方法引用相关研究\cite{zimmerman2007rtd}。

\begin{imdtexample}
这是可整体关闭的示范段落，正式内容不要放在这里。
\end{imdtexample}
```

已有 `\WriteHere` 与 `\TODO` 保持兼容，受同一个 hints 开关控制。不要把真正的正文写进提示或示例命令，否则关闭它们时其中内容也会被隐藏。普通 `figure`、`table`、`equation` 环境始终保留；它们的字号、标题、间距和编号由模板管理。

## 表格字段

所有字段均可直接放进 `\imdtsetup`：

| 键 | 内容 |
| --- | --- |
| `topic-scope` / `classification-number` | 选题范围 / 定密申请表编号 |
| `meeting-date` / `cross-discipline` | 开题会议日期 / 跨专业类别 |
| `domestic-references` / `foreign-references` | 查阅中外文献数量 |
| `key-references` | 主要文献，可用 `\par` 分段 |
| `advisor-comment` | 导师评语文本，由相应人员确认使用 |
| `research-conditions` / `project-category` | 研究条件 / 科研项目类别 |
| `work-plan` | 工作计划，可多段自动换行 |
| `literature-due` / `research-due` / `writing-due` | 文献阅读 / 研究 / 论文撰写完成时间 |
| `other-type` | 选择其他论文类型后的补充说明 |

选择项使用名称，模板自动定位勾号；重复设置同一组只保留最后一个选择。

| 键 | 允许值 |
| --- | --- |
| `secrecy` | `blank` / `public` / `secret` / `confidential` |
| `cross-discipline-check` / `expert-review` | `blank` / `yes` / `no` |
| `experiment` / `safety-training` / `safety-report` | `blank` / `yes` / `no` |
| `thesis-type` | `blank` / `research` / `survey` / `case` / `product` / `scheme` / `other` |

`blank` 清空一组选择。每个填写区超出宽度或高度时会警告，不以改变纸张、字号或分页来硬塞内容。

## 章节与文献

一章一个文件，通过 `\chapter`、`\section`、`\subsection` 自动套用字号、间距及编号。新段落之间留一空行；不要用连续 `\\`、手动 `\vspace` 或 `\fontsize` 排正文。`config/user.tex` 中 `chapters` 列表控制章节顺序。

长稿件先完整编译一次，再在配置末尾使用 `\includeonly{chapters/03-research-plan}` 局部编译；提交前重新注释。被排除章节保留已生成的目录、编号和引用缓存。

BibTeX 使用 `natbib + thuthesis-numeric.bst`，按首次引用排序。真实引文写在普通正文；未引用任何文献的空框架不生成空文献表。有实际 `\cite`、`\citet`、`\citep` 或 `\nocite` 后自动生成文献表。可从 Zotero/JabRef 导入真实会议论文等条目，避免手写编号和编辑 `.bbl`。

图表标签应唯一，图表的 `\label` 放在 `\caption` 后，使用 `\cref{fig:name}`、`\cref{tab:name}`、`\cref{eq:name}` 自动引用。单位置多文献使用 `\cite{key1,key2}`；正文式引文可用 `\inlinecite{key}`。完整示例和数据分别放在 `figures/`、`tables/`、`appendices/`、`data/`。

## 字体、格式和编译

私有 `fonts/` 提供真实字库后自动使用；公开预览的替代字体不作为严格字库一致的证明。正文 12 bp / 20 bp、两字首行缩进、标题层级和 Word 间距补偿由未修改的 ThuThesis 管理。原件对照和行政表格保持原始固定版式；普通写作的正文按段落正常流动和分页。依据见 `formatting-basis.md`。

使用 XeLaTeX。Overleaf 与本地 `latexmk` 自动完成 BibTeX 和重跑；`latexmkrc` 根据入口及用户配置指纹重建生成的根辅助文件，保留章节缓存。检查命令为 `python scripts/check-build.py build/*.log`。GitHub Actions 使用同一个任务名验证写作、提交、原件、表格及切换后的结果。
