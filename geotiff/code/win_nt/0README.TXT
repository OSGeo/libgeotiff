The following tarred, gziped attachment contains makefiles and
configuration scripts for compiling libtiff, libgeotiff, and the sample
executables with the libraries as DLLs if desired.  This can be posted
on either (or both) of your web pages.  I have no place outside our
firewall to post it.

This does not contain actual libs or DLLs, only the means to generate
them on your machine.

This distribution will compile either as archive libs or as DLLs.  It
supersedes any previous version that I have sent out.

I used .tgz since users have to have tar and gzip for the libtiff and
libgeotiff distributions anyway.  If a PKZIP version is desired, I can
deliver that also.

BTW: If the attachment causes problems, let me know and I'll ftp it
anywhere you want.

(The following info should be included with availability of the file)



  DISCLAIMER:
  No warranty is expressed or implied. I will be available 
  by email at egrissom@ingr.com (ed grissom) for questions, 
  problems or change requests.
 
  This should work on Win95 also (not tested).  It will 
  probably only work for MS Visual C++. I used version 2.2, 
  but any of the 2.x series should work. 4.x will probably 
  work as well, but I have no way of testing.

  Other WinNT/95 compilers have their own quirky syntax.  
  I'll be glad to help translate what I am doing if someone 
  wants, say, a Borland makefile, for instance. 


  To use:
  - gunzip
  - untar to a clean directory
  - Read README.TXT and follow instructions...... 

  ....which include, but are not limited to, ...
  -- run install.bat to copy some files
  -- edit two files
  -- run build.bat (possibly with options)
  -- copy dlls to bin directory or path.
  -- go!



 
--
 ed grissom
 egrissom@ingr.com
