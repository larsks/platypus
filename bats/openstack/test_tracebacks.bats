@test "check for tracebacks in service log files" {
    logfiles=$(rpm -qa -l 'openstack*' |
        grep /var/log |
        xargs -iLOGDIR find LOGDIR -name '*.log')

    failed=0
    for logfile in $logfiles; do
        [ -f "$logfile" ] || continue
        run grep -c Traceback "$logfile"
        if [[ $output > 0 ]]; then
            echo "found $output tracebacks in $logfile" >&2
            failed=1
        fi
    done

    [ "$failed" = 0 ]
}
