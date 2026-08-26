# 🚀 100% Automated 24/7 Social Media Pipeline (Cloud Architecture)

A production-grade, zero-PC-dependent media publishing pipeline running in the cloud via **GitHub Actions** and scheduled cloud triggers. It automatically ingests source videos from a local repository or **Google Drive Vault**, transcodes them with **FFmpeg** to 1080x1920 9:16 vertical MP4 format (`+faststart`, H.264, AAC), generates high-CTR algorithmic SEO packages with 15+ hashtags, and distributes them simultaneously across **YouTube Shorts**, **Instagram Reels**, and **Facebook Reels** 3 times daily (09:00 AM, 02:00 PM, 07:00 PM IST) with full deduplication.

---

## 🌟 Key Architecture Features

- **24/7 Zero-PC Cloud Execution:** Runs entirely on GitHub Actions runners triggered by GitHub Cron or external Webhooks (e.g. Cron-Job.org).
- **Multi-Platform Support:**
  - **YouTube Shorts:** YouTube Data API v3 OAuth 2.0 with automatic token refresh (`token.pickle` base64 decoded at runtime) & resumable chunked upload.
  - **Instagram Reels:** Official Instagram Graph API v19.0 container creation, status polling (`status_code=FINISHED`), and direct publishing.
  - **Facebook Reels:** Facebook Graph API v19.0 Pages Video Reels 3-phase upload (`start`, `transfer`, `finish` with `video_state=PUBLISHED`).
- **Universal FFmpeg Transcoding Pipeline:**
  - Standardized **1080x1920 9:16 vertical** aspect ratio with smart letterboxing/pad & `setsar=1`.
  - H.264 (`yuv420p`), AAC audio (`192k`/`44.1kHz`).
  - `+faststart` flag (relocates the `moov` atom to the head of the file for zero-buffering browser playback).
  - 60-second duration enforcement.
- **Dynamic SEO Engine:**
  - High-CTR viral hooks and slot-specific emojis.
  - 15+ algorithmic search tags & niche-specific hashtag pools (Motivation, Tech, Finance, Fitness, etc.).
  - Platform-tailored descriptions with engagement calls-to-action (CTAs).
- **Infinite Cycle Deduplication:**
  - Tracks uploaded videos in `logs/used_reels.json` via SHA256 checksums and filenames.
  - Auto-commits updated state back to GitHub repository so state persists across ephemeral cloud runs.
  - Automatically resets and increments cycle counter (Cycle 1 -> Cycle 2) when the vault is exhausted.

---

## 📁 Repository Structure

```
social-media-autopilot/
├── .github/
│   └── workflows/
│       └── autopilot.yml            # 24/7 Cloud runner workflow
├── core/
│   ├── __init__.py
│   ├── config.py                    # Environment & Base64 secrets loader
│   ├── deduplicator.py              # Deduplication & JSON state manager
│   ├── logger.py                    # UTF-8 safe dual console/file logging
│   ├── seo_engine.py                # High-CTR title & hashtag generator
│   ├── transcoder.py                # FFmpeg 1080x1920 9:16 +faststart pipeline
│   └── vault.py                     # Local & Google Drive vault ingest
├── uploaders/
│   ├── __init__.py
│   ├── facebook_uploader.py         # Facebook Reels 3-phase API
│   ├── instagram_uploader.py        # Instagram Reels Container API
│   └── youtube_uploader.py          # YouTube Shorts Data API v3
├── scripts/
│   ├── generate_youtube_token.py    # Local OAuth helper to generate secrets
│   └── test_upload_single.py        # CLI dry-run and single video tester
├── content_vault/                   # Store raw video clips here
├── logs/
│   └── used_reels.json              # Deduplication log (Synced via git)
├── unified_master_autopilot.py      # Master slot coordinator
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Deployment Guide

### Step 1: Clone & Configure Locally
```bash
git clone <your-repo-url>
cd social-media-autopilot
pip install -r requirements.txt
cp .env.example .env
```

---

### Step 2: Generate API Credentials

#### 1. YouTube Shorts (OAuth 2.0 Desktop App)
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable the **YouTube Data API v3**.
3. Create an **OAuth 2.0 Client ID** (Application type: *Desktop App*).
4. Download the JSON credentials file and rename it to `client_secrets.json` in your project root.
5. Run the interactive token generator:
   ```bash
   python scripts/generate_youtube_token.py
   ```
6. The script will open your browser to log in, create `token.pickle`, and print two Base64-encoded strings:
   - `YOUTUBE_TOKEN_PICKLE_B64`
   - `YOUTUBE_CLIENT_SECRETS_B64`

#### 2. Instagram Reels & Facebook Reels (Meta Graph API)
1. Go to [Meta for Developers](https://developers.facebook.com/) and create a Business App.
2. Link your Facebook Page and Instagram Professional Account.
3. Generate a long-lived Page Access Token with permissions:
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_posts`
   - `instagram_basic`
   - `instagram_content_publish`
