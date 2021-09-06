# Makefile for group project
# To run project, go ahead and run `make run`, and if your OS is windows, you run win `make run OS=win`
OS := unix

BIN := bin/main.py
TESTS := test/tests.py

unixpy := python3
winpy := py

run:
ifeq ($(OS),unix)
	$(unixpy) $(BIN)
else
	$(winpy) $(BIN)
endif

test:
ifeq ($(OS),unix)
	$(unixpy) $(TESTS)
else
	$(winpy) $(TESTS)
endif
