#!/usr/bin/env python
#******************************************************************************
#  $Id$
# 
#  Project:  GDAL
#  Purpose:  Build the epsg_pcs.csv table with the minimum information
#            required to define a PCS (not including GCS defs). 
#  Author:   Frank Warmerdam, warmerdam@pobox.com
# 
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

def SplitCSVLine( line ):
    tokens = []
    l = len(line)
    cur_token = ''
    in_quotes = 0
    escapted = 0
    for i in range(l):
        c = line[i]
        if c == '\\':
            escaped = 1
        elif c == '"' and not escaped:
            in_quotes = not in_quotes
        elif c == ',' and not in_quotes and not escaped:
            tokens.append( cur_token )
            cur_token = ''
        else:
            cur_token = cur_token + c
            escaped = 0
            
    tokens.append(cur_token)

    return tokens

class CSVTable:

    def __init__( self ):
        self.fields = []
        self.data = {}
        self.multi = 0

    def add_field( self, field_name ):
        self.fields.append( field_name )

    def read_from_csv( self, filename, multi = 0 ):

        self.multi = multi
        
        fd = open( filename )

        # Process the first line as field names.
        tokens = string.split( string.strip(fd.readline()), ',' )
        for field in tokens:
            self.fields.append( string.replace( field, '"', '' ) )

        # Process the rest of the file.
        rest_of_lines = fd.readlines()
        for line in rest_of_lines:
            if len(line) > 2:
                key, rest = string.split(line,',', 1 )
                key = int(key)
                if multi:
                    if self.data.has_key(key):
                        self.data[key].append(string.strip(line))
                    else:
                        self.data[key] = [string.strip(line)]
                else:
                    self.data[key] = string.strip(line)
            else:
                print 'problem line: %s\n' % line

    def write_to_csv( self, filename ):
        def_line = ''
        for i in range(len(self.fields)):
            if i > 0:
                def_line = def_line + ','
            def_line = def_line + '"' + self.fields[i] + '"'

        fd = open( filename, 'w' )
        fd.write( def_line + '\n' )

        keys = self.data.keys()
        keys.sort()
        for key in keys:
            fd.write( self.data[key] + '\n' )
        fd.close()

    def escape_field( self, in_text ):
        safe_chars = string.ascii_letters + string.digits + '.-'
        
        out_field = ''
        need_quotes = 0
        for c in in_text:
            if c not in safe_chars:
                need_quotes = 1
            if c == '"' or ord(c) == 92:
                out_field = out_field + chr(92)
            
            out_field = out_field + c
        if need_quotes:
            out_field = '"' + out_field + '"'

        return out_field

    def line_to_record( self, line ):
        tokens = SplitCSVLine( line )
        if len(tokens) != len(self.fields):
            print 'CSV lines field count does not match'

        record = {}
        for i in range(len(self.fields)):
            record[self.fields[i]] = tokens[i]

        return record

    def record_to_line( self, record ):
        line = ''
        for i in range(len(self.fields)):
            if record.has_key(self.fields[i]):
                field_val = self.escape_field( record[self.fields[i]] )
            else:
                field_val = ''
            if i > 0:
                line = line + ','
            line = line + field_val
        return line

    def add_record( self, key, record ):
        self.data[key] = self.record_to_line(record)
        
    def set_record( self, key, record ):
        self.data[key] = self.record_to_line(record)
        
    def get_record( self, key ):
        return self.line_to_record( self.data[key] )

    def get_records( self, key ):
        lines = self.data[key]
        records = []
        for line in lines:
            records.append( self.line_to_record( line ) )

        return records
        
