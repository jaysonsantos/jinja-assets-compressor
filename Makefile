test: clean
	py.test ${ARGS}

clean:
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
