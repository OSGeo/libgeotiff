#!/usr/bin/env python
#******************************************************************************
#  $Id$
# 
#  Project:  GDAL
#  Purpose:  Build the epsg_pcs.csv table with the minimum information
#            required to define a PCS (not including GCS defs). 
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
# Revision 1.9  2008/07/21 19:03:07  fwarmerdam
# various fixes and improvements done a while ago
#
# Revision 1.8  2007/07/20 18:28:43  fwarmerdam
# disable application of gcs.override.csv and pcs.override.csv
#
# Revision 1.7  2006/04/21 04:27:24  fwarmerdam
# added pcs.override support
#
# Revision 1.6  2006/04/21 04:00:20  fwarmerdam
# added SHOW_CRS and DEPRECATED to pcs.csv and gcs.csv
#
# Revision 1.5  2004/05/04 00:29:31  warmerda
# added gcs.override.csv support
#
# Revision 1.4  2004/03/20 07:52:28  warmerda
# more escape clauses for EPSG 6.5
#
# Revision 1.3  2003/03/31 14:27:21  warmerda
# added collection of GREENWICH_DATUM gcs column and related shift fix
#
#

import string
import csv_tools

def get_crs_uom( crs_rec, cs, caxis ):
    coord_sys_code = int(crs_rec['COORD_SYS_CODE'])

    ca_recs = caxis.get_records( coord_sys_code )
    return ca_recs[0]['UOM_CODE']

##############################################################################
# Read and index input files.

co_value = csv_tools.CSVTable()
co_value.read_from_csv( 'coordinate_operation_parameter_value.csv', multi=1 )

co = csv_tools.CSVTable()
co.read_from_csv( 'coordinate_operation.csv' )

crs = csv_tools.CSVTable()
crs.read_from_csv( 'coordinate_reference_system.csv' )

datums = csv_tools.CSVTable()
datums.read_from_csv( 'datum.csv' )

cs = csv_tools.CSVTable()
cs.read_from_csv( 'coordinate_system.csv', multi=0 )

caxis = csv_tools.CSVTable()
caxis.read_from_csv( 'coordinate_axis.csv', multi=1 )

##############################################################################
# Scan coordinate_reference_systems table to collect PCS ids.

pcs_keys = []
gcs_keys = []

for key in crs.data.keys():
    crs_rec = crs.get_record( key )
    if crs_rec['COORD_REF_SYS_KIND'] == 'projected':
        pcs_keys.append( key )
    elif crs_rec['COORD_REF_SYS_KIND'] == 'geographic 2D':
        gcs_keys.append( key )

pcs_keys.sort()
gcs_keys.sort()

print '%d PCS and %d GCS coordinate systems to process.' % (len(pcs_keys), len(gcs_keys))

##############################################################################
# Read PCS Override table for manually assigned transformations.

pcs_override_table = csv_tools.CSVTable()
pcs_override_table.read_from_csv( 'pcs.override.csv' )

##############################################################################
# Setup PCS table fields.

pcs_table = csv_tools.CSVTable()
pcs_table.add_field('COORD_REF_SYS_CODE')        # PCS #
pcs_table.add_field('COORD_REF_SYS_NAME')        # PCS Name
pcs_table.add_field('UOM_CODE')                  # linear units of projection.
pcs_table.add_field('SOURCE_GEOGCRS_CODE')       # GCS #
pcs_table.add_field('COORD_OP_CODE')             # same asPROJECTION_CONV_CODE
pcs_table.add_field('COORD_OP_METHOD_CODE')      # ie. 9807=Transvere Mercator
pcs_table.add_field('SHOW_CRS')                  # 0=false, 1=true
pcs_table.add_field('DEPRECATED')                # 0=false, 1=true
pcs_table.add_field('COORD_SYS_CODE')            # Used mainly for axes.

