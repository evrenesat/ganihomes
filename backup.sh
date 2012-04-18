#!/bin/bash

cd ~/db_backups
pg_dump -f `date +%y-%m-%d`.backup -Fc cagani
