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
 * $Log$
 * Revision 1.1  1999/03/09 03:28:43  geotiff
 * New
 *
 */

#include <stdio.h>

#include <windows.h>
#include <sql.h>
#include <errno.h>

#include "sqldirect.h"

static void ODBC2CSV( CSQLDirect *, FILE * fp );

int main( int argc, char ** argv )

{
   int            i;
   char           szDataSrc[128];

   if( argc < 2 ) 
   {
      printf("Usage: odbc2csv [-ds odbc_data_source] tablename ...\n" );
      exit( 1 );
   }

   strcpy( szDataSrc, "EPSG" );

   for( i = 1; i < argc; i++ )
   {
      if( strcmp(argv[i],"-ds") == 0 && i < argc-1 )
         strcpy( szDataSrc, argv[++i] );
      else
      {
         CSQLDirect      oDB( szDataSrc );
         char            szQuery[1024], szFilename[1024];
         FILE            *fp;

         sprintf( szFilename, "%s.csv", argv[i] );
         fp = fopen( szFilename, "w" );
         if( fp == NULL )
         {
            perror( "fopen" );
            exit( 1 );
         }
         
         sprintf( szQuery, "SELECT * FROM %s", argv[i] );
         if( oDB.ExecuteSQL( szQuery ) == SQL_SUCCESS )
         {
            ODBC2CSV( &oDB, fp );
            fclose( fp );
         }
         else
            exit( 1 );
      }
   }

   return 0;
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
       && strchr( pszInput, 10) == NULL )
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
            pszStaticBuf[iOut++] = '\\';
            pszStaticBuf[iOut++] = '\"';
            break;

         case '\\':
            pszStaticBuf[iOut++] = '\\';
            pszStaticBuf[iOut++] = '\\';
            break;

         case 10:
            pszStaticBuf[iOut++] = '\\';
            pszStaticBuf[iOut++] = '\n';
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

static void ODBC2CSV( CSQLDirect * poDB, FILE * fp )

{
   int            nFields, iField;
   
   /*
    * The first step is to capture, and emit all the record names.
    */
   nFields = poDB->GetColumnCount();
   for( iField = 1; iField <= nFields; iField++ )
   {
      if( iField > 1 )
         fprintf( fp, "," );

      fprintf( fp, "\"%s\"", poDB->GetColumnName( iField ) );
   }
   fprintf( fp, "\n" );

   /*
    * Loop over all the records, fetching them and writing one
    * field at a time.
    */

   while( poDB->Fetch() == SQL_SUCCESS )
   {
      for( iField = 1; iField <= nFields; iField++ )
      {
         const char      *pszValue;
         
         if( iField > 1 )
            fprintf( fp, "," );

         pszValue = poDB->GetCol( iField );
         fprintf( fp, "%s", CSVEscapeString( pszValue ) );
      }
      fprintf( fp, "\n" );
   }
}
