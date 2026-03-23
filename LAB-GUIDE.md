# GitHub Actions Basics Lab - Hands-On Guide

## What You'll Learn

By completing this lab, you will understand:
- How GitHub Actions workflows are structured (name, on, jobs, steps)
- How to trigger workflows on push, schedule, and multiple events
- How to read workflow logs in the GitHub UI
- How cron expressions work for scheduled automation
- How to use conditional logic based on event types
- How path filters control when workflows run

---

## Prerequisites

- **GitHub account** with a repository you can push to
- **Git** installed and configured (`git --version`)
- **Python 3.12+** installed (`python --version`)
- **VS Code** (recommended) or any text editor
- **Estimated time:** 2 hours

```bash
# Verify your setup
git --version
python --version       # or python3 --version
pip --version          # or pip3 --version
```

---

## Project Structure

```
lab-actions-basics/
│
├── app/                              THE APPLICATION
│   ├── __init__.py
│   ├── greeter.py                    Core business logic (greeting functions)
│   └── api.py                        Flask REST API (endpoints)
│
├── tests/                            THE TESTS
│   ├── unit/
│   │   └── test_greeter.py           Unit tests (test functions directly)
│   └── integration/
│       └── test_api.py               Integration tests (test API endpoints)
│
├── .github/workflows/                GITHUB ACTIONS WORKFLOWS
│   ├── lab1-hello-world.yml          Lab 1: Basic push-triggered workflow
│   ├── lab2-scheduled.yml            Lab 2: Cron-scheduled workflow
│   └── lab3-multi-trigger.yml        Lab 3: Multiple event triggers
│
├── scripts/                          LOCAL PIPELINE RUNNERS
│   ├── run-pipeline.sh               Local pipeline (Linux/WSL/Mac)
│   └── run-pipeline.bat              Local pipeline (Windows CMD)
│
├── Dockerfile                        Container for deployment
├── requirements.txt                  Python dependencies
├── pytest.ini                        Test configuration
├── .gitignore                        Files to exclude from git
└── LAB-GUIDE.md                      This file!
```

---

## How to Run Locally

Before pushing to GitHub, you can run all checks locally:

**On Windows CMD:**
```cmd
cd path\to\lab-actions-basics
scripts\run-pipeline.bat
```

**On WSL/Git Bash/Linux/Mac:**
```bash
cd path/to/lab-actions-basics
chmod +x scripts/run-pipeline.sh
./scripts/run-pipeline.sh
```

**Or run tests directly:**
```bash
# Install dependencies first
pip install -r requirements.txt

# Run unit tests only
python -m pytest tests/unit/ -v

# Run integration tests only
python -m pytest tests/integration/ -v

# Run ALL tests
python -m pytest -v
```

**Run the API server:**
```bash
python -m app.api
# Then open: http://127.0.0.1:5000/health
```

---

## Lab 1: Hello World Pipeline (30-45 min)

### Objective

Understand the basic structure of a GitHub Actions workflow: `name`, `on`, `jobs`, `runs-on`, and `steps`.

### Background

**What is a GitHub Actions workflow?**

A workflow is an automated process defined in a YAML file. When an event occurs (like pushing code), GitHub reads the workflow file and executes the steps on a cloud virtual machine called a "runner."

**Where do workflow files live?**

ALL workflow files MUST be in the `.github/workflows/` directory in your repository. GitHub only looks there. If you put a workflow file anywhere else, it will be ignored.

**What is YAML?**

YAML is a human-readable data format (like JSON but cleaner). Key rules:
- Indentation matters (use spaces, NEVER tabs)
- Key-value pairs use `key: value`
- Lists use `- item`
- Comments start with `#`

**Workflow structure:**
```yaml
name: "Display name"       # Shows in the Actions tab

on: push                   # WHEN to run (the trigger)

jobs:                       # WHAT to do
  my-job:                   #   Job name (your choice)
    runs-on: ubuntu-latest  #   WHERE to run (which VM)
    steps:                  #   Individual commands
      - name: "Step 1"
        run: echo "Hello"
```

### Instructions

**Step 1: Read the workflow file**

