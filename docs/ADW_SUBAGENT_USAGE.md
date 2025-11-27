# ADW Subagent Usage Guide

This guide explains how to use the new ADW Planning Subagent that replicates the functionality of `adws/adw_plan.py`.

## Overview

The ADW Planning workflow has been converted from a Python script into a **native Claude Code slash command** that can be invoked directly from Claude Code sessions.

### What Changed?

**Before (Python Script):**
```bash
uv run adws/adw_plan.py 123 adw-20231127-abc123
```

**After (Claude Code Slash Command):**
```
/plan_issue 123 adw-20231127-abc123
```

## Files Created

### 1. `.claude/commands/plan_issue.md`
The main slash command that executes the planning workflow. This replaces `adws/adw_plan.py`.

### 2. `.claude/agents/adw-planner.md`
Comprehensive documentation of the planning agent's workflow, tools, and responsibilities.

## How to Use

### Method 1: Direct Slash Command (Recommended)

In any Claude Code session, execute:

```
/plan_issue 123 adw-20231127-abc123
```

Where:
- `123` = GitHub issue number
- `adw-20231127-abc123` = ADW workflow ID

### Method 2: Via Task Tool (For Programmatic Use)

If you need to invoke the planner from another agent or script:

```javascript
Task({
  subagent_type: 'general-purpose',
  prompt: '/plan_issue 123 adw-20231127-abc123',
  model: 'opus'
})
```

### Method 3: Python Integration (Backward Compatible)

You can still call it from Python using the existing agent execution module:

```python
from adws.adw_modules.agent import execute_template
from adws.adw_modules.data_types import AgentTemplateRequest

request = AgentTemplateRequest(
    agent_name="adw_planner",
    slash_command="/plan_issue",
    args=["123", "adw-20231127-abc123"],
    adw_id="adw-20231127-abc123",
)

response = execute_template(request)
print(response.output)
```

## What the Planning Workflow Does

The `/plan_issue` command executes these steps automatically:

1. ✅ **Fetch GitHub Issue** - Gets issue details via `gh issue view`
2. ✅ **Classify Issue** - Determines if it's a chore, bug, or feature
3. ✅ **Generate Branch Name** - Creates standardized branch name
4. ✅ **Create Git Branch** - Checks out new feature branch
5. ✅ **Build Implementation Plan** - Creates detailed plan in `specs/` directory
6. ✅ **Commit Plan** - Commits plan with proper message
7. ✅ **Push and Create PR** - Pushes branch and creates draft PR
8. ✅ **Save State** - Persists workflow state to `agents/<adw_id>/state.json`
9. ✅ **Update GitHub Issue** - Posts status comments throughout workflow

## State Management

The planning workflow saves state to `agents/<adw_id>/state.json`:

```json
{
  "adw_id": "adw-20231127-abc123",
  "issue_number": "123",
  "issue_class": "/feature",
  "branch_name": "feature-issue-123-adw-20231127-abc123-add-user-auth",
  "plan_file": "specs/issue-123-adw-20231127-abc123-sdlc_planner-add-user-auth.md",
  "pr_url": "https://github.com/owner/repo/pull/456",
  "workflow": "adw_plan",
  "status": "completed",
  "completed_at": "2023-11-27T10:30:00Z"
}
```

This state file is used by the **build phase** to continue the workflow.

## Sub-Agents Used

The planning workflow coordinates these sub-agents (each is a slash command):

| Sub-Agent | Slash Command | Purpose |
|-----------|---------------|---------|
| Issue Classifier | `/classify_issue` | Determines issue type (chore/bug/feature) |
| Branch Generator | `/generate_branch_name` | Creates standardized branch name |
| SDLC Planner | `/chore`, `/bug`, `/feature` | Creates detailed implementation plan |
| Commit Generator | `/commit` | Generates formatted commit message |
| PR Creator | `/pull_request` | Creates pull request with description |

## Error Handling

If any step fails:
- Error is logged to `agents/<adw_id>/sdlc_planner/error.log`
- Error comment posted to GitHub issue
- State saved with `status: "failed"`
- Workflow stops and reports failure

