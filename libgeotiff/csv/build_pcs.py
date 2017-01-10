#!/usr/bin/env python
# -*- coding: utf-8 -*-
#******************************************************************************
#  $Id$
# 
#  Project:  GDAL
#  Purpose:  Build the pcs.csv, gcs.csv, compdcs.csv and geoccs.csv tables with
#            the minimum information required to define a PCS, GCS, COMPD_CS and
#            GEOCCS for GDAL.
#  Author:   Frank Warmerdam, warmerdam@pobox.com
#******************************************************************************
#  Copyright (c) 2002, 2010, Frank Warmerdam <warmerdam@pobox.com>
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

import csv_tools
import math

def get_crs_uom( crs_rec, cs, caxis ):
    coord_sys_code = int(crs_rec['COORD_SYS_CODE'])

    ca_recs = caxis.get_records( coord_sys_code )
    return ca_recs[0]['UOM_CODE']

def get_significant_digits(str_value):

    significant_digits = 0
    leading_stuff = True
    for c in str_value:
        if leading_stuff:
            if c >= '1' and c <= '9':
                leading_stuff = False
                significant_digits = 1
        else:
            if c == 'e':
                break
            if c != '.':
                significant_digits = significant_digits + 1
    return significant_digits

def stringify_with_same_precision(v, old_value):

    significant_digits = get_significant_digits(old_value)
    for i in range(15):
        format = "%%.%df" % i
        str_v = format % v
        if get_significant_digits(str_v) == significant_digits + 1:
            return str_v
    return str_v

def copy_datum_shift_parms( target_rec, parms ):

    for parm_rec in parms:
        # Confirm that the parameter codes in the expected units of measurement.
        # If not, try to correct expected cases and error out on others.
        value = parm_rec['PARAMETER_VALUE']
        code = parm_rec['PARAMETER_CODE']
        uom = parm_rec['UOM_CODE']

        # Linear parameters
        if code in ('8605','8606','8607'):
            if uom != '9001':
                print('Datum Shift x/y/z not in meters!')
                print(parm_rec)

        # angular parameters
        if code in ('8608','8609','8610'):
            # should be in arc-seconds.
            if uom == '9109':  # Micro-radians.
                v = float(value)
                v = (v / 1000000.0) * (180 / math.pi) * 3600.0
                value = stringify_with_same_precision(v, value)
            elif uom == '9101':  # Radians.
                v = float(value)
                v = v * (180 / math.pi) * 3600.0
                value = stringify_with_same_precision(v, value)
            elif uom == '9113':  # centesimal second
                v = float(value)
                # convert to radians
                v = v * (math.pi/200.0) / 10000.0
                # convert to arc seconds
                v = v * (180 / math.pi) * 3600.0
                value = stringify_with_same_precision(v, value)
            elif uom != '9104':
                print('Datum Shift rotation not in arc-seconds!')
                print(parm_rec)
            
        if code == '8605':
            target_rec['DX'] = value
        elif code == '8606':
            target_rec['DY'] = value
        elif code == '8607':
            target_rec['DZ'] = value
        elif code == '8608':
            target_rec['RX'] = value
        elif code == '8609':
            target_rec['RY'] = value
        elif code == '8610':
            target_rec['RZ'] = value
        elif code == '8611':
            target_rec['DS'] = value
            

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

area_tb = csv_tools.CSVTable()
area_tb.read_from_csv( 'area.csv' )

datum_shift_pref = csv_tools.CSVTable()
datum_shift_pref.read_from_csv( 'datum_shift_pref.csv' )

super = csv_tools.CSVTable()
super.read_from_csv( 'supersession.csv' )

##############################################################################
# Scan coordinate_reference_systems table to collect PCS ids.

pcs_keys = []
gcs_keys = []
compdcs_keys = []
vertcs_keys = []
geoccs_keys = []