Open `.github/workflows/lab1-hello-world.yml` in your editor. Read through it carefully. Notice:
- The `name:` field (what appears in the Actions tab)
- The `on: push` trigger (runs when code is pushed)
- Two jobs: `say-hello` and `parallel-job`
- Each job has its own `runs-on: ubuntu-latest` (separate VMs!)
- The `steps:` contain the actual commands

**Step 2: Create a GitHub repository and push**

```bash
# Navigate to the lab folder
cd path/to/lab-actions-basics

# Initialize git (if not already done)
git init
git add .
git commit -m "feat: add GitHub Actions basics lab"

# Create a GitHub repo and push
gh repo create actions-basics-lab --public --source=. --push

# OR if you already have a repo:
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

**Step 3: Watch it run in the Actions tab**

1. Go to your repository on GitHub
2. Click the **"Actions"** tab
3. You should see **"Lab 1 - Hello World"** running (or recently completed)
4. Click on it to see the workflow run
5. Click on each job to see the step-by-step logs

**Step 4: Observe the two parallel jobs**

In the workflow visualization:
- `Say Hello to the World` and `Parallel Job - System Check` appear side by side
- They start at approximately the same time
- Each runs on its own Ubuntu VM (notice different hostnames!)
- Neither waits for the other (no `needs:` dependency)

**Step 5: Read the logs carefully**

Click into the `Say Hello to the World` job and expand each step:
- **Hello World**: Your echo message
- **Show Runner Info**: What OS, Python, Node, Git versions are on the runner?
- **Show GitHub Context**: What repository, branch, commit SHA triggered this?

### What to Look For

```
┌─────────────────────────────────────────────┐
│  GitHub Actions UI                          │
│                                             │
│  ┌──────────┐    ┌──────────────────┐       │
│  │ say-hello │    │ parallel-job     │       │
│  │    ✓      │    │       ✓          │       │
│  └──────────┘    └──────────────────┘       │
│                                             │
│  Both jobs show green ✓ checkmarks          │
│  Both run at the same time (parallel)       │
│  Click each to see detailed step logs       │
└─────────────────────────────────────────────┘
```

### Checkpoint Questions

1. **Where must workflow files be stored?**
   → In the `.github/workflows/` directory. GitHub will NOT find them anywhere else.

2. **What does `runs-on: ubuntu-latest` specify?**
   → It tells GitHub to run this job on a fresh Ubuntu Linux virtual machine. Other options include `windows-latest` and `macos-latest`.

3. **Do the two jobs run sequentially or in parallel?**
   → In parallel! Jobs run at the same time unless you add `needs:` to create a dependency. Each job gets its own fresh VM.

4. **What is `${{ github.repository }}`?**
   → It's a GitHub context expression. It accesses metadata about the event. `github.repository` is `owner/repo-name`.

### Break It! (Troubleshooting Practice)

Try each of these changes. Push to GitHub and observe what happens in the Actions tab.

1. **Indent `steps:` wrong** (e.g., add an extra space)
   → The workflow will fail to parse. GitHub shows a YAML syntax error. This is the #1 most common mistake!

2. **Misspell `runs-on` as `run-on`**
   → GitHub will show an error: the job has no runner specified.

3. **Remove the entire `on:` section**
   → GitHub will show an error: the workflow has no trigger. Without `on:`, GitHub doesn't know WHEN to run it.

4. **Use `runs-on: ubuntu-999`**
   → The job will be queued but never start. GitHub can't find a runner matching that label.

**Remember to fix these changes before moving to Lab 2!**

---

## Lab 2: Scheduled Events / Cron (30-40 min)

### Objective

Create time-based workflows using cron expressions and understand `workflow_dispatch` for manual triggering.

### Background

**What is a cron schedule?**

Cron is a time-based job scheduler from Unix. A cron expression defines WHEN a job should run using 5 fields:

```
┌─────────── minute       (0 - 59)
│ ┌───────── hour         (0 - 23)
│ │ ┌─────── day of month (1 - 31)
│ │ │ ┌───── month        (1 - 12)
│ │ │ │ ┌─── day of week  (0 - 6, Sunday = 0)
│ │ │ │ │
* * * * *
```

**Common cron examples:**

| Expression      | Meaning                        |
|-----------------|--------------------------------|
| `*/5 * * * *`   | Every 5 minutes                |
| `0 * * * *`     | Every hour (at minute 0)       |
| `0 0 * * *`     | Every day at midnight          |
| `0 9 * * 1-5`   | Weekdays at 9:00 AM           |
| `0 0 1 * *`     | First day of every month       |
| `30 14 * * 3`   | Wednesday at 2:30 PM          |

**Tool:** Use [crontab.guru](https://crontab.guru) to build and validate cron expressions.

**Important cron notes for GitHub Actions:**

- All cron times are in **UTC** (not your local timezone!)
- Scheduled workflows only run on the **default branch** (usually `main`)
- GitHub may **delay** scheduled runs during high-load periods (up to 15+ minutes)
- The **minimum** interval is every 5 minutes (GitHub throttles faster ones)
- Scheduled workflows may be **disabled** if a repo has no activity for 60 days

**What is workflow_dispatch?**

`workflow_dispatch` allows you to manually trigger a workflow from the GitHub UI. This is extremely useful for:
- Testing scheduled workflows without waiting
- Running maintenance tasks on demand
- Debugging workflow issues

### Instructions

**Step 1: Read the workflow file**

Open `.github/workflows/lab2-scheduled.yml` in your editor. Notice:
- Two triggers: `schedule` (cron) and `workflow_dispatch` (manual)
- The cron expression `*/5 * * * *` (every 5 minutes)
- Steps that check system health and GitHub API rate limits

**Step 2: Push and trigger manually**

```bash
git add .
git commit -m "feat: add scheduled workflow"
git push
```

Then trigger it manually:
1. Go to GitHub > Actions tab
2. Click **"Lab 2 - Scheduled Health Check"** in the left sidebar
3. Click **"Run workflow"** dropdown button (top right)
4. Click the green **"Run workflow"** button
5. Watch it run!

**Step 3: Wait for a scheduled run (or check later)**

The cron is set to every 5 minutes. Come back in 10-15 minutes and check the Actions tab. You should see an automatic run with the trigger shown as "schedule" instead of "workflow_dispatch."

> Note: GitHub may delay the first scheduled run. Be patient!

**Step 4: Compare scheduled vs manual runs**

Click into both runs and compare:
- The **trigger** field: `schedule` vs `workflow_dispatch`
- The **timestamp**: Does the scheduled run match the cron time exactly? (Often it's delayed by a few minutes)
- The **output**: Both runs execute the same steps, but the trigger metadata differs

### Checkpoint Questions

1. **What timezone do GitHub scheduled workflows use?**
   → UTC. Always UTC. If you're in IST (UTC+5:30), a cron set to `0 9 * * *` runs at 2:30 PM IST.

2. **What is the minimum cron interval GitHub allows?**
   → Every 5 minutes (`*/5 * * * *`). GitHub will throttle or skip faster schedules.

3. **Do scheduled workflows run on non-default branches?**
   → No! Scheduled workflows ONLY run on the default branch (usually `main`). If you create a scheduled workflow on a feature branch, it will NOT run.

4. **Why do we include `workflow_dispatch` alongside `schedule`?**
   → So you can test the workflow immediately by clicking "Run workflow" in the UI, instead of waiting for the cron schedule.

### Break It!

1. **Use minute=60 in the cron expression** (e.g., `"60 * * * *"`)
   → GitHub will reject it. Valid minutes are 0-59.

2. **Create the workflow ONLY on a feature branch** (not main)
   → The scheduled trigger will never fire. It only runs on the default branch.

3. **Set two different schedules in one workflow:**
   ```yaml
   schedule:
     - cron: "0 0 * * *"
     - cron: "0 12 * * *"
   ```
   → This actually WORKS! You can have multiple cron schedules. The workflow runs at midnight AND noon UTC.

---

## Lab 3: Multiple Event Triggers (35-45 min)

### Objective

Configure one workflow to respond to push, pull_request, and issues events, using conditional logic to run different jobs for different events.

### Background

**What are GitHub events?**

Every action on GitHub generates an event. Workflows can listen for these events:

| Event            | When it fires                              |
|------------------|--------------------------------------------|
| `push`           | Code is pushed to a branch                 |
| `pull_request`   | A PR is opened, updated, or closed         |
| `issues`         | An issue is opened, edited, or closed      |
| `schedule`       | On a cron schedule (Lab 2)                 |
| `workflow_dispatch` | Manual trigger from UI                  |
| `release`        | A release is published                     |
| `fork`           | The repository is forked                   |

**What is a paths filter?**

The `paths` filter restricts push triggers to only fire when specific files change:

```yaml
on:
  push:
    paths:
      - "app/**"        # Only trigger when files in app/ change
      - "tests/**"      # Or when test files change
