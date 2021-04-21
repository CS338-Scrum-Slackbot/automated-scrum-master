#!/bin/bash

# MAKES COPIES OF SCRUM_BOARD.JSON FOR TESTING - RUN FROM ROOT DIRECTORY
# Start: uncomment mkdir, cp. Update: uncomment rm, cp

FOLDER_NAME="pytest_data"
NUM_FILES=5

#mkdir $FOLDER_NAME # need existing folder before touch command

for (( c=1; c<=$NUM_FILES; c++ ))
do
   #rm  $FOLDER_NAME/input$c.json # need remove to rewrite files
   #cp data/scrum_board.json $FOLDER_NAME/input$c.json
done