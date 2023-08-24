#!/bin/bash

VIDEO_UUID=$(python '01-download-process-translate.py' $1 | tail -1)
VIDEO_JSON=$(printf "output/%s.json" "$VIDEO_UUID")
echo $VIDEO_JSON
python '02-voice-subtitles.py' $VIDEO_JSON
python '03-change-voice.py' $VIDEO_JSON
python '04-dub.py' $VIDEO_JSON