for key in crs.data.keys():
    crs_rec = crs.get_record( key )
    if crs_rec['COORD_REF_SYS_KIND'] == 'projected':
        pcs_keys.append( key )
    elif crs_rec['COORD_REF_SYS_KIND'] == 'geographic 2D':
        gcs_keys.append( key )
    elif crs_rec['COORD_REF_SYS_KIND'] == 'compound':
        compdcs_keys.append( key )
    elif crs_rec['COORD_REF_SYS_KIND'] == 'vertical':
        vertcs_keys.append( key )
    elif crs_rec['COORD_REF_SYS_KIND'] == 'geocentric':
        geoccs_keys.append( key )

pcs_keys.sort()
gcs_keys.sort()
compdcs_keys.sort()
vertcs_keys.sort()
geoccs_keys.sort()

print('%d PCS, %d GCS, %d GeocCS, %d VertCS and %d COMPD_CS coordinate systems to process.' % (len(pcs_keys), len(gcs_keys), len(geoccs_keys), len(vertcs_keys), len(compdcs_keys)))

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

pcs_table.add_field('DX')                        # +towgs84 parameters.
pcs_table.add_field('DY')                        
pcs_table.add_field('DZ')                        
pcs_table.add_field('RX')                        
pcs_table.add_field('RY')                        
pcs_table.add_field('RZ')                        
pcs_table.add_field('DS')                        

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
        print('GEOGCRS missing for %s/%s' % (crs_rec['COORD_REF_SYS_CODE'],
                                             crs_rec['COORD_REF_SYS_NAME']))

    pcs_rec['UOM_CODE'] = get_crs_uom(crs_rec, cs, caxis )
                                             
    pcs_rec['COORD_OP_CODE']      = crs_rec['PROJECTION_CONV_CODE']

    co_rec = co.get_record( int(pcs_rec['COORD_OP_CODE']) )
    pcs_rec['COORD_OP_METHOD_CODE'] = co_rec['COORD_OP_METHOD_CODE']

    parm_recs = co_value.get_records( int(pcs_rec['COORD_OP_CODE']) )
    if len(parm_recs) > max_parms:
        print('COORD_OP_CODE %s has %d values.' % (pcs_rec['COORD_OP_CODE'],
                                                   len(parm_recs)))
        
    for parm_i in range(len(parm_recs)):
        parm_rec = parm_recs[parm_i]

        pin = '%d' % (parm_i+1)

        pcs_rec['PARAMETER_CODE_'+pin] = parm_rec['PARAMETER_CODE']
        pcs_rec['PARAMETER_VALUE_'+pin] = parm_rec['PARAMETER_VALUE']
        pcs_rec['PARAMETER_UOM_'+pin] = parm_rec['UOM_CODE']

    try:
        pref_rec = datum_shift_pref.get_record(key)
    except:
        pref_rec = None
    if pref_rec is not None:
        parms = co_value.get_records( int(pref_rec['COORD_OP_CODE']) )
        copy_datum_shift_parms( pcs_rec, parms )

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

op_keys = sorted(op_keys)
for key in op_keys:

    powp_rec = {}
    
    # Check COORD_OP_TYPE.
    if co.data[key].find(',conversion,') < 1:
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

        if source_crs in to_wgs84_ops:
            to_wgs84_ops[source_crs].append(key)
        else:
            to_wgs84_ops[source_crs] = [key]
        
    # Does this operation relate this GCS with a Greenwich meridian
    # equivelent?
    if co_rec['COORD_OP_METHOD_CODE'] == '9601':
        greenwich_equiv[int(co_rec['SOURCE_CRS_CODE'])] = \
                                            int(co_rec['TARGET_CRS_CODE'])

##############################################################################
# Identify coordinate operations that have been superseeded according to
# the supersession table.

superseded_operations = {}

for id in super.data.keys():
    record = super.get_record(id)

    if record['OBJECT_TABLE_NAME'] == 'epsg_coordoperation':
        superseded_operations[record['OBJECT_CODE']] = record['SUPERSEDED_BY']

##############################################################################
# Prepare a datum shift file containing all the datum shifts for each
# datum with a bit of supporting information.

