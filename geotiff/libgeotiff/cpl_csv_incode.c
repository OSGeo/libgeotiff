/**********************************************************************
 * $Id$
 *
 * Name:     cpl_struct.c
 * Project:  libgeotiff
 * Purpose:  Provide "CSV API" interface to in-code EPSG CSV tables.
 * Author:   Derrick J Brashear <shadow@dementia.org>
 *
 ******************************************************************************
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
 * $Log$
 * Revision 1.1  1999/12/10 18:00:58  warmerda
 * New
 *
 */

#include <stdio.h>
#include "cpl_csv.h"

#include "defs.h"

extern const datafile_rows_t *compd_cs_rows[];
extern const datafile_rows_t *ellips_alias_rows[];
extern const datafile_rows_t *ellipsoid_rows[];
extern const datafile_rows_t *gdatum_alias_rows[];
extern const datafile_rows_t *geod_datum_rows[];
extern const datafile_rows_t *geod_trf_rows[];
extern const datafile_rows_t *horiz_cs_rows[];
extern const datafile_rows_t *p_meridian_rows[];
extern const datafile_rows_t *trf_nonpolynomial_rows[];
extern const datafile_rows_t *trf_path_rows[];
extern const datafile_rows_t *uom_an_alias_rows[];
extern const datafile_rows_t *uom_angle_rows[];
extern const datafile_rows_t *uom_le_alias_rows[];
extern const datafile_rows_t *uom_length_rows[];
extern const datafile_rows_t *uom_scale_rows[];
extern const datafile_rows_t *uom_sc_alias_rows[];
extern const datafile_rows_t *vert_cs_rows[];
extern const datafile_rows_t *vert_datum_rows[];
extern const datafile_rows_t *vert_offset_rows[];


/* Pointers to data */
static const datafile_t files[] = {
  { "compd_cs", compd_cs_rows },
  { "ellips_alias", ellips_alias_rows },
  { "ellipsoid", ellipsoid_rows },
  { "gdatum_alias", gdatum_alias_rows },
  { "geod_datum", geod_datum_rows },
  { "geod_trf", geod_trf_rows },
  { "horiz_cs", horiz_cs_rows },
  { "p_meridian", p_meridian_rows },
  { "trf_nonpolynomial", trf_nonpolynomial_rows },
  { "trf_path", trf_path_rows },
  { "uom_an_alias", uom_an_alias_rows },
  { "uom_angle", uom_angle_rows },
  { "uom_le_alias", uom_le_alias_rows },
  { "uom_length", uom_length_rows },
  { "uom_sc_alias", uom_sc_alias_rows },
  { "uom_scale", uom_scale_rows },
  { "vert_cs", vert_cs_rows },
  { "vert_datum", vert_datum_rows },
  { "vert_offset", vert_offset_rows },
  { NULL, NULL }
};

#if 0
main()
{
  datafile_t *csvfile;
  char **papszRecord;
  int i, row, col;

  papszRecord = CSVScanFileByName( "horiz_cs.csv", "HORIZCS_CODE",
				   "2200", CC_Integer );

  printf ("%s %s\n", papszRecord[0], papszRecord[1]);
  csvfile = &files[0];
  while (csvfile->name != NULL) {
    printf("file name is %s\n", csvfile->name);
    for (i = 0; csvfile->cols[i]; i++) {
      printf("column name is %s\n", csvfile->cols[i]);
      row = 1; col = 0;
      if (csvfile->rows[row] && csvfile->rows[row][col])
	printf("value %d,%d is %s\n", row, col, csvfile->rows[row][col]);
    }
    csvfile++;
  }
}
#endif

const char * CSVFilename( const char *pszBasename )
{
  return pszBasename;
}

static int CSVCompare( const char * pszFieldValue, const char * pszTarget,
                       CSVCompareCriteria eCriteria )
{
    if( eCriteria == CC_ExactString )
    {
        return( strcmp( pszFieldValue, pszTarget ) == 0 );
    }
    else if( eCriteria == CC_ApproxString )
    {
        return( strcasecmp( pszFieldValue, pszTarget ) );
    }
    else if( eCriteria == CC_Integer )
    {
        return( atoi(pszFieldValue) == atoi(pszTarget) );
    }
    return FALSE;
}

static int __CSVGetFileId( const char * pszFilename)
{
  datafile_t *csvfile;
  int i = 0;

  csvfile = (datafile_t *)&files[i];
  for (i = 0; csvfile->name; i++, csvfile = (datafile_t *)&files[i])
  {
    if (!strncmp(csvfile->name,pszFilename,(strlen(pszFilename)-4)))
      return i;
  }

  return -1;
}

char **CSVScanFileByName( const char * pszFilename,
                          const char * pszKeyFieldName,
                          const char * pszValue, 
                          CSVCompareCriteria eCriteria )
{
  datafile_t *csvfile;
  int row, col;

  col = CSVGetFileFieldId(pszFilename, pszKeyFieldName);

  csvfile = (datafile_t *)&files[__CSVGetFileId(pszFilename)];
  for (row = 1; ((csvfile->rows[row] != 0) && (csvfile->rows[row][col] != 0));
       row++) {
    if (CSVCompare(csvfile->rows[row][col], pszValue, eCriteria))
      return ((char **)csvfile->rows[row]);
  }

  return NULL;
}

int CSVGetFileFieldId( const char * pszFilename, const char * pszFieldName)
{
    datafile_t *csvfile;
    int i;

    csvfile = (datafile_t *)&files[__CSVGetFileId(pszFilename)];
    if (!strncmp(csvfile->name,pszFilename,(strlen(pszFilename)-4)))
    {
        for (i = 0; csvfile->rows[0][i]; i++) 
            if (!strcasecmp(pszFieldName, csvfile->rows[0][i]))
                return i;
    }

    return -1;
}

const char *CSVGetField( const char * pszFilename,
                         const char * pszKeyFieldName,
                         const char * pszKeyFieldValue,
                         CSVCompareCriteria eCriteria,
                         const char * pszTargetField )
{
  char **papszRecord;

  papszRecord = CSVScanFileByName( pszFilename, pszKeyFieldName,
				   pszKeyFieldValue, CC_Integer );

  return (papszRecord[CSVGetFileFieldId(pszFilename, pszTargetField)]);
}

/* Dummy function */
void SetCSVFilenameHook( const char *(*pfnNewHook)( const char * ) )

{
}
