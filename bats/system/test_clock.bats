#!/bin/sh

load systemd_helper

@test "check chronyd clock synchronized" {
    if ! is_active chronyd; then
        skip
    fi

    run chronyc tracking
    [ "$status" -eq 0 ]
}

@test "check chronyd clock offset" {
    if ! is_active chronyd; then
        skip
    fi

    run chronyc tracking
    [ "$status" -eq 0 ]
    offset=$(awk '/RMS offset/ {print $4}' <<<"$output")
    echo "clock offset is ${offset:-unknown}" >&2
    (( $(echo "$offset<${PLATYPUS_MAX_CLOCK_OFFSET:-1}" | bc -l) ))
}

@test "check ntpd clock synchronized" {
    if ! is_active ntpd; then
        skip
    fi

    run ntpq -c peers
    [ "$status" -eq 0 ]

    # check that clock is synchronized
    awk '/^\*/ {sync=1} END {exit ! sync}' <<<"$output"
}

@test "check ntpd clock offset" {
    if ! is_active ntpd; then
        skip
    fi

    run ntpq -c peers
    [ "$status" -eq 0 ]

    # check that clock is synchronized
    awk '/^\*/ {sync=1} END {exit ! sync}' <<<"$output"

    # get offset
    offset=$(awk '/^\*/ {print $9}' <<<"$output")
    echo "clock offset is ${offset:-unknown}" >&2
    (( $(echo "$offset<${PLATYPUS_MAX_CLOCK_OFFSET:-1}" | bc -l) ))
}
