#!/bin/sh
echo '---------------------------------------------'
echo 'Now downloading all test vectors from vectors.txt'
echo '---------------------------------------------'

while read p;
  do wget "$p";
done < vectors.txt
