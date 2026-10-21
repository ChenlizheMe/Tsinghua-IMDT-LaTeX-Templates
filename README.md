# 清华大学 IMDT 开题报告与论文工作计划 LaTeX 模板

[![Build LaTeX](https://github.com/ChenlizheMe/Tsinghua-IMDT-LaTeX-Templates/actions/workflows/latex.yml/badge.svg)](https://github.com/ChenlizheMe/Tsinghua-IMDT-LaTeX-Templates/actions/workflows/latex.yml)

包含两个主入口；面向清华大学深圳国际研究生院电子信息（互动媒体设计与技术）专业。不是学校官方发布的 IMDT 模板。

| 编译入口 | 用途 |
| --- | --- |
| `imdt-proposal-report.tex` | 默认可直接写作的开题报告：封面、自动目录、分章正文、BibTeX；可切换完整 12 页 Word 对照模式 |
| `imdt-topic-work-plan.tex` | 4 页 B5 选题及论文工作计划表，共用同一套元信息 |

## 先填姓名、学号和题目

**只需打开 [config/user.tex](config/user.tex)，在已有 `\imdtsetup` 的花括号内填写。不要修改排版坐标或内部宏。** 例如下面是虚构的填写示例：

```latex
\imdtsetup{
  title       = {面向交互体验的原型设计研究},
  author      = {张三},
  student-id  = {2026123456},
  supervisor  = {李老师},
  report-date = {2026年10月21日},
  form-date   = {2026年10月21日},
  defense-date = {2028年6月},
}
```

题目、姓名、学号、培养单位、专业和导师会自动进入两份材料。日期按实际提交日期填写。新项目不预填个人信息。

## 显示、隐藏提示，以及生成正式稿

这些命令均写在 `config/user.tex` 中；后写的配置覆盖先写的配置。

```latex
\imdthidehints       % 隐藏所有红色/灰色填写提示
\imdtshowhints       % 重新显示
\imdthideexamples    % 隐藏演示图、示例公式、演示引文、示例表格
\imdtshowexamples    % 重新显示
```

也可统一用键值配置：

```latex
\imdtsetup{hints=hide, examples=hide}
```

**提交时，在配置文件末尾取消 `\imdtsubmission` 的注释即可。** 该命令启用写作模式，关闭全部提示、演示内容和示例附录。只关闭提示不会删除普通正文；所有你自己的内容都应写在提示命令与示例环境之外。正式稿缺题目、姓名或学号时会在日志中明确提示。

## 正文写在哪里

在 [chapters/](chapters/) 按章写普通 LaTeX。不要手动给每段加字体和空行调整排版。

```latex
\chapter{课题背景与意义}
\section{选题背景}
这是正式正文。新段落之间留一个空行，模板自动处理缩进和行距。

这里继续写下一段，并引用真实文献\cite{zimmerman2007rtd}。
\subsection{研究问题}
这里写研究问题。
```

`\imdthint{这里是写作提示}` 只用于提示。`imdtexample` 环境只用于可整体关闭的示范内容；正式图表、公式和段落不要包在里面。新增章节文件后，在 `config/user.tex` 的 `chapters={...}` 列表中加入文件路径，文档顺序、目录、编号及交叉引用自动更新。

## 排版如何保证

正文由固定的 **ThuThesis 7.7.1** 自动排版，未改动上游类文件：A4、四边 3 cm；中文宋体、英文 Times New Roman、小四 12 bp、固定 20 bp 行距、段前段后 0、首行缩进两字；章节标题自动采用黑体/Arial 及规定字号和间距。图题在下、表题在上，图表公式按章编号。无需逐段套格式。

章标题的 Word 段前 24 磅/段后 18 磅由上游针对 Word/TeX 不同行距算法作视觉补偿，不能把 TeX 内部的 27/27 bp 数值直接当成 Word 段距。规则、来源及验证口径见 [格式依据](docs/formatting-basis.md)。报告沿用 IMDT 专用封面；行政表格保持原件 B5 结构。

在私人 Overleaf 的 `fonts/` 提供原字库后，`fonts=auto` 自动启用真实宋体、黑体、Times New Roman、Arial 等；缺失严格字库会报错。公共 ZIP 不分发商业字体，没有原字库时仅用 Fandol/TeX Gyre 便携预览，不能称为原字体。详见 [字体配置](fonts/README.md)。

## 表格如何填

同样编辑 `config/user.tex`，使用原生选择值，互斥选择自动清空前一项：

```latex
\imdtsetup{
  meeting-date = {2026年10月21日},
  secrecy = public,
  cross-discipline-check = no,
  experiment = yes, safety-training = yes, safety-report = yes,
  thesis-type = product,
  research-conditions = {已具备原型制作与用户研究条件。},
  work-plan = {第一阶段完成文献调研。\par 第二阶段实现并评价原型。},
}
```

配置文件内已有可取消注释的完整示范；全部字段及选择值见 [使用说明](docs/writing-workflow.md)。填写区自动换行；超出固定四页表格的预留空间会明确报警，应精简或另附续页。

## Overleaf 与本地编译

1. 下载整个仓库 ZIP，在 Overleaf 选择 New Project → Upload Project。
2. Compiler 选 **XeLaTeX**，Main document 选上述一个主入口。
3. 打开 `config/user.tex` 填信息；正文编辑 `chapters/`；文献维护 `bib/references.bib`。
4. 重新编译；latexmk 自动运行 BibTeX 并解析目录、图表与交叉引用。

GitHub 同步可在 Overleaf Integrations → GitHub 中手动拉取/推送，需要 Overleaf 的相应权限；没有同步权限可用 ZIP。见 [Overleaf 官方说明](https://docs.overleaf.com/integrations-and-add-ons/git-integration-and-github-synchronization/github-synchronization)。

本地支持 `make`、`make check` 和 `scripts/build.ps1`。VS Code 配置已附。GitHub Actions 编译两个入口，并检查写作、提交、原件对照、填写表格及共享缓存切换，保存 PDF 产物。

## 查看原 Word 的完整 12 页

```latex
\imdtsetup{mode=reference, hints=show}
```

保留原件全部说明、空白页、图表示例及两套备选提纲；用于对照学习。回到写作使用 `\imdtsetup{mode=writing}`。原件对照采用原生可检索字形与规则线，封面元信息仍可配置；不是整页截图或 PDF 背景。两份原始 Word 保留原文件名和字节，位于 [references/originals/](references/originals/)，附 SHA-256。

## 格式版本与资料

完整条文核对清华官方的 **2025 年 3 月写作指南**，并核对 ThuThesis 维护者记录的 **2026 年 5 月修订**，采用已适配更新的 7.7.1。未取得可独立核验的 2026 完整指南全文，因此所存 PDF 仍明确标为 2025-03。详情见 [格式依据](docs/formatting-basis.md)、[原件核对](docs/source-comparison.md) 和 [第三方说明](THIRD_PARTY_NOTICES.md)。