max_parms = 7
for i in range(max_parms):
    pcs_table.add_field('PARAMETER_CODE_%d' % (i+1))
    pcs_table.add_field('PARAMETER_VALUE_%d' % (i+1))
    pcs_table.add_field('PARAMETER_UOM_%d' % (i+1))

##############################################################################
# Populate PCS table.Setup PCS table fields.

for key in pcs_keys:

    """
    try:
        o_rec = pcs_override_table.get_record( key )
        
        print 'PCS %d overridden from pcs.override.csv file' % key
        pcs_table.add_record( key, o_rec )
        continue
    except:
        pass
    """

    crs_rec = crs.get_record( key )
    pcs_rec = {}
    pcs_rec['COORD_REF_SYS_CODE'] = crs_rec['COORD_REF_SYS_CODE']
    pcs_rec['COORD_REF_SYS_NAME'] = crs_rec['COORD_REF_SYS_NAME']
    pcs_rec['SOURCE_GEOGCRS_CODE'] = crs_rec['SOURCE_GEOGCRS_CODE']
    pcs_rec['SHOW_CRS']           = crs_rec['SHOW_CRS']
    pcs_rec['DEPRECATED']         = crs_rec['DEPRECATED']
    pcs_rec['COORD_SYS_CODE']     = crs_rec['COORD_SYS_CODE']
    
    if len(pcs_rec['SOURCE_GEOGCRS_CODE']) == 0:
        print 'GEOGCRS missing for %s/%s' % (crs_rec['COORD_REF_SYS_CODE'],
                                             crs_rec['COORD_REF_SYS_NAME'])

    pcs_rec['UOM_CODE'] = get_crs_uom(crs_rec, cs, caxis )
                                             
    pcs_rec['COORD_OP_CODE']      = crs_rec['PROJECTION_CONV_CODE']

    co_rec = co.get_record( int(pcs_rec['COORD_OP_CODE']) )
    pcs_rec['COORD_OP_METHOD_CODE'] = co_rec['COORD_OP_METHOD_CODE']

    parm_recs = co_value.get_records( int(pcs_rec['COORD_OP_CODE']) )
    if len(parm_recs) > max_parms:
        print 'COORD_OP_CODE %s has %d values.' % (pcs_rec['COORD_OP_CODE'],
                                                   len(parm_recs))
        
    for parm_i in range(len(parm_recs)):
        parm_rec = parm_recs[parm_i]

        pin = '%d' % (parm_i+1)

        pcs_rec['PARAMETER_CODE_'+pin] = parm_rec['PARAMETER_CODE']
        pcs_rec['PARAMETER_VALUE_'+pin] = parm_rec['PARAMETER_VALUE']
        pcs_rec['PARAMETER_UOM_'+pin] = parm_rec['UOM_CODE']

    pcs_table.add_record( key, pcs_rec )

pcs_table.write_to_csv( 'pcs.csv' )
pcs_table = None

##############################################################################
# Setup projop_wparm (projection operations with parameters) table fields.
# This table will contain all projection related entries from the
# coordinate_operation.csv table, with the parameter values from
# coordinate_operation_parameter_value.csv appended to the record. 

powp_table = csv_tools.CSVTable()
powp_table.add_field('COORD_OP_CODE')             # 
powp_table.add_field('COORD_OP_NAME')             # 
powp_table.add_field('COORD_OP_METHOD_CODE')      # ie. 9807=Transvere Mercator

max_parms = 7
for i in range(max_parms):
    powp_table.add_field('PARAMETER_CODE_%d' % (i+1))
    powp_table.add_field('PARAMETER_VALUE_%d' % (i+1))
    powp_table.add_field('PARAMETER_UOM_%d' % (i+1))


##############################################################################
# Build and write the projop_wparm table.

op_keys = co.data.keys()

