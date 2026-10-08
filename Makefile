PYTHON ?= python3

.PHONY: check integrity paper trial88 cyclic-traces

check:
	$(PYTHON) verify_sector_refinement.py
	$(PYTHON) verify_cyclic_traces.py
	$(PYTHON) verify_spectral_refinement.py
	$(PYTHON) verify_adaptive_bound.py
	$(PYTHON) verify_signed_extension.py
	$(PYTHON) verify_companion_corollary.py
	$(PYTHON) verify_gap_improvement.py

trial88:
	$(PYTHON) verify_trial88.py

cyclic-traces:
	$(PYTHON) recompute_cyclic_traces.py

integrity:
	$(PYTHON) tools/check_integrity.py

paper:
	cd paper && pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error note.tex
	cd paper && pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error note.tex
