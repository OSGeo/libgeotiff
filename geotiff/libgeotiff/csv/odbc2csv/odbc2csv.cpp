/******************************************************************************
 * Copyright (c) 1999, Frank Warmerdam
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 ******************************************************************************
 *
 * The output format is ``Comma Separated Value'' format.
 *
 *  o There is always exactly one line per record.
 *  o The first line is a record with the column titles instead of column
 *    values.
 *  o Fields are separated by commas.
 *  o Some fields are enclosed in double quotes.  When reading the double
 *    quotes should be stripped off the field.
 *  o Quoted fields may contain escape sequences that should be interpreted
 *    specially:
 *            ""   should map to    "
 *
 * Note that error checking in this program is weak.  Fields are read as
 * simple strings.  Anything that doesn't translate well to strings may not
 * work (does ODBC support raw binary data?).
 * 
 * $Log$
 * Revision 1.6  2004/02/24 17:19:10  warmerda
 * fixed error in c generation case
 *
 * Revision 1.5  2002/11/28 15:34:33  warmerda
 * corrected to use standard CSV quoting mechanisms
 *
 * Revision 1.4  2002/11/25 20:28:28  warmerda
 * quote table name
 *
 * Revision 1.3  1999/12/10 17:43:55  warmerda
 * updated to support C Source output
 *
 * Revision 1.2  1999/03/12 13:47:28  geotiff
 * added docs on csv format
 *
 * Revision 1.1  1999/03/09 03:28:43  geotiff
 * New
 *
 */

#include <stdio.h>

#include <windows.h>
#include <sql.h>
#include <errno.h>
#include <ctype.h>

#include "sqldirect.h"

static void ODBC2CSV( CSQLDirect *, FILE * fp, int bGenerateC,
                      const char * pszTableName );

static const char *SanitizeName( const char *pszInputName );

int main( int argc, char ** argv )

{
    int            i;
    char           szDataSrc[128];
    int            bGenerateC = 0;

    if( argc < 2 ) 
    {
        printf("Usage: odbc2csv [-ds odbc_data_source] [-c] tablename ...\n" );
        exit( 1 );
    }

    strcpy( szDataSrc, "EPSG" );

    for( i = 1; i < argc; i++ )
    {
        if( strcmp(argv[i],"-ds") == 0 && i < argc-1 )
            strcpy( szDataSrc, argv[++i] );
        else if( strcmp(argv[i],"-c") == 0 )
            bGenerateC = 1;
        else if( !bGenerateC )
        {
            CSQLDirect      oDB( szDataSrc );
            char            szQuery[1024], szFilename[1024];
            FILE            *fp;

            sprintf( szFilename, "%s.csv", SanitizeName(argv[i]) );
            fp = fopen( szFilename, "w" );
            if( fp == NULL )
            {
                perror( "fopen" );
                exit( 1 );
            }
         
            sprintf( szQuery, "SELECT * FROM \"%s\"", argv[i] );
            if( oDB.ExecuteSQL( szQuery ) == SQL_SUCCESS )
            {
                ODBC2CSV( &oDB, fp, bGenerateC, argv[i] );
                fclose( fp );
            }
            else
                exit( 1 );
        }
        else if( bGenerateC )
        {
            CSQLDirect      oDB( szDataSrc );
            char            szQuery[1024], szFilename[1024];
            FILE            *fp;

            sprintf( szFilename, "%s.c", SanitizeName(argv[i]) );
            fp = fopen( szFilename, "w" );
            if( fp == NULL )
            {
                perror( "fopen" );
                exit( 1 );
            }
         
            fprintf( fp, "%s\n", "#include \"defs.h\"" );
            sprintf( szQuery, "SELECT * FROM \"%s\"", argv[i] );
            if( oDB.ExecuteSQL( szQuery ) == SQL_SUCCESS )
            {
                ODBC2CSV( &oDB, fp, bGenerateC, argv[i] );
                fclose( fp );
            }
            else
                exit( 1 );
        }
    }

    return 0;
}

static const char *SanitizeName( const char *pszInputName )

