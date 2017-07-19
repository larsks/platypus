@test "check if debug logs are enabled" {
    config_files=$(rpm -qa -c 'openstack-*' | grep '/etc/[^/]*/[^/]*\.conf')

    failed=0
    for config_file in $config_files; do
        [ -f "$config_file" ] || continue
        if grep --with-filename -i '^debug *= *true' $config_file >&2; then
            failed=1
        fi
    done

    [ "$failed" = 0 ]
}