ds_table = csv_tools.CSVTable()
ds_table.add_field('SEQ_KEY')             
ds_table.add_field('COORD_OP_CODE')             
ds_table.add_field('SOURCE_CRS_CODE')             
ds_table.add_field('TARGET_CRS_CODE')             
ds_table.add_field('REMARKS')
ds_table.add_field('COORD_OP_SCOPE')
ds_table.add_field('AREA_OF_USE_CODE')
ds_table.add_field('AREA_SOUTH_BOUND_LAT')
ds_table.add_field('AREA_NORTH_BOUND_LAT')
ds_table.add_field('AREA_WEST_BOUND_LON')
ds_table.add_field('AREA_EAST_BOUND_LON')
ds_table.add_field('SHOW_OPERATION')
ds_table.add_field('DEPRECATED')
ds_table.add_field('COORD_OP_METHOD_CODE')   # +towgs84 parameters.
ds_table.add_field('DX')                        
ds_table.add_field('DY')                        
ds_table.add_field('DZ')                        
ds_table.add_field('RX')                        
ds_table.add_field('RY')                        
ds_table.add_field('RZ')                        
ds_table.add_field('DS')                        
ds_table.add_field('PREFERRED')

##############################################################################
# populate table.

ignore_towgs84_gcs_list = []

seq_key = 0
for gcs in to_wgs84_ops.keys():
    preferred_op = None
    preferred_op_area = 0

    try:
        pref_rec = datum_shift_pref.get_record(gcs)

        # keep track of gcs'es we don't want a transform for, like NAD27
        if pref_rec['COORD_OP_CODE'] == '-1':
            pref_rec = None
            ignore_towgs84_gcs_list.append( gcs )
            print('Ignore TOWGS84 for GCS ', gcs)
            
    except:
        pref_rec = None
    
    for shift_ops in to_wgs84_ops[gcs]:

        seq_key = seq_key + 1
        
        ds_rec = {}
       
        co_rec = co.get_record( shift_ops )
        ds_rec['SEQ_KEY'] = str(seq_key)
        ds_rec['COORD_OP_CODE'] = co_rec['COORD_OP_CODE']
        ds_rec['SOURCE_CRS_CODE'] = co_rec['SOURCE_CRS_CODE']
        ds_rec['TARGET_CRS_CODE'] = co_rec['TARGET_CRS_CODE']
        ds_rec['REMARKS'] = co_rec['REMARKS']
        ds_rec['COORD_OP_SCOPE'] = co_rec['COORD_OP_SCOPE']
        ds_rec['AREA_OF_USE_CODE'] = co_rec['AREA_OF_USE_CODE']
        ds_rec['SHOW_OPERATION'] = co_rec['SHOW_OPERATION']
        ds_rec['DEPRECATED'] = co_rec['DEPRECATED']
        ds_rec['PREFERRED'] = '0'
        ds_rec['COORD_OP_METHOD_CODE'] = co_rec['COORD_OP_METHOD_CODE']
        
        parms = co_value.get_records( int(co_rec['COORD_OP_CODE']) )
        copy_datum_shift_parms( ds_rec, parms )

        area_rec = area_tb.get_record( int(ds_rec['AREA_OF_USE_CODE']) )
        ds_rec['AREA_SOUTH_BOUND_LAT'] = area_rec['AREA_SOUTH_BOUND_LAT']
        ds_rec['AREA_NORTH_BOUND_LAT'] = area_rec['AREA_NORTH_BOUND_LAT']
        ds_rec['AREA_WEST_BOUND_LON'] = area_rec['AREA_WEST_BOUND_LON']
        ds_rec['AREA_EAST_BOUND_LON'] = area_rec['AREA_EAST_BOUND_LON']
        area_size = \
                  abs(float(ds_rec['AREA_NORTH_BOUND_LAT'])          \
                      - float(ds_rec['AREA_SOUTH_BOUND_LAT'])) *     \
                  abs(float(ds_rec['AREA_EAST_BOUND_LON'])           \
                      - float(ds_rec['AREA_WEST_BOUND_LON']))

        ds_table.add_record( seq_key, ds_rec )

        if pref_rec is not None \
           and pref_rec['COORD_OP_CODE'] == ds_rec['COORD_OP_CODE']:
            preferred_op = seq_key
            
        if pref_rec is None \
           and ds_rec['DEPRECATED'] == '0' \
           and not ds_rec['COORD_OP_CODE'] in superseded_operations:
            if preferred_op is None or area_size > preferred_op_area:
                preferred_op = seq_key
                preferred_op_area = area_size

    if preferred_op is None and pref_rec is not None:
        print('Failed to find preferred datum shift coord_op_code %s for GCS %d' % (pref_rec['COORD_OP_CODE'],gcs))
        
    if preferred_op is not None:
        ds_rec = ds_table.get_record( preferred_op )
        ds_rec['PREFERRED'] = '1'

        coc = int(ds_rec['COORD_OP_CODE'])
        # Promote to front of list.
        to_wgs84_ops[gcs].remove( coc )
        to_wgs84_ops[gcs] = [coc] + to_wgs84_ops[gcs]

        ds_table.set_record( preferred_op, ds_rec )

