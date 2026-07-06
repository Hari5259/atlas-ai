#!/bin/bash

# Fix all bot@atlas.ai commits to use your account email
# This script rewrites commit history safely

echo "🔧 Fixing commit history..."
echo "Setting up git config..."

# Configure git with your correct email
git config user.email "shariharasudhan333@gmail.com"
git config user.name "Hari Hara sudhan S"

echo "✅ Git configured"
echo ""
echo "🔄 Rewriting commit history (this may take a moment)..."

# Rewrite all commits with bot@atlas.ai to use your email
git filter-branch --env-filter '
if [ "$GIT_COMMITTER_EMAIL" = "bot@atlas.ai" ]
then
    export GIT_COMMITTER_EMAIL="shariharasudhan333@gmail.com"
    export GIT_COMMITTER_NAME="Hari Hara sudhan S"
fi
if [ "$GIT_AUTHOR_EMAIL" = "bot@atlas.ai" ]
then
    export GIT_AUTHOR_EMAIL="shariharasudhan333@gmail.com"
    export GIT_AUTHOR_NAME="Hari Hara sudhan S"
fi
' -- --all

echo "✅ History rewritten!"
echo ""
echo "📤 Pushing changes to GitHub..."

# Force push with safety check
git push origin main --force-with-lease

echo ""
echo "✅ Done! Your commits have been fixed."
echo "🟢 Check your contribution graph in a few minutes:"
echo "   https://github.com/Hari5259?tab=contributions&from=2026-05-01&to=2026-12-31"
