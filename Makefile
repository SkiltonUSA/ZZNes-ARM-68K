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
	$(CC) -O2 -g -fsanitize=address,undefined -Idevelopment/borders-20261016/source -Idevelopment/beta-20261015/source/amiga/emulator tests/amiga/emulator/model.c -o .context/test-current
	.context/test-current
	$(CC) -O2 -g -fsanitize=address,undefined -Itests/amiga/emulator/mock -Idevelopment/borders-20261016/source tests/amiga/emulator/scan.c -o .context/test-scan
	.context/test-scan
	$(MODEL_PYTHON) tests/amiga/emulator/check_current_arm.py

.PHONY: test-library-large
test-library-large:
	mkdir -p .context
	$(CC) -O2 -g -fsanitize=address,undefined -Idevelopment/borders-20261016/source tests/amiga/emulator/large_library.c -o .context/test-large
	.context/test-large
	$(CC) -O2 -g -fsanitize=address,undefined -Idevelopment/borders-20261016/source tests/amiga/emulator/legacy_model.c -o .context/test-legacy
	.context/test-legacy

.PHONY: test-zip
test-zip:
	ROM_ZIP_INCLUDE=development/borders-20261016/source/zip $(PYTHON) tests/amiga/emulator/zip/test.py

.PHONY: test-border
test-border:
	mkdir -p .context
	$(CC) -O2 -g -fsanitize=address,undefined -DBORDER_NES -Idevelopment/borders-20261016/source -Idevelopment/borders-20261016/player -Idevelopment/beta-20261015/build-inputs/player tests/amiga/emulator/border.c -o .context/test-border
	.context/test-border

# Measured development candidate; neither target deploys to hardware.
optimisation:
	$(PYTHON) scripts/build_current.py --arm --optimisation
test-optimisation-native:
	mkdir -p .context
	$(CXX) -std=c++14 -O2 -g -fsanitize=address,undefined -Idevelopment/optimisation-20261018/player -Idevelopment/borders-20261016/player -Idevelopment/beta-20261015/build-inputs/player tests/amiga/emulator/optimisation.cpp -o .context/test-optimisation-pixels
	.context/test-optimisation-pixels
	$(CC) -O2 -g -fsanitize=address,undefined -Idevelopment/optimisation-20261018/source -Idevelopment/borders-20261016/source tests/amiga/emulator/optimisation_library.c -o .context/test-optimisation-library
	.context/test-optimisation-library
	$(CC) -O2 -g -fsanitize=address,undefined -Idevelopment/optimisation-20261018/source -Idevelopment/borders-20261016/source tests/amiga/emulator/legacy_model.c -o .context/test-optimisation-legacy
	.context/test-optimisation-legacy

.PHONY: test-optimisation-arm test-scrolling
test-optimisation-arm:
	CURRENT_ARM_DIR=.context/optimisation-build/player $(MODEL_PYTHON) tests/amiga/emulator/check_current_arm.py
	CURRENT_ARM_DIR=.context/optimisation-build/player $(MODEL_PYTHON) tests/amiga/emulator/check_smooth_arm.py
test-scrolling:
	$(PYTHON) tests/amiga/emulator/test_scroll_native.py

.PHONY: test-scanline-key
test-scanline-key:
	mkdir -p .context
	$(CC) -O2 -g -fsanitize=address,undefined -Idevelopment/optimisation-20261018/host tests/amiga/emulator/scanline_key.c -o .context/test-scanline-key
	.context/test-scanline-key
