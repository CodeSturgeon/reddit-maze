#!/bin/bash

# Load mini.csv in to dev
appcfg.py upload_data --config_file=tools/loader.py --filename=tools/mini.csv --kind=Tile --url=http://localhost:8080/remote_api .
