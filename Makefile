PYTHON ?= python3
MODEL_PYTHON ?= .context/venv/bin/python

.PHONY: all player bench mesen test test-arm
all: player
player:
	$(PYTHON) scripts/build_fceux_player.py
bench:
	$(PYTHON) scripts/build_fceux_bench.py --host
mesen:
	$(PYTHON) scripts/build_mesen_nes.py --player --arm
test: player bench
	$(PYTHON) scripts/test_standalone.py
test-arm: player
	$(PYTHON) scripts/make_nes_demo.py .context/amiga/fceux-player/standalone-demo.nes
	$(MODEL_PYTHON) tests/amiga/fceux_player/check_arm.py .context/amiga/fceux-player/standalone-demo.nes 6
