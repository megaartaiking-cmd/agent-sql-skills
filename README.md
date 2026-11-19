# agent-sql-skills

> **Agent Skills for SQLite — explore schemas, run queries, and export results to CSV. Offline, stdlib-only Python.**

**1 skill · 1 CLI · 0 dependencies · 100% offline**

[![GitHub stars](https://img.shields.io/github/stars/megaartaiking-cmd/agent-sql-skills?style=social)](https://github.com/megaartaiking-cmd/agent-sql-skills/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](tools/sqltool.py)

AI agents are great at code, but a SQLite database still means opening a database app or writing a one-off script to see what is inside. This repo fixes that gap: a small Agent Skill (SKILL.md) plus a tiny Python CLI that explores schemas, runs queries, and exports results to CSV — in the terminal, on the user's own PC.

Works with Claude Code, Cursor, GitHub Copilot, Codex, Gemini CLI, and any agent that reads SKILL.md files.

## Why this exists

Agent Skills are the fastest-growing category on GitHub — small, composable skill bundles, one job per skill, install in one step. SQLite is the database agents meet most — in apps, in exports, in local data — and there is no small, offline, agent-native way to look inside one or pull data out of it.

This one is:

- **Agent-native** — a skill in the open SKILL.md format, one job, clear rules
- **Offline** — no upload, no cloud, the database never leaves the PC
- **Lightweight** — stdlib-only Python, no pip install, no database server
- **Safe** — queries are read-only by default. Only SELECT and WITH run unless you add `--write`

## Skills

| Skill | What it does | Command |
|---|---|---|
| `sqlite-data` | Explore schema, query, export to CSV | `sqltool.py` |

The skill lives in `skills/sqlite-data/SKILL.md` — copy that folder into your agent's skills folder, or point your agent at this repo.

## Quick start

```sh
git clone https://github.com/megaartaiking-cmd/agent-sql-skills.git
cd agent-sql-skills

# 1. Create the sample database
sqlite3 shop.db < examples/sample.sql

# 2. Explore the schema
python tools/sqltool.py schema shop.db

# 3. Run a query
python tools/sqltool.py query shop.db "SELECT * FROM products LIMIT 5"
```

No installation needed — Python 3.9+ is the only requirement (sqlite3 is only needed to build the sample database).

## Usage

```sh
# List tables, columns, and row counts
python tools/sqltool.py schema shop.db

# Run a read-only query
python tools/sqltool.py query shop.db "SELECT * FROM products LIMIT 5"
python tools/sqltool.py query shop.db "SELECT name, price FROM products WHERE stock > 0"

# Export query results to CSV
python tools/sqltool.py export shop.db "SELECT * FROM products" products.csv
```

Queries are read-only by default. Only SELECT and WITH run unless `--write` is given. See [examples/commands.md](examples/commands.md) for all commands, and [examples/sample.sql](examples/sample.sql) for the sample database.

## How it works

1. You (or your agent) describe the job in plain words: "what tables are in this database?"
2. The skill in `skills/sqlite-data/` tells the agent the exact workflow, the command to run, and the rules — read-only by default, never guess table names.
3. `tools/sqltool.py` (stdlib-only Python) opens the database locally and reports the result.
4. Nothing is uploaded. The work happens on your PC.

## Works with

- Claude Code
- Cursor
- GitHub Copilot
- Codex
- Gemini CLI
- Any agent that reads Agent Skills (SKILL.md)

Copy `skills/sqlite-data/` into your agent's skills directory, or ask your agent to read the SKILL.md file in this repo directly.

## FAQ

**Does it need the internet?**
No. After `git clone`, everything runs offline.

**Does it need a database server?**
No. SQLite is a single file — the tool opens it directly.

**Can it change my data?**
Not by default. Queries are read-only; only SELECT and WITH run. Add `--write` only when you explicitly want to change data.

**What if a query returns no rows?**
The tool says so. It does not invent data.

**Will it run on an old PC?**
Yes — that is the point. It is a small Python script with no dependencies.

**Can I add a skill?**
Yes — copy `skills/sqlite-data/` as a template, write a SKILL.md with a clear name, description, workflow, and rules, and open a pull request.

## Contributing

Issues and pull requests are welcome. Keep skills small, one job per skill, with a tested command in `tools/sqltool.py`. Please do not add dependencies — stdlib only.

## License

MIT — see [LICENSE](LICENSE).

## More Agent Skills

More offline Agent Skills by the same author — one focused skill per repo:

- [agent-audio-skills](https://github.com/megaartaiking-cmd/agent-audio-skills) — Trim podcasts, normalize volume, extract audio from video
- [agent-csv-skills](https://github.com/megaartaiking-cmd/agent-csv-skills) — Clean, filter, summarize CSVs; convert to JSON and Markdown
- [agent-json-skills](https://github.com/megaartaiking-cmd/agent-json-skills) — Validate, format, flatten, query, and diff JSON
- [agent-markdown-skills](https://github.com/megaartaiking-cmd/agent-markdown-skills) — Markdown to HTML, table of contents, link check, word count
- [agent-git-skills](https://github.com/megaartaiking-cmd/agent-git-skills) — Commit messages, changelogs, repo health, branch cleanup
- [agent-text-skills](https://github.com/megaartaiking-cmd/agent-text-skills) — Summarize text, extract keywords, readability, dedupe
- [agent-file-skills](https://github.com/megaartaiking-cmd/agent-file-skills) — Organize folders, find duplicates, batch rename
- [agent-video-skills](https://github.com/megaartaiking-cmd/agent-video-skills) — Edit video offline — trim, make Shorts, add titles, colour-grade
- [LiteCut Pro](https://github.com/megaartaiking-cmd/LIGHT-CUT-VIDEO-EDITOR) — lightweight offline video editor for Windows 10

---

**Keywords:** agent skills, AI agent SQLite, SQLite schema, SQLite query, export to CSV, Claude Code skills, Cursor skills, offline SQLite tool, Python SQLite CLI, database explorer
