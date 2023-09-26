accelerate launch --main_process_por $MAIN_PROCESS_POR train_dreambooth768.py \
  --pretrained_model_name_or_path=$MODEL_NAME  \
  --instance_data_dir=$INSTANCE_DIR \
  --output_dir=$OUTPUT_DIR \
  --train_text_encoder \
  "--instance_prompt=$INSTANCE_PROMPT"  \
  --resolution=$RESOLUTION \
  --train_batch_size=$TRAIN_BATCH_SIZE \
  --gradient_accumulation_steps=$GRADIENT_ACCUMULATION_STEPS \
  --learning_rate=$LR \
  --lr_scheduler=$LR_SCHEDULER \
  --lr_warmup_steps=$LR_WARMUP_STEPS \
  --max_train_steps=$MAX_TRAINING_STEPS \
  --api_run_name=$API_RUN_NAME