Example error in GitHub issue:
```
adw_bot adw-20231127-abc123_ops: Error in Step 5: Failed to create branch: branch already exists
```

## Output Example

When successful, the workflow returns:

```
✅ Planning Phase Complete

Issue: #123
Classification: feature
Branch: feature-issue-123-adw-20231127-abc123-add-user-auth
Plan File: specs/issue-123-adw-20231127-abc123-sdlc_planner-add-user-auth.md
Pull Request: https://github.com/owner/repo/pull/456
Workflow ID: adw-20231127-abc123

Next Steps:
- Review the implementation plan at specs/issue-123-adw-20231127-abc123-sdlc_planner-add-user-auth.md
- Execute the build phase with: /build_issue 123 adw-20231127-abc123
```

## Advantages Over Python Script

### 1. **Native Claude Code Integration**
- No external Python process needed
- Runs directly in Claude Code environment
- Access to all Claude Code tools and permissions

### 2. **Better Error Handling**
- Claude Code's built-in error recovery
- Can ask clarifying questions if needed
- More intelligent failure recovery

### 3. **Easier Debugging**
- Full conversation history visible
- Can inspect intermediate steps
- Better logging and state visibility

### 4. **More Flexible**
- Can adapt to unexpected situations
- Can handle edge cases intelligently
- No need to update Python code for minor changes

### 5. **Unified Tooling**
- All ADW workflows use same tool (Claude Code)
- Consistent user experience
- Easier onboarding for new developers

## Migrating from Python Script

If you have existing workflows using `adw_plan.py`:

### Option 1: Direct Replacement

Replace:
```bash
uv run adws/adw_plan.py $ISSUE_NUMBER $ADW_ID
```

With:
```bash
claude -p "/plan_issue $ISSUE_NUMBER $ADW_ID"
```

### Option 2: Keep Python Wrapper

Keep `adws/adw_plan.py` but have it call the slash command:

```python
# In adw_plan.py
import subprocess

def main():
    issue_number = sys.argv[1]
    adw_id = sys.argv[2]

    # Call the slash command via Claude Code CLI
    result = subprocess.run([
        "claude",
        "-p", f"/plan_issue {issue_number} {adw_id}",
        "--model", "opus"
    ])

    sys.exit(result.returncode)
```

## Prerequisites

The planning workflow requires:

1. **GitHub CLI (`gh`)** - Must be authenticated
   ```bash
   gh auth login
   ```

2. **Git** - Must be in a git repository with GitHub remote
   ```bash
   git remote -v
   ```

3. **Claude Code CLI** - Set in environment
   ```bash
   export CLAUDE_CODE_PATH="claude"
   ```

4. **Permissions** - Ensure `.claude/settings.json` allows:
   - `Bash(git:*)` - Git operations
   - `Bash(gh:*)` - GitHub CLI operations
   - `Write` - Creating files

## Next Steps

### Create Build Subagent

Follow the same pattern to create `/build_issue` command that:
1. Reads the plan from state
2. Implements the plan
3. Runs tests
4. Updates PR

### Create Coordinator Subagent

Create `/adw_coordinator` that orchestrates both planning and building:

```
/adw_coordinator 123
```

This would:
1. Generate ADW ID
2. Call `/plan_issue 123 <adw_id>`
3. Call `/build_issue 123 <adw_id>`
4. Return final results

## Troubleshooting

### "Command not found: /plan_issue"

Make sure `.claude/commands/plan_issue.md` exists and is properly formatted.

### "gh: command not found"

Install GitHub CLI:
```bash
# macOS
brew install gh

# Windows
winget install GitHub.cli

# Linux
sudo apt install gh
```

### "Failed to create branch: already exists"

The branch already exists. Either:
- Delete the branch: `git branch -D <branch_name>`
- Or use a new ADW ID

### "Permission denied: Bash(git push:*)"

Add to `.claude/settings.json`:
```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Bash(gh:*)"
    ]
  }
}
```

## See Also

- `.claude/agents/adw-planner.md` - Detailed agent documentation
- `.claude/commands/plan_issue.md` - Slash command source
- `adws/adw_plan.py` - Original Python implementation
- `docs/ADW_ARCHITECTURE.md` - Overall ADW system design
