#!/bin/bash

rm -rf artifacts
mkdir -p artifacts/gdal  artifacts/postgis artifacts/proj artifacts/libgeotiff
container="projcontainer"
docker run --name $container hobu/proj.4  tail -f /dev/null &

# wait for the container to wake up
sleep 5
docker cp $container:/gdal/gdal/data/ artifacts/gdal
docker cp $container:/gdal/gdal/data/epsg artifacts/proj
docker cp $container:/gdal/gdal/data/spatial_ref_sys.sql artifacts/postgis
docker cp $container:/libgeotiff/csv/ artifacts/libgeotiff
docker kill $container
docker rm projcontainer
