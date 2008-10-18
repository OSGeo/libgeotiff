
main.exe:      odbc2csv.obj sqldirect.obj sqlcolumn.obj
	cl odbc2csv.obj sqldirect.obj sqlcolumn.obj odbc32.lib 

sqldirect.obj:	sqldirect.cpp
	cl /c sqldirect.cpp

sqlcolumn.obj:	sqlcolumn.cpp
	cl /c sqlcolumn.cpp

odbc2csv.obj:	odbc2csv.cpp
	cl /c odbc2csv.cpp