##############################################################################
# Write the datum shift table.

ds_table.write_to_csv('datum_shift.csv')

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
gcs_table.add_field('COORD_OP_CODE')             # datum shift operation code.
gcs_table.add_field('COORD_OP_CODE_MULTI')       # more than one datum shift?
gcs_table.add_field('COORD_OP_METHOD_CODE')      # datum shift method
gcs_table.add_field('DX')                        # +towgs84 parameters.
gcs_table.add_field('DY')                        
gcs_table.add_field('DZ')                        
gcs_table.add_field('RX')                        
gcs_table.add_field('RY')                        
gcs_table.add_field('RZ')                        
gcs_table.add_field('DS')                        

##############################################################################
# Populate and write GCS table.

skipped_funky_gcs = 0

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

    if key > 10000000:
        skipped_funky_gcs += 1
        continue

    crs_rec = crs.get_record( key )
    gcs_rec = {}
    gcs_rec['COORD_REF_SYS_CODE'] = crs_rec['COORD_REF_SYS_CODE']
    gcs_rec['COORD_REF_SYS_NAME'] = crs_rec['COORD_REF_SYS_NAME']
    gcs_rec['DATUM_CODE']         = crs_rec['DATUM_CODE']
    gcs_rec['SHOW_CRS']           = crs_rec['SHOW_CRS']
    gcs_rec['DEPRECATED']         = crs_rec['DEPRECATED']
    gcs_rec['COORD_SYS_CODE']     = crs_rec['COORD_SYS_CODE']
    gcs_rec['COORD_OP_CODE_MULTI'] = '0'

    gcs_rec['UOM_CODE'] = get_crs_uom(crs_rec, cs, caxis )

    try:
        datum_id = int(crs_rec['DATUM_CODE'])
    except:
        print('No DATUM_CODE for %s, skipping.' % crs_rec['COORD_REF_SYS_NAME'])
        continue
    
    datum_rec = datums.get_record( datum_id )
    gcs_rec['DATUM_NAME'] = datum_rec['DATUM_NAME']
    gcs_rec['ELLIPSOID_CODE'] = datum_rec['ELLIPSOID_CODE']
    gcs_rec['PRIME_MERIDIAN_CODE'] = datum_rec['PRIME_MERIDIAN_CODE']

    if key in greenwich_equiv:
        towgs84_gcs = greenwich_equiv[key]
        crs_rec_base = crs.get_record( towgs84_gcs )
        gcs_rec['GREENWICH_DATUM'] = crs_rec_base['DATUM_CODE']
    else:
        gcs_rec['GREENWICH_DATUM'] = crs_rec['DATUM_CODE']
        towgs84_gcs = key
    
    if towgs84_gcs in to_wgs84_ops \
       and to_wgs84_ops[towgs84_gcs] is not None \
       and not (towgs84_gcs in ignore_towgs84_gcs_list):
    
        coc_list = to_wgs84_ops[towgs84_gcs]
        co_rec = co.get_record( coc_list[0] )

        gcs_rec['COORD_OP_CODE'] = str(coc_list[0])
        if len(coc_list) > 1:
            gcs_rec['COORD_OP_CODE_MULTI'] = '1'
        gcs_rec['COORD_OP_METHOD_CODE'] = co_rec['COORD_OP_METHOD_CODE']

        parms = co_value.get_records( int(co_rec['COORD_OP_CODE']) )
        copy_datum_shift_parms( gcs_rec, parms )
        
    gcs_table.add_record( key, gcs_rec )

