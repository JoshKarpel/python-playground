#!/usr/bin/env just --justfile

default: check

watch cmd:
    uvx watchfiles --verbosity warning 'just {{cmd}}' src/

alias w := watch

check:
    git add -u
    uv run pre-commit run
    git add -u

play SUBCOMMAND:
    uv run play {{SUBCOMMAND}}

alias p := play
