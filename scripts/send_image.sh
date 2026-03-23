#!/bin/bash
# Usage: ./send_image.sh <local_image_path> [recipient]
# Copies image to outbound dir and sends via Feishu
# Requires OpenClaw message tool — run within an active OpenClaw session

set -e

IMAGE_PATH="$1"
RECIPIENT="$2"  # optional: open_id or chat_id

if [ -z "$IMAGE_PATH" ]; then
  echo "Usage: $0 <local_image_path> [recipient]"
  exit 1
fi

if [ ! -f "$IMAGE_PATH" ]; then
  echo "File not found: $IMAGE_PATH"
  exit 1
fi

FILENAME=$(basename "$IMAGE_PATH")
OUTBOUND_DIR="$HOME/.openclaw/media/outbound"
mkdir -p "$OUTBOUND_DIR"

cp "$IMAGE_PATH" "$OUTBOUND_DIR/$FILENAME"

echo "Image copied to $OUTBOUND_DIR/$FILENAME"
echo "Now use message tool with:"
echo "  filePath: $OUTBOUND_DIR/$FILENAME"
echo "  target: ${RECIPIENT:-<current chat>}"
