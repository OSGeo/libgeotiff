#ifndef __SQLDIRECT
#define __SQLDIRECT

#include "sqlcolumn.h"

class CSQLDirect {
public:
	CSQLDirect();
	CSQLDirect( const char * );
	~CSQLDirect();

	void Init( void );
	void GetError( const char *& );
	void Close( void );
	int ExecuteSQL( LPCSTR );
	int Connect( LPCSTR );
	int Fetch( void );
        int GetColumnCount();
	int GetColumnID( const char *,const char * );
	int GetColumnType( int );
	const char * GetCol( int );
	const char * GetCol( const char *,const char * = "" );
	const char * GetColumnName( int );

	inline void CSQLDirect::SupressErrors( bool bSupress = true ) { m_bSupressErrors=bSupress; }

private:
	void KillCols( void );
	void AddColumn( int,const char * );
	void DisplayError( void );
	int FindColumn( int );
	CSQLColumn* GetColumn( int );

private:
	unsigned char * m_psvSQL;
	unsigned char * m_psvErrorMsg;
	HENV		m_hEnv;
	HDBC		m_hDBC;
	HSTMT		m_hStmt;
        int             m_nResultColCount;
        
        int             m_nColumn;
        CSQLColumn    **m_papoColArray;
	bool		m_bSupressErrors;
};

#endif // __SQL
