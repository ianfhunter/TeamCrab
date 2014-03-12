.PHONY: all test clean install uninstall
version = RC1_rc5
install_pyc_prefix = /opt
install_sh_prefix = /usr/local/bin

build:
	python -m compileall src
	mkdir -p bin
	cd src; find . ! -path . -type d | cpio -pdumv ../bin
	cd src; find . \( -iname "*.pyc" ! -iname "global_config.pyc" \) | xargs cp --parents -t ../bin/
	cp src/global_config.py bin/global_config.py
	find src -name *.pyc -delete
	chmod a+x bin/SESimulator.pyc
	@echo Build successful!

all:
test:
	$(MAKE) build
	@nosetests -I ^notunit_ -I importme.py -w test engine UI; if [ $$? -eq 0 ] ; \
	then echo "All tests passed!" ; else echo "Tests failed"; fi
	@rm bin/global_config.pyc

install:
	$(MAKE) build
	mkdir -p $(install_pyc_prefix)/SESimulator_v$(version)
	mkdir -p $(install_pyc_prefix)/SESimulator_v$(version)/bin
	mkdir -p $(install_pyc_prefix)/SESimulator_v$(version)/media
	cp -R bin/* $(install_pyc_prefix)/SESimulator_v$(version)/bin
	cp -R media/* $(install_pyc_prefix)/SESimulator_v$(version)/media
	cp src/SESimulator.sh $(install_sh_prefix)/SESimulator
	@echo "#!/bin/bash \np=$(install_pyc_prefix)" | cat - $(install_sh_prefix)/SESimulator > temp && mv temp $(install_sh_prefix)/SESimulator
	chmod +x $(install_sh_prefix)/SESimulator
	@echo Installation complete!

clean:
	rm -rf bin/*
	@echo Build cleaned!

uninstall:
	rm -rf $(install_pyc_prefix)/SESimulator_v$(version)/*
	rmdir $(install_pyc_prefix)/SESimulator_v$(version)
	@echo SESimulator has been uninstalled!

uninstall-script:
	rm $(install_sh_prefix)/SESimulator

run:
	python bin/SESimulator.pyc

docs:
	cd src; pydoc -w ./
	mkdir -p docs
	mv src/*.html docs/
	find src -name *.pyc -delete
