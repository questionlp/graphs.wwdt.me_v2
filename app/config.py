# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""Configuration Loading and Parsing for Wait Wait Graphs Site"""

import json
from typing import Any, Dict
import pytz

from app import utility


def load_config(
    config_file_path: str = "config.json", connection_pool_size: int = 12
) -> Dict[str, Dict[str, Any]]:
    with open(config_file_path, "r") as config_file:
        app_config = json.load(config_file)

    database_config = app_config["database"]
    settings_config = app_config["settings"]

    if "database" in app_config:
        database_config = app_config["database"]

        # Set database connection pooling settings if and only if there
        # is a ``use_pool`` key and it is set to True. Remove the key
        # after parsing through the configuration to prevent issues
        # with mysql.connector.connect()
        if "use_pool" in database_config and database_config["use_pool"]:
            if "pool_name" not in database_config or not database_config["pool_name"]:
                database_config["pool_name"] = "wwdtm_graphs"

            if "pool_size" not in database_config or not database_config["pool_size"]:
                database_config["pool_size"] = connection_pool_size

            if "pool_size" in database_config and database_config["pool_size"] < 8:
                database_config["pool_size"] = 8

            del database_config["use_pool"]
        else:
            if "pool_name" in database_config:
                del database_config["pool_name"]

            if "pool_size" in database_config:
                del database_config["pool_size"]

            if "use_pool" in database_config:
                del database_config["use_pool"]

    if "time_zone" in settings_config and settings_config["time_zone"]:
        time_zone = settings_config["time_zone"]
        time_zone_object, time_zone_string = utility.time_zone_parser(time_zone)

        settings_config["app_time_zone"] = time_zone_object
        settings_config["time_zone"] = time_zone_string
        settings_config["time_zone"] = time_zone_string
    else:
        settings_config["app_time_zone"] = pytz.timezone("UTC")
        settings_config["time_zone"] = "UTC"
        settings_config["time_zone"] = "UTC"

    return {
        "database": database_config,
        "settings": settings_config,
    }
