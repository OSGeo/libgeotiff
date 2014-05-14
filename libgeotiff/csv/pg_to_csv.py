#!/usr/bin/env python
# -*- coding: utf-8 -*-
#******************************************************************************
#  $Id$
# 
#  Project:  libgeotiff
#  Purpose:  Dump Postgres EPSG database to GeoTIFF ready CSV files.
#  Author:   Frank Warmerdam, warmerdam@pobox.com
#******************************************************************************
#  Copyright (c) 2006, Frank Warmerdam <warmerdam@pobox.com>
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
# Revision 1.1  2006/02/28 05:41:01  fwarmerdam
# New
#
#
#

import ogr, os, sys


def CopyTable( in_ds, out_ds, in_tablename, out_tablename, keyname,
               drop_list = [] ):

    stmt = 'select * from ' + in_tablename
    stmt = stmt + ' order by ' + keyname

    src_layer = in_ds.ExecuteSQL( stmt )

    dst_layer = out_ds.CreateLayer( out_tablename, geom_type = ogr.wkbNone )

    src_defn = src_layer.GetLayerDefn()
    for findex in range(src_defn.GetFieldCount()):
        if src_defn.GetFieldDefn(findex).GetName() not in drop_list:
            dst_layer.CreateField( src_defn.GetFieldDefn(findex) )

    dst_feat = ogr.Feature( dst_layer.GetLayerDefn() )
    src_feat = src_layer.GetNextFeature()
    while src_feat is not None:
        dst_feat.SetFrom( src_feat )
        dst_layer.CreateFeature( dst_feat )
        src_feat = src_layer.GetNextFeature()

    in_ds.ReleaseResultSet( src_layer )



# Main

try:
    x = os.stat('out')
    os.system('rm -rf out')
except:
    pass

in_ds = ogr.Open( 'PG:dbname=epsg host=localhost' )
if in_ds is None:
    in_ds = ogr.Open( 'PG:dbname=epsg' )
out_ds = ogr.GetDriverByName('CSV').CreateDataSource('out')

CopyTable( in_ds, out_ds, 'epsg_coordinatereferencesystem',
           'coordinate_reference_system', 'coord_ref_sys_code' )

CopyTable( in_ds, out_ds, 'epsg_coordinateaxis',
           'coordinate_axis', 'coord_sys_code',
           drop_list = ['coord_axis_code'] )

CopyTable( in_ds, out_ds, 'epsg_coordinateaxisname',
           'coordinate_axis_name', 'coord_axis_name_code' )

CopyTable( in_ds, out_ds, 'epsg_coordinatesystem',
           'coordinate_system', 'coord_sys_code' )

CopyTable( in_ds, out_ds, 'epsg_coordoperation',
           'coordinate_operation', 'coord_op_code' )

CopyTable( in_ds, out_ds, 'epsg_coordoperationmethod',
           'coordinate_operation_method', 'coord_op_method_code' )

CopyTable( in_ds, out_ds, 'epsg_coordoperationparam',
           'coordinate_operation_parameter', 'parameter_code' )

CopyTable( in_ds, out_ds, 'epsg_coordoperationparamvalue',
           'coordinate_operation_parameter_value', 'coord_op_code' )

CopyTable( in_ds, out_ds, 'epsg_coordoperationpath',
           'coordinate_operation_path', 'concat_operation_code' )

CopyTable( in_ds, out_ds, 'epsg_datum',
           'datum', 'datum_code' )

CopyTable( in_ds, out_ds, 'epsg_ellipsoid',
           'ellipsoid', 'ellipsoid_code' )

CopyTable( in_ds, out_ds, 'epsg_unitofmeasure',
           'unit_of_measure', 'uom_code' )

CopyTable( in_ds, out_ds, 'epsg_area',
           'area', 'area_code' )

CopyTable( in_ds, out_ds, 'epsg_supersession',
           'supersession', 'supersession_id' )

CopyTable( in_ds, out_ds, 'epsg_primemeridian',
           'prime_meridian', 'prime_meridian_code' )

