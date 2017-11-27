test: clean
	py.test tests ${ARGS}

coverage:
	$(MAKE) test ARGS="--cov=jac --cov=tests ${ARGS}"

clean:
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@rm -rf build/ dist/

lint:
	flake8 jac tests setup.py

isort_fix:
	isort -y --recursive jac tests setup.py

.PHONY: test coverage clean lint isort_fix
