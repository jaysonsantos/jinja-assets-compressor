test: clean
	py.test tests ${ARGS}

coverage:
	$(MAKE) test ARGS="--cov=jac --cov=tests ${ARGS}"

clean:
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@rm -rf build/ dist/

lint:
	flake8 jac tests
	isort -c --recursive jac tests

isort_fix:
	isort -y --recursive jac tests
