#!/bin/bash

rm -r ./Data/Testaments_and_Books/Apocrypha/*
rm -r ./Data/Testaments_and_Books/Assessalonians/*
echo "" > ./Data/Testaments_and_Books/Apocrypha/.gitkeep
echo "" > ./Data/Testaments_and_Books/Assessalonians/.gitkeep
sed -i '/\"token\"\:/c\\t\"token\"\: \"\"\,' ./lib/app_config.py
sed -i '/\"domain\"\:/c\\t\"domain\"\: \"\"\,' ./lib/app_config.py
sed -i '/\"repo\"\:/c\\t\"repo\"\: \"\"\,' ./lib/app_config.py
sed -i '/\"id\"\:/c\\t\"id\"\: 1\,' ./lib/app_config.py
