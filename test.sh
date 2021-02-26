#!/bin/bash

flake8 --max-line-length=119 \
&& mypy --ignore-missing-imports . \
&& pytest
