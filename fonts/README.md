# Word 字体配置

报告与工作计划表共用 `config/word-fonts.tex`。这里不分发字体二进制文件。

要在 Overleaf 使用与原 Word 相同的字库，将自己可使用的以下文件放在本目录，注意 Linux 文件名区分大小写：

- `SimSun.ttc`、`SimHei.ttf`、`Simkai.ttf`、`Simfang.ttf`
- `times.ttf`、`timesbd.ttf`、`timesi.ttf`、`timesbi.ttf`
- `arial.ttf`、`arialbd.ttf`、`ariali.ttf`、`arialbi.ttf`
- `Deng.ttf`（等线；原报告页码使用）

检测到 `fonts/SimSun.ttc` 后，两份主入口自动启用真实宋体、黑体、Times New Roman 和 Arial；楷体和仿宋用于中文斜体与辅助字体。严格模式缺少文件会明确报错，不会静默替换字库。

在已安装这些字体的 Windows 机器上，也可直接将 `IMDTUseWindowsFonts` 设为 true，使用系统字库。

公开仓库不含这些文件，因此其默认预览采用 Fandol 与 TeX Gyre；该预览不能宣称字体与 Word 完全一致。字体文件已被 `.gitignore` 排除，`git archive` 导出的公共 ZIP 也不含字体。
