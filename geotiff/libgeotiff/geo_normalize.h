
/*
 * Note: This file should be merged into geotiff.h eventually.
 */

#include "geotiff.h"

#ifdef __cplusplus
extern "C" {
#endif
    
#define MAX_GTIF_PROJPARMS 	10

typedef struct {
    int		Model;		/* ModelTypeGeographic or ModelTypeProjected */
    int		PCS;		/* code */
    int		GCS;		/* code */

    int		UOMLength;	/* code */
    double	UOMLengthInMeters;  /* one UOM = UOMLengthInMeters meters*/

    int		Datum;		/* code */

    int		PM;		/* prime meridian code */
    double	PMLongToGreenwich; /* dec. deg (Long of PM rel.to Green)*/

    int		Ellipsoid;
    double	SemiMajor;	/* in meters */
    double	SemiMinor;	/* in meters */

    int		ProjCode;	/* ProjectionGeoKey ... eg. Proj_UTM_11S */

    int		Projection;	/* EPSG code from TRF_METHOD */
    int		CTProjection;   /* GeoTIFF CT_* code from geo_ctrans.inc
                                   eg. CT_TransverseMercator */

    int		nParms;
    double	ProjParm[MAX_GTIF_PROJPARMS];
    int		ProjParmId[MAX_GTIF_PROJPARMS]; /* geokey identifier,
                                                   eg. ProjFalseEastingGeoKey*/

} GTIFDefn;

int GTIFGetPCSInfo( int nPCSCode, char **ppszEPSGName,
                    int *pnUOMLengthCode, int *pnUOMAngleCode,
                    int *pnGeogCS, int *pnProjectionCSCode );
int GTIFGetProjTRFInfo( int nProjTRFCode,
                        char ** ppszProjTRFName,
                        int * pnProjMethod,
                        double * padfProjParms );
int GTIFGetGCSInfo( int nGCSCode, char **ppszName, int * pnDatum, int * pnPM );
int GTIFGetDatumInfo( int nDatumCode, char **ppszName, int * pnEllipsoid );
int GTIFGetEllipsoidInfo( int nEllipsoid, char ** ppszName,
                          double * pdfSemiMajor, double * pdfSemiMinor );
int GTIFGetPMInfo( int nPM, char **ppszName, double * pdfLongToGreenwich );

double GTIFAngleStringToDD( const char *pszAngle, int nUOMAngle );
int GTIFGetUOMLengthInfo( int nUOMLengthCode,
                          char **ppszUOMName,
                          double * pdfInMeters );

int GTIFGetDefn( GTIF *, GTIFDefn * );
void GTIFPrintDefn( GTIFDefn *, FILE * );
void GTIFFreeDefn( GTIF * );

char * GTIFGetProj4Defn( GTIFDefn * );

void SetCSVFilenameHook( const char *(*)(const char *) );

#ifdef __cplusplus
}
#endif
    
