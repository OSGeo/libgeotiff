#include "defs.h"
datafile_rows_t uom_scale_row_1[] = {"UOM_SCALE_CODE","UNIT_OF_MEAS_EPSG_NAME","UNIT_OF_MEAS_USER_NAME","ABBREVIATION","DESCRIPTION","TARGET_UOM_SCALE_CODE","FACTOR_B","FACTOR_C","REVISION_DATE","INFORMATION_SOURCE","DATA_SOURCE","REMARKS","CHANGE_ID",NULL};
datafile_rows_t uom_scale_row_2[] = {"9201","unity","","","","9201","1.0","1.0","1996-09-12 00:00:00","","EPSG","","",NULL};
datafile_rows_t uom_scale_row_3[] = {"9202","parts per million","","ppm","","9201","1.0","1000000.0","1996-09-12 00:00:00","","EPSG","","",NULL};

datafile_rows_t *uom_scale_rows[] = {uom_scale_row_1,uom_scale_row_2,uom_scale_row_3,NULL};
