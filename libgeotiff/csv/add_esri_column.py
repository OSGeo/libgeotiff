#!/usr/bin/env python
# -*- coding: utf-8 -*-
#******************************************************************************
#  $Id$
# 
#  Project:  GDAL
#  Purpose:  This script will append an ESRI_DATUM_NAME field to the
#            datum file.  This is just used by GDAL for morphToESRI(), and
#            isn't really related to GeoTIFF at all.
#  Author:   Frank Warmerdam, warmerdam@pobox.com
# 
#******************************************************************************
#  Copyright (c) 2003, Frank Warmerdam <warmerdam@pobox.com>
# 
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
# 
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
# 
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#******************************************************************************
# 

# This scritps depends on a set of ArcGIS .prj files that are usually only
# available on Frank's machine. But it can
# also work with an alternate method if you have OGR configured with FileGDB and
# OpenFileGDB drivers (GDAL >= 1.11)

import string
import sys
import osr

sys.path.append( '/home/warmerda/libgeotiff/csv' )
import csv_tools


epsg_prj_path = '/usr3/data/esri/prj/epsg'

def get_esri_wkt_from_gcs_code_from_epsg_prj(gcs_code):
    filename = '%s/%d.prj' % (epsg_prj_path, gcs_code)

    try:
        esri_gcs_wkt = open(filename).read()
        return esri_gcs_wkt
    except:
        print 'Failed to find ', filename
        return None

def get_esri_wkt_from_gcs_code_from_filegdb(gcs_code):

    import shutil
    try:
        shutil.rmtree('tmp.gdb')
    except:
        pass
    from osgeo import ogr
    ds = ogr.GetDriverByName('FileGDB').CreateDataSource('tmp.gdb')
    srs = osr.SpatialReference()
    # Fake WKT: the important thing is the EPSG code
    srs.ImportFromWkt( """GEOGCS["BLA",DATUM["BLA",SPHEROID["BLA",1,0]],AUTHORITY["EPSG","%d"]]""" % gcs_code )
    lyr = ds.CreateLayer('foo', geom_type = ogr.wkbPoint, srs = srs)
    ds = None

    # Read with OpenFileGDB driver !
    ds = ogr.Open('tmp.gdb/a00000003.gdbtable')
    lyr = ds.GetLayer(0)
    # Skip first WKT that is always EPSG:4326
    feat = lyr.GetNextFeature()
    # Here's the interesting WKT
    feat = lyr.GetNextFeature()
    if feat is not None:
        ret = feat.GetField('SRTEXT')
    else:
        ret = None
    ds = None

    try:
        shutil.rmtree('tmp.gdb')
    except:
        pass

    return ret

gcs_table = csv_tools.CSVTable()
gcs_table.read_from_csv( 'gcs.csv' )

datum_table = csv_tools.CSVTable()
datum_table.read_from_csv( 'datum.csv' )

print('%d GCS defined.' % len(gcs_table.data.keys()))

esri_gcs_names = {}
esri_datum_names = {}

try:
    os.stat(epsg_prj_path)
    prj_epsg_exists = True
except:
    prj_epsg_exists = False
    pass

filegdb_method = False
if not prj_epsg_exists:
    from osgeo import ogr
    if ogr.GetDriverByName('FileGDB') is not None and ogr.GetDriverByName('OpenFileGDB') is not None:
        filegdb_method = True

if prj_epsg_exists or filegdb_method:
    #
    # First try looking up all the EPSG GCS codes in the ESRI "epsg" directory,
    # and using those examples to correspond an EPSG datum code with an ESRI datum
    # name ... note that datums that aren't used in the EPSG GCS set will be missed.
    #
    for gcs_code in gcs_table.data.keys():
        gcs_code = int(gcs_code)

        if prj_epsg_exists:
            esri_gcs_wkt = get_esri_wkt_from_gcs_code_from_epsg_prj(gcs_code)
        else:
            esri_gcs_wkt = get_esri_wkt_from_gcs_code_from_filegdb(gcs_code)
        if esri_gcs_wkt is None:
            continue

        srs = osr.SpatialReference()
        srs.ImportFromWkt( esri_gcs_wkt )

        gcs_name = srs.GetAttrValue( 'GEOGCS' )
        datum_name = srs.GetAttrValue( 'DATUM' )

        esri_gcs_names[gcs_code] = gcs_name

        print 'GCS %d = %s, %s' % (gcs_code, gcs_name, datum_name)

        try:
            gcs_rec = gcs_table.get_record( gcs_code )
            datum_code = int(gcs_rec['DATUM_CODE'])

            esri_datum_names[datum_code] = datum_name
        except:
            print 'Failed to get gcs record, or datum info'
else:
    print 'WARNING: ESRI_DATUM_NAME column will be empty !'

#
# Now add mappings from the manual override table esri_datum_override.csv
#
overrides = csv_tools.CSVTable()
overrides.read_from_csv( 'esri_datum_override.csv' )

for datum_code in overrides.data.keys():
    record = overrides.get_record( datum_code )
    esri_datum_names[datum_code] = record['ESRI_DATUM_NAME']

# Make sure the output datum table has the ESRI_DATUM_NAME field    

if 'ESRI_DATUM_NAME' not in datum_table.fields:
    datum_table.add_field( 'ESRI_DATUM_NAME' )

# Loop over all datums, adding the esri name where we have it.

for datum_code in datum_table.data.keys():
    datum_rec = datum_table.get_record( datum_code )
    if esri_datum_names.has_key(datum_code):
        print 'match for ', datum_code
        datum_rec['ESRI_DATUM_NAME'] = esri_datum_names[datum_code]
    else:
        print 'no match for ', datum_code
        datum_rec['ESRI_DATUM_NAME'] = ''

    datum_table.set_record( datum_code, datum_rec )

datum_table.write_to_csv( 'gdal_datum.csv' )
