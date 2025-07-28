#!/bin/bash
# Switch to Claude Opus 4 for planning sessions

echo "🧠 Switching to Claude Opus 4 for planning..."

# Backup current settings if they exist
if [ -f .claude/settings.json ]; then
    mv .claude/settings.json .claude/settings.json.bak
    echo "✓ Backed up Sonnet settings"
fi

echo "✓ Ready for planning with Opus 4"
echo "📝 Remember to save your plans to implementation_plan.md"
echo ""

# Start Claude Code
claude