```

If you push a change to `README.md`, the workflow will NOT trigger. Only changes to files matching the paths filter will trigger it.

**What are activity types?**

For events like `pull_request` and `issues`, you can specify which activities trigger the workflow:

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened]
```

- `opened`: A new PR is created
- `synchronize`: New commits are pushed to the PR branch
- `reopened`: A previously closed PR is reopened

**What is conditional logic (`if:`)?**

You can use `if:` on jobs or steps to control when they run:

```yaml
jobs:
  my-job:
    if: github.event_name == 'push'    # Only run on push events
```

### Instructions

**Step 1: Read the workflow file**

Open `.github/workflows/lab3-multi-trigger.yml`. Notice:
- Three triggers: `push` (with paths filter), `pull_request`, and `issues`
- Three jobs with different `if:` conditions
- The `identify-trigger` job runs for ALL events
- The `run-tests` job only runs for push/PR
- The `issue-response` job only runs for issues

**Step 2: Push a change to a tracked file**

Edit something in `app/greeter.py` (e.g., change the greeting text) and push:

```bash
# Edit app/greeter.py (change the greeting message)
git add app/greeter.py
git commit -m "feat: update greeting message"
git push
```

Go to Actions tab. You should see:
- `identify-trigger` job ran (shows "push" event details)
- `run-tests` job ran (tests pass)
- `issue-response` job was SKIPPED (not an issue event)

