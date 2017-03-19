"""
This module provides a function that allows me to distinguish
between two modes: development and production (ec2 hosted).
On ec2 I don't have the EDITOR environment variable set.
"""

import os

def development_mode():
    return os.getenv('EDITOR')
