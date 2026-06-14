# AI Captain Deployment Guide

## 1. Database (Supabase)
1. Create a new project in [Supabase](https://supabase.com/).
2. Go to the **SQL Editor**.
3. Copy and run the contents of `docs/supabase-schema.sql`.
4. Go to **Project Settings > Database** and copy the **Connection String (URI)**. It looks like:
   `postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres`

## 2. Backend (Render)
1. Create a new **Web Service** on [Render](https://render.com/).
2. Connect your GitHub repository.
3. **Root Directory:** `backend`
4. **Environment:** `Python 3`
5. **Build Command:** `pip install -r requirements.txt`
6. **Start Command:** `gunicorn manage:app`
7. **Environment Variables:**
   - `FLASK_ENV`: `prod`
   - `SECRET_KEY`: `[A-LONG-RANDOM-STRING]`
   - `DATABASE_URL`: `[YOUR-SUPABASE-CONNECTION-STRING]`
   - `PYTHON_VERSION`: `3.14.6` (Match your local version if possible, or use a stable 3.12+)

## 3. Frontend (Vercel)
1. Create a new project in [Vercel](https://vercel.com/).
2. Connect your GitHub repository.
3. **Root Directory:** `frontend`
4. **Build Command:** `npm run build`
5. **Output Directory:** `dist`
6. **Environment Variables:**
   - `VITE_API_URL`: `[YOUR-RENDER-SERVICE-URL]/api` (e.g., `https://ai-captain-api.onrender.com/api`)

## 4. Post-Deployment Verification
1. Access your Vercel URL.
2. Register a new user.
3. Calculate a route.
4. Verify the route is saved in your Supabase database.
