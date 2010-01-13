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
# Revision 1.3  2004/04/27 20:42:57  warmerda
# fixed up C version
#
# Revision 1.2  2004/03/20 07:31:16  warmerda
# improved filename handling
#
# Revision 1.1  2004/03/20 07:10:21  warmerda
# New
#
#

import string
import sys
import csv_tools
import os.path

###############################################################################
def emit_token_line( fd, field_list, counter, varname ):
    fd.write( 'datafile_rows_t %s_row_%d[] = {' % (varname, counter) )
    for item in field_list:
        item = string.replace(item,'\n',' ')
        item = string.replace(item,'"','\\\"')
        fd.write( '"%s",' % item )
    fd.write( 'NULL};\n' )
    
###############################################################################
def convert_csv_table( csv_filename ):

    without_ext, ext = os.path.splitext( csv_filename )
    c_filename = without_ext + '.c'
    csv_filename = without_ext + '.csv'
    varname = os.path.basename(without_ext)

    lines = csv_tools.merge_split_lines(open(csv_filename).readlines())

    c_fd = open( c_filename, 'w' )
    c_fd.write( '#include "geo_incode_defs.h"\n' )

    data_lines = 0
    for line in lines:
        emit_token_line( c_fd, csv_tools.SplitCSVLine(line), data_lines,
                         varname )
        data_lines = data_lines + 1

    c_fd.write( 'datafile_rows_t *%s_rows[] = {' % varname )
    for i in range(data_lines):
        if i != 0:
            c_fd.write(' ,')
        c_fd.write( '%s_row_%d' % (varname, i) )
    c_fd.write( ',NULL};\n' )
    c_fd = None

###############################################################################
# main
if len(sys.argv) < 2:
    print 'Usage: csv2c.py filename.csv [...]'
    sys.exit( 1 )

for arg in sys.argv[1:]:
    convert_csv_table( arg )
