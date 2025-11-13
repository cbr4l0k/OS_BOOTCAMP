# Git Workflow Guide for Team Members

This guide will help you contribute to the OS_BOOTCAMP project, even if you're new to Git and GitHub.

## Table of Contents
1. [Initial Setup](#initial-setup)
2. [Making Changes](#making-changes)
3. [Creating a Pull Request](#creating-a-pull-request)
4. [Keeping Your Fork Updated](#keeping-your-fork-updated)
5. [Common Git Commands](#common-git-commands)
6. [Troubleshooting](#troubleshooting)

---

## Initial Setup

### 1. Fork the Repository

A **fork** is your personal copy of the project on GitHub.

1. Go to the main repository: `https://github.com/cbr4l0k/OS_BOOTCAMP`
2. Click the **Fork** button in the top-right corner
3. GitHub will create a copy under your account: `https://github.com/YOUR_USERNAME/OS_BOOTCAMP`

### 2. Clone Your Fork

**Clone** means downloading the repository to your computer.

```bash
# Replace YOUR_USERNAME with your GitHub username
git clone https://github.com/YOUR_USERNAME/OS_BOOTCAMP.git

# Navigate into the project folder
cd OS_BOOTCAMP
```

### 3. Set Up Remote Repositories

Add a connection to the original repository (called "upstream") so you can get updates later.

```bash
# Add the original repository as "upstream"
git remote add upstream https://github.com/cbr4l0k/OS_BOOTCAMP.git

# Verify your remotes
git remote -v
```

You should see:
- `origin` → your fork
- `upstream` → the original repository

---

## Making Changes

### 1. Create a New Branch

**Never work directly on the `main` branch.** Always create a new branch for your changes.

```bash
# Make sure you're on main
git checkout main

# Pull latest changes from upstream
git pull upstream main

# Create and switch to a new branch
# Use a descriptive name like: feature/reddit-adapter or fix/typo-in-readme
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Edit the files you're assigned to work on
- Follow the structure and examples in the placeholder files
- Add comments to explain your code

### 3. Check What Changed

```bash
# See which files you modified
git status

# See the actual changes in detail
git diff
```

### 4. Stage and Commit Your Changes

**Staging** means preparing files to be committed.

```bash
# Stage specific files
git add src/adapters/retrieval/reddit_adapter.py

# Or stage all changed files
git add .

# Commit with a clear message
git commit -m "Implement Reddit adapter for retrieving posts"
```

**Good commit messages:**
- ✅ "Implement Reddit adapter for retrieving posts"
- ✅ "Add error handling to SERP adapter"
- ✅ "Fix typo in README"

**Bad commit messages:**
- ❌ "Update"
- ❌ "Changes"
- ❌ "Fixed stuff"

### 5. Push to Your Fork

```bash
# Push your branch to your fork (origin)
git push origin feature/your-feature-name
```

---

## Creating a Pull Request

A **Pull Request (PR)** is how you propose your changes to be merged into the main project.

### 1. Go to GitHub

After pushing, GitHub will show a banner on your fork's page with a **"Compare & pull request"** button. Click it!

Alternatively:
1. Go to the original repository: `https://github.com/cbr4l0k/OS_BOOTCAMP`
2. Click **"Pull requests"** → **"New pull request"**
3. Click **"compare across forks"**
4. Select:
   - **base repository**: `cbr4l0k/OS_BOOTCAMP` **base**: `main`
   - **head repository**: `YOUR_USERNAME/OS_BOOTCAMP` **compare**: `feature/your-feature-name`

### 2. Fill Out the Pull Request

**Title**: Short description of what you did
```
Implement Reddit adapter
```

**Description**: Explain your changes
```markdown
## What I Did
- Implemented the Reddit adapter to retrieve posts from subreddits
- Added error handling for API rate limits
- Added tests for the retrieve method

## How to Test
1. Run `python -m pytest tests/test_reddit_adapter.py`
2. Check that posts are retrieved correctly

## Related Issue
Closes #42
```

### 3. Submit the Pull Request

Click **"Create pull request"** and wait for review!

---

## Keeping Your Fork Updated

The main repository will change as others contribute. Keep your fork up-to-date:

```bash
# Switch to your main branch
git checkout main

# Get latest changes from the original repository
git fetch upstream

# Merge those changes into your main branch
git merge upstream/main

# Push the updates to your fork
git push origin main
```

If you have an active feature branch, update it too:

```bash
# Switch to your feature branch
git checkout feature/your-feature-name

# Merge the latest main into your branch
git merge main

# Fix any conflicts if they appear (see Troubleshooting)
# Then push the updated branch
git push origin feature/your-feature-name
```

---

## Common Git Commands

### Checking Status
```bash
git status              # See what files are modified/staged
git log                 # See commit history
git log --oneline       # See commit history (compact)
git diff                # See unstaged changes
git diff --staged       # See staged changes
```

### Branch Management
```bash
git branch              # List all local branches
git branch -a           # List all branches (including remote)
git checkout main       # Switch to main branch
git checkout -b new-branch  # Create and switch to new branch
git branch -d old-branch    # Delete a local branch
```

### Undoing Changes
```bash
# Discard changes in a specific file (before staging)
git checkout -- filename

# Unstage a file (but keep changes)
git reset filename

# Undo last commit (but keep changes)
git reset --soft HEAD~1

# Discard all local changes (CAREFUL!)
git reset --hard HEAD
```

### Getting Help
```bash
git help                # General help
git help commit         # Help for a specific command
```

---

## Troubleshooting

### "I accidentally committed to main"

```bash
# Move your changes to a new branch
git branch feature/my-changes
git reset --hard upstream/main
git checkout feature/my-changes
```

### "I have merge conflicts"

Merge conflicts happen when the same file was changed in different ways.

1. Git will mark conflicts in your files like this:
```
<<<<<<< HEAD
Your changes
=======
Their changes
>>>>>>> main
```

2. Edit the file to resolve the conflict (remove the markers, keep what you want)
3. Stage the resolved file:
```bash
git add resolved-file.py
```
4. Complete the merge:
```bash
git commit -m "Merge main and resolve conflicts"
```

### "My pull request has conflicts"

Update your branch with the latest changes from main (see "Keeping Your Fork Updated").

### "I pushed to the wrong branch"

```bash
# Create a new branch from the correct point
git checkout -b correct-branch

# Push the new branch
git push origin correct-branch

# Delete the incorrect remote branch
git push origin --delete wrong-branch
```

### "I need to undo my last push"

⚠️ **Only do this if no one else has pulled your changes!**

```bash
# Undo the last commit locally
git reset --hard HEAD~1

# Force push to update the remote
git push --force origin your-branch-name
```

---

## Best Practices

1. **Commit often**: Make small, focused commits rather than one giant commit
2. **Write clear messages**: Future you will thank you!
3. **Pull before you push**: Always get the latest changes before pushing
4. **One feature per branch**: Don't mix multiple unrelated changes in one branch
5. **Test your code**: Make sure it works before creating a pull request
6. **Ask for help**: If you're stuck, ask in the team chat or create a draft PR

---

## Need Help?

- **Git Documentation**: https://git-scm.com/doc
- **GitHub Guides**: https://guides.github.com/
- **Interactive Git Tutorial**: https://learngitbranching.js.org/
- **Team Lead**: Contact @cbr4l0k for project-specific questions

---

**Remember**: Everyone makes mistakes with Git when learning. Don't worry about messing up—that's what forks and branches are for! 🚀
