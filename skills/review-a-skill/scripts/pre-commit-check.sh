#!/bin/sh
# Reject commits that touch both skills/*/SKILL.md and skills/review-a-skill/scripts/*
if git diff --cached --name-only | grep -q '^skills/.*/SKILL\.md$' \
   && git diff --cached --name-only | grep -q '^skills/review-a-skill/scripts/'; then
    echo "Validator Independence Rule: commit cannot touch both skill files and validator scripts" >&2
    exit 1
fi
