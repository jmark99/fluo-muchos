#!/bin/sh

OLDPWD=$PWD
ACCUMULO_VERSION=2.1.0-SNAPSHOT
ACCUMULO_DIR="$HOME/dev/accumulo"
TARGET_DIR="$ACCUMULO_DIR/assemble/target"
ACCUMULO_GZIP="accumulo-${ACCUMULO_VERSION}-bin.tar.gz"
UPLOAD_DIR="$HOME/ansible/fluo-muchos/conf/upload"

cd $ACCUMULO_DIR
cmd="$HOME/bin/aBuildWithNoTestsFast"
$cmd
status=$?
if [ $status -eq 0 ]; then
  echo "$cmd command was successful"
else
  echo "$cmd failed"
  exit $status
fi
cp "$TARGET_DIR/$ACCUMULO_GZIP" "$UPLOAD_DIR/."
cd $OLDPWD