gcs_table.write_to_csv( 'gcs.csv' )
gcs_table = None

print( 'Skipped %d very large GCS codes, the (deg) versions presumably.' \
       % skipped_funky_gcs )
                             
##############################################################################
# Read VertCS Override table for manually assigned transformations.

vertcs_override_table = csv_tools.CSVTable()
vertcs_override_table.read_from_csv( 'vertcs.override.csv' )

##############################################################################
# Setup VertCS table fields.

vertcs_table = csv_tools.CSVTable()
vertcs_table.add_field('COORD_REF_SYS_CODE')        # GCS #
vertcs_table.add_field('COORD_REF_SYS_NAME')        # GCS Name
vertcs_table.add_field('DATUM_CODE')                # Datum #
vertcs_table.add_field('DATUM_NAME')                # 
vertcs_table.add_field('UOM_CODE')                  # Angular units for GCS.
vertcs_table.add_field('SHOW_CRS')                  # 0=false, 1=true
vertcs_table.add_field('DEPRECATED')                # 0=false, 1=true
vertcs_table.add_field('COORD_SYS_CODE')            # mainly for axes
vertcs_table.add_field('COORD_OP_METHOD_CODE_1')    # vert datum shift method
vertcs_table.add_field('PARM_1_1')

##############################################################################
# Populate and write vertcs table.

for key in vertcs_keys:
    try:
        o_rec = vertcs_override_table.get_record( key )
        
        print('VertCS %d overridden from vertcs.override.csv file' % key)
        vertcs_table.add_record( key, o_rec )
        continue
    except:
        pass

    crs_rec = crs.get_record( key )
    vertcs_rec = {}
    vertcs_rec['COORD_REF_SYS_CODE'] = crs_rec['COORD_REF_SYS_CODE']
    vertcs_rec['COORD_REF_SYS_NAME'] = crs_rec['COORD_REF_SYS_NAME']
    vertcs_rec['DATUM_CODE']         = crs_rec['DATUM_CODE']
    vertcs_rec['SHOW_CRS']           = crs_rec['SHOW_CRS']
    vertcs_rec['DEPRECATED']         = crs_rec['DEPRECATED']
    vertcs_rec['COORD_SYS_CODE']     = crs_rec['COORD_SYS_CODE']

    vertcs_rec['UOM_CODE'] = get_crs_uom(crs_rec, cs, caxis )

    try:
        datum_id = int(crs_rec['DATUM_CODE'])
    except:
        print('No DATUM_CODE for %s, skipping.' % crs_rec['COORD_REF_SYS_NAME'])
        continue
    
    datum_rec = datums.get_record( datum_id )
    vertcs_rec['DATUM_NAME'] = datum_rec['DATUM_NAME']

    vertcs_table.add_record( key, vertcs_rec )

vertcs_table.write_to_csv( 'vertcs.csv' )
vertcs_table = None

##############################################################################
# Setup COMPD_CS table fields.

compdcs_table = csv_tools.CSVTable()
compdcs_table.add_field('COORD_REF_SYS_CODE')        
compdcs_table.add_field('COORD_REF_SYS_NAME')        
compdcs_table.add_field('CMPD_HORIZCRS_CODE')       
compdcs_table.add_field('CMPD_VERTCRS_CODE')       
compdcs_table.add_field('SHOW_CRS')                  # 0=false, 1=true
compdcs_table.add_field('DEPRECATED')                # 0=false, 1=true