op_keys.sort()
for key in op_keys:

    powp_rec = {}
    
    # Check COORD_OP_TYPE.
    if string.find(co.data[key],',conversion,') < 1:
        continue
    
    co_rec = co.get_record(key)

    powp_rec['COORD_OP_CODE'] = co_rec['COORD_OP_CODE']
    powp_rec['COORD_OP_NAME'] = co_rec['COORD_OP_NAME']
    powp_rec['COORD_OP_METHOD_CODE'] = co_rec['COORD_OP_METHOD_CODE']

    try:
        parm_recs = co_value.get_records( key )
    except:
        # this happens for parameterless methods like DMSH conversions.
        parm_recs = []
        
    if len(parm_recs) > max_parms:
        print 'COORD_OP_CODE %d has %d values.' % (key, len(parm_recs))
        
    for parm_i in range(len(parm_recs)):
        parm_rec = parm_recs[parm_i]

        pin = '%d' % (parm_i+1)

        powp_rec['PARAMETER_CODE_'+pin] = parm_rec['PARAMETER_CODE']
        powp_rec['PARAMETER_VALUE_'+pin] = parm_rec['PARAMETER_VALUE']
        powp_rec['PARAMETER_UOM_'+pin] = parm_rec['UOM_CODE']

    powp_table.add_record( key, powp_rec )

powp_table.write_to_csv( 'projop_wparm.csv' )
    
##############################################################################
# Build a map of coordinate operation codes for all mappings to 4326 (WGS84)

op_keys = co.data.keys()
to_wgs84_ops = {}
greenwich_equiv = {}

for key in op_keys:
    co_rec = co.get_record(key)

    if co_rec['TARGET_CRS_CODE'] == '4326' \
       and (co_rec['COORD_OP_METHOD_CODE'] == '9603'
            or co_rec['COORD_OP_METHOD_CODE'] == '9606'
            or co_rec['COORD_OP_METHOD_CODE'] == '9607'):

        source_crs = int(co_rec['SOURCE_CRS_CODE'])
        
        if to_wgs84_ops.has_key(source_crs):
            if to_wgs84_ops[source_crs] is not None:
                print 'GCS %d has multiple ways to WGS84.' % source_crs
                print to_wgs84_ops[source_crs], key
                to_wgs84_ops[source_crs] = None
        else:
            to_wgs84_ops[source_crs] = key

    # Does this operation relate this GCS with a Greenwich meridian
    # equivelent?
    if co_rec['COORD_OP_METHOD_CODE'] == '9601':
        greenwich_equiv[int(co_rec['SOURCE_CRS_CODE'])] = \
                                            int(co_rec['TARGET_CRS_CODE'])

##############################################################################
# Read GCS Override table for manually assigned transformations.

gcs_override_table = csv_tools.CSVTable()
gcs_override_table.read_from_csv( 'gcs.override.csv' )

##############################################################################
# Setup GCS table fields.

gcs_table = csv_tools.CSVTable()
gcs_table.add_field('COORD_REF_SYS_CODE')        # GCS #
gcs_table.add_field('COORD_REF_SYS_NAME')        # GCS Name
gcs_table.add_field('DATUM_CODE')                # Datum #
gcs_table.add_field('DATUM_NAME')                # 
gcs_table.add_field('GREENWICH_DATUM')           # Greenwich equiv datum
gcs_table.add_field('UOM_CODE')                  # Angular units for GCS.
gcs_table.add_field('ELLIPSOID_CODE')            # 
gcs_table.add_field('PRIME_MERIDIAN_CODE')       #
gcs_table.add_field('SHOW_CRS')                  # 0=false, 1=true
gcs_table.add_field('DEPRECATED')                # 0=false, 1=true
gcs_table.add_field('COORD_SYS_CODE')            # mainly for axes
gcs_table.add_field('COORD_OP_METHOD_CODE')      # 
gcs_table.add_field('DX')                        # +towgs84 parameters.
gcs_table.add_field('DY')                        
gcs_table.add_field('DZ')                        
gcs_table.add_field('RX')                        
gcs_table.add_field('RY')                        
gcs_table.add_field('RZ')                        
gcs_table.add_field('DS')                        

