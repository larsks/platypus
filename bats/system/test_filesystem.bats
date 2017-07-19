@test "check available disk space" {
    mounts=$(awk '$3 ~ /^(xfs|ext[234]|btrfs)$/ {print $2}' < /proc/mounts)

    failed=0
    for mount in $mounts; do
        run df --output=pcent $mount
        run tail -1 <<<"$output"
        output=${output//%}
        if ! [[ $output -lt 80 ]]; then
            echo "filesystem $mount is ${output}% full" >&2
            failed=1
        fi
    done

    [ "$failed" = 0 ]
}