**Step 3: Push a change to an untracked file**

Create a file that is NOT in the paths filter:

```bash
echo "This is a note" > notes.txt
git add notes.txt
git commit -m "docs: add notes"
git push
```

Go to Actions tab. The workflow should NOT have triggered! The paths filter excluded `notes.txt` because it's not in `app/`, `tests/`, or `requirements.txt`.

**Step 4: Create a branch, push, and open a PR**

```bash
git checkout -b feature/test-pr
echo "# test change" >> app/greeter.py
git add app/greeter.py
git commit -m "feat: test PR trigger"
git push -u origin feature/test-pr
```

Now open a Pull Request on GitHub (or use `gh pr create`). Go to Actions tab. You should see:
- `identify-trigger` shows "pull_request" event details
- `run-tests` ran (tests should pass)
- `issue-response` was SKIPPED

Notice how `github.ref` is different for PRs: `refs/pull/NUMBER/merge` instead of `refs/heads/main`.

**Step 5: Open an issue**

Go to your repo on GitHub > Issues tab > "New issue." Give it a title like "Test issue trigger" and submit.

Go to Actions tab. You should see:
- `identify-trigger` shows "issues" event details
- `run-tests` was SKIPPED (no code change to test)
- `issue-response` ran (logs issue details)

**Step 6: Compare context data across all three triggers**

Open each workflow run and compare the `identify-trigger` job logs:

| Field             | Push               | Pull Request           | Issue           |
|-------------------|--------------------|------------------------|-----------------|
| `event_name`      | `push`             | `pull_request`         | `issues`        |
| `ref`             | `refs/heads/main`  | `refs/pull/1/merge`    | `refs/heads/main` |
| `sha`             | commit hash        | merge commit hash      | HEAD of main    |
| Conditional jobs  | run-tests runs     | run-tests runs         | issue-response runs |

### Checkpoint Questions

1. **What does the `paths` filter do?**
   → It restricts the push trigger to only fire when files matching the listed patterns are changed. Changes to files outside those patterns are ignored.

2. **How is `github.ref` different for push vs pull_request?**
   → For push, it's `refs/heads/BRANCH` (e.g., `refs/heads/main`). For pull_request, it's `refs/pull/NUMBER/merge` (e.g., `refs/pull/1/merge`).

