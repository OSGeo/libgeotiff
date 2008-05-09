/**********************************************************************
 *
 *  geo_simpletags.h 
 *
 * Provides interface for a "simple tags io in memory" mechanism
 * as an alternative to accessing a real tiff file using libtiff.
 *
 **********************************************************************/

#ifndef __geo_simpletags_h_
#define __geo_simpletags_h_

#include "geotiff.h"
#include "cpl_serv.h"

#if defined(__cplusplus)
extern "C" {
#endif

#define STT_SHORT   1
#define STT_DOUBLE  2
#define STT_ASCII   3

typedef struct {
    int tag;
    int count;
    int type;
    void *data;
} ST_KEY;

typedef struct {
    int key_count;
    ST_KEY *key_list;
} ST_TIFF;

typedef void *STIFF;

void CPL_DLL GTIFSetSimpleTagsMethods(TIFFMethod *method);

int CPL_DLL ST_SetKey( ST_TIFF *, int tag, int count, 
                       int st_type, void *data );
int CPL_DLL ST_GetKey( ST_TIFF *, int tag, int *count, 
                       int *st_type, void **data_ptr );

ST_TIFF CPL_DLL *ST_Create();
void CPL_DLL ST_Destroy( ST_TIFF * );

int CPL_DLL ST_TagType( int tag );

#if defined(__cplusplus)
} 
#endif

#endif /* __geo_simpletags_h_ */
