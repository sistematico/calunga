#!/usr/bin/env bash

# [ "$EUID" -ne 0 ] && echo "Este script precisa rodar como root" && exit

[ "$EUID" -eq 0 ] && systemctl daemon-reload

if ! id "calunga" &>/dev/null; then
    useradd -m -r -d /var/calunga -s /bin/bash calunga
    passwd calunga
fi

[ ! -f /etc/systemd/system/calunga.service ] && [ "$EUID" -eq 0 ] && cp etc/systemd/system/calunga.service /etc/systemd/system/
[ ! -f /etc/sudoers.d/95-calunga ] && [ "$EUID" -eq 0 ] && cp etc/sudoers.d/95-calunga /etc/sudoers.d/

[ "$EUID" -eq 0 ] && chmod 440 /etc/sudoers.d/95-calunga

if [ "$(systemctl is-active calunga)" == "inactive" ]; then
    [ "$EUID" -eq 0 ] && systemctl enable calunga || sudo systemctl enable calunga
fi

#[ "$EUID" -eq 0 ] && systemctl restart calunga || sudo systemctl restart calunga