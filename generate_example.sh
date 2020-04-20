#!/bin/bash

FILE=/home/irma/PycharmProjects/RickyFinalProject/RickyRenunciaLlevateJunta.csv
SIZE=200
head -n $SIZE $FILE > example.jsonl
tail -n $SIZE $FILE > example_tail.jsonl
head -n $SIZE $FILE > example_head_tail.jsonl
tail -n $SIZE $FILE >> example_head_tail.jsonl

SPLIT_SIZE=50000
PREFIX=rickyrenunciaparts/
split -l $SPLIT_SIZE $FILE $PREFIX


# Not used, file is small (19914 rows)
SPLIT_SIZE=5000
PREFIX=luchasiparts/
FILE2=/home/irma/PycharmProjects/RickyFinalProject/luchaSiEntregano.csv
split -l $SPLIT_SIZE $FILE2 $PREFIX
