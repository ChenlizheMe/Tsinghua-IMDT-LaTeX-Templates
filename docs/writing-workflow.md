# 大型稿件写作工作流

## 文件分工

个人信息只在 config/metadata.tex 修改一次。报告正文写入 chapters/，一章一个文件；较大的章节也可继续用 input 拆成子文件。主入口只保留文档顺序，不在里面堆积正文与宏包设置。

图表放在 figures/ 和 tables/，较长的算法、问卷或补充材料放在 appendices/。数据说明和图表生成依据放在 data/。排版调整统一进入 config/report-setup.tex，避免在各章重复添加字号、间距和颜色命令。

## 草稿与提交模式

config/project-options.tex 中的开关由两个主入口共用。

| 开关 | true 时的行为 | 默认 |
| --- | --- | --- |
| IMDTDraft | 显示 WriteHere 和 TODO 提示 | true |
| IMDTPrint | 按研究生指南插入适合双面印刷的必要空白页 | false |
| IMDTUseWindowsFonts | 使用指南点名的 Windows 中西文字库 | false |
| IMDTShowLists | 生成插图与附表清单 | false |
| IMDTShowSymbols | 生成符号和缩略语说明 | false |
| IMDTIncludeAppendix | 加入可选排版示例附录 | false |

默认电子版保留“封面—目录—正文”的开题材料顺序。打印模式只影响报告；原始工作计划表继续使用其四页 B5 表格版式。

正式正文不要放进 WriteHere 或 TODO 内部。应删除整条提示命令，并在其位置写入正常正文；否则关闭草稿提示时，写在提示宏里的内容也会隐藏。

## BibTeX 文献管理

1. 在 Zotero、JabRef 等工具中整理真实文献，将条目导出或维护为 UTF-8 BibTeX。
2. 把条目添加到 bib/references.bib。文献键宜稳定，例如作者姓氏、年份和主题词的组合；合作写作时避免多人使用同一个键指向不同论文。
3. 正文使用 cite，文献表由 BibTeX 自动生成，编号按首次引用排序。同一位置可引用多个键。
4. 修改文献后让 latexmk 完成整轮编译，不要手动编辑 .aux、.bbl 或 .blg。

~~~latex
研究方法已有相关讨论\cite{zimmerman2007rtd,wobbrock2007dollar}。
文献\inlinecite{zimmerman2007rtd}给出了另一种讨论方式。
~~~

~~~bibtex
@inproceedings{stableCitationKey,
  author    = {Family, Given and Family, Given},
  title     = {Paper title with protected {HCI} capitalization},
  booktitle = {Conference proceedings title},
  year      = {2026},
  publisher = {Publisher},
  pages     = {1--10},
  doi       = {Replace with the verified DOI},
}
~~~

上面的条目仅演示字段结构，不应直接作为真实文献加入库中。中文机构作者可用双层花括号保护，例如 author = {{清华大学研究生院}}。检查题名、作者、年份、卷期、页码、DOI 等元数据；自动样式无法替代事实核验。

当前默认使用符合清华研究生要求的 thuthesis-numeric.bst，而不是直接套用 ACM/IEEE 会议排版。BibTeX 是文献处理工具，输出样式仍应服从学位论文指南。

## 章节与局部编译

主入口使用 include，便于保存每章辅助信息并选择局部编译。初次先完整编译一次，再启用：

~~~latex
\includeonly{chapters/03-research-plan}
~~~

没有完整编译产生的辅助信息时，被排除章节的编号、目录和引用可能暂时不完整。提交或生成最终 PDF 前，重新注释 includeonly 并完整构建。Overleaf 改动较大时可使用 Recompile from scratch。

## 图表公式与引用

建议标签命名：

| 对象 | 前缀示例 |
| --- | --- |
| 章 | chap:research-plan |
| 节 | sec:research-question |
| 图 | fig:research-route |
| 表 | tab:schedule |
| 公式 | eq:example |
| 算法 | alg:iteration |
| 附录 | app:examples |

标签必须唯一。图表的 label 放在 caption 后面，正文用 cref 自动生成带对象名称的引用。公式也可使用式加 eqref。不要在正文中手写“见图3.1”，否则移动章节时容易出现错号。

矢量框图可以用 TikZ；照片、截图和导出的图放到 figures/，由 includegraphics 加载。复用外部图片时注明来源。一个图含多个子图时用 subfigure，并同时给总图和分图设置标签。

常规数据表用 booktabs 三线表；需要文本换行时用 tabularx；跨页表使用 longtable，配好续页表头和表尾，不要把 longtable 放进 table 浮动体。表下注释使用 threeparttable。

可选附录已经演示了子图、表下注释、跨页表、算法、定义、单位和自动引用。启用 IMDTIncludeAppendix 可一起编译检查；正式正文只保留与课题相关的内容。

## 字体与打印

默认便携字库保证 Overleaf 开箱即用。若提交要求具体的中易宋体、黑体、仿宋、Times New Roman 和 Arial，开启 IMDTUseWindowsFonts 后，在已安装相应字体的 Windows 环境中构建。Overleaf 则需要使用者有权使用并按 ThuThesis 的字库配置说明提供相应字体；本仓库不分发商业字体。

开启 IMDTPrint 生成适合双面印刷的必要空白页；使用实际纸张尺寸，报告为 A4，工作计划表为 B5。不要依靠打印机“缩放到纸张”改变原始表格比例。

## 构建、核对与协作

Windows 可运行 scripts/build.ps1。macOS/Linux 可运行 make。latexmk 会自动完成 XeLaTeX、BibTeX 与必要的重复编译。本地脚本将产物放入 build/，该目录已忽略，不提交到 Git。

~~~sh
python scripts/check-build.py build/*.log
~~~

日志检查会对缺字、溢出、未解析引用、重复标签、编译错误和仍需重跑返回非零状态。Underfull 等提示不直接作为错误。日志通过后仍需检查 PDF 页面，尤其是长表、跨页公式、图片、目录和签名栏。

GitHub Actions 在推送和拉取请求时编译两个主入口，并检查日志。完成后可在运行页面的 Artifacts 下载 PDF。仓库中的原始 Word 和指南仅供对照，不参与编译。

合作写作时可按章节分工，个人信息、公共配置与文献库的修改应协调合并。GitHub 与 Overleaf 的同步为手动操作，尽量先拉取再编辑，推送前检查差异，减少同一文件同时修改引起的冲突。

## 提交前核对

- 替换所有提示、演示段落、示例图表和日期，按实际课题完善研究内容。
- 核对 20 篇中外文献、5000 字、25 字题目等 IMDT 原材料中的要求。
- 完成真实文献元数据与引文的一一核对，确保没有问号、重复标签和缺字。
- 关闭局部编译与草稿提示，选择所需字体和电子/打印模式，再完整构建。
- 逐页确认目录、页边距、图表、参考文献、签字和计划表内容。
