#include <windows.h>
#include <sql.h>
#include <sqlext.h>
#include "sqldirect.h"
#include <stdio.h>

static void MyTrimRight( char * pszString )

{
   int      i;

   for( i = strlen(pszString)-1; i >= 0 && pszString[i] == ' '; i-- )
      pszString[i] = '\0';
}

CSQLDirect::CSQLDirect()
{ 
	Init();
}

CSQLDirect::CSQLDirect( const char * svConnect )
{
	Init();

	Connect( svConnect );
}

CSQLDirect::~CSQLDirect()
{
	if( m_psvErrorMsg )
		delete m_psvErrorMsg;

	if( m_psvSQL )
		delete m_psvSQL;

	if( m_hStmt!=NULL )
		SQLFreeStmt( m_hStmt, SQL_DROP );

	if( m_hDBC!=NULL ) {
		SQLDisconnect( m_hDBC );
		SQLFreeConnect( m_hDBC );
	}

	if( m_hEnv!=NULL )
		SQLFreeEnv( m_hEnv );

	KillCols();
}

void CSQLDirect::Init( void )
{
	m_psvErrorMsg=0;
	m_psvSQL=0;

	m_psvErrorMsg=new unsigned char[ SQL_MAX_MESSAGE_LENGTH-1 ];

	m_hDBC=NULL;
	m_hEnv=NULL;
	m_hStmt=NULL;
        m_nResultColCount = -1;

	m_bSupressErrors=false;

        m_papoColArray = NULL;
        m_nColumn = 0;
}

int CSQLDirect::ExecuteSQL( LPCSTR svSQL )
{
	if( m_psvSQL )
		delete m_psvSQL;

	if( m_hStmt!=NULL )
		Close();
	
        m_nResultColCount = -1;
	m_psvSQL=new unsigned char[ strlen( svSQL )+1 ];
	strcpy( (char*)m_psvSQL,svSQL );

	int nRet=SQLExecDirect( m_hStmt,m_psvSQL,SQL_NTS );

	if( ( nRet!=SQL_SUCCESS && nRet!=SQL_SUCCESS_WITH_INFO ) && !m_bSupressErrors ) 
		DisplayError();

	return nRet;
}

int CSQLDirect::Connect( LPCSTR svSource )
{
   int nConnect=SQLAllocEnv( &m_hEnv );

   if( nConnect==SQL_SUCCESS ) {
      nConnect=SQLAllocConnect( m_hEnv,&m_hDBC );

      if( nConnect==SQL_SUCCESS ) {
         SQLSetConnectOption( m_hDBC,SQL_LOGIN_TIMEOUT,5 );

         // Connect to the datasource.
         unsigned char *psvSource=new unsigned char[ strlen( svSource )+1 ];
         unsigned char *psvUser=new unsigned char;
         unsigned char *psvPassword=new unsigned char;

         strcpy( (char*)psvSource,svSource );

         nConnect=SQLConnect( m_hDBC,psvSource,SQL_NTS,psvUser,SQL_NTS,psvPassword,SQL_NTS );

         if( nConnect==SQL_SUCCESS || nConnect==SQL_SUCCESS_WITH_INFO ) {
				// Now that the datasource is open, get our SQL statement handle.
            nConnect=SQLAllocStmt( m_hDBC,&m_hStmt );
         }

         delete psvSource;
         delete psvUser;
         delete psvPassword;
      }
      else 
         DisplayError();
   }
   else 
      DisplayError();

   return nConnect;
}

void CSQLDirect::DisplayError( void )
{
	if( !m_bSupressErrors ) {
		const char * svError;
		GetError( svError );

		// We'll get fancier later.
		if( svError != NULL && strlen(svError) > 0 )
                   fprintf( stderr, "%s\n", svError );
	}
}

void CSQLDirect::GetError( const char *& svMsg )
{
	unsigned char* pSqlState=new unsigned char[SQL_MAX_MESSAGE_LENGTH-1];
	SDWORD NativeError;
	SWORD svErrorMsg;

	SQLError( m_hEnv,m_hDBC,m_hStmt,pSqlState,&NativeError,m_psvErrorMsg,
		SQL_MAX_MESSAGE_LENGTH-1,&svErrorMsg );

	delete pSqlState;

	svMsg=(const char *) m_psvErrorMsg;
}

void CSQLDirect::KillCols( void ) 
{
   for( int nItem=0;nItem< m_nColumn; nItem++ ) {
      delete m_papoColArray[nItem];
   }

   if( m_papoColArray )        
      free( m_papoColArray );

   m_papoColArray = NULL;
   m_nColumn = 0;
}

const char * CSQLDirect::GetCol( int nCol )
{
   char * svValue;

   // Due to the nature of the SQL API, repeated calls to the same column will result in a NULL value passed
   // back into svData. We need to keep track of the columns that have been used already and if so, pass back
   // the data stored in our array.
   int nIndex=FindColumn( nCol );

   if( nIndex==-1 ) {
      // Get the column from the SQL cursor.
      char svData[8193];
      SDWORD cbDataLen;

      svData[0] = '\0';
      SQLGetData( m_hStmt,nCol,GetColumnType( nCol ),&svData,8192,&cbDataLen );
      svData[cbDataLen] = '\0';
      svValue=svData;
      MyTrimRight( svValue );

      AddColumn( nCol,svValue );
   }
   else {
      // Get the value from the column array.
      svValue = (char *) GetColumn( nCol )->m_svValue;
   }

   return svValue;
}

