# 🚀 UdanMeter (APIx) - Complete Zero-Cost Deployment Guide
### MoSPI & RBI Real-time Airfare Price Index Platform

This guide provides end-to-end instructions for deploying both the FastAPI backend and React Vite frontend to **100% free cloud tiers** with persistent serverless PostgreSQL.

---

## 🏗️ Deployment Architecture

```
                       ┌────────────────────────────────────────┐
                       │           End Users & RBI              │
                       └───────────────────┬────────────────────┘
                                           │
                                           ▼
                       ┌────────────────────────────────────────┐
                       │       Vercel (React Frontend)          │
                       │       https://udanmeter.vercel.app     │
                       └───────────────────┬────────────────────┘
                                           │ HTTPS (API Requests)
                                           ▼
                       ┌────────────────────────────────────────┐
                       │       Render (FastAPI Backend)         │
                       │       https://udanmeter-api.onrender   │
                       └───────────────────┬────────────────────┘
                                           │ SSL Connection Pool
                                           ▼
                       ┌────────────────────────────────────────┐
                       │       Neon (PostgreSQL Database)       │
                       │       Serverless AWS us-east-2         │
                       └────────────────────────────────────────┘
```

| Layer | Platform | Free Tier Benefits | Cost |
| :--- | :--- | :--- | :--- |
| **Database** | [Neon.tech](https://neon.tech) / [Supabase](https://supabase.com) | 0.5 GB Serverless PostgreSQL, branching, auto-sleep | **₹0 / Free** |
| **Backend** | [Render.com](https://render.com) | 750 free instance hours/month, automatic SSL, git auto-deploy | **₹0 / Free** |
| **Frontend** | [Vercel](https://vercel.com) | Unlimited bandwidth for personal/open-source projects, global CDN edge | **₹0 / Free** |

---

## 📋 Pre-requisites: Push Code to GitHub

Make sure all your local commits are pushed to your remote repository:

```bash
git push -u origin main
```

---

## 🗄️ Step 1: Setup Free PostgreSQL Database (Neon.tech)

1. Go to [https://neon.tech](https://neon.tech) and sign up with your GitHub account.
2. Click **Create Project**:
   - **Project Name:** `udanmeter-db`
   - **Postgres Version:** 16 (default)
   - **Region:** Choose closest region (e.g. `AWS - ap-southeast-1` or `us-east-2`).
3. Once created, go to the **Dashboard** and copy your **Connection String**.
   - Make sure **Pooled connection** or direct connection string is selected.
   - Example:
     ```text
     postgresql://neondb_owner:npg_AbCdEf1234@ep-quiet-star-12345.us-east-2.aws.neon.tech/neondb?sslmode=require
     ```

### Initialize Database Tables & Seeds
You have two options:

- **Option A (Automated Python Script):**
  In your local `backend` directory, create a `.env` file with your `DATABASE_URL`:
  ```bash
  DATABASE_URL=postgresql+psycopg2://neondb_owner:YOUR_PASSWORD@ep-xxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
  ```
  Run:
  ```bash
  python init_db.py
  ```

- **Option B (Direct SQL in Neon Console):**
  1. In your Neon dashboard, open **SQL Editor**.
  2. Open [`backend/schema.sql`](file:///c:/Users/hp/Desktop/sih2/backend/schema.sql) from this repository, copy its entire contents, paste it into the editor, and click **Run**.
  3. All 5 tables, indexes, and initial DGCA weights will be created instantly.

---

## ⚙️ Step 2: Deploy Backend to Render.com

1. Sign up at [https://render.com](https://render.com) using your GitHub account.
2. Click **New +** → **Web Service**.
3. Select your repository: `Ramkishangupta/UdanMeter`.
4. Configure the service with these settings:

| Setting | Value |
| :--- | :--- |
| **Name** | `udanmeter-api` |
| **Region** | Singapore / Oregon / Frankfurt (closest to your DB) |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

5. Scroll down to **Environment Variables** and add:

| Key | Value | Example |
| :--- | :--- | :--- |
| `DATABASE_URL` | Your Neon PostgreSQL connection URI | `postgresql+psycopg2://neondb_owner:...@ep-...neon.tech/neondb?sslmode=require` |
| `ENVIRONMENT` | `production` | `production` |
| `CORS_ORIGINS` | `*` (or your Vercel URL once generated) | `https://udanmeter.vercel.app,http://localhost:5173` |
| `LOG_LEVEL` | `INFO` | `INFO` |

6. Click **Create Web Service**.
7. Render will install dependencies and start the app. Once finished, you will receive a URL like:
   `https://udanmeter-api.onrender.com`

### Test Your Backend:
Open your browser and test:
- `https://udanmeter-api.onrender.com/` → Should return HTTP 200 with `"database": "PostgreSQL (Production Pool)"`
- `https://udanmeter-api.onrender.com/docs` → Interactive Swagger API documentation
- `https://udanmeter-api.onrender.com/api/v1/apix/summary` → National Price Index summary payload

---

## ⚡ Step 3: Deploy Frontend to Vercel

1. Sign up / Log in to [https://vercel.com](https://vercel.com) using your GitHub account.
2. Click **Add New...** → **Project**.
3. Select `Ramkishangupta/UdanMeter`.
4. Configure the project:
   - **Framework Preset:** `Vite`
   - **Root Directory:** Click **Edit** and choose `frontend`.
   - **Build Command:** `npm run build` (detected automatically)
   - **Output Directory:** `dist` (detected automatically)

5. Expand the **Environment Variables** section and add:

| Key | Value |
| :--- | :--- |
| `VITE_API_BASE_URL` | `https://udanmeter-api.onrender.com/api/v1` *(replace with your Render backend URL)* |

6. Click **Deploy**.
7. In ~30 seconds, Vercel will deploy your site to a live URL (e.g., `https://udanmeter.vercel.app`).

---

## 🔒 Step 4: Final Security & CORS Lockdown (Post-Deploy)

Once you have your production Vercel frontend URL:
1. Go to your **Render Dashboard** → `udanmeter-api` → **Environment**.
2. Update `CORS_ORIGINS`:
   ```text
   CORS_ORIGINS=https://udanmeter.vercel.app,http://localhost:5173
   ```
3. Click **Save Changes** (Render will auto-restart the service with strict CORS protection).

---

## 🔍 Step 5: Verification Checklist

| Check | Expected Result | Verified |
| :--- | :--- | :---: |
| **API Root** | `GET /` returns `200 OK` and confirms PostgreSQL engine | ⬜ |
| **Swagger UI** | `GET /docs` loads all interactive endpoints | ⬜ |
| **APIx Index** | `GET /api/v1/apix/summary` returns composite index and active basket | ⬜ |
| **Frontend UI** | Vercel URL loads executive dark-mode dashboard without blank screen | ⬜ |
| **Live Charts** | Recharts render 30-day index trend and carrier parity cards | ⬜ |
| **Database Pool** | Neon console shows active connection with `pool_pre_ping` safety | ⬜ |

---

## 🛠️ Troubleshooting & FAQs

### Q1: Render free tier takes 30-50 seconds to respond on the first visit?
> **Answer:** Render free web services spin down after 15 minutes of inactivity. The first request after a sleep period takes ~30-40 seconds for a "cold start". Subsequent requests respond instantly in under 50ms.
> 
> *Tip:* You can use a free pinging service like [UptimeRobot](https://uptimerobot.com) to ping `https://your-api.onrender.com/` every 10 minutes to keep it warm 24/7!

### Q2: Frontend shows "Network Error" or data doesn't load?
> **Check 1:** Ensure `VITE_API_BASE_URL` in Vercel includes `/api/v1` at the end (e.g. `https://your-api.onrender.com/api/v1`).
> 
> **Check 2:** Verify `CORS_ORIGINS` in Render includes your exact Vercel domain without trailing slashes.

### Q3: How to trigger a fresh scraping snapshot in production?
> Send an authorized POST request or execute from the interactive Swagger documentation:
> ```bash
> curl -X POST https://your-backend.onrender.com/api/v1/scrape/trigger
> ```

---

**Developed for:** Smart India Hackathon (SIH 26056)  
**Beneficiary:** Ministry of Statistics and Programme Implementation (MoSPI) & Reserve Bank of India (RBI)
