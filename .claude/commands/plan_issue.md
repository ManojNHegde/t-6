# Plan Issue - ADW Planning Workflow

Execute the complete ADW planning workflow for a GitHub issue. This command replicates the functionality of `adws/adw_plan.py` as a native Claude Code workflow.

## Variables

issue_number: $1
adw_id: $2

## Instructions

You are the **ADW Planner Agent**. Your job is to execute the complete planning phase for issue #`{issue_number}` with workflow ID `{adw_id}`.

### IMPORTANT: Sequential Execution Required

Execute each step in order. Do NOT skip steps. Do NOT execute steps in parallel unless explicitly stated.

### Step 1: Environment Validation

Check that all required tools are available:

```bash
gh --version && git --version
```

Verify we're in a git repository:
```bash
git remote -v | grep origin
```

If any check fails, stop and report the error.

### Step 2: Fetch GitHub Issue

Fetch the issue details using GitHub CLI:

```bash
gh issue view {issue_number} --json number,title,body,state,labels
```

Parse the JSON output and extract the issue data. Store this in memory for later use.

Post initial status comment:
```bash
gh issue comment {issue_number} --body "adw_bot {adw_id}_ops: Starting planning phase"
```

### Step 3: Classify Issue

Use the `/classify_issue` slash command to determine if this is a chore, bug, or feature.

Create a minimal issue JSON with only `number`, `title`, and `body` fields.

Execute the classification. The result should be one of: `/chore`, `/bug`, `/feature`

Post classification result:
```bash
gh issue comment {issue_number} --body "adw_bot {adw_id}_ops: Issue classified as: <classification>"
```

Save the classification (without the slash) as `issue_type` for later use.

### Step 4: Generate Branch Name

Use the `/generate_branch_name` slash command with:
- Issue type (e.g., "chore", "bug", "feature")
- ADW ID: `{adw_id}`
- Minimal issue JSON

The output should be a branch name following this pattern:
```
<type>-issue-<number>-adw-<adw_id>-<descriptive-name>
```

Example: `feature-issue-123-adw-20231127-abc123-add-user-auth`

### Step 5: Create Git Branch

Create and checkout the new branch:

```bash
git checkout -b <branch_name>
```

Verify the branch was created:
```bash
git branch --show-current
```

Post branch creation:
```bash
gh issue comment {issue_number} --body "adw_bot {adw_id}_ops: Working on branch: <branch_name>"
```

### Step 6: Build Implementation Plan

This is the core planning step. Execute the appropriate slash command based on classification:

- If issue type is "chore": `/chore {issue_number} {adw_id} <minimal_issue_json>`
- If issue type is "bug": `/bug {issue_number} {adw_id} <minimal_issue_json>`
- If issue type is "feature": `/feature {issue_number} {adw_id} <minimal_issue_json>`

The planning command will:
1. Research the codebase
2. Create a detailed implementation plan
3. Save the plan to `specs/issue-{issue_number}-adw-{adw_id}-sdlc_planner-<name>.md`
4. Return the path to the plan file

Extract the plan file path from the output. It should start with `specs/` and end with `.md`.

Validate the plan file exists:
```bash
ls -la <plan_file_path>
```

Post planning completion:
```bash
gh issue comment {issue_number} --body "adw_bot {adw_id}_sdlc_planner: Implementation plan created"
gh issue comment {issue_number} --body "adw_bot {adw_id}_ops: Plan file created: <plan_file_path>"
```

### Step 7: Generate Commit Message

Use the `/commit` slash command to generate a proper commit message:

Arguments:
- Agent name: `sdlc_planner`
- Issue type: `<issue_type>` (chore/bug/feature)
- Minimal issue JSON

The output will be a formatted commit message.

### Step 8: Commit the Plan

Stage the plan file and commit:

```bash
git add <plan_file_path>
git status
git commit -m "<commit_message>"
```

Verify the commit was created:
```bash
git log -1 --oneline
```

Post commit status:
```bash
gh issue comment {issue_number} --body "adw_bot {adw_id}_sdlc_planner: Plan committed"
```

### Step 9: Push Branch and Create PR

Push the branch to origin:

```bash
git push -u origin <branch_name>
```

Use the `/pull_request` slash command to create a PR:

Arguments:
- Branch name: `<branch_name>`
- Minimal issue JSON
- Plan file path: `<plan_file_path>`
- ADW ID: `{adw_id}`

The output will be a PR URL.

### Step 10: Save State and Report

Create state file at `agents/{adw_id}/state.json`:

```json
{
  "adw_id": "{adw_id}",
  "issue_number": "{issue_number}",
  "issue_class": "/<issue_type>",
  "branch_name": "<branch_name>",
  "plan_file": "<plan_file_path>",
  "pr_url": "<pr_url>",
  "workflow": "adw_plan",
  "status": "completed",
  "completed_at": "<ISO timestamp>"
}
```

Post final status:
```bash
gh issue comment {issue_number} --body "adw_bot {adw_id}_ops: Planning phase completed"
```

Post final state summary:
```bash
gh issue comment {issue_number} --body "adw_bot {adw_id}_ops: Final planning state:
\`\`\`json
<state_json>
\`\`\`"
```

## Error Handling

If any step fails:
1. Log the error
2. Post error comment to GitHub:
   ```bash
   gh issue comment {issue_number} --body "adw_bot {adw_id}_ops: Error in <step_name>: <error_message>"
   ```
3. Save error state to `agents/{adw_id}/state.json` with `status: "failed"`
4. Stop execution and report the failure

## Report

Return a structured summary:

```
✅ Planning Phase Complete

Issue: #{issue_number}
Classification: <issue_type>
Branch: <branch_name>
Plan File: <plan_file_path>
Pull Request: <pr_url>
Workflow ID: {adw_id}

Next Steps:
- Review the implementation plan at <plan_file_path>
- Execute the build phase with: /build_issue {issue_number} {adw_id}
```

## Notes

- This command coordinates multiple sub-agents (classifier, branch generator, planner, PR creator)
- Each sub-agent is invoked via slash commands defined in `.claude/commands/`
- State is persisted to `agents/{adw_id}/state.json` for use by build phase
- All status updates are posted to the GitHub issue for transparency
- The workflow creates a feature branch, plan file, and draft PR ready for implementation
