# Deploy on Vercel - Instructions

## Setup Steps:

### 1. Environment Variable
In the Vercel dashboard, you need to add the environment variable:

1. Go to **Settings** → **Environment Variables**
2. Add:
   - **Name**: `TMDB_API_KEY`
   - **Value**: your TMDB API key
   - **Environments**: Production, Preview, Development (select all)

### 2. Build Settings (automatic configuration via vercel.json)
The `vercel.json` file is already configured, but verify it looks like this:
- **Framework Preset**: Other
- **Build Command**: (leave empty)
- **Output Directory**: (leave empty)
- **Install Command**: `pip install -r requirements.txt`

### 3. Redeploy
After adding the environment variable:
1. Go to **Deployments**
2. Click the three dots on the latest deployment
3. Select **Redeploy**

### Troubleshooting

If you continue getting "Oops something wrong" error:

1. **Check the logs**:
   - In Vercel, go to **Deployments** → click on deployment → **Functions**
   - View the function error logs

2. **Test the API Key**:
   - Make sure the TMDB API key is correct
   - Test at: https://api.themoviedb.org/3/genre/movie/list?api_key=YOUR_KEY

3. **Check CORS**:
   - If needed, you may need to add CORS headers

### Getting the TMDB API Key
1. Visit: https://www.themoviedb.org/settings/api
2. Login or create an account
3. Request an API key (it's free)
4. Paste the key in Vercel's environment variables
