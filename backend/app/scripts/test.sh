#!/usr/bin/env bash

set -e
set -x
export APP_ENV="test"
pytest --cov=app --cov-report=term-missing app/tests "${@}"
