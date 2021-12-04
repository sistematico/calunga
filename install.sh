#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]; then
    echo "Este script precisa rodar como root"
    exit
fi

systemctl daemon-reload

if ! id "calunga" &>/dev/null; then
    useradd -m -r -d /var/calunga -s /bin/bash calunga
    passwd calunga
fi

[ ! -f /etc/systemd/system/calunga.service ] && cp etc/systemd/system/calunga.service /etc/systemd/system/
[ ! -f /etc/sudoers.d/95-calunga ] && cp etc/sudoers.d/95-calunga /etc/sudoers.d/

chmod 440 /etc/sudoers.d/95-calunga

if [ "$(systemctl is-active calunga)" == "inactive" ]; then
    systemctl enable calunga
fi

systemctl restart calunga