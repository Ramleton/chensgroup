#!/bin/bash

MONGO_HOST="localhost"
MONGO_PORT="27017"
DB_NAME="names"

# Replace MONGO_PATH's value with the location of mongosh on your PC
MONGO_PATH=""

SETUP_COMMANDS=$(cat <<EOF
use $DB_NAME;
db.first_names.drop();
db.createCollection("first_names");
db.first_names.insertMany([
  { "name": "Ishaan" },
  { "name": "Gary" },
  { "name": "Larry" },
  { "name": "Mary" },
  { "name": "John" },
  { "name": "Joe" },
  { "name": "Xanathar" },
  { "name": "Rick" },
  { "name": "Mordecai" },
  { "name": "Carly" },
  { "name": "Sam" },
]);
EOF
)
# Connect to MongoDB and run the setup commands
echo "$SETUP_COMMANDS" | $MONGO_PATH --host $MONGO_HOST --port $MONGO_PORT

# Check if setup was successful based on exit status of previously executed command

if [ $? -eq 0 ]; then
  echo "Database setup completed successfully"
else
  echo "Database setup failed."
fi

echo "Installing required packages..."

pip install -r requirements.txt

if [ $? -eq 0 ]; then
  echo "Setup completed successfully"
else
  echo "Setup failed."
fi