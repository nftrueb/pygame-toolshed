APPNAME="{{PROJECT_APP_NAME}}"
TITLE="{{PROJECT_TITLE}}"
ROOT=./web/

# copy source code to web root
mkdir -p $ROOT
mkdir -p $ROOT/$APPNAME
mkdir -p $ROOT/toolshed
cp ./src/$APPNAME/*.py $ROOT/$APPNAME 
cp ../toolshed/src/toolshed/*.py ./web/toolshed/

mkdir $ROOT/assets
cp -r ./assets/ $ROOT/assets

# start local server 
.venv/bin/pygbag \
    --app_name "$APPNAME" \
    --title "$TITLE" \
    --icon ./assets/icon.png \
    $ROOT
    