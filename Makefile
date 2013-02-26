test: clean
	py.test ${ARGS}

coverage:
	$(MAKE) test ARGS="--cov=jac ${ARGS}"

clean:
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
