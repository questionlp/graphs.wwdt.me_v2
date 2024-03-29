# Copyright (c) 2018-2024 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Show Bluff the Listener Data Retrieval Functions."""
from flask import current_app
from mysql.connector import connect


def build_bluff_data_dict() -> dict:
    """Return a dictionary used to populate Bluff the Listener data."""
    return {
        "Jan": {"correct": 0, "incorrect": 0},
        "Feb": {"correct": 0, "incorrect": 0},
        "Mar": {"correct": 0, "incorrect": 0},
        "Apr": {"correct": 0, "incorrect": 0},
        "May": {"correct": 0, "incorrect": 0},
        "Jun": {"correct": 0, "incorrect": 0},
        "Jul": {"correct": 0, "incorrect": 0},
        "Aug": {"correct": 0, "incorrect": 0},
        "Sep": {"correct": 0, "incorrect": 0},
        "Oct": {"correct": 0, "incorrect": 0},
        "Nov": {"correct": 0, "incorrect": 0},
        "Dec": {"correct": 0, "incorrect": 0},
    }


def build_bluff_data_year_month_dict() -> dict | None:
    """Return a dictionary used to populate Bluff the Listener data."""
    database_connection = connect(**current_app.config["database"])

    # Override session SQL mode value to unset ONLY_FULL_GROUP_BY
    query = (
        "SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,"
        "NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';"
    )
    cursor = database_connection.cursor()
    cursor.execute(query)
    _ = cursor.fetchall()
    cursor.close()

    query = """
        SELECT date_format(s.showdate, '%b %Y') AS date
        FROM ww_shows s
        JOIN ww_showbluffmap blm ON blm.showid = s.showid
        WHERE blm.correctbluffpnlid IS NOT NULL
        OR blm.chosenbluffpnlid IS NOT NULL
        GROUP BY YEAR(s.showdate), MONTH(s.showdate)
        ORDER BY s.showdate ASC;
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    year_month = {}
    for row in result:
        year_month[row.date] = {"correct": 0, "incorrect": 0}

    return year_month


def retrieve_all_bluff_counts() -> dict | None:
    """Retrieve a dictionary containing Bluff the Listener all counts broken down by month."""
    bluff_data = build_bluff_data_year_month_dict()
    database_connection = connect(**current_app.config["database"])

    # Override session SQL mode value to unset ONLY_FULL_GROUP_BY
    query = (
        "SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,"
        "NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';"
    )
    cursor = database_connection.cursor()
    cursor.execute(query)
    _ = cursor.fetchall()
    cursor.close()

    # Retrieve counts where listener contestant chose the
    # correct Bluff story
    query = """
        SELECT date_format(s.showdate, '%b %Y') AS date,
        COUNT(s.showdate) AS correct
        FROM ww_showbluffmap blm
        JOIN ww_shows s ON s.showid = blm.showid
        WHERE s.repeatshowid IS NULL
        AND chosenbluffpnlid IS NOT NULL
        AND correctbluffpnlid IS NOT NULL
        AND ((s.bestof = 0) OR
             (s.bestof = 1 AND s.bestofuniquebluff = 1))
        AND chosenbluffpnlid = correctbluffpnlid
        GROUP BY year(s.showdate), month(s.showdate)
        ORDER BY s.showdate ASC;
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query)
    correct_result = cursor.fetchall()

    # Retrieve counts where listener contestant chose the
    # incorrect Bluff story
    query = """
        SELECT date_format(s.showdate, '%b %Y') AS date,
        COUNT(s.showdate) AS incorrect
        FROM ww_showbluffmap blm
        JOIN ww_shows s ON s.showid = blm.showid
        WHERE s.repeatshowid IS NULL
        AND chosenbluffpnlid IS NOT NULL
        AND correctbluffpnlid IS NOT NULL
        AND ((s.bestof = 0) OR
             (s.bestof = 1 AND s.bestofuniquebluff = 1))
        AND chosenbluffpnlid <> correctbluffpnlid
        GROUP BY year(s.showdate), month(s.showdate)
        ORDER BY s.showdate ASC
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query)
    incorrect_result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not correct_result and not incorrect_result:
        return None

    for row in correct_result:
        bluff_data[row.date]["correct"] = row.correct

    for row in incorrect_result:
        bluff_data[row.date]["incorrect"] = row.incorrect

    return bluff_data


def retrieve_bluff_count_year(year: int) -> dict | None:
    """Retrieve a dictionary containing Bluff the Listener counts broken down by month."""
    bluff_data = build_bluff_data_dict()
    database_connection = connect(**current_app.config["database"])

    # Override session SQL mode value to unset ONLY_FULL_GROUP_BY
    query = (
        "SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,"
        "NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';"
    )
    cursor = database_connection.cursor()
    cursor.execute(query)
    _ = cursor.fetchall()
    cursor.close()

    # Retrieve counts where listener contestant chose the
    # correct Bluff story
    query = """
        SELECT YEAR(s.showdate) as year,
        DATE_FORMAT(s.showdate, '%b') AS month,
        COUNT(s.showdate) AS correct
        FROM ww_showbluffmap blm
        JOIN ww_shows s ON s.showid = blm.showid
        WHERE YEAR(s.showdate) = %s
        AND s.repeatshowid IS NULL
        AND chosenbluffpnlid IS NOT NULL
        AND correctbluffpnlid IS NOT NULL
        AND ((s.bestof = 0) OR
             (s.bestof = 1 AND s.bestofuniquebluff = 1))
        AND chosenbluffpnlid = correctbluffpnlid
        GROUP BY YEAR (s.showdate), MONTH(s.showdate)
        ORDER BY s.showdate ASC;
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query, (year,))
    correct_result = cursor.fetchall()

    # Retrieve counts where listener contestant chose the
    # incorrect Bluff story
    query = """
        SELECT YEAR(s.showdate) as year,
        DATE_FORMAT(s.showdate, '%b') AS month,
        COUNT(s.showdate) AS incorrect
        FROM ww_showbluffmap blm
        JOIN ww_shows s ON s.showid = blm.showid
        WHERE YEAR(s.showdate) = %s
        AND s.repeatshowid IS NULL
        AND chosenbluffpnlid IS NOT NULL
        AND correctbluffpnlid IS NOT NULL
        AND ((s.bestof = 0) OR
             (s.bestof = 1 AND s.bestofuniquebluff = 1))
        AND chosenbluffpnlid <> correctbluffpnlid
        GROUP BY YEAR (s.showdate), MONTH(s.showdate)
        ORDER BY s.showdate ASC;
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query, (year,))
    incorrect_result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not correct_result and not incorrect_result:
        return None

    for row in correct_result:
        bluff_data[row.month]["correct"] = row.correct

    for row in incorrect_result:
        bluff_data[row.month]["incorrect"] = row.incorrect

    return bluff_data
