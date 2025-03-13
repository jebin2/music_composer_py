#!/bin/bash

# Exit immediately if any command fails
set -e

# Define the Docker image name
IMAGE_NAME="music_composer_test"

echo "🚀 Building Docker image: $IMAGE_NAME ..."
sudo docker build --no-cache -t $IMAGE_NAME .

echo "✅ Build complete!"

echo "🔄 Running the application in a fresh container..."
sudo docker run --rm $IMAGE_NAME

echo "🗑️ Deleting the Docker image: $IMAGE_NAME ..."
sudo docker rmi $IMAGE_NAME -f

echo "🎉 Test completed and image removed successfully!"
