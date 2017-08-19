update-nix-deps:
	cd nix && pypi2nix -V 3 \
		-r ../requirements.txt \
		-r ../development-requirements.txt \
		--default-overrides

check-types:
	mypy src/

check-pep8:
	flake8 src/

check-tests:
	PYTHONPATH=$(PWD)/src:$(PYTHONPATH) pytest tests

check: check-types check-pep8 check-tests

.PHONY: update-nix-deps check check-pep8 check-types check-tests
