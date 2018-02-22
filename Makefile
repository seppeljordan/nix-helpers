PYPI2NIX="/home/sebastian/src/pypi2nix/examples/pypi2nix/bin/pypi2nix"

update-nix-deps:
	cd nix && $(PYPI2NIX) -V 3 \
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

clean:
	rm -rf .cache .mypy_cache *~ src/nix/__pycache__

.PHONY: update-nix-deps check check-pep8 check-types check-tests clean
