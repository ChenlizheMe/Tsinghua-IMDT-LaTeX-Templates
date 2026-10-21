# 清华大学 IMDT 硕士开题报告与论文工作计划模板

[![Build LaTeX](https://github.com/ChenlizheMe/Tsinghua-IMDT-LaTeX-Templates/actions/workflows/latex.yml/badge.svg)](https://github.com/ChenlizheMe/Tsinghua-IMDT-LaTeX-Templates/actions/workflows/latex.yml)

面向清华大学深圳国际研究生院电子信息（互动媒体设计与技术，IMDT）的模块化 LaTeX 写作工程。包含两个主入口，适合从开题报告持续扩展为较大规模的研究稿件；不是学校官方发布的 IMDT 模板。

| 主入口 | 用途 |
| --- | --- |
| [imdt-proposal-report.tex](imdt-proposal-report.tex) | A4 开题报告，封面、目录、分章正文、BibTeX 参考文献 |
| [imdt-topic-work-plan.tex](imdt-topic-work-plan.tex) | 原始 202401 版选题及论文工作计划表，保留四页 B5 结构 |

**先修改 [个人信息](config/metadata.tex)，再编辑 [章节](chapters/) 和 [文献库](bib/references.bib)。** 两份原始 Word 已完整放在 [原始材料](references/originals/) 中。

## Overleaf 开始使用

1. 下载整个仓库 ZIP，在 Overleaf 选择 New Project → Upload Project。请上传整个工程，不能只上传两个主入口。
2. Compiler 选择 **XeLaTeX**。使用近期 TeX Live；工程自带固定版本的排版类和参考文献样式。
3. Main document 选择上表中的一个主入口，重新编译。Overleaf 的 latexmk 会自动调用 BibTeX；不需要手动维护文献编号。
4. 切换 Main document 可分别得到报告和工作计划表。两份文档使用不同排版类，切换后请在 Recompile 旁的下拉菜单选择 **Recompile from scratch**，避免旧辅助文件互相影响。

需要 GitHub 同步时，在 Overleaf 关联 GitHub，再用 New Project → Import from GitHub 导入本仓库。后续通过 Integrations → GitHub 手动推送或拉取。该同步功能需要 Overleaf 的相应订阅权限；没有同步权限也能上传 ZIP 编译。参见 [Overleaf 官方说明](https://docs.overleaf.com/integrations-and-add-ons/git-integration-and-github-synchronization/github-synchronization)。

## 这个工程提供什么

- 固定使用 **ThuThesis 7.7.1**，由其管理研究生报告的页边距、标题、目录、页眉页码、图表、公式和脚注格式。正文四边页边距为 3 cm，行距为 20 bp。
- **BibTeX + natbib + thuthesis-numeric.bst**：独立 UTF-8 文献库、按首次引用自动排序编号、连续编号压缩、DOI/URL、会议论文条目和中文机构作者。
- 正文按章节拆分，图、表、封面、附录和表格页分别管理；可用 includeonly 局部编译长稿件。
- 共用个人信息；草稿提示、打印模式、指定字库、图表清单、术语表和附录均有集中开关。
- 提供可编辑 TikZ 矢量图，以及可选的子图、三线表、表下注释、跨页长表、算法、定义、单位和自动交叉引用示例。
- 支持 latexmk、Windows PowerShell、Make 和 VS Code LaTeX Workshop；GitHub Actions 自动编译两个 PDF、检查最终日志并保存下载产物。
- 原始 Word 文件保留原文件名与字节内容，附 SHA-256；学校指南、版本依据和第三方许可证均有记录。

## 工程结构

~~~text
imdt-proposal-report.tex        报告主入口
imdt-topic-work-plan.tex        工作计划表主入口
config/
  metadata.tex                 两份材料共用的个人信息
  project-options.tex          草稿、打印、字库、附录等开关
  report-setup.tex              报告宏包、引用与自定义命令
  work-plan-fields.tex          计划表的选择项及内容
  form-layout.tex              B5 表格排版
chapters/                      四章正文，一章一个文件
frontmatter/                   IMDT 封面、可选术语表
bib/references.bib             BibTeX 文献库
figures/                       图片与可编辑矢量图
tables/                        独立表格
appendices/                    可选的长稿件写作示例
forms/                         计划表的四个页面
data/                          图表数据和数据说明
references/originals/          两份原始 Word
references/guidelines/         完整指南的公开版本
docs/                          写作流程、格式核对、来源说明
scripts/                       构建与编译日志检查
vendor/thuthesis/              固定上游版本的源文件与许可证
.github/workflows/latex.yml    自动编译与 PDF 下载
~~~

## 写作与引用

在章节里直接写正文。灰色 WriteHere 和红色 TODO 命令仅用于提示，正式内容应写在这些命令之外。完成后将公共开关中的 IMDTDraft 设为 false，隐藏剩余提示。

~~~latex
\section{研究问题}
\label{sec:research-question}
在此撰写正式正文，并引用相关研究\cite{zimmerman2007rtd}。
技术路线如\cref{fig:research-route}所示。
~~~

将 Zotero 或 JabRef 导出的 BibTeX 条目放入文献库，用稳定的文献键引用。不要手写 [1]、[2]，也不要编辑生成的 .bbl 文件。库中附了两篇经 DOI 核对的真实会议论文和学校指南作为演示；它们不能代替本课题应完成的文献阅读。

原 IMDT 材料要求不少于 20 篇中外文献、报告不少于 5000 字，题目控制在 25 个汉字（符）以内。正式提交前应替换示例，检查内容要求。更多操作见 [长稿件写作工作流](docs/writing-workflow.md)。

## 本地构建

需要 TeX Live 或 MiKTeX 中的 XeLaTeX、BibTeX 和 latexmk。默认使用 TeX Live 自带的 Fandol 与 TeX Gyre 字体，无需额外上传字体。

~~~powershell
# Windows：构建两份 PDF，输出到 build/
.\scripts\build.ps1
.\scripts\build.ps1 -Target Report
~~~

~~~sh
# macOS / Linux
make
make check

# 直接使用 latexmk 也可以
latexmk -xelatex imdt-proposal-report.tex
latexmk -xelatex imdt-topic-work-plan.tex
~~~

每次推送到 main，GitHub Actions 都会构建。运行完成后，在 Actions 的对应运行页面下载 imdt-compiled-pdfs。默认提供 14 天的构建产物保留期。

## 格式依据与版本

本工程核对了清华官方域名发布的 **2025 年 3 月完整研究生写作指南**，并核对了 ThuThesis 维护者公布的 **2026 年 5 月指南与模板修订记录**，采用已适配该更新的 ThuThesis 7.7.1。2026 年公开修订记录指出主要变更为博士、硕士授权页统一；本开题报告不加入学位论文授权页。

仓库中保留的完整 PDF 明确标为 2025-03，没有把它冒称为 2026 版。逐项规则、来源、已核对范围和 IMDT 专用格式见 [格式依据](docs/formatting-basis.md)。

默认便携字体与指南点名的中易宋体、黑体、Times New Roman、Arial 并非完全相同字库。需要指定字库时可开启 IMDTUseWindowsFonts，并在有权使用这些字体的环境中编译。字体和打印模式的切换方法见写作工作流。

上游 ThuThesis 文件未经修改，其许可证和来源见 [第三方说明](THIRD_PARTY_NOTICES.md)。
