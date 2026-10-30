## Anti-patterns

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| R13-SEQ | Sequential padding | abcdefghijklmn | Fails due to sequential padding | Run `lint_skill.py --strict` |
