#include <windows.h>
#include <sql.h>
#include <sqlext.h>

#include "sqlcolumn.h"

CSQLColumn::CSQLColumn()
{
   m_nCol=0;
   m_nType=SQL_C_DEFAULT;
   m_svValue="";
}

CSQLColumn::~CSQLColumn()
{
}

