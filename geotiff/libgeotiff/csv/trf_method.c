#include "defs.h"
datafile_rows_t trf_method_row_1[] = {"COORD_TRF_METHOD_CODE","CTRF_METHOD_EPSG_NAME","CTRF_METHOD_USER_NAME","DESCRIPTION","PARAM_1_NAME","PARAM_2_NAME","PARAM_3_NAME","PARAM_4_NAME","PARAM_5_NAME","PARAM_6_NAME","PARAM_7_NAME","PARAM_8_NAME","PARAM_9_NAME","PARAM_10_NAME","PARAM_11_NAME","PARAM_12_NAME","PARAM_13_NAME","PARAM_14_NAME","PARAM_15_NAME","PARAM_16_NAME","PARAM_17_NAME","PARAM_18_NAME","PARAM_19_NAME","PARAM_20_NAME","PARAM_21_NAME","PARAM_22_NAME","PARAM_23_NAME","PARAM_24_NAME","PARAM_25_NAME","PARAM_26_NAME","PARAM_27_NAME","PARAM_28_NAME","PARAM_29_NAME","PARAM_30_NAME","PARAM_31_NAME","PARAM_32_NAME","PARAM_33_NAME","PARAM_34_NAME","PARAM_35_NAME","PARAM_36_NAME","PARAM_37_NAME","FORMULA","EXAMPLE","REVISION_DATE","INFORMATION_SOURCE","DATA_SOURCE","REMARKS","CHANGE_ID",NULL};
datafile_rows_t trf_method_row_2[] = {"9610","2nd-order Polynomial function","","","Ordinate 1 of source evaluation point","Ordinate 2 of source evaluation point","Ordinate 1 of target evaluation point","Ordinate 2 of target evaluation point","A1","A2 * m","A3 * n","A4 * mm","A5 * mn","A6 * nn","B1","B2 * m","B3 * n","B4 * mm","B5 * mn","B6 * nn","","","","","","","","","","","","","","","","","","","","","","","","1996-09-18 00:00:00","","EPSG","","",NULL};
datafile_rows_t trf_method_row_3[] = {"9611","3rd-order Polynomial function","","","Ordinate 1 of source evaluation point","Ordinate 2 of source evaluation point","Ordinate 1 of target evaluation point","Ordinate 2 of target evaluation point","A1","A2 * m","A3 * n","A4 * mm","A5 * mn","A6 * nn","A7 * mmm","A8 * mmn","A9 * mnn","A10 * nnn","B1","B2 * m","B3 * n","B4 * mm","B5 * mn","B6 * nn","B7 * mmm","B8 * mmn","B9 * mnn","B10 * nnn","","","","","","","","","","","","","","","","1996-09-18 00:00:00","","EPSG","","",NULL};
datafile_rows_t trf_method_row_4[] = {"9612","4th-order Polynomial function","","","Ordinate 1 of source evaluation point","Ordinate 2 of source evaluation point","Ordinate 1 of target evaluation point","Ordinate 2 of target evaluation point","A1","A2 * m","A3 * n","A4 * mm","A5 * mn","A6 * nn","A7 * mmm","A8 * mmn","A9 * mnn","A10 * nnn","A11 * mmmm","A12 * mmmn","A13 * mmnn","A14 * mnnn","A15 * nnnn","B1","B2 * m","B3 * n","B4 * mm","B5 * mn","B6 * nn","B7 * mmm","B8 * mmn","B9 * mnn","B10 * nnn","B11 * mmmm","B12 * mmmn","B13 * mmnn","B14 * mnnn","B15 * nnnn","","","","For TRF_POLYNOMIAL 1000, m=Latitude (degrees) of Source Evaluation Point  - 55, and n=longitude of Source Evaluation Point  (degrees east of Greenwich)","","1996-09-18 00:00:00","","EPSG","","",NULL};
datafile_rows_t trf_method_row_5[] = {"9613","NADCON","","Geodetic transformation operating on geographic coordinate differences by bi-linear interpolation.  Used specifically for some NAD27<->NAD83 transformations in USA.","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","Latitude difference gridded binary file","Longitude difference gridded binary file","","","","1996-09-18 00:00:00","US Coast and geodetic Survey - http://www.ngs.noaa.gov","EPSG","Input expects longitudes to be positive west.","",NULL};
datafile_rows_t trf_method_row_6[] = {"9601","Longitude rotation","","The value of the origin of longitude system 2 in longitude system 1.","Longitude rotation","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","1996-09-18 00:00:00","","EPSG","","",NULL};
datafile_rows_t trf_method_row_7[] = {"9602","Geodetic/geocentric conversions","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","Latitude, P, and Longitude, L, in terms of Geographic Coordinate System (GCS) A may \
be expressed in terms of a geocentric (earth centred) cartesian coordinate system X, Y, Z \
with the Z axis corresponding with the Polar axis positive northwards, the X a","Consider a North Sea point with coordinates derived by GPS satellite in the WGS84 geographical coordinate system with coordinates of:\
\
           latitude    53 deg 48 min 33.82 sec N, \
           longitude 02 deg 07 min 46.38 sec E, \
    and ellipsoid","1996-09-18 00:00:00","\"Transformation from spatial to geographical coordinates\"; B. R. Bowring; Survey Review number 181; July 1976.","EPSG","","97.29",NULL};
