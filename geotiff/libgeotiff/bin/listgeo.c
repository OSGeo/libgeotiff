/*
 * listgeo.c -- example client code for LIBGEO geographic
 *     TIFF tag support. Dumps info to GeoTIFF metadata file.
 *
 *  Author: Niles D. Ritter
 *
 */

#include "geotiff.h"
#include "xtiffio.h"
#include <stdio.h>

void main(int argc, char *argv[])
{
	char *fname = (argc==1) ? "newgeo.tif" : argv[1];
	TIFF *tif=(TIFF*)0;  /* TIFF-level descriptor */
	GTIF *gtif=(GTIF*)0; /* GeoKey-level descriptor */

	tif=XTIFFOpen(fname,"r");
	if (!tif) goto failure;
	
	gtif = GTIFNew(tif);
	if (!gtif)
	{
		fprintf(stderr,"failed in GTIFNew\n");
		goto failure;
	}
	
	/* dump the GeoTIFF metadata to std out */

	GTIFPrint(gtif,0,0);
	GTIFFree(gtif);
	XTIFFClose(tif);
	return;
		
failure:
	fprintf(stderr,"failure in listgeo\n");
	if (tif) TIFFClose(tif);
	if (gtif) GTIFFree(gtif);
	return;
}

