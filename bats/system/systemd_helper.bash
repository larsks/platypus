is_active() {
    systemctl is-active "$@" > /dev/null 2>&1
}