datafile_rows_t trf_method_row_8[] = {"9603","Geocentric translations","","","X-axis translation","Y-axis translation","Z-axis translation","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","If  we may assume that the minor axes of the ellipsoids are parallel, then shifts dX, dY, dZ \
in the sense from datum A to datum B may then be applied as\
\
   XB = XA + dX \
   YB = YA + dY\
   ZB = ZA + dZ","Given a three parameter datum shift from WGS84 to ED50 for this North Sea area is given as \
dX = +84.87m, dY = +96.49m, dZ = +116.95m. \
\
The WGS84 geographical coordinates convert to the following GS84 geocentric values using \
the above formulas for X,","1996-09-18 00:00:00","POSC Epicentre 2.2.1","EPSG","","",NULL};
datafile_rows_t trf_method_row_9[] = {"9604","Molodenski","","","X-axis translation","Y-axis translation","Z-axis translation","Semi-major axis length difference","Flattening difference","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","1996-09-18 00:00:00","","EPSG","","",NULL};
datafile_rows_t trf_method_row_10[] = {"9605","Abridged Molodenski","","","X-axis translation","Y-axis translation","Z-axis translation","Semi-major axis length difference","Flattening difference","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","As an alternative to the computation of the new latitude, longitude and height above ellipsoid in discrete steps through geocentric coordinates, the changes in these coordinates may be derived directly by formulas derived by Molodenski. Abridged versions o","","1999-04-22 00:00:00","","EPSG","","99.01",NULL};
datafile_rows_t trf_method_row_11[] = {"9606","Position Vector 7-param. transformation","","","X-axis translation","Y-axis translation","Z-axis translation","X-axis rotation","Y-axis rotation","Z-axis rotation","Scale difference","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","Transformation of coordinates from one geographic coordinate system into another (also known as a \"datum transformation\") is usually carried out as an implicit concatenation of three transformations:\
[geographical to geocentric >> geocentric to geocentric","Input point: \
Coordinate system: WGS72 (geographic 3D)\
  Latitude =   55 deg 00 min 00 sec \
  Longitude =  4 deg 00 min 00 sec \
  Ellipsoidal height =  0 m\
This transforms to cartesian geocentric coords:\
    X = 3 657 660.66 (m)  \
    Y =    255 768","1996-09-18 00:00:00","","EPSG","","98.16",NULL};
