#!/bin/bash
cd /Users/anushka/cab_navigation

echo "📝 Staging all changes..."
git add .

echo "📤 Committing changes..."
git commit -m "Final update: Remove Ola, fix API keys, optimize timeouts, add verification" --no-edit

echo "🚀 Force pushing to GitHub..."
git push -f origin main

echo "✅ Done!"
