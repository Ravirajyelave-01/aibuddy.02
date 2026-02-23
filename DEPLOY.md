# Free Deployment Guide

## Option 1: Render.com (Recommended - Free)

### Step 1: Push Code to GitHub
1. Create a new repository on GitHub
2. Push your code:
```
bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ravichange.git
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to https://render.com and sign up with GitHub
2. Click "New +" → "Web Service"
3. Select your repository
4. Configure:
   - Name: ravichange
   - Build Command: (leave blank)
   - Start Command: python app.py
   - Free instance type
5. Click "Deploy"

Your app will be live at: https://ravichange.onrender.com

## Option 2: Railway.app

1. Go to https://railway.app and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python
5. Set environment variable: PORT = 5000
6. Deploy!

## Option 3: Fly.io (Free)

1. Install flyctl: `winget install flyctl`
2. Run: `fly launch`
3. Follow prompts
4. Deploy with: `fly deploy`
