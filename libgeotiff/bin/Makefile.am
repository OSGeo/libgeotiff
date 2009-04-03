
makegeo_SOURCES = makegeo.c
geotifcp_SOURCES = geotifcp.c
listgeo_SOURCES = listgeo.c
csv2html_SOURCES = csv2html.c
applygeo_SOURCES = applygeo.c

bin_PROGRAMS = makegeo geotifcp listgeo csv2html applygeo
AM_CFLAGS = -I../libxtiff 
LDADD = ../libgeotiff.la
csv2html_LDADD = ../cpl_csv.lo ../libgeotiff.la


