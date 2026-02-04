#!/bin/bash
# Lighthouse Macro - Claude Context Sync Script
# Syncs CLAUDE_MASTER.md to all Claude interfaces
# Updates LAST_SYNC date automatically

MASTER="/Users/bob/LHM/Strategy/CLAUDE_MASTER.md"
CODE_TARGET="/Users/bob/.claude/CLAUDE.md"
WEB_EXPORT="/Users/bob/LHM/Strategy/CLAUDE_WEB_EXPORT.md"
GEMINI_EXPORT="/Users/bob/LHM/Strategy/GEMINI_CONTEXT.md"
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
echo "  2. Web Export:     DONE ($WEB_EXPORT)"
echo "  3. Gemini Export:  DONE ($GEMINI_EXPORT)"
echo ""
echo "MANUAL (copy from exports above):"
echo "  4. Claude.ai Project → paste web export"
echo "  5. Claude Desktop → paste to custom instructions"
echo "  6. Gemini → paste gemini export"
echo ""
echo "========================================"
