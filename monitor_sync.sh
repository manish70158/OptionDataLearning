#!/bin/bash
# Monitor data sync progress for NIFTY option data

TASK_ID=$1

if [ -z "$TASK_ID" ]; then
    echo "Usage: ./monitor_sync.sh <task_id>"
    echo "Current running sync: 6c8cc1cb"
    exit 1
fi

echo "Monitoring sync task: $TASK_ID"
echo "Press Ctrl+C to stop monitoring (sync will continue in background)"
echo ""

while true; do
    clear
    echo "=== NIFTY DATA SYNC PROGRESS ==="
    echo ""

    # Get sync status
    RESPONSE=$(curl -s http://localhost:8000/api/data/sync/$TASK_ID/status)
    STATUS=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['status'])" 2>/dev/null)
    PROGRESS=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['progress'])" 2>/dev/null)

    echo "Status: $STATUS"
    echo "Progress: $PROGRESS%"
    echo ""

    # Check cache
    echo "=== CACHE STATUS ==="
    sqlite3 /Users/manishkumar/Documents/learning/OptionDataLearning/web/cache.db \
        "SELECT COUNT(DISTINCT date) as days, MIN(date) as first, MAX(date) as last, COUNT(*) as premiums FROM option_premiums WHERE instrument='NIFTY';" \
        | awk -F'|' '{printf "Trading days: %s\nDate range: %s to %s\nOption premiums: %s\n", $1, $2, $3, $4}'

    if [ "$STATUS" = "completed" ]; then
        echo ""
        echo "✅ SYNC COMPLETED!"
        break
    fi

    if [ "$STATUS" = "failed" ]; then
        echo ""
        echo "❌ SYNC FAILED"
        echo "Error details:"
        echo $RESPONSE | python3 -m json.tool
        break
    fi

    sleep 10
done
