# Word 字体配置

报告与工作计划表共用 `config/word-fonts.tex`。这里不分发字体二进制文件。

要在 Overleaf 使用与原 Word 相同的字库，将自己可使用的以下文件放在本目录，注意 Linux 文件名区分大小写：

- `SimSun.ttc`、`SimHei.ttf`、`Simkai.ttf`、`Simfang.ttf`
- `times.ttf`、`timesbd.ttf`、`timesi.ttf`、`timesbi.ttf`
- `arial.ttf`、`arialbd.ttf`、`ariali.ttf`、`arialbi.ttf`
- `Deng.ttf`（等线；原报告页码使用）
- `symbol-unicode.ttf`（旧 Symbol 勾选提示的 Unicode 访问副本，见下）

Word 表格的两处勾选提示使用旧 Symbol 私用区字符。为保留原字形，并让 PDF 可复制为 `√`，先在本地运行：

```sh
python scripts/prepare-symbol-font.py /path/to/symbol.ttf fonts/symbol-unicode.ttf
```

Windows 原字库通常在 `C:/Windows/Fonts/symbol.ttf`。脚本不改动原文件，只为副本补充 Unicode 字符映射，字形轮廓、度量和 hinting 保持原样。将生成的副本上传到私人 Overleaf 项目的 `fonts/`，不要加入公共仓库。公开便携预览仍使用宋体替代根号。

检测到 `fonts/SimSun.ttc` 后，两份主入口自动启用真实宋体、黑体、Times New Roman 和 Arial；楷体和仿宋用于中文斜体与辅助字体。严格模式缺少文件会明确报错，不会静默替换字库。

在已安装这些字体的 Windows 机器上，也可直接将 `IMDTUseWindowsFonts` 设为 true，使用系统字库。

公开仓库不含这些文件，因此其默认预览采用 Fandol 与 TeX Gyre；该预览不能宣称字体与 Word 完全一致。字体文件已被 `.gitignore` 排除，`git archive` 导出的公共 ZIP 也不含字体。
