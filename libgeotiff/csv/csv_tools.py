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

import string

def SplitCSVLine( line ):
    tokens = []
    l = len(line)
    cur_token = ''
    in_quotes = 0
    escaped = 0
    for i in range(l):
        c = line[i]
        if c == '"':
            if escaped == 0 and in_quotes and i < l-1 and line[i+1] == '"':
                escaped = 1
            elif escaped == 1:
                cur_token = cur_token + '"'
                escaped = 0
            else:
                in_quotes = not in_quotes
        elif c == ',' and not in_quotes:
            tokens.append( cur_token )
            cur_token = ''
        else:
            cur_token = cur_token + c
            
    tokens.append(cur_token)

    return tokens

# Merge records split by newlines within quotes.
def merge_split_lines( raw_lines ):
    rest_of_lines = []
    cur_line = ''
    for line in raw_lines:
        cur_line = cur_line + line
        quote_count = cur_line.count('"')
        if quote_count % 2 == 0:
            rest_of_lines.append( cur_line )
            cur_line = ''
    if cur_line != '':
        rest_of_lines.append( cur_line )
    return rest_of_lines
    
class CSVTable:

    def __init__( self ):
        self.fields = []
        self.data = {}
        self.multi = 0

    def add_field( self, field_name, default_value = '' ):
        self.fields.append( field_name )
        for key in self.data.keys():
            self.data[key] = self.data[key] + ',' + default_value

    def read_from_csv( self, filename, multi = 0 ):

        self.multi = multi
        
        fd = open( filename )

        # Process the first line as field names.
        tokens = fd.readline().strip().split( ',' )
        for field in tokens:
            self.fields.append(field.replace( '"', '' ).upper())

        # Load the rest of the files, merging records split by newlines
        # within quotes.
        rest_of_lines = merge_split_lines( fd.readlines() )

        # Build lines into an indexed hash table.
        line_counter = -1
        for line in rest_of_lines:
            line_counter += 1
            
            if line[0] == '#':
                continue
            
            if len(line) > 2:
                key, rest = line.split( ',', 1 )
                key = int(key)
                if multi:
                    if key in self.data:
                        self.data[key].append(line.strip())
                    else:
                        self.data[key] = [line.strip()]
                else:
                    self.data[key] = line.strip()
            else:
                print('Problem reading line %d of file %s:%s\n' \
                      % ( line_counter, filename, line))

    def write_to_csv( self, filename ):
        def_line = ''
        for i in range(len(self.fields)):
            if i > 0:
                def_line = def_line + ','
            def_line = def_line + '"' + self.fields[i] + '"'

        fd = open( filename, 'w' )
        fd.write( def_line + '\n' )

        keys = self.data.keys()
        keys = sorted(keys)
        for key in keys:
            fd.write( self.data[key] + '\n' )
        fd.close()

    def escape_field( self, in_text ):
        safe_chars = string.ascii_letters + string.digits + '.- '
        
        out_field = ''
        need_quotes = 0
        for c in in_text:
            if c not in safe_chars:
                need_quotes = 1

            if c == '"':
                # add extra quote for quotes.
                out_field = out_field + '"'
                need_quotes = 1
            
            out_field = out_field + c

        if need_quotes:
            out_field = '"' + out_field + '"'

        return out_field

    def line_to_record( self, line ):
        tokens = SplitCSVLine( line )
        if len(tokens) != len(self.fields):
            print('CSV lines field count does not match')
            print(line)
            print(len(tokens))
            print(len(self.fields))
            print(tokens)

        record = {}
        for i in range(len(self.fields)):
            record[self.fields[i]] = tokens[i]

        return record

    def record_to_line( self, record ):
        line = ''
        for i in range(len(self.fields)):
            if self.fields[i] in record:
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
        
