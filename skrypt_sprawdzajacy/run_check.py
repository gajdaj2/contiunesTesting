#!/usr/bin/env python3
"""Tiny runner for skrypt.py to keep invocation simple."""

from __future__ import annotations

import sys

import skrypt


if __name__ == "__main__":
    raise SystemExit(skrypt.main(sys.argv[1:]))