##############################################################################
# Populate and write GCS table.

for key in gcs_keys:

    """
    try:
        o_rec = gcs_override_table.get_record( key )
        
        print 'GCS %d overridden from gcs.override.csv file' % key
        gcs_table.add_record( key, o_rec )
        continue
    except:
        pass
    """

    crs_rec = crs.get_record( key )
    gcs_rec = {}
    gcs_rec['COORD_REF_SYS_CODE'] = crs_rec['COORD_REF_SYS_CODE']
    gcs_rec['COORD_REF_SYS_NAME'] = crs_rec['COORD_REF_SYS_NAME']
    gcs_rec['DATUM_CODE']         = crs_rec['DATUM_CODE']
    gcs_rec['SHOW_CRS']           = crs_rec['SHOW_CRS']
    gcs_rec['DEPRECATED']         = crs_rec['DEPRECATED']
    gcs_rec['COORD_SYS_CODE']     = crs_rec['COORD_SYS_CODE']

    gcs_rec['UOM_CODE'] = get_crs_uom(crs_rec, cs, caxis )

    try:
        datum_id = int(crs_rec['DATUM_CODE'])
    except:
        print 'No DATUM_CODE for %s, skipping.' % crs_rec['COORD_REF_SYS_NAME']
        continue
    
    datum_rec = datums.get_record( datum_id )
    gcs_rec['DATUM_NAME'] = datum_rec['DATUM_NAME']
    gcs_rec['ELLIPSOID_CODE'] = datum_rec['ELLIPSOID_CODE']
    gcs_rec['PRIME_MERIDIAN_CODE'] = datum_rec['PRIME_MERIDIAN_CODE']

    if greenwich_equiv.has_key(key):
        towgs84_gcs = greenwich_equiv[key]
        crs_rec_base = crs.get_record( towgs84_gcs )
        gcs_rec['GREENWICH_DATUM'] = crs_rec_base['DATUM_CODE']
    else:
        gcs_rec['GREENWICH_DATUM'] = crs_rec['DATUM_CODE']
        towgs84_gcs = key
    
    if to_wgs84_ops.has_key(towgs84_gcs) and to_wgs84_ops[towgs84_gcs] is not None:
        co_rec = co.get_record( to_wgs84_ops[towgs84_gcs] )
        gcs_rec['COORD_OP_METHOD_CODE'] = co_rec['COORD_OP_METHOD_CODE']

        parms = co_value.get_records( int(co_rec['COORD_OP_CODE']) )

        for parm_rec in parms:
            if parm_rec['PARAMETER_CODE'] == '8605':
                gcs_rec['DX'] = parm_rec['PARAMETER_VALUE']
            elif parm_rec['PARAMETER_CODE'] == '8606':
                gcs_rec['DY'] = parm_rec['PARAMETER_VALUE']
            elif parm_rec['PARAMETER_CODE'] == '8607':
                gcs_rec['DZ'] = parm_rec['PARAMETER_VALUE']
            elif parm_rec['PARAMETER_CODE'] == '8608':
                gcs_rec['RX'] = parm_rec['PARAMETER_VALUE']
            elif parm_rec['PARAMETER_CODE'] == '8609':
                gcs_rec['RY'] = parm_rec['PARAMETER_VALUE']
            elif parm_rec['PARAMETER_CODE'] == '8610':
                gcs_rec['RZ'] = parm_rec['PARAMETER_VALUE']
            elif parm_rec['PARAMETER_CODE'] == '8611':
                gcs_rec['DS'] = parm_rec['PARAMETER_VALUE']

        
    gcs_table.add_record( key, gcs_rec )

gcs_table.write_to_csv( 'gcs.csv' )
gcs_table = None

