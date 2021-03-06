# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""Testing Main Routes Module and Blueprint Views"""


def test_index(client):
    """Testing main.index"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Wait Wait Don't Tell Me! Graphs" in response.data
    assert b"/panelists/" in response.data
    assert b"/shows/" in response.data


def robots_txt(client):
    """Testing main.robots_txt"""
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert b"Sitemap:" in response.data
    assert b"User-agent:" in response.data
