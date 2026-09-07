# Data Tools - Free Data Cleaning & API Management

**Hosted on GitHub Pages for free** with zero configuration.

## How to Deploy (1 hour)
1. Create new GitHub repo: `data-tools`
2. Paste all files above into the repo
3. Go to `Settings` → `Actions` → Create workflow `Deploy to GitHub Pages`
4. Use this workflow (paste below):

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install --no-cache-dir -r requirements.txt

      - name: Build and deploy
        run: |
          gunicorn app:app --bind 0.0.0.0:5000
          cd dist && git init && git remote add origin https://github.com/${{ github.owner }}/${{ github.repository }}.git && git add . && git commit -m
"Deploy" && git push -u origin main
