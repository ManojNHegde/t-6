# ADW Planner Subagent - Quick Start

## What It Does

The **adw-planner** subagent replicates the complete functionality of `adws/adw_plan.py` as a native Claude Code subagent.

## How to Invoke

### Method 1: Task Tool (Recommended for Programmatic Use)

```javascript
Task({
  subagent_type: 'adw-planner',
  prompt: 'Plan issue #123 with ADW ID adw-20231127-abc123',
  model: 'opus'
})
```

### Method 2: Direct Invocation in Claude Code

Simply type in the Claude Code chat:

```
Use the adw-planner subagent to plan issue #123 with ADW ID adw-20231127-abc123
```

Claude will automatically recognize the subagent and invoke it.

### Method 3: Python Integration (Backward Compatible)

```python
from adws.adw_modules.agent import execute_template
from adws.adw_modules.data_types import AgentTemplateRequest

# Create a request to invoke the adw-planner subagent
request = AgentTemplateRequest(
    agent_name="adw_planner",
    slash_command="",  # Not needed for direct subagent invocation
    args=[],  # Pass prompt directly via claude CLI
    adw_id="adw-20231127-abc123",
)

# Execute via Claude Code
import subprocess
result = subprocess.run([
    "claude",
    "-p", "Use the adw-planner subagent to plan issue #123 with ADW ID adw-20231127-abc123",
    "--model", "opus"
], capture_output=True, text=True)

print(result.stdout)
```

## Configuration

The subagent is configured in `.claude/agents/adw-planner.md` with:

```yaml
---
name: adw-planner
description: Executes the complete ADW planning workflow...
tools: Bash, Read, Write, SlashCommand
model: opus
permissionMode: default
---
```

### Key Configuration Fields

- **name**: `adw-planner` - This is the `subagent_type` you use in Task() calls
- **tools**: `Bash, Read, Write, SlashCommand` - Tools the subagent can use
- **model**: `opus` - Uses Opus model for complex planning tasks
- **permissionMode**: `default` - Uses standard permission handling

## What It Does Step-by-Step

1. ✅ Validates environment (gh CLI, git)
2. ✅ Fetches GitHub issue details
3. ✅ Classifies issue type (chore/bug/feature)
4. ✅ Generates standardized branch name
5. ✅ Creates and checks out feature branch
6. ✅ Builds detailed implementation plan
7. ✅ Generates proper commit message
8. ✅ Commits plan to git
9. ✅ Pushes branch to remote
10. ✅ Creates pull request
11. ✅ Saves workflow state
12. ✅ Posts updates to GitHub issue

## Expected Output

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

## State Output

The subagent creates `agents/<adw_id>/state.json`:

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

## Prerequisites

1. **GitHub CLI** - Must be authenticated
   ```bash
   gh auth login
   ```

2. **Git** - In a git repository with GitHub remote
   ```bash
   git remote -v
   ```

3. **Slash Commands** - These must exist in `.claude/commands/`:
   - `/classify_issue`
   - `/generate_branch_name`
   - `/chore`, `/bug`, `/feature`
   - `/commit`
   - `/pull_request`

## Error Handling

If the subagent fails:
- Error logged to `agents/<adw_id>/sdlc_planner/error.log`
- Error comment posted to GitHub issue
- State saved with `status: "failed"`
- Returns error message to caller

## Replacing Python Script

### Old Way (Python)
```bash
uv run adws/adw_plan.py 123 adw-20231127-abc123
```

### New Way (Subagent)
```bash
claude -p "Task({ subagent_type: 'adw-planner', prompt: 'Plan issue #123 with ADW ID adw-20231127-abc123' })"
```

Or in a conversation:
```
Use adw-planner to plan issue #123 with ADW ID adw-20231127-abc123
```

## Advantages Over Python Script

1. **Native Integration** - No subprocess needed, runs in Claude Code
2. **Better Error Recovery** - Can adapt to unexpected situations
3. **Interactive** - Can ask questions if something is unclear
4. **Transparent** - Full conversation history visible
5. **Flexible** - Easy to modify behavior without changing code
6. **Consistent** - Uses same tools and permissions as main session

## Next: Build Subagent

Create `adw-builder` subagent using the same pattern to:
1. Read plan from state
2. Implement the plan
3. Run tests
4. Update PR

Then create `adw-coordinator` to orchestrate both!

## Troubleshooting

### "Subagent not found: adw-planner"

Check that `.claude/agents/adw-planner.md` exists and has valid YAML frontmatter.

### "Permission denied: Bash(git:*)"

Add to `.claude/settings.json`:
```json
{
  "permissions": {
    "allow": ["Bash(git:*)", "Bash(gh:*)"]
  }
}
```

### "Slash command not found: /classify_issue"

Ensure all required slash commands exist in `.claude/commands/`:
```bash
ls -la .claude/commands/classify_issue.md
ls -la .claude/commands/generate_branch_name.md
ls -la .claude/commands/feature.md
ls -la .claude/commands/commit.md
ls -la .claude/commands/pull_request.md
```

## Full Example

```javascript
// In a Claude Code session or via Task tool
Task({
  subagent_type: 'adw-planner',
  prompt: 'Plan issue #456 with ADW ID adw-20231201-xyz789',
  model: 'opus'
})

// The subagent will:
// 1. Fetch issue #456 from GitHub
// 2. Classify it (e.g., as "feature")
// 3. Generate branch: feature-issue-456-adw-20231201-xyz789-description
// 4. Create branch and checkout
// 5. Build implementation plan in specs/
// 6. Commit plan
// 7. Push to origin
// 8. Create PR
// 9. Save state to agents/adw-20231201-xyz789/state.json
// 10. Return summary

// Output:
// ✅ Planning Phase Complete
// Issue: #456
// Classification: feature
// Branch: feature-issue-456-adw-20231201-xyz789-add-export-feature
// Plan File: specs/issue-456-adw-20231201-xyz789-sdlc_planner-add-export.md
// Pull Request: https://github.com/owner/repo/pull/789
// Workflow ID: adw-20231201-xyz789
```

## See Also

- `.claude/agents/adw-planner.md` - Subagent definition
- `docs/ADW_SUBAGENT_USAGE.md` - Detailed usage guide
- `adws/adw_plan.py` - Original Python implementation
