DESTDIR=/

all:

clean:

install: all
	install -d $(DESTDIR)/usr/share/tpfancod-profiles
	install -m 644 usr/share/tpfancod-profiles/* $(DESTDIR)/usr/share/tpfancod-profiles
	echo Installation complete.

uninstall:
	rm -rf $(DESTDIR)/usr/share/tpfancod-profiles



