                   ษอออออออออออออออออออออออออออออออออออป
                   บ     EPSG Geodesy Parameters       บ
                   บ    version 2.1, 2nd June 1995.    บ
                   ศอออออออออออออออออออออออออออออออออออผ       
                          

The European Petroleum Survey Group (EPSG) has compiled and is
distrubuting this set of parameters defining various geodetic
and cartographic coordinate systems to encourage
standardisation across the Exploration and Production segment
of the oil industry.  The data is included as reference data
in the Geotiff data exchange specification, in Iris21 the
Petroconsultants data model, and in Epicentre, the POSC data
model.  Parameters map directly to the POSC Epicentre model
v2.0, except for data item codes which are included in the
files for data management purposes.  Geodetic datum parameters
are embedded within the geographic coordinate system file. 
This has been done to ease parameter maintenance as there is a
high correlation between geodetic datum names and geographic
coordinate system names.  The Projected Coordinate System v2.0
tabulation consists of systems associated with locally used
projections.  Systems utilising the popular UTM grid system
have also been included.

Criteria used for material in these lists include:
  - information must be in the public domain: "private" data   
    is not included.
  - data must be in current use.
  - parameters are given to a precision consistent with
    coordinates being to a precision of one centimetre.

The user assumes the entire risk as to the accuracy and the
use of this data.  The data may be copied and distributed
subject to the following conditions:

     1)   All data must then be copied without modification
and all pages must be included;
          
     2)   All components of this data set must be distributed
together;
          
     3)   The data may not be distributed for profit by any 
third party; and

     4)   Acknowledgement to the original source must be
given.
          
INFORMATION  PROVIDED IN THIS DOCUMENT IS PROVIDED "AS IS"
WITHOUT WARRANTY  OF  ANY  KIND,  EITHER  EXPRESSED OR 
IMPLIED, INCLUDING  BUT  NOT LIMITED TO THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.

Data is distributed on MS-DOS formatted diskette in comma-
separated record format.  Additional copies may be obtained
from Jean-Patrick Girbig at the address below at a cost of
US$100 to cover media and shipping, payment to be made in
favour of Petroconsultants S.A at Union Banque Suisses,
1211 Geneve 11, Switzerland (compte number 403 458 60 K).

The data is to be made available on a bulletin board shortly.


Shipping List
-------------

This data set consists of 8 files:

PROJCS.CSV  Tabulation of Projected Coordinate Systems to     
            which map grid coordinates may be referenced.

GEOGCS.CSV  Tabulation of Geographic Coordinate Systems to    
            which latitude and longitude coordinates may be   
            referenced.  This table includes the equivalent   
            geocentric coordinate systems and also the        
            geodetic datum, reference to which allows latitude
            and longitude or geocentric XYZ to uniquely       
            describe a location on the earth.

VERTCS.CSV  Tabulation of Vertical Coordinate Systems to     
            which heights or depths may be referenced. This
            table is currently in an early form.

PROJ.CSV    Tabulation of transformation methods and          
            parameters through which Projected Coordinate     
            Systems are defined and related to Geographic     
            Coordinate Systems.

ELLIPS.CSV  Tabulation of reference ellipsoids upon which     
            geodetic datums are based.

PMERID.CSV  Tabulation of prime meridians upon which geodetic 
            datums are based.

UNITS.CSV   Tabulation of length units used in Projected and  
            Vertical Coordinate Systems and angle units used  
            in Geographic Coordinate Systems.

README.TXT  This file.




The data files (.CSV) have a heirarchical structure:

ษอออออออออออออออออออออออออออป   ษออออออออออออออออออออออออออออป
บ           VERTCS          บ   บ           PROJCS           บ
วฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤถ   วฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤถ
บVertical Coordinate Systemsบ   บProjected Coordinate Systemsบ
ศอออออออออออออัอออออออออออออผ   ศออออออออออออัอออออออออออออออผ
              ณ                              ณ
     ฺฤฤฤฤฤฤฤฤู                              ณ
     ณ                                       ณ
     ณ            ฺฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤด
     ณ            ณ                          ณ
     ณ            ณ            ษอออออออออออออฯอออออออออออออออป
     ณ            ณ            บ            GEOGCS           บ
     ณ            ณ            วฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤถ
     ณ            ณ            บGeographic Coordinate Systemsบ
     ณ            ณ            บGeocentric Coordinate Systemsบ
     ณ            ณ            วฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤถ
     ณ            ณ            บ       Geodetic Datums       บ
     ณ            ณ            ศอออออออออออออัอออออออออออออออผ
     ณ            ณ                          ณ
     ณ            ณ                 ฺฤฤฤฤฤฤฤฤมฤฤฤฤฤฤฤฟ
     ณ            ณ                 ณ                ณ    
     ณ     ษออออออฯอออออป    ษออออออฯอออออป   ษออออออฯอออออออป
     ณ     บ    PROJ    บ    บ   ELLIPS   บ   บ    PMERID    บ
     ณ     วฤฤฤฤฤฤฤฤฤฤฤฤถ    วฤฤฤฤฤฤฤฤฤฤฤฤถ   วฤฤฤฤฤฤฤฤฤฤฤฤฤฤถ
     ณ     บ Projection บ    บ Ellipsoid  บ   บPrime Meridianบ
     ณ     บ Parameters บ    บ Parameters บ   บ  Parameters  บ
     ณ     ศออออออัอออออผ    ศออออออัอออออผ   ศออออออัอออออออผ
     ณ            ณ                 ณ                ณ
     ภฤฤฤฤฤฤฤฤฤฤฤฤมฤฤฤฤฤฤฤฤฤฤฤยฤฤฤฤฤมฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤู         
                              ณ                          
                ษอออออออออออออฯออออออออออออป
                บ           UNITS          บ
                วฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤฤถ
                บ Linear and Angular Units บ
                ศออออออออออออออออออออออออออผ




The parameter listings are "living documents" and will be
updated by the EPSG from time to time. Any comment or
suggestions for improvements should be directed to:

  Jean-Patrick Girbig,      or   Roger Lott,
  Manager Cartography,           Head of Survey,
  Petroconsultants S.A.,         BP Exploration,
  PO Box 152,                    Uxbridge One,
  24 Chemin de la Marie,         Harefield Road,
  1258 Perly-Geneva,             Uxbridge,
  Switzerland.                   Middlesex UB8 1PD,
                                 England.
                                
                                 Internet:
                                  lottrj@txpcap.hou.xwh.bp.com

Requests for the inclusion of new data should include supporting 
documentation.  Requests for changing existing data should include 
reference to both the name and code of the item.

10th June 1995.
