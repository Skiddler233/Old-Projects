#!/bin/bash

THRESHOLD=30  # Set the threshold percentage for memory usage
SLEEP_DURATION=1800  # 20 minutes in seconds

convert_bytes() {
    # Convert bytes to a human-readable format
    local bytes=$1
    if [ "$bytes" -lt 1024 ]; then
        echo "${bytes} Bytes"
    elif [ "$bytes" -ge 1024 ] && [ "$bytes" -lt 1048576 ]; then
        echo "$(awk -v bytes="$bytes" 'BEGIN {printf "%.2f", bytes / 1024}') KB"
    elif [ "$bytes" -ge 1048576 ] && [ "$bytes" -lt 1073741824 ]; then
        echo "$(awk -v bytes="$bytes" 'BEGIN {printf "%.2f", bytes / 1048576}') MB"
    else
        echo "$(awk -v bytes="$bytes" 'BEGIN {printf "%.2f", bytes / 1073741824}') GB"
    fi
}

show_alert_dialog() {
    # Display an alert dialog box
    osascript -e 'display dialog "Your Memory usage is quite High \nPlease consider quitting some apps" buttons {"OK"} default button "OK" with icon caution'

}

get_memory_usage() {
    # Get total and used memory from sysctl
    total_memory=$(sysctl -n hw.memsize)
    used_memory=$(vm_stat | awk '/Pages active/ {print $3 * 4096}' | tr -d ' ')

    # Convert total and used memory to bytes
    total_memory_bytes=$(echo "$total_memory" | tr -d ' ')
    used_memoryx10=$((used_memory * 10))
    used_memory_bytes=$(awk -v used_memory="$used_memoryx10" 'BEGIN {printf "%.0f", used_memory}')

    # Calculate memory usage percentage
    memory_percentage=$(awk -v used_memory_bytes="$used_memory_bytes" -v total_memory_bytes="$total_memory_bytes" 'BEGIN {if (total_memory_bytes != 0) printf "%.2f", (used_memory_bytes / total_memory_bytes) * 100}')

    # Print memory usage information
    echo "Total Memory: $(convert_bytes "$total_memory_bytes")"
    echo "Used Memory: $(convert_bytes "$used_memory_bytes")"
    echo "Memory Usage Percentage: $memory_percentage%"

    # Check if memory usage exceeds the threshold
    if [ ! -z "$memory_percentage" ] && (( $(echo "$memory_percentage > $THRESHOLD" | bc -l) )); then
        echo "Memory usage exceeds the threshold of $THRESHOLD%. ALERT!"
        show_alert_dialog

        echo "Sleeping for 30 minutes..."
        sleep $SLEEP_DURATION
    fi
}

while true; do
    get_memory_usage
    # interval (in seconds) for monitoring
    sleep 30
done
