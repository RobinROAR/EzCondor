#!/bin/sh


y=$(cat $1)
((y+=1))
echo $y > $2







