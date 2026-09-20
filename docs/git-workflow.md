# Git Workflow

## Branching Strategy

We use a simple branching model:

- **`main`** — production-ready code, always deployable
- **`develop`** — integration branch for next release (optional, for larger projects)
- **`feature/*`** — new features
- **`fix/*`** — bug fixes
- **`docs/*`** — documentation changes
- **`experiment/*`** — trying things out (not for production)

### Branch Naming

```
feature/add-user-auth
fix/fix-login-error
docs/update-api-reference
experiment/test-new-model
```

## Commit Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- `feat` — new feature
- `fix` — bug fix
- `docs` — documentation
- `style` — formatting, no code change
- `refactor` — code restructuring, no feature change
- `test` — adding or updating tests
- `chore` — maintenance tasks
- `perf` — performance improvement

### Examples

```
feat(auth): add JWT authentication
fix(api): handle empty response from LLM
docs(learning): add RAG guide
refactor(services): extract LLM client into separate module
test(auth): add tests for token validation
```

## Pull Request Workflow

### 1. Create a Branch

```bash
git checkout main
git pull
git checkout -b feature/my-new-feature
```

### 2. Make Changes

```bash
# Make your changes
git add .
git commit -m "feat(module): add new feature"
```

### 3. Push and Create PR

```bash
git push -u origin feature/my-new-feature
# Create PR on GitHub
```

### 4. PR Description Template

```markdown
## What

Brief description of the change.

## Why

Why this change is needed.

## How

How the change works.

## Testing

How to test this change.

## Checklist

- [ ] Tests pass
- [ ] Linter passes
- [ ] Type checker passes
- [ ] Documentation updated (if needed)
```

### 5. Code Review

- At least one approval required
- Address all comments
- Squash merge into `main`

## Commit Rules

1. **Atomic commits** — one logical change per commit
2. **Pass CI** — tests and linter must pass before merge
3. **No secrets** — never commit API keys, passwords, or tokens
4. **Descriptive messages** — write commits for future-you

## Stashing

```bash
# Save uncommitted changes
git stash

# List stashes
git stash list

# Apply and remove stash
git stash pop

# Apply without removing
git stash apply
```

## Undoing Changes

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes) — USE WITH CAUTION
git reset --hard HEAD~1

# Revert a committed change (creates new commit)
git revert <commit-hash>
```