datafile_rows_t trf_method_row_12[] = {"9607","Coordinate Frame rotation","","","X-axis translation","Y-axis translation","Z-axis translation","X-axis rotation","Y-axis rotation","Z-axis rotation","Scale difference","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","<<<<<This text is continued from the description of the Position Vector Transformation formula>>>>>\
\
Although being common practice in particularly the European E&P industry Position Vector Transformation sign convention is not universally accepted.  A v","The same example as for the Position Vector Transformation can be calculated, however the following transformation parameters have to be applied to achieve the same input and output in terms of coordinate values:\
\
Transformation parameters Coordinate Fra","1996-09-18 00:00:00","","EPSG","","",NULL};
datafile_rows_t trf_method_row_13[] = {"9608","Similarity transform","","","A1","A2 * m","A3 * n","B1","B2 * m","B3 * n","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","1996-09-18 00:00:00","","EPSG","","",NULL};
datafile_rows_t trf_method_row_14[] = {"9609","2-dimensional Affine transformation","","","A1","A2 * m","A3 * n","B1","B2 * m","B3 * n","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","1996-09-18 00:00:00","","EPSG","","",NULL};
datafile_rows_t trf_method_row_15[] = {"9614","NTv1","","Geodetic transformation operating on geographic coordinate differences by bi-linear interpolation.  Used specifically for some NAD27<->NAD83 transformations in Canada.","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","Latitude and longitude difference file","","","","","1997-11-13 00:00:00","Geomatics Canada - Geodetic Survey Division.","EPSG","Superceded in 1997 by NTv2 (transformation method code 9615).   Input expects longitudes to be positive west.","",NULL};
datafile_rows_t trf_method_row_16[] = {"9615","NTv2","","Geodetic transformation operating on geographic coordinate differences by bi-linear interpolation.","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","Latitude and longitude difference file","","","","","1997-11-13 00:00:00","www.geod.emr.ca/html-public/GSDapps/English/NTv2_Fact_Sheet.html","EPSG","Supercedes  NTv1 (transformation method code 9614).  Input expects longitudes to be positive west.","",NULL};
datafile_rows_t trf_method_row_17[] = {"9616","Vertical Offset","","The value of the origin of vertical coordinate system 2 in vertical coordinate system 1.","Vertical offset","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","V2 = [(V1 * U1) - (O12 * Uoff)] * (m / U2) where V2 = value in second vertical coordinate system; V1 = value in first system; O12 is the value of the the origin of system 2 in system 1; m is unit direction multiplier (m=1if both systems are height or both ","","1997-11-13 00:00:00","","EPSG","","",NULL};
datafile_rows_t trf_method_row_18[] = {"9617","Madrid to ED50","","","","","","","A","B","C","D","E","F","G","H","J","","","","","","","","","","","","","","","","","","","","","","","","","The original geographic coordinate system for the Spanish mainland was based on Madrid 1870 datum, Struve 1860 ellipsoid, with longitudes related to the Madrid meridian.  Three polynomial expressions have been empirically derived by El Servicio Geográfico ","Input point coordinate system: Madrid 1870 (Madrid) (geographic 3D)\
   Latitude =   42 deg 38 min 52.77 sec N = 42.647992 degrees\
   Longitude =  3 deg 39 min 34.57 sec E of Madrid = +3.659603 degrees from the Madrid meridian.\
   Height =  0 m\
\
For th","1999-04-22 00:00:00","Institut de Geomatica; Barcelona","EPSG","","99.284",NULL};
datafile_rows_t trf_method_row_19[] = {"9618","Geographical and Height Offsets","","The value of the origin of geographical coordinate system 2 in geographical coordinate system 1.  Lat2 = Lat1 + dLat;  Lon2 = Lon1 + dLon; EllipsoidHeight2 = GravityHeight1 + dHeight.","Latitude offset","Longitude offset","Gravity-related to ellipsoid height","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","1998-12-12 00:00:00","","EPSG","","",NULL};
datafile_rows_t trf_method_row_20[] = {"9619","Geographical Offsets","","The value of the origin of geographical coordinate system 2 in geographical coordinate system 1.  Lat2 = Lat1 + dLat;  Lon2 = Lon1 + dLon.","Latitude offset","Longitude offset","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","1999-04-22 00:00:00","","EPSG","","",NULL};
datafile_rows_t trf_method_row_21[] = {"9620","Norway Offshore Interpolation","","","","","","","","Geod. tfm. code for northern boundary","Geod. tfm. code for southern boundary","","","","","","","","","","","","","","","","","","","","","","","","","","","","Geod. tfm. name for northern boundary","Geod. tfm. name for southern boundary","","","","1999-04-22 00:00:00","Norwegian Mapping Authority note of 13-Feb-1991 \"Om Transformasjon mellom Geodetiske Datum i Norge\".","EPSG","","",NULL};
datafile_rows_t trf_method_row_22[] = {"9801","Lambert Conic Conformal (1SP)","","","Latitude of natural origin","Longitude of natural origin","","","Scale factor at natural origin","False easting","False northing","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","Lambert Conic Conformal\
\
Conical projections with one standard parallel are normally considered to maintain the nominal map scale along the parallel of latitude which is the line of contact between the imagined cone and the ellipsoid. For a one standard ","For Projected Coordinate System JAD69 / Jamaica National Grid\
\
Parameters:\
Ellipsoid:  Clarke 1866, a = 6378206.400 m., 1/f = 294.97870\
                                   then  e = 0.08227185 and e^2 = 0.00676866\
\
Latitude Natural Origin         18 d","1996-09-18 00:00:00","POSC Epicentre 1.4.1","EPSG","","",NULL};
datafile_rows_t trf_method_row_23[] = {"9802","Lambert Conic Conformal (2SP)","","","Latitude of false origin","Longitude of false origin","Latitude of 1st standard parallel","Latitude of 2nd standard parallel","","Easting at false origin","Northing at false origin","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","Lambert Conic Conformal\
		\
Conical projections with one standard parallel are normally considered to maintain the \
nominal map scale along the parallel of latitude which is the line of contact between the \
imagined cone and the ellipsoid. For a one sta","For Projected Coordinate System NAD27 / Texas South Central\
\
Parameters:\
Ellipsoid  Clarke 1866, a = 6378206.400 metres = 20925832.16 US survey feet\
                                   1/f = 294.97870\
then e = 0.08227185 and e^2 = 0.00676866\
\
First S","1999-04-22 00:00:00","POSC Epicentre 1.4.1","EPSG","","99.281",NULL};
datafile_rows_t trf_method_row_24[] = {"9803","Lambert Conic Conformal (2SP Belgium)","","","Latitude of false origin","Longitude of false origin","Latitude of 1st standard parallel","Latitude of 2nd standard parallel","","Easting at false origin","Northing at false origin","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","Since 1972 a modified form of the two standard parallel case has been used in Belgium.  \
For the Lambert Conic Conformal (2 SP Belgium), the formulas for the standard two \
standard parallel case given above are used except for: \
	Easting, E = EF + r sin","For Projected Coordinate System Belge l972 / Belge Lambert 72\
\
Parameters:\
Ellipsoid  International 1924,  a = 6378388 metres\
                                              1/f = 297\
then e = 0.08199189 and e^2 = 0.006722670\
\
First Standard Parallel ","1999-04-22 00:00:00","POSC Epicentre 1.4.1","EPSG","","99.281",NULL};
datafile_rows_t trf_method_row_25[] = {"9804","Mercator (1SP)","","","Latitude of natural origin","Longitude of natural origin","","","Scale factor at natural origin","False easting","False northing","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","Mercator\
	\
The Mercator projection is a special case of the Lambert Conic Conformal projection  \
with the equator as the single standard parallel. All other parallels of latitude are straight \
lines and the meridians are also straight lines at right an","For Projected Coordinate System Makassar / NEIEZ\
\
Parameters:\
Ellipsoid   Bessel 1841  a = 6377397.155 m   1/f = 299.15281\
then e = 0.08169683\
\
Latitude Natural Origin         00o00'00\"N  = 0.0000000 rad\
Longitude Natural Origin    110o00'00\"E  = 1.","1996-09-18 00:00:00","POSC Epicentre 1.4.2","EPSG","","",NULL};
datafile_rows_t trf_method_row_26[] = {"9805","Mercator (2SP)","","","Latitude of 1st standard parallel","Longitude of natural origin","","","","False easting","False northing","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","Mercator\
	\
The Mercator projection is a special case of the Lambert Conic Conformal projection  \
with the equator as the single standard parallel. All other parallels of latitude are straight \
lines and the meridians are also straight lines at right an","For Projected Coordinate System Pulkovo 1942 / Mercator Caspian Sea\
\
Parameters:\
Ellipsoid  Krassowski 1940   a = 6378245.00m   1/f = 298.300\
then e = 0.08181333 and e^2 = 0.00669342\
\
Latitude first SP                             42o00'00\"N = 0.73303","1996-09-18 00:00:00","POSC Epicentre 1.4.2","EPSG","","",NULL};
datafile_rows_t trf_method_row_27[] = {"9806","Cassini-Soldner","","","Latitude of natural origin","Longitude of natural origin","","","","False easting","False northing","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","Cassini-Soldner Formula\
\
The Cassini-Soldner projection is the ellipsoidal version of the Cassini projection for the \
sphere. It is not conformal but as it is relatively simple to construct it was extensively used \
in the last century and is still usef","For Projected Coordinate System Trinidad 1903 / Trinidad Grid \
Parameters:\
Ellipsoid   Clarke 1858     a = 20926348 ft    = 31706587.88 links\
                                        b = 20855233 ft\
\
then 1/f = 294.97870 and e^2 = 0.00676866\
\
Latitud","1996-09-18 00:00:00","POSC Epicentre 1.4.3","EPSG","","",NULL};
datafile_rows_t trf_method_row_28[] = {"9807","Transverse Mercator","","","Latitude of natural origin","Longitude of natural origin","","","Scale factor at natural origin","False easting","False northing","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","Transverse Mercator Formula\
\
The Transverse Mercator projection in its various forms is the most widely used projected \
coordinate system for world topographical and offshore mapping. All versions have the \
same basic characteristics and formulas. The ","For Projected Coordinate System OSGB 1936 / British National Grid\
\
Parameters:\
Ellipsoid  Airy 1830  a = 6377563.396 m  1/f = 299.32496\
then e'^2 = 0.00671534 and e^2 = 0.00667054\
\
Latitude Natural Origin         49o00'00\"N   = 0.85521133 rad\
Longit","1996-09-18 00:00:00","POSC Epicentre 1.4.4","EPSG","","",NULL};
datafile_rows_t trf_method_row_29[] = {"9808","Transverse Mercator (South Orientated)","","","Latitude of natural origin","Longitude of natural origin","","","Scale factor at natural origin","False easting","False northing","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","For the mapping of southern Africa a south oriented Transverse Mercator projection is \
used. Here the coordinate axes are called Westings and Southings and increment to the \
West and South from the origin respectively.  The Transverse Mercator formulas n","","1996-09-18 00:00:00","POSC Epicentre 1.4.4","EPSG","","",NULL};
datafile_rows_t trf_method_row_30[] = {"9809","Oblique Stereographic","","","Latitude of natural origin","Longitude of natural origin","","","Scale factor at natural origin","False easting","False northing","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","Stereographic\
\
The Stereographic projection may be imagined to be a projection of the earth's surface \
onto a plane in contact with the earth at a single tangent point from the opposite end of \
the diameter through that tangent point. \
\
This projecti","For Projected Coordinate System RD / Netherlands New\
\
Parameters:\
Ellipsoid   Bessel 1841    a = 6377397.155 m    1/f = 299.15281\
then e = 0.08169683\
\
Latitude Natural Origin      52o09'22.178\"N  = 0.910296727 rad\
Longitude Natural Origin     5o23'1","1996-09-18 00:00:00","POSC Epicentre 1.4.6","EPSG","","",NULL};
datafile_rows_t trf_method_row_31[] = {"9810","Polar Stereographic","","","Latitude of natural origin","Longitude of natural origin","","","Scale factor at natural origin","False easting","False northing","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","Polar Stereographic Formula\
\
For the forward transformation from latitude and longitude,\
\
	E = FE + * sin (* - *o)\
	N = FN - * cos (* - *o)\
where\
	* = 2 a ko t /{[(1+e)(1+e) (1-e)(1-e)]0.5}\
	t = tan (*/4 - */2) / [(1-esin* ) / (1 + e sin*)]e/2\
\
F","","1996-09-18 00:00:00","US Geological Survey Professional Paper 1395; \"Map Projections - A Working Manual\";  J. Snyder","EPSG","","",NULL};
datafile_rows_t trf_method_row_32[] = {"9811","New Zealand Map Grid","","","Latitude of natural origin","Longitude of natural origin","","","","False easting","False northing","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","1996-09-18 00:00:00","New Zealand Department of Lands technical circular 1973/32","EPSG","","",NULL};
datafile_rows_t trf_method_row_33[] = {"9812","Hotine Oblique Mercator","","","Latitude of projection centre","Longitude of projection centre","Azimuth of initial line","Angle from Rectified to Skew Grid","Scale factor on initial line","False easting","False northing","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","Oblique Mercator\
\
It has been noted that the Transverse Mercator projection is employed for the topographical mapping of longitudinal bands of territories, limiting the amount of scale distortion by limiting the extent of the projection either side of th","For Projected Coordinate System  Timbalai 1948 / R.S.O. Borneo (m)\
\
Parameters:\
	Ellipsoid:  Everest 1830 (1967 Definition)\
				a = 6377298.556 metres 	1/f = 300.8017\
				then	e = 0.081472981	e2 = 0.006637847\
					\
	Latitude Projection Centre	fc  	4","1997-11-13 00:00:00","POSC Epicentre 1.4.5","EPSG","","97.62",NULL};
