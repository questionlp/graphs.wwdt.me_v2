# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""Error Handlers Module for Wait Wait Graphs Site"""
from flask import render_template


def not_found(error):
    """Handle resource not found conditions"""
    return render_template("errors/404.html", error_description=error.description), 404


def handle_exception(error):
    """Handle exceptions in a slightly more graceful manner"""
    return render_template("errors/500.html"), 500
