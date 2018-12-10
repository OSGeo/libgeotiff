# Executables paths passed to test scripts
THIS_DIR = $(top_srcdir)/test
EXEPATH = ../bin
LISTGEOEXE = $(EXEPATH)/listgeo

# Test scripts
TESTLISTGEO = $(THIS_DIR)/testlistgeo

EXTRA_DIST = testlistgeo testlistgeo_out.dist \
             data/byte.tif data/pcs_32064.tif

check-local:
	$(TESTLISTGEO) $(LISTGEOEXE)

