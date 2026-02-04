#!/bin/bash
# Lighthouse Macro - Claude Context Sync Script
# Syncs CLAUDE_MASTER.md to all Claude interfaces

MASTER="/Users/bob/LHM/Strategy/CLAUDE_MASTER.md"
CODE_TARGET="/Users/bob/.claude/CLAUDE.md"
WEB_EXPORT="/Users/bob/LHM/Strategy/CLAUDE_WEB_EXPORT.md"
LOG="/Users/bob/LHM/logs/sync.log"

# Ensure master exists
if [ ! -f "$MASTER" ]; then
    echo "ERROR: Master file not found at $MASTER"
    exit 1
fi

# Timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Sync to Claude Code
cp "$MASTER" "$CODE_TARGET"
echo "[$TIMESTAMP] Synced to Claude Code: $CODE_TARGET" >> "$LOG"

# Create web export (same content, but could be trimmed version later)
cp "$MASTER" "$WEB_EXPORT"
echo "[$TIMESTAMP] Created web export: $WEB_EXPORT" >> "$LOG"

# Summary
echo "========================================"
echo "CLAUDE CONTEXT SYNCED - $TIMESTAMP"
echo "========================================"
echo ""
echo "1. Claude Code:    DONE (automatic)"
echo "2. Web Export:     DONE (created at $WEB_EXPORT)"
echo ""
echo "MANUAL STEPS REQUIRED:"
echo "----------------------------------------"
echo "3. Claude.ai (Web + iOS):"
echo "   - Go to claude.ai/projects"
echo "   - Open 'Lighthouse Macro' project"
echo "   - Update Project Knowledge with $WEB_EXPORT"
echo ""
echo "4. Claude Desktop:"
echo "   - Open Claude Desktop preferences"
echo "   - Update custom instructions"
echo "========================================"
echo ""
echo "Log updated: $LOG"
