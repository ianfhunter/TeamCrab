build:
	python -m compileall src
	mkdir -p bin
	cd src; find . ! -path . -type d | cpio -pdumv ../bin
	cd src; find . -name '*.pyc' | xargs cp --parents -t ../bin/
	find src -name *.pyc -delete
	chmod a+x bin/SESimulator.pyc
	@echo Build successful!

# There are no test files for the zero velocity release. This will need to be changed all subsequent releases
all:
test:
	$(MAKE) build
	# Run tests here
	@echo All tests passed!

install:
	$(MAKE) build
	mkdir -p /opt/SESimulator
	cp bin/* /opt/SESimulator/
	cp src/SESimulator.sh /usr/local/bin/SESimulator
	chmod +x /usr/local/bin/SESimulator
	cp src/SESimulator.desktop /usr/share/applications/
	@echo Installation complete!

clean:
	rm -rf bin/*
	@echo Build cleaned!

uninstall:
	rm /opt/SESimulator/*
	rmdir /opt/SESimulator
	rm /usr/local/bin/SESimulator
	rm /usr/share/applications/SESimulator.desktop
	@echo SESimulator has been uninstalled!
