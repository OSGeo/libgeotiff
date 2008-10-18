#!/usr/bin/env python
#******************************************************************************
#  $Id$
# 
#  Project:  GDAL
#  Purpose:  Build stateplane.csv, relating USGS state plane numbers with
#            EPSG coordinate system, and some supporting info fields.
#  Author:   Frank Warmerdam, warmerdam@pobox.com
#******************************************************************************
#  Copyright (c) 2002, Frank Warmerdam <warmerdam@pobox.com>
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
# Revision 1.1  2002/11/28 16:11:47  warmerda
# New
#
#


import string
import csv_tools

##############################################################################
# read_stateplane_txt()

def read_stateplane_txt( filename ):
    spt = csv_tools.CSVTable()
    spt.add_field( "ID" )
    spt.add_field( "STATE" )
    spt.add_field( "ZONE" )
    spt.add_field( "PROJ_METHOD" )
    spt.add_field( "DATUM" )
    spt.add_field( "USGS_CODE" )
    spt.add_field( "EPSG_PCS_CODE" )

    src_lines = open(filename).readlines()

    for line in src_lines:
        rec = {}
        rec['STATE'] = string.strip(line[0:16])
        rec['ZONE'] = string.strip(line[16:39])
        rec['PROJ_METHOD'] = string.strip(line[39:40])
        rec['DATUM'] = string.strip(line[48:65])
        rec['USGS_CODE'] = string.strip(line[65:])
        rec['EPSG_PCS_CODE'] = ''
        if rec['DATUM'] == 'NAD27':
            rec['ID'] = str(int(rec['USGS_CODE']) + 10000)
        else:
            rec['ID'] = rec['USGS_CODE']

        spt.add_record( int(rec['ID']), rec )

    return spt

##############################################################################
# main()

spt = read_stateplane_txt( '/home/warmerda/gdal/data/stateplane.txt' )

pcs = csv_tools.CSVTable()
pcs.read_from_csv( 'coordinate_reference_system.csv' )

coord_sys_by_name = {}
ids_to_replace = []

pcs_keys = pcs.data.keys()
#pcs_keys = [ 2204, 32036 ]

for pcs_key in pcs_keys:
    rec = pcs.get_record( pcs_key )

    if rec['COORD_REF_SYS_KIND'] != 'projected':
        continue

    dep = rec['DEPRECATED']
    
    coc = int(rec['PROJECTION_CONV_CODE'])
    
    if rec['SOURCE_GEOGCRS_CODE'] == '4269':
        zone = coc - 10030
        id = zone
    else:
        zone = coc - 10000
        id = zone + 10000

    if dep == '0':
        name = rec['COORD_REF_SYS_NAME']
        if coord_sys_by_name.has_key(name):
            print 'Yikes, more than one ', name
        else:
            coord_sys_by_name[name] = pcs_key
            
    if spt.data.has_key(id):
        spt_rec = spt.get_record( id )
        if len(spt_rec['EPSG_PCS_CODE']) > 0:
            raise ValueError, 'already have this State Plane Zone!'
        
        spt_rec['EPSG_PCS_CODE'] = str(pcs_key)
        spt.set_record( id, spt_rec )

        if dep == '1':
            ids_to_replace.append( id )

print 'Found %d deprecated PCS codes to upgrade by name.' % len(ids_to_replace)

for id in ids_to_replace:
    spt_rec = spt.get_record( id )
    dep_pcs_rec = pcs.get_record( int(spt_rec['EPSG_PCS_CODE']) )
    name = dep_pcs_rec['COORD_REF_SYS_NAME']
    if coord_sys_by_name.has_key(name):
        spt_rec['EPSG_PCS_CODE'] = str(coord_sys_by_name[name])
    else:
        print 'Unable to find non-deprecated value for ', name

for spt_id in spt.data.keys():
    rec = spt.get_record(spt_id)
    if len(rec['EPSG_PCS_CODE']) == 0:
        print 'Never got match for %s / %s' % (rec['STATE'], rec['ZONE'])
            
spt.write_to_csv( 'stateplane.csv' )
        

