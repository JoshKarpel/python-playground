#!/usr/bin/env just --justfile

default: check

watch cmd:
    uvx watchfiles --verbosity warning 'just {{cmd}}' src/ pyproject.toml justfile

alias w := watch

check:
    uv run mypy

play SUBCOMMAND:
    uv run play {{SUBCOMMAND}}

alias p := play
