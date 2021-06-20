#!/usr/bin/env bash
set -x FERNET_KEY (python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)")
printf "%s " "Enter mail for recieving alerts: : "
read user
set -x MAIL_USER $user
printf "%s " "Enter mail password: : "
read -s pass
set -x MAIL_PASSWORD $pass
