# Git Branching Strategies

Git branching strategies define how teams organize their work with branches. Choosing the right strategy depends on team size, release cadence, and deployment model.

## Feature Branches

The most fundamental pattern: create a new branch for each feature or bug fix, work on it in isolation, then merge it back to the main branch. This keeps the main branch stable and allows parallel development. Feature branches should be short-lived to minimize merge conflicts.

## GitHub Flow

GitHub Flow is a lightweight branching model designed for continuous deployment. The rules are simple: create a feature branch from `main`, make commits, open a pull request for code review, and merge back to `main` after approval. The `main` branch is always deployable. There are no separate release or develop branches. This simplicity makes it well-suited for teams that deploy frequently and want minimal process overhead.

## Git Flow

Git Flow uses two long-lived branches: `main` (production-ready code) and `develop` (integration branch for the next release). Feature branches are created from `develop`, and when a release is ready, a `release` branch is created from `develop` for final testing before merging to both `main` and `develop`. Hotfix branches are created from `main` for urgent production fixes. Git Flow is more structured but adds complexity and is best for projects with scheduled releases.

## Merge vs Rebase

**Merge** creates a merge commit that preserves the full branch history. It is non-destructive and safe for shared branches. Use merge for pull requests and when you want a clear record of when branches were integrated.

**Rebase** replays commits from one branch onto another, creating a linear history. Use rebase to keep a feature branch up to date with `main` before merging. This results in a cleaner, easier-to-read commit log. Never rebase commits that have been pushed to a shared branch, as it rewrites history and can cause conflicts for other developers.

## Trunk-Based Development

In trunk-based development, all developers commit directly to `main` (the trunk) or use very short-lived branches (less than a day). This approach requires strong CI/CD pipelines and feature flags to manage incomplete features. It minimizes merge conflicts and encourages small, frequent commits.
