![Windows CI](https://github.com/OSGeo/libgeotiff/workflows/Windows%20CI/badge.svg)
[![Travis Status](https://travis-ci.org/OSGeo/libgeotiff.svg?branch=master)](https://travis-ci.org/OSGeo/libgeotiff)
[![Appveyor Status](https://ci.appveyor.com/api/projects/status/github/OSGeo/libgeotiff?svg=true)](https://ci.appveyor.com/project/OSGeo/libgeotiff/branch/master)
[![Release Version](https://img.shields.io/github/release/OSGeo/libgeotiff)](https://github.com/OSGeo/libgeotiff/releases)

# libgeotiff

This library is designed to permit the extraction and parsing of the "GeoTIFF" Key directories, as well as definition and installation of GeoTIFF keys in new files. More information about GeoTIFF specifications, projection codes and use can be found [here](https://www.ogc.org/standards/geotiff). Information on the mailing list and archived SVN repository can be found [here](https://trac.osgeo.org/geotiff/)

Archived releases can be found on the [GitHub releases page](https://github.com/OSGeo/libgeotiff/releases) or the [OSGeo archive page](http://download.osgeo.org/geotiff/)

To ask questions and to follow release announcements, subscribe at the [mailing list](https://lists.osgeo.org/mailman/listinfo/geotiff).

You can also report [issues](https://github.com/OSGeo/libgeotiff/issues) (do not use issue tracker for questions)

## Dependencies

[LibTIFF](http://www.simplesystems.org/libtiff/) 

[PROJ](https://github.com/OSGeo/PROJ)

[SQLite3](https://sqlite.org/index.html), as a dependency of PROJ

## Compilation Instructions

`libgeotiff` supports out of tree builds.

### Linux
```
cd libgeotiff
./autogen.sh
./configure
make dist
tar xvzf libgeotiff*.tar.gz
cd libgeotiff*
mkdir build_autoconf
cd build_autoconf
CFLAGS="-Wall -Wextra -Werror" ../configure
make -j3
make check
cd ..
mkdir build_cmake
cd build_cmake
cmake -DCMAKE_C_COMPILER_LAUNCHER=ccache -DCMAKE_C_FLAGS="-Wall -Wextra -Werror" ..
make -j3 
```

### Windows

`libgeotiff` should work with the [Visual Studio toolchain](https://visualstudio.microsoft.com/vs/features/cplusplus/). See [.appveyor.yml](https://github.com/OSGeo/libgeotiff/blob/master/.appveyor.yml) for example.

```
cd libgeotiff
mkdir build && cd build
cmake -G "%VS_FULL%" .. -DBUILD_SHARED_LIBS=ON -DCMAKE_BUILD_TYPE=Release  -DCMAKE_C_FLAGS="/WX" -DCMAKE_CXX_FLAGS="/WX"  -DCMAKE_INSTALL_PREFIX="%BUILD_FOLDER%/install" -DPROJ_INCLUDE_DIR="%BUILD_FOLDER%/install/include" -DPROJ_LIBRARY="%BUILD_FOLDER%/install/lib/proj.lib" -DCMAKE_TOOLCHAIN_FILE=c:/projects/libgeotiff/vcpkg/scripts/buildsystems/vcpkg.cmake

cmake --build . --config Release --target install

```

## Testing

There are two demonstration test programs `makegeo` and `listgeo` that create and list-out the GeoTIFF tags and keys associated with a small TIFF file, as well as a full-featured utility called `geotifcp`. These will all be built in the `bin/` directory as a matter of course, though may require modification if you are not using `LibTIFF`, as they make explicit calls to `LibTIFF` for opening the files and setting the tags. 

To run them simply call:

`./makegeo`

 `./listgeo newgeo.tif`

to generate and list an example GeoTIFF file. To see the `geotifcp` utility in action, first call:

`listgeo newgeo.tif > metadata.txt`

to create a GeoTIFF metadata file `metadata.txt`, and then

`geotifcp -g metadata.txt newgeo.tif newer.tif`

to copy the TIFF file `newgeo.tif` to `newer.tif`, using the GeoTIFF metadata as stored in `metadata.txt`. See `docs/manual.txt` for further uses of geotifcp.

To convert a projection metafile, an ESRI world file, and a raw TIFF file into a GeoTIFF file do something like the following:

`tiffcp -g metadata.txt -e abc.tfw abc.tif geo_abc.tif`

## [License](./libgeotiff/LICENSE)

## Credits

- This library was originally written by Niles Ritter (also the primary author of the GeoTIFF specification).

- Eric Brown of Universal Systems, who contributed a bug fix to `GTIFPCSToImage()`.

- [Safe Software](www.safe.com) who supported by upgrade to use the `EPSG 6.2.2` database for `libgeotiff 1.2.0`.

- Many others who contributed before it occured to me to maintain credits.
