#!/usr/bin/env bash

set -e

EXIT_STATUS=0
CHECK_FLAG="--check"

args=""

if [[ "${@#-h}" != "$@" || "${@#--help}" != "$@" ]]
then
    echo "Use no flags to run Black formatting on python files."
    echo "Use '--check' flag to lint python files."
    exit 0
fi

[[ "${@#${CHECK_FLAG}}" != "$@" ]] && args=${CHECK_FLAG}

black ${args} $PWD/src || EXIT_STATUS=1

if [[ ${EXIT_STATUS} == 0 ]]; then
    echo "Linting succeeded! Squeaky clean..."
else
    echo "Linting failed."
fi

