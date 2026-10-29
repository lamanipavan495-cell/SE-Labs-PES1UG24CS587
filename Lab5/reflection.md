# Lab 5: Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The Flake8 issues were the easiest. Each one (E203, E231, E261, E302) pointed at an exact line and column, and
the fix was a single space or blank line with no effect on behaviour. Most Pylint messages were also simple once
I understood them: adding docstrings and renaming camelCase names to snake_case was mechanical, although the
renames had to be applied to every call site so the program kept working.

The hardest was the Bandit B605 shell-injection warning in `publishTable`. Swapping `os.system` for
`subprocess.run` with a list was only the first step: Bandit then reported B404 and B603, and I still had to
think about scp option injection (a server name starting with `-`). I added input validation, a `--` separator
and a full path to `scp`, then decided the remaining notices were acceptable and suppressed them with specific
`# nosec` IDs. That needed judgement, not just following the tool's message.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Partly. B105 (hardcoded password) and B311 (`random` is not cryptographically secure) are flagged on pattern
alone. In this demo `REFEREE_PASSWORD` is never used, and a coin toss in a demo script is not a security
feature, so their real risk here is low. I still fixed them because the fixes are cheap and match good practice.

The clearer false positives were B404 and B603, raised *after* my fix. Bandit flags every `subprocess` import and
call regardless of how safely it is used, so once the code used an argument list, no shell and validated input,
these warnings no longer described a real problem. I documented and suppressed them rather than removing a
legitimate feature.

## 3. How would you integrate static analysis tools into your actual software development workflow?

- **Locally, before each commit:** a `pre-commit` hook running Flake8 (and optionally an auto-formatter such as
  Black) so style issues never reach the repository.
- **In the editor:** Pylint/Flake8 integration so problems are shown while typing.
- **In CI (e.g. GitHub Actions) on every push and pull request:** run all three tools and fail the build on any
  Flake8 error, any Bandit Medium/High finding, or a Pylint score below a threshold such as 9.5.
- **Shared configuration** (`.pylintrc`, `setup.cfg`/`.flake8`, `.bandit`) committed to the repo so everyone and
  the CI server use the same rules, with any suppressions reviewed in code review.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Security:** the High-severity command injection and the Medium-severity temp-file race are gone; Bandit went
  from 4 issues to none, and the secret is no longer in source control.
- **Robustness:** the mutable default bug (all teams sharing one `players` list) is fixed, `is_top_two` no longer
  crashes with fewer than two teams, `record_match` no longer leaves half-updated stats for an unknown team, and
  the module can be imported for testing without running the demo.
- **Readability and maintainability:** consistent snake_case names, docstrings on every function and simpler
  control flow. Pylint went from 4.75/10 to 10.00/10 and Flake8 reports nothing.
- **Behaviour preserved:** the league table output is identical to the original run.