##############################################################################
# Populate COMPD_CS table.

for key in compdcs_keys:

    crs_rec = crs.get_record( key )
    compd_rec = {}
    compd_rec['COORD_REF_SYS_CODE'] = crs_rec['COORD_REF_SYS_CODE']
    compd_rec['COORD_REF_SYS_NAME'] = crs_rec['COORD_REF_SYS_NAME']
    compd_rec['SHOW_CRS']           = crs_rec['SHOW_CRS']
    compd_rec['DEPRECATED']         = crs_rec['DEPRECATED']
    compd_rec['CMPD_HORIZCRS_CODE'] = crs_rec['CMPD_HORIZCRS_CODE']
    compd_rec['CMPD_VERTCRS_CODE']  = crs_rec['CMPD_VERTCRS_CODE']

    compdcs_table.add_record( key, compd_rec )

compdcs_table.write_to_csv( 'compdcs.csv' )
compdcs_table = None

##############################################################################
# Setup Geocentric table fields.

geoccs_table = csv_tools.CSVTable()
geoccs_table.add_field('COORD_REF_SYS_CODE')        
geoccs_table.add_field('COORD_REF_SYS_NAME')        
geoccs_table.add_field('DATUM_CODE')                # Datum #
geoccs_table.add_field('DATUM_NAME')                # 
geoccs_table.add_field('GREENWICH_DATUM')           # Greenwich equiv datum
geoccs_table.add_field('UOM_CODE')                  # Linear units for GCS.
geoccs_table.add_field('ELLIPSOID_CODE')            # 
geoccs_table.add_field('PRIME_MERIDIAN_CODE')       #
geoccs_table.add_field('SHOW_CRS')                  # 0=false, 1=true
geoccs_table.add_field('DEPRECATED')                # 0=false, 1=true
geoccs_table.add_field('COORD_SYS_CODE')            # mainly for axes

##############################################################################
# Populate Geocentric table.

for key in geoccs_keys:

    crs_rec = crs.get_record( key )

    geoccs_rec = {}
    geoccs_rec['COORD_REF_SYS_CODE'] = crs_rec['COORD_REF_SYS_CODE']
    geoccs_rec['COORD_REF_SYS_NAME'] = crs_rec['COORD_REF_SYS_NAME']
    geoccs_rec['SHOW_CRS']           = crs_rec['SHOW_CRS']
    geoccs_rec['DEPRECATED']         = crs_rec['DEPRECATED']
    geoccs_rec['UOM_CODE']           = get_crs_uom(crs_rec, cs, caxis )
    geoccs_rec['DATUM_CODE']         = crs_rec['DATUM_CODE']
    geoccs_rec['COORD_SYS_CODE']     = crs_rec['COORD_SYS_CODE']
    try:
        datum_id = int(crs_rec['DATUM_CODE'])
    except:
        print('No DATUM_CODE for %s, skipping.' % crs_rec['COORD_REF_SYS_NAME'])
        continue
    
    datum_rec = datums.get_record( datum_id )
    geoccs_rec['DATUM_NAME'] = datum_rec['DATUM_NAME']
    geoccs_rec['ELLIPSOID_CODE'] = datum_rec['ELLIPSOID_CODE']
    geoccs_rec['PRIME_MERIDIAN_CODE'] = datum_rec['PRIME_MERIDIAN_CODE']

    if key in greenwich_equiv:
        towgs84_gcs = greenwich_equiv[key]
        crs_rec_base = crs.get_record( towgs84_gcs )
        geoccs_rec['GREENWICH_DATUM'] = crs_rec_base['DATUM_CODE']
    else:
        geoccs_rec['GREENWICH_DATUM'] = crs_rec['DATUM_CODE']

    geoccs_table.add_record( key, geoccs_rec )

geoccs_table.write_to_csv( 'geoccs.csv' )
geoccs_table = None
