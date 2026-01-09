# GitHub Setup Instructions

## Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Repository name: `ai-news-aggregation` (or any name you prefer)
5. Description: "AI-Powered News Aggregation & Chatbot System"
6. Choose **Public** or **Private**
7. **DO NOT** initialize with README, .gitignore, or license (we already have these)
8. Click "Create repository"

## Step 2: Push Your Code

After creating the repository, GitHub will show you commands. Use these:

```bash
cd /Users/dhruvgulwani/Desktop/NewsPaper_Foboh/NewsPaper

# Add the remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ai-news-aggregation.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Alternative: Using SSH

If you prefer SSH:

```bash
git remote add origin git@github.com:YOUR_USERNAME/ai-news-aggregation.git
git branch -M main
git push -u origin main
```

## Quick Push Command

If you've already set up the remote, you can use:

```bash
git push -u origin main
```

## Security Note

✅ Your `.env` file with the API key is already in `.gitignore` and will NOT be pushed to GitHub.

## After Pushing

Your repository will be available at:
`https://github.com/YOUR_USERNAME/ai-news-aggregation`

