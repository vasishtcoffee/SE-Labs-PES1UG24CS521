# Lab 5 — Static Code Analysis: Issue Documentation

| Issue | Type | Original line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Mutable default argument | Potential bug | 9 | The default `guests=[]` could cause different events to share a guest list. | Changed the default to `None` and created a separate guest list for each event. |
| Unsafe pickle import | Security — B403 | 2 | Pickle can be unsafe when processing untrusted serialized data. | Replaced pickle persistence with JSON. |
| Unsafe deserialization | Security — B301 | 51 | `pickle.load()` can execute malicious code when reading untrusted data. | Replaced it with `json.load()`. |
| Shell command execution | Security — B605 | 56 | `os.system()` executed a shell command containing an event name. | Removed shell execution and changed the badge helper to display validated file contents. |
| Standard pseudo-random selection | Security — B311 | 72 | The standard `random` module is not designed for security-sensitive random selection. | Replaced `random.choice()` with `secrets.choice()`. |
| Missing documentation and naming issues | Code quality | 1, 9, 15, 27, 32, 39, 44, 49, 54, 59 | Missing docstrings and camelCase names reduced readability and maintainability. | Added docstrings and converted function and parameter names to `snake_case`. |
| Unused sorting argument | Code quality — W0613 | 39 | The guest-report function accepted a sort argument without using it. | Implemented ascending and descending sorting using the argument. |
| Unnecessary `else` after `return` | Code quality — R1705 | 33 | The `else` branch was redundant after a return statement. | Removed the unnecessary `else`. |
| Missing whitespace after comma | Style — E231 | 61 | A comma lacked the required following space. | Added the missing space. |
| Missing operator whitespace | Style — E225 | 66 | An assignment operator lacked surrounding spaces. | Applied standard spacing around the operator. |
| Inline comment spacing | Style — E261 | 75 | The inline comment lacked the required preceding spaces. | Corrected comment spacing. |
| Insufficient blank lines | Style — E305 | 79 | The original file did not contain the required blank lines after a function. | Added the required blank lines. |

## Final Verification

- Initial Pylint score: 4.64/10.
- Final Pylint score: 10.00/10.
- Initial Bandit findings: four.
- Final Bandit findings: zero.
- Initial Flake8 violations: four.
- Final Flake8 violations: zero.
- Program execution: verified after the fixes.
- Three separate tool-specific fix commits: created and pushed to the `lab5-static-analysis` branch.

Line numbers in the table refer to the original version before the fixes.