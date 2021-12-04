#!/usr/bin/env bash

# [ "$EUID" -ne 0 ] && echo "Este script precisa rodar como root" && exit

[ "$EUID" -ne 0 ] && systemctl daemon-reload

if ! id "calunga" &>/dev/null; then
    useradd -m -r -d /var/calunga -s /bin/bash calunga
    passwd calunga
fi

[ ! -f /etc/systemd/system/calunga.service ] && cp etc/systemd/system/calunga.service /etc/systemd/system/
[ ! -f /etc/sudoers.d/95-calunga ] && cp etc/sudoers.d/95-calunga /etc/sudoers.d/

[ "$EUID" -ne 0 ] && chmod 440 /etc/sudoers.d/95-calunga

if [ "$(systemctl is-active calunga)" == "inactive" ]; then
    [ "$EUID" -ne 0 ] && systemctl enable calunga || sudo systemctl enable calunga
fi

[ "$EUID" -ne 0 ] && systemctl restart calunga || sudo systemctl restart calunga