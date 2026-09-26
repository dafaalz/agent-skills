# Automated pre-commit hooks and staged verification

Runbook for setting up deterministic pre-commit verification gates with Husky v9 and lint-staged.

## 1. Installation and initialization

Install the required dev dependencies and initialize Husky:

```bash
npm install --save-dev husky lint-staged
npx husky init
```

The initialization command creates the `.husky/` directory and sets the `prepare` lifecycle script in `package.json`.

## 2. Configuration for lint-staged

Create `.lintstagedrc.json` in the project root:

```json
{
  "*.{js,jsx,ts,tsx}": [
    "prettier --write",
    "eslint --fix --max-warnings=0",
    "npm test -- --findRelatedTests --passWithNoTests --bail"
  ],
  "*.{json,md,css,scss}": [
    "prettier --write"
  ]
}
```

Rules for staged linters:
1. Always append `--findRelatedTests` to test runners (Jest, Vitest) to execute only tests covering the staged files.
2. Fast completion invariant. Pre-commit hooks must finish in under 5 seconds. If full test suites take longer, move them to pre-push or CI.

## 3. Pre-commit hook configuration

Edit `.husky/pre-commit` to invoke lint-staged:

```bash
#!/usr/bin/env sh
npx lint-staged
```

Ensure the hook script is executable:

```bash
chmod +x .husky/pre-commit
```

## 4. Pre-push type check gate

Do not run heavy whole-project typechecks on pre-commit. Instead, configure a pre-push hook for whole-project safety:

```bash
cat << 'EOF' > .husky/pre-push
#!/usr/bin/env sh
npx tsc --noEmit
EOF
chmod +x .husky/pre-push
```

This split keeps commit cycles instantaneous while blocking broken builds before network push.
