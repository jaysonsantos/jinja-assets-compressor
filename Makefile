test: clean
	py.test tests ${ARGS}

coverage:
	$(MAKE) test ARGS="--cov=jac --cov=tests ${ARGS}"

clean:
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@rm -rf build/ dist/
