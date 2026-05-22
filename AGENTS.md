# AGENTS.md

This file provides guidance to Antigravity (and other agents) when working with code in this repository.

## Status

Pre-implementation. Until source code, a build system, and a test suite land, treat any task here as greenfield — there is nothing existing to conform to. Run `git ls-files` to see the current surface rather than trusting a list here.

## Project intent

**antigravityd** — "Antigravity daemon for delegated repo tasks and reviewable PRs". Hosted under the `agentculture` GitHub org (`github.com/agentculture/antigravityd`), which also owns sibling projects in this workspace:

- `culture` — IRC-based agent mesh (peer-to-peer agent collaboration over a custom async Python IRCd)
- `steward` — align and maintain resident agents across Culture projects
- `agtag` — Agent to Agent communication CLI

## Stack expectations

The project uses Python >=3.12, **uv** for dependency management (`uv venv && uv pip install -e ".[dev]"`, `pytest`), and Hatchling for build-backend.

## Workspace conventions worth preserving

- **Version bumping before PRs.** Sibling projects use a version-bump workflow that updates `pyproject.toml`, `__init__.py`, and `CHANGELOG.md` together; CI enforces it.
- **Online posting signature.** PR descriptions / issue comments authored on the user's behalf should be signed `- antigravityd (Antigravity)` when this repo gains a `culture.yaml`.

## What not to invent

Do not fabricate commands, module layouts, or test invocations in this file or in conversation.
