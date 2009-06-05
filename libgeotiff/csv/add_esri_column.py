#!/usr/bin/env python
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
# $Log$
# Revision 1.2  2004/03/20 07:52:44  warmerda
# use local paths
#
# Revision 1.1  2003/06/20 21:28:24  warmerda
# New
#

import string
import sys
import osr

sys.path.append( '/Users/pramsey/Code/libgeotiff-svn/csv' )
import csv_tools

gcs_table = csv_tools.CSVTable()
gcs_table.read_from_csv( 'gcs.csv' )

datum_table = csv_tools.CSVTable()
datum_table.read_from_csv( 'datum.csv' )

print '%d GCS defined.', len(gcs_table.data.keys())

esri_gcs_names = {}
esri_datum_names = {}

#
# First try looking up all the EPSG GCS codes in the ESRI "epsg" directory,
# and using those examples to correspond an EPSG datum code with an ESRI datum
# name ... note that datums that aren't used in the EPSG GCS set will be missed.
#
for gcs_code in gcs_table.data.keys():
    gcs_code = int(gcs_code)
    filename = '/Users/pramsey/Downloads/epsg/%d.prj' % gcs_code

    try:
        esri_gcs_wkt = open(filename).read()
    except:
        print 'Failed to find ', filename
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



    

    
