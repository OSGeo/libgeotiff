/******************************************************************************
 * $Id$
 *
 * Project:  libgeotiff
 * Purpose:  Code to abstract translation between pixel/line and PCS
 *           coordinates.
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
 * Revision 1.6  2001/03/04 22:37:39  warmerda
 * fixed memory leak for fields fetched with gt_methods.get - Alan Gray
 *
 * Revision 1.5  2000/08/22 03:32:46  warmerda
 * removed GTIFTiepointTranslate code
 *
 * Revision 1.4  1999/09/17 01:19:51  warmerda
 * Fixed bug in use of transform matrix.
 *
 * Revision 1.3  1999/09/16 21:25:40  warmerda
 * Added tiepoint, and transformation matrix based translation.  Note
 * that we don't try to invert the transformation matrix for
 * GTIFPCSToImage().
 *
 * Revision 1.2  1999/09/07 20:00:40  warmerda
 * Fixed count/tiepoint_count bug in GTIFPCSToImage().
 *
 * Revision 1.1  1999/05/04 03:07:57  warmerda
 * New
 *
 */
 
#include "geotiff.h"
#include "geo_tiffp.h" /* external TIFF interface */
#include "geo_keyp.h"  /* private interface       */
#include "geokeys.h"

/************************************************************************/
/*                       GTIFTiepointTranslate()                        */
/************************************************************************/

int GTIFTiepointTranslate( int gcp_count, double * gcps_in, double * gcps_out,
                           double x_in, double y_in,
                           double *x_out, double *y_out )

{
    /* I would appreciate a _brief_ block of code for doing second order
       polynomial regression here! */
    return FALSE;
}


/************************************************************************/
/*                           GTIFImageToPCS()                           */
/************************************************************************/

/**
 * Translate a pixel/line coordinate to projection coordinates.
 *
 * @param gtif The handle from GTIFNew() indicating the target file.
 * @param x A pointer to the double containing the pixel offset on input,
 * and into which the easting/longitude will be put on completion.
 * @param y A pointer to the double containing the line offset on input,
 * and into which the northing/latitude will be put on completion.
 *
 * @return TRUE if the transformation succeeds, or FALSE if it fails.  It may
 * fail if the file doesn't have properly setup transformation information,
 * or it is in a form unsupported by this function.
 */

static double *tiepoints   = 0;
static double *pixel_scale = 0;
static double *transform   = 0;

static void cleanup()
{
  if(tiepoints)   { _GTIFFree(tiepoints);    tiepoints   = 0; }
  if(pixel_scale) { _GTIFFree(pixel_scale);  pixel_scale = 0; }
  if(transform)   { _GTIFFree(transform);    transform   = 0; }
}

int GTIFImageToPCS( GTIF *gtif, double *x, double *y )

{
    int     res = FALSE;
    int     tiepoint_count, count, transform_count;
    tiff_t *tif=gtif->gt_tif;

    if (!(gtif->gt_methods.get)(tif, GTIFF_TIEPOINTS,
                              &tiepoint_count, &tiepoints ))
        tiepoint_count = 0;

    if (!(gtif->gt_methods.get)(tif, GTIFF_PIXELSCALE, &count, &pixel_scale ))
        count = 0;

    if (!(gtif->gt_methods.get)(tif, GTIFF_TRANSMATRIX,
                                &transform_count, &transform ))
        transform_count = 0;

/* -------------------------------------------------------------------- */
/*      If the pixelscale count is zero, but we have tiepoints use      */
/*      the tiepoint based approach.                                    */
/* -------------------------------------------------------------------- */

    if( tiepoint_count > 6 && count == 0 ) {

        res = GTIFTiepointTranslate( tiepoint_count / 6,
                                     tiepoints, tiepoints + 3,
                                     *x, *y, x, y );

    } else if( transform_count == 16 ) {
    
/* -------------------------------------------------------------------- */
/*	If we have a transformation matrix, use it. 			*/
/* -------------------------------------------------------------------- */

        double x_in = *x, y_in = *y;

        *x = x_in * transform[0] + y_in * transform[1] + transform[3];
        *y = x_in * transform[4] + y_in * transform[5] + transform[7];
        
        res = TRUE;

    } else if( count < 3 || tiepoint_count < 6 ) {

/* -------------------------------------------------------------------- */
/*      For now we require one tie point, and a valid pixel scale.      */
/* -------------------------------------------------------------------- */

        res = FALSE;

    } else {

        *x = (*x - tiepoints[0]) * pixel_scale[0] + tiepoints[3];
        *y = (*y - tiepoints[1]) * (-1 * pixel_scale[1]) + tiepoints[4];

        res = TRUE;
    }
    cleanup();

    return res;
}

/************************************************************************/
/*                           GTIFPCSToImage()                           */
/************************************************************************/

int GTIFPCSToImage( GTIF *gtif, double *x, double *y )

{
    double 	*tiepoints;
    int 	tiepoint_count, count;
    double	*pixel_scale;
    tiff_t *tif=gtif->gt_tif;

    if (!(gtif->gt_methods.get)(tif, GTIFF_TIEPOINTS,
                              &tiepoint_count, &tiepoints ))
        tiepoint_count = 0;

    if (!(gtif->gt_methods.get)(tif, GTIFF_PIXELSCALE, &count, &pixel_scale ))
        count = 0;

/* -------------------------------------------------------------------- */
/*      If the pixelscale count is zero, but we have tiepoints use      */
/*      the tiepoint based approach.                                    */
/* -------------------------------------------------------------------- */
    if( tiepoint_count > 6 && count == 0 )
    {
        return GTIFTiepointTranslate( tiepoint_count / 6,
                                      tiepoints + 3, tiepoints,
                                      *x, *y, x, y );
    }
    
/* -------------------------------------------------------------------- */
/*      For now we require one tie point, and a valid pixel scale.      */
/* -------------------------------------------------------------------- */
    if( count < 3 || tiepoint_count < 6 )
        return FALSE;

    *x = (*x - tiepoints[3]) / pixel_scale[0] + tiepoints[0];
    *y = (*y - tiepoints[4]) / (-1 * pixel_scale[1]) + tiepoints[1];

    return TRUE;
}

