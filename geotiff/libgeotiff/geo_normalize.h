/******************************************************************************
 * $Id$
 *
 * Project:  libgeotiff
 * Purpose:  Include file related to geo_normalize.c containing Code to
 *           normalize PCS and other composite codes in a GeoTIFF file.
 * Author:   Frank Warmerdam, warmerda@home.com
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
 * Revision 1.4  1999/03/18 21:35:19  geotiff
 * Added PROJ.4 related stuff
 *
 * Revision 1.3  1999/03/17 20:44:04  geotiff
 * added CPL_DLL related support
 *
 * Revision 1.2  1999/03/10 18:24:06  geotiff
 * corrected to use int'
 *
 */

#ifndef GEO_NORMALIZE_H_INCLUDED
#define GEO_NORMALIZE_H_INCLUDED

#include "geotiff.h"

#ifdef __cplusplus
extern "C" {
#endif
    
#define MAX_GTIF_PROJPARMS 	10

typedef struct {
    short	Model;		/* GTModelTypeGeoKey:
                                   ModelTypeGeographic or ModelTypeProjected */
    short	PCS;		/* ProjectedCSTypeGeoKey */
    short	GCS;		/* GeographicTypeGeoKey (Datum+PM) */

    short	UOMLength;	/* ProjLinearUnitsGeoKey (eg. Linear_Meter) */
    double	UOMLengthInMeters;  /* one UOM = UOMLengthInMeters meters*/

    short	Datum;		/* GeogGeodeticDatumGeoKey */

    short	PM;		/* GeogPrimeMeridianGeoKey */
    double	PMLongToGreenwich; /* dec. deg (Long of PM rel.to Green)*/

    short	Ellipsoid;	/* GeogEllipsoidGeoKey */
    double	SemiMajor;	/* in meters */
    double	SemiMinor;	/* in meters */

    short	ProjCode;	/* ProjectionGeoKey ... eg. Proj_UTM_11S */

    short	Projection;	/* EPSG code from TRF_METHOD */
    short	CTProjection;   /* ProjCoordTransGeoKey:
                                   GeoTIFF CT_* code from geo_ctrans.inc
                                   eg. CT_TransverseMercator */

    int		nParms;
    double	ProjParm[MAX_GTIF_PROJPARMS];
    int		ProjParmId[MAX_GTIF_PROJPARMS]; /* geokey identifier,
                                                   eg. ProjFalseEastingGeoKey*/

} GTIFDefn;

int CPL_DLL GTIFGetPCSInfo( int nPCSCode, char **ppszEPSGName,
                            short *pnUOMLengthCode, short *pnUOMAngleCode,
                            short *pnGeogCS, short *pnProjectionCSCode );
int CPL_DLL GTIFGetProjTRFInfo( int nProjTRFCode,
                                char ** ppszProjTRFName,
                                short * pnProjMethod,
                                double * padfProjParms );
int CPL_DLL GTIFGetGCSInfo( int nGCSCode, char **ppszName,
                            short *pnDatum, short *pnPM );
int CPL_DLL GTIFGetDatumInfo( int nDatumCode, char **ppszName,
                              short * pnEllipsoid );
int CPL_DLL GTIFGetEllipsoidInfo( int nEllipsoid, char ** ppszName,
                                  double * pdfSemiMajor,
                                  double * pdfSemiMinor );
int CPL_DLL GTIFGetPMInfo( int nPM, char **ppszName,
                           double * pdfLongToGreenwich );

double CPL_DLL GTIFAngleStringToDD( const char *pszAngle, int nUOMAngle );
int CPL_DLL GTIFGetUOMLengthInfo( int nUOMLengthCode,
                                  char **ppszUOMName,
                                  double * pdfInMeters );

int CPL_DLL GTIFGetDefn( GTIF *, GTIFDefn * );
void CPL_DLL GTIFPrintDefn( GTIFDefn *, FILE * );
void CPL_DLL GTIFFreeDefn( GTIF * );

void CPL_DLL SetCSVFilenameHook( const char *(*)(const char *) );

const char CPL_DLL *GTIFDecToDMS( double, const char *, int );

/*
 * These are only useful if using libgeotiff with libproj (PROJ.4+).
 */
char CPL_DLL *GTIFGetProj4Defn( GTIFDefn * );
int  CPL_DLL  GTIFProj4ToLatLong( GTIFDefn *, int, double *, double * );
int  CPL_DLL  GTIFProj4FromLatLong( GTIFDefn *, int, double *, double * );

#if defined(HAVE_LIBPROJ) && defined(HAVE_PROJECTS_H)
#  define HAVE_GTIFPROJ4
#endif

#ifdef __cplusplus
}
#endif
    
#endif /* ndef GEO_NORMALIZE_H_INCLUDED */
