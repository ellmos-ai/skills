#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thin runtime entry point for the canonical community-outreach core."""

import sys

sys.dont_write_bytecode = True

from outreach_engine import main

if __name__ == "__main__":
    raise SystemExit(main())
