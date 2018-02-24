#!/bin/bash



echo "Training OPEN-SESAME..."
python ${OPEN_SESAME_HOME}/src/segrnn-argid.py \
  --mode train \
  --model ${XP_DIR}/model/segrnn-argid.model
