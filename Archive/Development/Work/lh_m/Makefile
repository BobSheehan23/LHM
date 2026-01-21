PY := python

.PHONY: charts clean nb

charts:
	@echo "→ Generating charts into ./charts …"
	$(PY) make_charts.py
	@echo "✓ Charts updated."

clean:
	@echo "→ Removing generated charts …"
	@rm -f charts/*.png || true
	@echo "✓ Clean."

nb:
	@echo "→ Launching Jupyter Lab (uses your venv kernel)"
	jupyter lab
