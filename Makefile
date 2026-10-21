.PHONY: all report form check clean

all: report form

report:
	mkdir -p build/chapters build/appendices
	latexmk -xelatex -outdir=build imdt-proposal-report.tex

form:
	mkdir -p build
	latexmk -xelatex -outdir=build imdt-topic-work-plan.tex

check:
	python3 scripts/check-build.py build/*.log

clean:
	latexmk -C -outdir=build imdt-proposal-report.tex imdt-topic-work-plan.tex
