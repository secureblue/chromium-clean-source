#! /bin/sh -x

wget https://versionhistory.googleapis.com/v1/chrome/platforms/linux/channels/stable/versions/all/releases?filter=endtime=none -O chromium-version.json
cat chromium-version.json | grep \"version\" | grep -oh "[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*" > chromium-version.txt

cp ./chromium-clean-source/chromium-clean-source.spec .