4. Obtain:
   - `INSTAGRAM_ACCOUNT_ID`: Your Instagram Business Account ID
   - `INSTAGRAM_ACCESS_TOKEN`: Long-lived User/Page token
   - `FACEBOOK_PAGE_ID`: Your Facebook Page ID
   - `FACEBOOK_PAGE_ACCESS_TOKEN`: Page access token

---

### Step 3: Configure GitHub Repository Secrets

In your GitHub repository, navigate to:
**Settings** ➔ **Secrets and variables** ➔ **Actions** ➔ **New repository secret**

Add the following secrets:

| Secret Name | Description |
|---|---|
| `YOUTUBE_TOKEN_PICKLE_B64` | Base64 string from `generate_youtube_token.py` |
| `YOUTUBE_CLIENT_SECRETS_B64` | Base64 string of `client_secrets.json` |
| `INSTAGRAM_ACCOUNT_ID` | Instagram Professional Account ID |
| `INSTAGRAM_ACCESS_TOKEN` | Meta Graph API Access Token |
| `FACEBOOK_PAGE_ID` | Facebook Page ID |
| `FACEBOOK_PAGE_ACCESS_TOKEN` | Facebook Page Access Token |
| `VAULT_TYPE` | `local` (or `gdrive`) |
| `NICHE_CATEGORY` | `motivation` / `tech` / `finance` / `fitness` |
| `BRAND_NAME` | Your Brand/Channel name (e.g. `AutoClips`) |

---

### Step 4: Schedule Details (Zero-PC 24/7 Cloud)

The GitHub Actions workflow `.github/workflows/autopilot.yml` runs 3 times daily:

| Slot Name | IST Time (Local) | UTC Schedule (Cron) |
|---|---|---|
| **Morning Slot** | 09:00 AM IST | `30 3 * * *` |
| **Afternoon Slot** | 02:00 PM IST | `30 8 * * *` |
| **Evening Slot** | 07:00 PM IST | `30 13 * * *` |

#### Optional: Guaranteed Cloud Scheduler via Cron-Job.org
To bypass GitHub Actions free-tier cron latency, configure a free webhook on [Cron-Job.org](https://cron-job.org):
- **URL:** `https://api.github.com/repos/<username>/<repo>/dispatches`
- **Method:** `POST`
- **Headers:**
  - `Accept: application/vnd.github.v3+json`
  - `Authorization: Bearer <YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>`
- **Body (JSON):**
  ```json
  {"event_type": "trigger_autopilot"}
  ```

---

## 🧪 Testing the Pipeline

### 1. Test Transcoding & SEO (Dry Run)
```bash
python scripts/test_upload_single.py --dry-run --slot Morning
```

### 2. Test Master Runner (Dry Run)
```bash
python unified_master_autopilot.py --dry-run
```

### 3. Test Single Video Live Upload (YouTube Only)
```bash
python scripts/test_upload_single.py --platform youtube --slot Evening
```

---

## 📊 Deduplication State (`logs/used_reels.json`)
The deduplication state tracks:
- Current active cycle (e.g., Cycle 1)
- Timestamped upload history with SHA256 hashes
- Platform post URLs / Media IDs
- Automatic rollover when all videos in `content_vault/` are posted
