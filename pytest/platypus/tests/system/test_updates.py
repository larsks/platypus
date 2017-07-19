import subprocess

def test_updates():
    try:
        out = subprocess.check_call(['yum', 'check-update'])
    except subprocess.CalledProcessError as exc:
        assert exc.returncode != 100, (
            'updates: uninstalled updates are available')