datafile_rows_t trf_method_row_34[] = {"9813","Laborde Oblique Mercator","","","Latitude of projection centre","Longitude of projection centre","Azimuth of initial line","","Scale factor on initial line","False easting","False northing","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","1996-09-18 00:00:00","\"La nouvelle projection du Service Geographique de Madagascar\"; J. Laborde; 1928","EPSG","Can be accomodated by Oblique Mercator method (code 9815).","97.613",NULL};
datafile_rows_t trf_method_row_35[] = {"9814","Swiss Oblique Cylindrical","","","Latitude of projection centre","Longitude of projection centre","","","","Easting at projection centre","Northing at projection centre","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","1996-09-18 00:00:00","\"Die projecktionen der Schweizerischen Plan und Kartenwerke\"; J Bollinger; 1967","EPSG","Can be accomodated by Oblique Mercator method (code 9815).","97.612",NULL};
datafile_rows_t trf_method_row_36[] = {"9815","Oblique Mercator","","","Latitude of projection centre","Longitude of projection centre","Azimuth of initial line","Angle from Rectified to Skew Grid","Scale factor on initial line","Easting at projection centre","Northing at projection centre","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","1997-07-22 00:00:00","POSC Epicentre 1.4.5","EPSG","","",NULL};
datafile_rows_t trf_method_row_37[] = {"9816","Tunisia Mining Grid","","","Latitude of origin","Longitude of origin","","","","False easting","False northing","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","This grid is used as the basis for mineral leasing in Tunsia.  Lease areas are approximately 2 x 2 km or 400 hectares.  The corners of these blocks are defined through a six figure grid reference where the first three digits are an easting in kilometres an","For grid location 302598,\
Latitude = 36.5964 + [(598 - 360) * A].  As N > 360, A = 0.01005.\
Latitude = 38.97997 grads = 35.08197 degrees.\
\
Longitude  = 7.83445 + [(E - 270) * 0.01285, where E = 302.\
Longitude  = 8.22437 grads east of Paris = 9.73916 d","1998-11-11 00:00:00","POSC Epicentre 1.4.8","EPSG","","",NULL};
datafile_rows_t trf_method_row_38[] = {"9817","Lambert Conic Near-Conformal","","","Latitude of natural origin","Longitude of natural origin","","","Scale factor at natural origin","False easting","False northing","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","1999-04-22 00:00:00","POSC Epicentre 1.4.1","EPSG","","",NULL};
datafile_rows_t trf_method_row_39[] = {"9818","American Polyconic","","","Latitude of natural origin","Longitude of natural origin","","","Scale factor at natural origin","False easting","False northing","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","1999-04-22 00:00:00","POSC Epicentre 1.4.9","EPSG","","",NULL};

datafile_rows_t *trf_method_rows[] = {trf_method_row_1,trf_method_row_2,trf_method_row_3,trf_method_row_4,trf_method_row_5,trf_method_row_6,trf_method_row_7,trf_method_row_8,trf_method_row_9,trf_method_row_10,trf_method_row_11,trf_method_row_12,trf_method_row_13,trf_method_row_14,trf_method_row_15,trf_method_row_16,trf_method_row_17,trf_method_row_18,trf_method_row_19,trf_method_row_20,trf_method_row_21,trf_method_row_22,trf_method_row_23,trf_method_row_24,trf_method_row_25,trf_method_row_26,trf_method_row_27,trf_method_row_28,trf_method_row_29,trf_method_row_30,trf_method_row_31,trf_method_row_32,trf_method_row_33,trf_method_row_34,trf_method_row_35,trf_method_row_36,trf_method_row_37,trf_method_row_38,trf_method_row_39,NULL};
