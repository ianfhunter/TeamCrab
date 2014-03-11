.PHONY: all test clean install uninstall
version = RC1_rc4
install_dir = /opt/SESimulator_v$(version)

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
	@nosetests -I ^notunit_ -I importme.py -w test engine; if [ $$? -eq 0 ] ; \
	then echo "All tests passed!" ; else echo "Tests failed"; fi

install:
	$(MAKE) build
	mkdir -p $(install_dir)
	mkdir -p $(install_dir)/bin
	mkdir -p $(install_dir)/media
	cp -R bin/* $(install_dir)/bin
	cp -R media/* $(install_dir)/media
	cp src/SESimulator.sh /usr/local/bin/SESimulator
	chmod +x /usr/local/bin/SESimulator
	cp src/SESimulator.desktop /usr/share/applications/
	@echo Installation complete!

clean:
	rm -rf bin/*
	@echo Build cleaned!

uninstall:
	rm -rf $(install_dir)/*
	rmdir $(install_dir)
	rm /usr/share/applications/SESimulator.desktop
	@echo SESimulator has been uninstalled!

uninstall-script:
	rm /usr/local/bin/SESimulator

run:
	python bin/SESimulator.pyc

docs:
	cd src; pydoc -w ./
	mkdir -p docs
	mv src/*.html docs/
	find src -name *.pyc -delete
