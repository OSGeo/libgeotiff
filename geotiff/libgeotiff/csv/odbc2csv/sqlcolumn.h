#ifndef __SQLCOLUMN
#define __SQLCOLUMN

class CSQLColumn {
public:
	CSQLColumn();
	~CSQLColumn();

public:
	const char *m_svValue;
	int	m_nCol;
	int m_nType;
};

#endif //__SQLCOLUMN
