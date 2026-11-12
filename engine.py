name: TE SE Autonomous Production

on:
  workflow_dispatch:
  schedule:
    - cron: '0 9,18 * * *'

jobs:
  produce-and-publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install Dependencies
        run: |
          sudo apt-get update && sudo apt-get install -y ffmpeg imagemagick
          sed -i 's/rights="none" pattern="@\*"/rights="read|write" pattern="@*"/' /etc/ImageMagick-6/policy.xml || true
          pip install --upgrade pip
          pip install edge-tts moviepy==1.0.3 requests google-api-python-client google-auth-oauthlib
      - name: Run Engine
        env:
          YT_CLIENT_ID: ${{ secrets.YT_CLIENT_ID }}
          YT_CLIENT_SECRET: ${{ secrets.YT_CLIENT_SECRET }}
          YT_REFRESH_TOKEN: ${{ secrets.YT_REFRESH_TOKEN }}
          PEXELS_API_KEY: ${{ secrets.PEXELS_API_KEY }}
        run: python engine.py
      - name: Save Backup Artifact
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: te-se-latest-video
          path: final_short.mp4
          if-no-files-found: ignore
