#!/bin/bash

docker run --detach --name ius-db \
-v init_db.sql:/docker-entrypoint-initdb.d/init_db.sql \
-e MARIADB_ROOT_PASSWORD=12345 \
-p 3306:3306\
mariadb:latest
