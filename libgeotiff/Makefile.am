SUBDIRS = libxtiff . bin

if PROJ_IS_CONFIG
PROJ_CPPFLAGS = @PROJ_INC@ -DHAVE_LIBPROJ=1
endif

if PROJECTS_H_IS_CONFIG
PROJ_CPPFLAGS = -DHAVE_PROJECTS_H=1 -DHAVE_LIBPROJ=1 @PROJ_INC@
endif

if TIFF_IS_CONFIG
TIFF_CPPFLAGS = @TIFF_INC@ -DHAVE_TIFF=1
endif

AM_CPPFLAGS = $(PROJ_CPPFLAGS) $(TIFF_CFLAGS)

include_HEADERS =   geotiff.h \
                    geotiffio.h \
                    geovalues.h \
                    geonames.h \
                    geokeys.h \
                    geo_tiffp.h \
                    geo_keyp.h \
                    geo_normalize.h \
                    cpl_serv.h \
                    geo_simpletags.h \
                    epsg_datum.inc \
                    epsg_gcs.inc \
                    epsg_pm.inc \
                    epsg_units.inc \
                    geo_ctrans.inc \
                    epsg_ellipse.inc \
                    epsg_pcs.inc \
                    epsg_proj.inc \
                    epsg_vertcs.inc \
                    geokeys.inc 


libgeotiff_la_SOURCES = cpl_serv.c \
                        cpl_csv.c \
                        geo_extra.c \
                        geo_free.c \
                        geo_get.c \
                        geo_names.c \
                        geo_new.c \
                        geo_normalize.c \
                        geo_print.c \
                        geo_set.c \
                        geo_simpletags.c \
                        geo_tiffp.c \
                        geo_trans.c \
                        geo_write.c \
                        geotiff_proj4.c 

if CSV_IS_CONFIG
    libgeotiff_la_SOURCES += csv/datum.c \
                             csv/ellipsoid.c \
                             csv/gcs.c \
                             csv/pcs.c \
                             csv/prime_meridian.c \
                             csv/projop_wparm.c \
                             csv/unit_of_measure.c 
endif

libgeotiff_la_LDFLAGS = -version-info 1:2:0

libgeotiff_la_LIBADD = libxtiff/libxtiff.la

lib_LTLIBRARIES = libgeotiff.la