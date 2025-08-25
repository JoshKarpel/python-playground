#!/usr/bin/env just --justfile

default: main

watch cmd:
    uvx watchfiles --verbosity warning 'just {{cmd}}' main.py

main:
    uv run python main.py
