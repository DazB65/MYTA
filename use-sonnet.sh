#!/bin/bash
# Switch to Claude Sonnet for implementation sessions

echo "⚡ Switching to Claude Sonnet for implementation..."

# Restore Sonnet settings if backed up
if [ -f .claude/settings.json.bak ]; then
    mv .claude/settings.json.bak .claude/settings.json
    echo "✓ Restored Sonnet settings"
elif [ ! -f .claude/settings.json ]; then
    echo "⚠️  No settings file found. Creating default Sonnet configuration..."
    mkdir -p .claude
    cat > .claude/settings.json << 'EOF'
{
  "model": "claude-3-5-sonnet-20241022",
  "temperature": 0.2,
  "maxTokens": 8192
}
EOF
fi

echo "✓ Ready for implementation with Sonnet"
echo "📋 Load implementation_plan.md to continue where planning left off"
echo ""

# Start Claude Code
claude