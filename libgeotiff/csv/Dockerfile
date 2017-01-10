FROM ubuntu:16.04
MAINTAINER Howard Butler <howard@hobu.co>

RUN apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 16126D3A3E5C1192
RUN apt-get update -qq
RUN apt-get -qq remove postgis

RUN apt-get update && apt-get install -y --fix-missing --no-install-recommends \
        build-essential \
        ca-certificates \
        cmake \
        git \
        wget \
        automake \
        libtool \
        subversion \
        python-dev \
        python-numpy \
        python-software-properties \
        clang \
        unzip \
        libtiff5-dev \
        pkgconf \
        postgresql \
        sudo \
        python-pip \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ADD filegdb_api_1_3-64.tar.gz /

RUN cp -r /FileGDB_API/lib/* /usr/lib


RUN git clone --depth=1 https://github.com/OSGeo/gdal.git \
    &&    cd gdal/gdal \
    && CXXFLAGS="-D_GLIBCXX_USE_CXX11_ABI=0" ./configure --prefix=/usr \
            --mandir=/usr/share/man \
            --includedir=/usr/include/gdal \
            --with-threads \
            --with-pg=/usr/bin/pg_config \
            --with-fgdb=/FileGDB_API \
            --with-hide-internal-symbols=yes \
            --with-rename-internal-libtiff-symbols=yes \
            --with-rename-internal-libgeotiff-symbols=yes \
            --with-libtiff=internal \
            --with-geotiff=internal \
    && make -j 4 \
    && make install

RUN cd /gdal/gdal/swig/python \
    && python setup.py build \
    && python setup.py install


RUN mkdir /vdatum \
    && cd /vdatum \
    && wget http://download.osgeo.org/proj/vdatum/usa_geoid2012.zip && unzip -j -u usa_geoid2012.zip -d /usr/share/proj \
    && wget http://download.osgeo.org/proj/vdatum/usa_geoid2009.zip && unzip -j -u usa_geoid2009.zip -d /usr/share/proj \
    && wget http://download.osgeo.org/proj/vdatum/usa_geoid2003.zip && unzip -j -u usa_geoid2003.zip -d /usr/share/proj \
    && wget http://download.osgeo.org/proj/vdatum/usa_geoid1999.zip && unzip -j -u usa_geoid1999.zip -d /usr/share/proj \
    && wget http://download.osgeo.org/proj/vdatum/vertcon/vertconc.gtx && mv vertconc.gtx /usr/share/proj \
    && wget http://download.osgeo.org/proj/vdatum/vertcon/vertcone.gtx && mv vertcone.gtx /usr/share/proj \
    && wget http://download.osgeo.org/proj/vdatum/vertcon/vertconw.gtx && mv vertconw.gtx /usr/share/proj \
    && wget http://download.osgeo.org/proj/vdatum/egm96_15/egm96_15.gtx && mv egm96_15.gtx /usr/share/proj \
    && wget http://download.osgeo.org/proj/vdatum/egm08_25/egm08_25.gtx && mv egm08_25.gtx /usr/share/proj \
    && rm -rf /vdatum
#
RUN git clone --depth=1 https://github.com/OSGeo/proj.4.git \
    &&    cd proj.4 \
    &&    ./autogen.sh \
    && ./configure --prefix=/usr \
            --mandir=/usr/share/man \
    && make -j 4 \
    && make install

RUN svn co https://svn.osgeo.org/metacrs/geotiff/trunk/libgeotiff/  \
    && cd libgeotiff \
    && ./autogen.sh \
    && ./configure --prefix=/usr \
    && make \
    && make install

RUN wget http://www.epsg.org/Portals/0/EPSG%20files/v9-0/epsg-v9_0sql-PostgreSQL.zip -O temp.zip \
    && unzip temp.zip \
    && rm temp.zip

RUN apt-get update && apt-get install -y --fix-missing --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i '1s/^/\\encoding WIN1252\nBEGIN;\n/' EPSG*_Data_PostgreSQL.sql \
    && echo "COMMIT;" | cat EPSG*_Data_PostgreSQL.sql - > EPSG_Data_PostgreSQL.sql.tmp \
    && mv EPSG_Data_PostgreSQL.sql.tmp EPSG*_Data_PostgreSQL.sql \
    && sed -i -- 's/254/300/g' EPSG*_Tables_PostgreSQL.sql

RUN service postgresql start ; \
    sudo -u postgres createuser root -s \
    && createdb -E UTF8 -T template0 epsg \
    && psql epsg -f EPSG*_Tables_PostgreSQL.sql \
    && psql epsg -f EPSG*_Data_PostgreSQL.sql \
    && service postgresql stop

RUN service postgresql start ; \
    sleep 10; \
    cd /libgeotiff/csv \
    && python pg_to_csv.py \
    && mv out/* . \
    && python build_pcs.py \
    && service postgresql stop

RUN service postgresql start ; \
    sleep 10; \
    cd /libgeotiff/csv \
    && chmod +x  /gdal/gdal/swig/python/scripts/epsg_tr.py \
    && python add_esri_column.py \
    && cp *.csv /usr/share/gdal \
    && cp *.csv /gdal/gdal/data \
    && cd /gdal/gdal/data \
    && /gdal/gdal/swig/python/scripts/epsg_tr.py --config OVERRIDE_PROJ_DATUM_WITH_TOWGS84 FALSE -proj4 -skip -list gcs.csv > epsg \
    && /gdal/gdal/swig/python/scripts/epsg_tr.py --config OVERRIDE_PROJ_DATUM_WITH_TOWGS84 FALSE -proj4 -skip -list pcs.csv >> epsg \
    && /gdal/gdal/swig/python/scripts/epsg_tr.py --config OVERRIDE_PROJ_DATUM_WITH_TOWGS84 FALSE -proj4 -skip -list geoccs.csv >> epsg \
    && /gdal/gdal/swig/python/scripts/epsg_tr.py --config OVERRIDE_PROJ_DATUM_WITH_TOWGS84 FALSE -proj4 -skip -list compdcs.csv >> epsg \
    && /gdal/gdal/swig/python/scripts/epsg_tr.py --config OVERRIDE_PROJ_DATUM_WITH_TOWGS84 FALSE -postgis -skip -list gcs.csv > spatial_ref_sys.sql \
    && /gdal/gdal/swig/python/scripts/epsg_tr.py --config OVERRIDE_PROJ_DATUM_WITH_TOWGS84 FALSE -postgis -skip -list pcs.csv >> spatial_ref_sys.sql \
    && /gdal/gdal/swig/python/scripts/epsg_tr.py --config OVERRIDE_PROJ_DATUM_WITH_TOWGS84 FALSE -postgis -skip -list geoccs.csv >> spatial_ref_sys.sql \
    && /gdal/gdal/swig/python/scripts/epsg_tr.py --config OVERRIDE_PROJ_DATUM_WITH_TOWGS84 FALSE -postgis -skip -list compdcs.csv >> spatial_ref_sys.sql \
    && service postgresql stop

#
