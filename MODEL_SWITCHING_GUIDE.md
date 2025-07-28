# Claude Code Model Switching Guide

This guide explains how to use different Claude models for different phases of your development workflow.

## Overview

- **Claude Opus 4**: Best for planning, architecture, and complex reasoning
- **Claude Sonnet**: Efficient for implementation and coding tasks
- **Claude Haiku**: Fast for simple tasks and quick responses

## Current Setup

### Planning Phase (Opus 4)
When you want to use Opus 4 for planning:

1. **Option A - Direct Selection**:
   ```bash
   # Start Claude Code without the local settings override
   cd ~/CreatorMate
   mv .claude/settings.json .claude/settings.json.bak
   claude
   # (Opus 4 is the default when no settings are specified)
   ```

2. **Option B - Environment Variable**:
   ```bash
   # Set the model via environment variable
   ANTHROPIC_MODEL=claude-opus-4-20250514 claude
   ```

### Implementation Phase (Sonnet)
When you want to use Sonnet for implementation:

1. **Using Local Settings** (Already configured):
   ```bash
   cd ~/CreatorMate
   claude
   # Will automatically use Sonnet due to .claude/settings.json
   ```

2. **Environment Variable Override**:
   ```bash
   ANTHROPIC_MODEL=claude-3-5-sonnet-20241022 claude
   ```

## Workflow Process

### 1. Planning Session (Opus 4)
```bash
# Temporarily disable local settings to use Opus 4
mv .claude/settings.json .claude/settings.json.bak
claude

# In the session:
# - Create comprehensive plans
# - Design architecture
# - Fill out implementation_plan.md
# - Save and exit
```

### 2. Implementation Session (Sonnet)
```bash
# Restore settings to use Sonnet
mv .claude/settings.json.bak .claude/settings.json
claude

# In the session:
# - Read implementation_plan.md
# - Execute the plan
# - Focus on efficient coding
```

## Quick Switching Scripts

### Create these helper scripts:

**use-opus.sh**:
```bash
#!/bin/bash
# Switch to Opus 4 for planning
if [ -f .claude/settings.json ]; then
    mv .claude/settings.json .claude/settings.json.bak
fi
echo "Switched to Claude Opus 4 for planning"
claude
```

**use-sonnet.sh**:
```bash
#!/bin/bash
# Switch to Sonnet for implementation
if [ -f .claude/settings.json.bak ]; then
    mv .claude/settings.json.bak .claude/settings.json
fi
echo "Switched to Claude Sonnet for implementation"
claude
```

## Best Practices

1. **Clear Handoffs**: Always save your planning work to `implementation_plan.md`
2. **Session Management**: Complete one phase before switching models
3. **Documentation**: Update the plan with any discoveries during implementation
4. **Context Preservation**: Use clear file structures and comments

## Verification

To verify which model you're using:
1. Ask "What model are you?" at the start of a session
2. Check for the presence of `.claude/settings.json`
3. Look at the model's response style (Opus is more detailed, Sonnet is more concise)

## Advanced Usage

### Using Task Tool for Delegation
From an Opus 4 session, you can delegate implementation tasks:
```
/task "Implement the authentication system based on the plan in implementation_plan.md"
```

### Environment-Based Configuration
Add to your shell profile (`.zshrc` or `.bashrc`):
```bash
alias claude-opus='ANTHROPIC_MODEL=claude-opus-4-20250514 claude'
alias claude-sonnet='ANTHROPIC_MODEL=claude-3-5-sonnet-20241022 claude'
alias claude-haiku='ANTHROPIC_MODEL=claude-3-5-haiku-20241022 claude'
```

## Troubleshooting

- **Model not switching**: Check if environment variables are overriding settings
- **Settings not found**: Ensure `.claude/settings.json` is in the project root
- **Unexpected model**: Verify with "What model are you?" query