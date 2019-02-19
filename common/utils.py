# -*- coding: utf-8 -*-

"""
Module providing helper functions.
"""


def validate_id(*args):
    """
    Checks if all given id is valid.
    """
    if all(len(mongo_id) == 24 for mongo_id in args):
        return True
    return False
