#!/usr/bin/env ash
set -e

config_file="/config/config.yml"

if [[ ! -f $config_file ]]; then
    echo "Error : $config_file not found."
    exit 1
fi

python3 /app/ddns-myaddr.py