# Lab 5: Issues Found and Fixed — `tournament_scoreboard.py`

Line numbers refer to the **original** file, before any fixes.

## Results summary

| Tool   | Before                         | After                 |
|--------|--------------------------------|-----------------------|
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | No issues identified |
| Pylint | 4.75/10 (32 messages)          | 10.00/10              |
| Flake8 | 4 issues                       | 0 issues (empty report) |

Program output is unchanged apart from the random coin toss.
Reports are in `reports/before/` and `reports/after/`.

## Issue table (high and medium severity first)

| # | Issue | Type | Tool / Code | Line(s) | Description | Fix Approach |
|---|-------|------|-------------|---------|-------------|--------------|
| 1 | Shell command injection | Security (High) | Bandit B605 | 71 | `os.system("scp table.json " + server + ...)` builds a shell command from a parameter. A value like `host; rm -rf ~` would run extra commands. | Replaced with `subprocess.run([...], check=True)` using an argument list (no shell). Validated `server` with a regex, added `--` so a value starting with `-` can't become an scp option, and resolved scp's full path with `shutil.which`. |
| 2 | Insecure temp file | Security (Medium) | Bandit B306 | 66 | `tempfile.mktemp()` only returns a name; another process can create that file first (race condition, CWE-377). | Used `tempfile.mkstemp()`, which creates the file atomically, then closed the descriptor and returned the path. |
| 3 | Mutable default argument | Bug | Pylint W0102 | 11 | `players=[]` is created once and shared by every team added without a list, so adding a player to one team adds it to all of them. | Default changed to `None`; a new list is created inside the function (and a copy is stored when a list is passed in). |
| 4 | Hardcoded password | Security (Low) | Bandit B105 | 6 | `REFEREE_PASSWORD = "referee-demo"` puts a secret in source code and version control. | Read from the environment: `os.environ.get("REFEREE_PASSWORD")`. |
| 5 | Non-crypto random | Security (Low) | Bandit B311 | 61 | `random.choice` is predictable; a coin toss that decides a match should not be guessable. | Used `secrets.choice`. |
| 6 | Fragile top-two check | Bug / Refactor | Pylint R1714 | 56–58 | `teamName == table[0] or teamName == table[1]` raises `IndexError` when fewer than two teams exist. | `return team_name in league_table()[:2]` — simpler and safe for any table size. |
| 7 | Unnecessary `elif`/`else` after `return` | Refactor | Pylint R1705 | 17–22 | Extra branches after `return` add nesting for no reason. | Replaced with plain `if` statements and a final `return "draw"`. |
| 8 | Naming convention | Convention | Pylint C0103 (×21) | 11–69 | camelCase names (`addTeam`, `teamName`, …) break PEP 8. | Renamed all functions and arguments to snake_case (`add_team`, `team_name`, …) and updated every call. |
| 9 | Missing docstrings | Convention | Pylint C0114, C0116 (×10) | 1, 11–74 | No module or function docstrings. | Added a module docstring and a one-line docstring to every function. |
| 10 | Code runs on import | Bug | Manual review | 92 | `main()` was called at module level, so importing the file (e.g. for tests) ran the demo. | Wrapped in `if __name__ == "__main__":`. |
| 11 | Partial update on bad team name | Bug | Manual review | 25–31 | `recordMatch` with an unknown away team updated the home team's stats before crashing, leaving the table inconsistent. | Check both teams exist before changing anything; raise a clear `KeyError`. |
| 12 | Whitespace before `:` | Style | Flake8 E203 | 5 | `{"win" : 3, ...}` | `{"win": 3, ...}` |
| 13 | Missing blank lines | Style | Flake8 E302 | 60 | Only one blank line before `def tossCoin`. | Added a second blank line. |
| 14 | Missing space after `,` | Style | Flake8 E231 | 79 | `recordMatch(..., 2,1)` | `record_match(..., 2, 1)` |
| 15 | Inline comment spacing | Style | Flake8 E261 | 87 | One space before `# one row per team`. | Two spaces before the inline comment. |

## Notes on the two `# nosec` comments

After fix #1, Bandit raises two Low-severity notices that are inherent to running any external program:
B404 (importing `subprocess`) and B603 (`subprocess` call without shell). Both were reviewed: the call uses a fixed
argument list, no shell, a validated server name and a full path to `scp`. They are suppressed with targeted
`# nosec B404` / `# nosec B603` comments (specific test IDs, not a blanket `# nosec`), with a comment explaining why.

## Commits

1. `Lab 5: add original tournament_scoreboard.py`
2. `before fixes` (baseline reports)
3. `Fix Bandit security issues (B605, B306, B105, B311)`
4. `Fix Pylint issues (score 4.75 -> 10.00)`
5. `Fix Flake8 style issues (E203, E302, E231, E261)`
6. `Add after reports, issue table and reflection`
