$pdf_mode = 5;
$xelatex = 'xelatex -interaction=nonstopmode -halt-on-error -file-line-error -synctex=1 %O %S';
$bibtex = 'bibtex %O %B';
$bibtex_use = 1;
$max_repeat = 5;
@default_files = ('imdt-proposal-report.tex', 'imdt-topic-work-plan.tex');
