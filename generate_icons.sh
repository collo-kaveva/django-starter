#!/bin/bash
# Script to generate PWA icons from SVG
# Requires ImageMagick or similar tool

# Check if ImageMagick is installed
if ! command -v convert &> /dev/null; then
    echo "ImageMagick not found. Please install it first:"
    echo "  Ubuntu/Debian: sudo apt-get install imagemagick"
    echo "  macOS: brew install imagemagick"
    exit 1
fi

# Create icons in different sizes
sizes=(72 96 128 144 152 192 384 512)

for size in "${sizes[@]}"; do
    convert static/images/icons/icon.svg -resize ${size}x${size} static/images/icons/icon-${size}x${size}.png
    echo "Generated icon-${size}x${size}.png"
done

echo "All icons generated successfully!"