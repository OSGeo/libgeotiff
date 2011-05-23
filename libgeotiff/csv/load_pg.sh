#!/bin/sh

dropdb epsg
createdb epsg

psql epsg -f EPSG*_Tables_PostgreSQL.sql
psql epsg -f EPSG*_Data_PostgreSQL.sql