{
    static char szSafeName[1000];
    int i;

    strcpy( szSafeName, pszInputName );
    for( i = 0; szSafeName[i] != '\0'; i++ )
    {
        if( szSafeName[i] == ' ' )
            szSafeName[i] = '_';
        szSafeName[i] = tolower(szSafeName[i]);
    }

    return szSafeName;
}
static const char *CSVEscapeString( const char * pszInput )

{
    static char    *pszStaticBuf = NULL;
    static int     nStaticBufSize = 0;
    int            i, iOut;

    /*
     * Passing in a NULL just cleans up the internal buffer.
     */
    if( pszInput == NULL )
    {
        if( pszStaticBuf != NULL )
            free( pszStaticBuf );
        pszStaticBuf = NULL;
        nStaticBufSize = 0;

        return NULL;
    }

    /*
     * If there are no double quotes, newlines, or commas we don't have
     * to do anything special.
     */
    if( strchr( pszInput, '\"' ) == NULL
        && strchr( pszInput, ',') == NULL
        && strchr( pszInput, 10) == NULL 
        && strchr( pszInput, 13) == NULL )
        return( pszInput );

    /*
     * Make sure the output buffer is big enough to hold anything the
     * input buffer could permute into.
     */

    if( nStaticBufSize < strlen(pszInput) * 2 + 10 )
    {
        nStaticBufSize = strlen(pszInput) * 2 + 20;
        if( pszStaticBuf != NULL )
            free( pszStaticBuf );

        pszStaticBuf = (char *) malloc( nStaticBufSize );
    }

    /*
     * Copy characters, adding double quotes, and escaping anything odd.
     */
    pszStaticBuf[0] = '\"';
    iOut = 1;
    for( i = 0; pszInput[i] != '\0'; i++ )
    {
        switch( pszInput[i] )
        {
            case '\"':
                pszStaticBuf[iOut++] = '\"';
                pszStaticBuf[iOut++] = '\"';
                break;

            case 13:
                /* don't carry through DOS LF */
                break;

            default:
                pszStaticBuf[iOut++] = pszInput[i];
                break;
        }
    }

    pszStaticBuf[iOut++] = '\"';
    pszStaticBuf[iOut++] = '\0';

    return( pszStaticBuf );
}

static void ODBC2CSV( CSQLDirect * poDB, FILE * fp, int bGenerateC,
                      const char * pszTableName )

{
    int            nFields, iField;
    int            iRow = 0;
    /*
     * The first step is to capture, and emit all the record names.
     */
    if( bGenerateC )
        fprintf( fp, "datafile_rows_t %s_row_%d[] = {", 
                 pszTableName, ++iRow );

    nFields = poDB->GetColumnCount();
    for( iField = 1; iField <= nFields; iField++ )
    {
        if( iField > 1 )
            fprintf( fp, "," );

        fprintf( fp, "\"%s\"", poDB->GetColumnName( iField ) );
    }
    if( bGenerateC )
        fprintf( fp, ",NULL};");
    fprintf( fp, "\n" );

    /*
     * Loop over all the records, fetching them and writing one
     * field at a time.
     */

    while( poDB->Fetch() == SQL_SUCCESS )
    {
        if( bGenerateC )
            fprintf( fp, "datafile_rows_t %s_row_%d[] = {", 
                     pszTableName, ++iRow );

        for( iField = 1; iField <= nFields; iField++ )
        {
            const char      *pszValue;
         
            if( iField > 1 )
                fprintf( fp, "," );

            pszValue = poDB->GetCol( iField );
            if( strlen(pszValue) > 256 && bGenerateC )
                ((char *)pszValue)[256] = '\0';

            const char *      pszEscapedField = CSVEscapeString( pszValue );

            if( bGenerateC && pszEscapedField[0] != '\"' )
                fprintf( fp, "\"%s\"", pszEscapedField );
            else
                fprintf( fp, "%s", pszEscapedField );
        }

        if( bGenerateC )
            fprintf( fp, ",NULL};");

        fprintf( fp, "\n" );
    }

    if( bGenerateC )
    {
        int            i;

        fprintf( fp, "\ndatafile_rows_t *%s_rows[] = {", 
                 pszTableName );

        for( i = 0; i < iRow; i++ )
        {
            fprintf( fp, "%s_row_%d,", pszTableName, i+1 );
        }
        fprintf( fp, "NULL};\n" );
    }
}
