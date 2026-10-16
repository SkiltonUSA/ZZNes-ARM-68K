SCHEDULING ?= baseline
PYTHON ?= python3
MODEL_PYTHON ?= .context/venv/bin/python

.PHONY: all player bench mesen test test-arm
all: player
player:
	$(PYTHON) scripts/build_fceux_player.py --scheduling $(SCHEDULING)
bench:
	$(PYTHON) scripts/build_fceux_bench.py --host
mesen:
	$(PYTHON) scripts/build_mesen_nes.py --player --arm
test: player bench
	$(PYTHON) scripts/test_standalone.py
test-arm: player
	$(PYTHON) scripts/make_nes_demo.py .context/amiga/fceux-player/standalone-demo.nes
	$(MODEL_PYTHON) tests/amiga/fceux_player/check_arm.py .context/amiga/fceux-player/standalone-demo.nes 6

.PHONY: beta verify-beta
beta:
	$(PYTHON) scripts/build_beta.py
verify-beta:
	$(PYTHON) scripts/verify_beta.py

# Current sidebar/display beta
current:
	$(PYTHON) scripts/build_current.py
current-arm:
	$(PYTHON) scripts/build_current.py --arm
verify-current:
	$(PYTHON) scripts/verify_current.py
test-current:
	mkdir -p .context
	$(CC) -O2 -g -fsanitize=address,undefined -Idevelopment/logo-20261016/source -Idevelopment/beta-20261015/source/amiga/emulator tests/amiga/emulator/model.c -o .context/test-current
	.context/test-current
	$(CC) -O2 -g -fsanitize=address,undefined -Itests/amiga/emulator/mock -Idevelopment/logo-20261016/source tests/amiga/emulator/scan.c -o .context/test-scan
	.context/test-scan
	$(MODEL_PYTHON) tests/amiga/emulator/check_current_arm.py

.PHONY: test-library-large
test-library-large:
	mkdir -p .context
	$(CC) -O2 -g -fsanitize=address,undefined -Idevelopment/logo-20261016/source tests/amiga/emulator/large_library.c -o .context/test-large
	.context/test-large
	$(CC) -O2 -g -fsanitize=address,undefined -Idevelopment/logo-20261016/source tests/amiga/emulator/legacy_model.c -o .context/test-legacy
	.context/test-legacy
