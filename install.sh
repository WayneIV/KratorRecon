#!/bin/bash
set -e

# detect os
if command -v pkg >/dev/null; then
    PKG="pkg"
    SUDO=""
else
    PKG="apt-get"
    SUDO="sudo"
fi

$SUDO $PKG update -y
$SUDO $PKG install -y python3 python3-pip git
pip3 install --user rich requests beautifulsoup4 face_recognition Pillow ipwhois dnspython pyfiglet questionary simple-term-menu

# create alias
if [ -n "$PREFIX" ]; then
    BIN="$PREFIX/bin/kratorstrike"
else
    BIN="/usr/local/bin/kratorstrike"
fi
REPO_DIR="$(pwd)"
cat <<EOL > kratorstrike.sh
#!/bin/bash
python3 "$REPO_DIR/kratorstrike.py" "$@"
EOL
chmod +x kratorstrike.sh
$SUDO mv kratorstrike.sh "$BIN"

echo "Installed kratorstrike to $BIN"