int CSQLDirect::GetColumnType( int nCol )
{
	int nType=SQL_C_DEFAULT;

	// Due to the nature of the SQL API, repeated calls to the same column will result in a NULL value passed
	// back into svData. We need to keep track of the columns that have been used already and if so, pass back
	// the data stored in our array.
	int nIndex=FindColumn( nCol );

	if( nIndex==-1 ) {
		// Get the column from the SQL cursor.
		UCHAR svColName[256];
		SWORD swCol,swType,swScale,swNull;
		UDWORD pcbColDef;

		SQLDescribeCol( m_hStmt,nCol,svColName,256,&swCol,&swType,&pcbColDef,&swScale,&swNull );

		nType=(int)swType;
	}
	else {
		// Get the value from the column array.
		nType=GetColumn( nCol )->m_nType;
	}

	switch( nType ) {
	case SQL_LONGVARBINARY:
		nType=SQL_C_DEFAULT;
		break;
	default:
		nType=SQL_C_CHAR;
		break;
	};

	return nType;
}

void CSQLDirect::AddColumn( int nCol,const char * svData )
{
    m_nColumn++;

    m_papoColArray = (CSQLColumn **) 
       realloc(m_papoColArray, sizeof(void*) * m_nColumn );

   m_papoColArray[m_nColumn-1] = new CSQLColumn;
   m_papoColArray[m_nColumn-1]->m_nCol=nCol;
   m_papoColArray[m_nColumn-1]->m_svValue=svData;
}

int CSQLDirect::FindColumn( int nCol )
{
   bool bFound=false;

   for( int nIndex=0;nIndex<m_nColumn;nIndex++ ) {
      CSQLColumn* pCol=m_papoColArray[nIndex];

      if( pCol->m_nCol==nCol ) {
         bFound=true;
         break;
      }
   }

   return ( bFound ) ? nIndex : -1;
}

int CSQLDirect::Fetch( void )
{
   // Start with a fresh batch of columns.
   KillCols();

   // Fetch the next row.
   int nRet=SQLFetch( m_hStmt );

   if( ( nRet!=SQL_SUCCESS && nRet!=SQL_SUCCESS_WITH_INFO ) 
            && !m_bSupressErrors )
      DisplayError();

   return nRet;
}

const char * CSQLDirect::GetColumnName( int nCol )
{
   static UCHAR svColName[256];
   SWORD swCol,swType,swScale,swNull;
   UDWORD pcbColDef;

   SQLDescribeCol( m_hStmt,nCol,svColName,256,&swCol,&swType,&pcbColDef,
                   &swScale,&swNull );

   return (const char *) svColName;
}

int CSQLDirect::GetColumnCount()

{
   if( m_nResultColCount == -1 )
   {
      short nMaxCols=0; 
      SQLNumResultCols(m_hStmt,&nMaxCols); 
      m_nResultColCount = nMaxCols;
   }

   return m_nResultColCount; 
}

int CSQLDirect::GetColumnID( const char * svField,const char * svTable )
{
   UCHAR svColName[256];
   UCHAR ucOwner[256];
   SWORD swCol,swType,swScale,swNull;
   UDWORD pcbColDef;
   SDWORD wColLen;

   int nCol=1;

   // Get the total # of columns in this query.
   SQLColAttributes( m_hStmt,0,SQL_COLUMN_COUNT,ucOwner,256,&swScale,&wColLen );
   int nMaxCols=(int)wColLen;

   while( nCol<=nMaxCols ) {
      int nRet=SQLDescribeCol( m_hStmt,nCol,svColName,256,&swCol,&swType,&pcbColDef,&swScale,&swNull );
      SQLColAttributes( m_hStmt,nCol,SQL_COLUMN_TABLE_NAME,ucOwner,256,&swScale,&wColLen );

      // If we hit this condition, then our field is not in the dataset.
      if( nRet!=SQL_SUCCESS ) {
         nCol=0;
         break;
      }

      char * svName= (char *) svColName;
      char * svOwner= (char *) ucOwner;

      MyTrimRight( svName );
      MyTrimRight( svOwner );

      if( stricmp(svName,svField) == 0 ) {
         if(  svTable != NULL && strlen(svTable) > 0 ) {
            if( stricmp(svOwner,svTable) == 0 )
               break;
            else
               nCol++;
         }
         else
            break;
      }
      else
         nCol++;
   }

   return nCol;
}

const char * CSQLDirect::GetCol( const char * svName, const char * svTable )
{
	return GetCol( GetColumnID( svName,svTable ) );
}

CSQLColumn* CSQLDirect::GetColumn( int nCol )
{
	int nIndex=FindColumn( nCol );

	if( nIndex==-1 )
		return 0;
	
	return m_papoColArray[nIndex];
}

void CSQLDirect::Close( void )
{
	if( m_hStmt!=NULL ) {
		// Free
		SQLFreeStmt( m_hStmt, SQL_DROP );

		KillCols();

		// Allocate again.
		SQLAllocStmt( m_hDBC,&m_hStmt );
	}
}

