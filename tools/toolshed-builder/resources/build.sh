#! /bin/sh

APPNAME="{{APPNAME}}"
MAIN_SCRIPT="src/{{PROJECT_NAME}}/main.py"
ICON="assets/icon.icns"

.venv/bin/pyinstaller \
    --windowed \
    --noconfirm \
    --clean \
    --add-data ./assets/*.png:./assets \
    --add-data ./assets/*.icns:./assets \
    --add-data ./assets/*.ttf:./assets \
    --optimize 1 \
    --icon $ICON \
    --name "$APPNAME" \
    $MAIN_SCRIPT

rm -rf /Applications/"$APPNAME".app
cp -r dist/"$APPNAME".app /Applications/

ln -s /Applications/"$APPNAME".app ~/Desktop/"$APPNAME"

echo "Successfully updated "$APPNAME".app in /Applications"
