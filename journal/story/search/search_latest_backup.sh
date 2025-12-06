#!/bin/bash
#echo finding latest back up file json
latestDb=$(ls -t ~/Downloads/ | grep -i journey_ | head -n 1)
echo $latestDb
export  latestDb