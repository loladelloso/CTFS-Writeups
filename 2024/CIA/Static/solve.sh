#!/bin/bash

mkdir "results" "results/frames" "results/differences"

convert "Recursos/static.gif" "results/frames/%03d.png"

for i in $(seq -w 0 118); do
  j=$(printf "%03d" $((10#$i + 1)))
  compare "results/frames/${i}.png" "results/frames/${j}.png" "results/differences/${i}_${j}.png"
done
