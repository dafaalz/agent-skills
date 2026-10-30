## Anti-patterns

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| R13-PAD | Periodic padding | abcabc abcabc abcabc | Fails due to padding | Run `lint_skill.py --strict` |
