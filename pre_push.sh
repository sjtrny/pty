#!/usr/bin/env bash
black  --config pyproject.toml ./
flake8 --exclude=.git,*migrations*,venv,docs
pydocstyle --convention=numpy --add-ignore=D100,D412 pty_expect.py
pytest
