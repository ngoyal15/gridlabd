python-install:
	@echo "python $(top_srcdir)/gldcore/link/python/setup.py --quiet install"
	@( export SRCDIR=$(top_srcdir) ; python $(top_srcdir)/gldcore/link/python/setup.py --quiet install )

python-clean:
	@echo "python $(top_srcdir)/gldcore/link/python/setup.py clean"
	@( export SRCDIR=$(top_srcdir) ; python $(top_srcdir)/gldcore/link/python/setup.py clean )
	-rm -rf $(SRCDIR)/build/lib.*
