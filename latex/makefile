LA  = pdflatex -shell-escape 
BIB = biber

default: report

report:
	$(LA) report.tex
	$(BIB) report
	$(LA) report.tex