3. **What is the purpose of `types: [opened, synchronize]`?**
   → It limits the pull_request trigger to only fire when a PR is first opened or when new commits are pushed to the PR branch. Without `types`, it would fire on many more activities (labeled, assigned, closed, etc.).

### Break It!

1. **Push a change to a file NOT in the paths list** (e.g., `notes.txt`)
   → The workflow does NOT trigger. The paths filter prevents it.

2. **Replace `paths` with `paths-ignore`**
   ```yaml
   push:
     paths-ignore:
       - "*.md"
       - "docs/**"
   ```
   → Now the workflow triggers on ALL pushes EXCEPT changes to `.md` files and docs/. This is the opposite of `paths`.

3. **Use a type that doesn't exist for pull_request** (e.g., `types: [bananas]`)
   → GitHub will accept the workflow but it will never trigger for that type, since `bananas` is not a valid activity type.

---

## Key Takeaways

```
1. WORKFLOW FILES live in .github/workflows/*.yml
   GitHub automatically detects and runs them.

2. TRIGGERS (on:) define WHEN a workflow runs:
   - push:              on code push
   - pull_request:      on PR activity
   - schedule:          on cron schedule (UTC!)
   - workflow_dispatch: manual trigger
   - issues:            on issue activity

3. JOBS run on cloud VMs (runners):
   - ubuntu-latest, windows-latest, macos-latest
   - Each job gets a FRESH VM
   - Jobs run in PARALLEL unless you use needs:

4. STEPS are the individual commands within a job:
   - run: executes shell commands
   - uses: runs a pre-built action (e.g., actions/checkout@v4)

5. FILTERS control which events trigger workflows:
   - branches: only specific branches
   - paths: only specific file changes
   - types: only specific activity types

6. CONDITIONALS (if:) control which jobs/steps run:
   - github.event_name == 'push'
   - github.ref == 'refs/heads/main'

7. CRON schedules use UTC and run on default branch only.
   Use crontab.guru to build expressions.
```

---

## Quick Reference

### Common Commands

| Command | Description |
|---------|-------------|
| `python -m pytest -v` | Run all tests with verbose output |
| `python -m pytest tests/unit/ -v` | Run only unit tests |
| `python -m pytest tests/integration/ -v` | Run only integration tests |
| `python -m pytest -k "test_greet"` | Run tests matching a pattern |
| `python -m pytest --durations=5` | Show 5 slowest tests |
| `python -m pytest -x` | Stop on first failure |
| `python -m app.api` | Start the API server locally |
| `scripts\run-pipeline.bat` | Run local pipeline (Windows) |
| `./scripts/run-pipeline.sh` | Run local pipeline (Linux/Mac) |

### Workflow YAML Cheat Sheet

```yaml
# Minimal workflow
name: "My Workflow"
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Hello"

# Push with branch + path filter
on:
  push:
    branches: [main, develop]
    paths: ["src/**", "tests/**"]

# Cron + manual trigger
on:
  schedule:
    - cron: "0 0 * * *"     # midnight UTC daily
  workflow_dispatch:

# Multiple events
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  issues:
    types: [opened]

# Conditional job
jobs:
  deploy:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying!"

# Job dependency
jobs:
  build:
    runs-on: ubuntu-latest
    steps: [...]
  test:
    needs: build          # waits for build to finish
    runs-on: ubuntu-latest
    steps: [...]
```

### GitHub Context Variables

| Variable | Description |
|----------|-------------|
| `github.event_name` | Event that triggered the workflow (push, pull_request, etc.) |
| `github.repository` | Owner/repo name |
| `github.ref` | Branch or tag ref |
| `github.sha` | Commit SHA |
| `github.actor` | User who triggered the workflow |
| `github.run_id` | Unique ID for this workflow run |
| `github.run_number` | Sequential number for this workflow |
| `github.workspace` | Working directory path on the runner |

---

## What's Next?

After completing this lab, you've learned the fundamentals of GitHub Actions:
- Workflow structure and YAML syntax
- Push triggers and parallel jobs
- Cron schedules and manual triggers
- Multiple events with conditional logic

**Next lab:** `lab-workflow-logic` (Phase 2) covers:
- Environment variables and secrets
- Matrix builds (test on multiple OS/Python versions)
- Job dependencies with `needs:`
- Artifacts and caching
- Reusable workflows
