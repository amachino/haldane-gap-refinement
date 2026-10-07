PYTHON ?= python3

.PHONY: check integrity paper

check:
	$(PYTHON) verify_gap_improvement.py

integrity:
	$(PYTHON) tools/check_integrity.py

paper:
	cd paper && pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error note.tex
	cd paper && pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error note.tex
