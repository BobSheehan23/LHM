#!/bin/bash
# Lighthouse Macro - Claude Context Sync Script
# Syncs CLAUDE_MASTER.md to all Claude interfaces
# Updates LAST_SYNC date automatically

MASTER="/Users/bob/LHM/Strategy/CLAUDE_MASTER.md"
CODE_TARGET="/Users/bob/.claude/CLAUDE.md"
WEB_EXPORT="/Users/bob/Desktop/LHM_CLAUDE_CONTEXT.md"
GEMINI_EXPORT="/Users/bob/Desktop/LHM_GEMINI_CONTEXT.md"
LOG="/Users/bob/LHM/logs/sync.log"

# Ensure master exists
if [ ! -f "$MASTER" ]; then
    echo "ERROR: Master file not found at $MASTER"
    exit 1
fi

# Get today's date
TODAY=$(date '+%Y-%m-%d')
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Update LAST_SYNC in master file
sed -i '' "s/^\*\*LAST_SYNC:\*\* .*/\*\*LAST_SYNC:\*\* $TODAY/" "$MASTER"
echo "[$TIMESTAMP] Updated LAST_SYNC to $TODAY" >> "$LOG"

# Sync to Claude Code
cp "$MASTER" "$CODE_TARGET"
echo "[$TIMESTAMP] Synced to Claude Code: $CODE_TARGET" >> "$LOG"

# Create web export (same content)
cp "$MASTER" "$WEB_EXPORT"
echo "[$TIMESTAMP] Created web export: $WEB_EXPORT" >> "$LOG"

# Create Gemini export (same content, could be trimmed later)
cp "$MASTER" "$GEMINI_EXPORT"
echo "[$TIMESTAMP] Created Gemini export: $GEMINI_EXPORT" >> "$LOG"

# Summary
echo "========================================"
echo "CLAUDE CONTEXT SYNCED - $TIMESTAMP"
echo "========================================"
echo ""
echo "LAST_SYNC updated to: $TODAY"
echo ""
echo "AUTOMATIC:"
echo "  1. Claude Code:    DONE"
echo "  2. Desktop Export: DONE (~/Desktop/LHM_CLAUDE_CONTEXT.md)"
echo "  3. Gemini Export:  DONE (~/Desktop/LHM_GEMINI_CONTEXT.md)"
echo ""
echo "MANUAL (copy from Desktop - accessible from phone via iCloud):"
echo "  4. Claude.ai/iOS → paste LHM_CLAUDE_CONTEXT.md"
echo "  5. Claude Desktop → paste to custom instructions"
echo "  6. Gemini → paste LHM_GEMINI_CONTEXT.md"
echo ""
echo "========================================"
