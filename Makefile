RUNTEST=pipenv run python -m unittest -v -b

ALLMODULES=$(patsubst %.py, %.py, $(wildcard test_*.py))

all:
	${RUNTEST} ${ALLMODULES}

% : test_%.py
	${RUNTEST} test_$@
