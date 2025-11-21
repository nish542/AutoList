# Deployment Configuration

## Frontend Deployment (Vercel)

**Live URL:** https://auto-list.vercel.app/

### Environment Variables in Vercel

Go to your Vercel project settings and add:

```
VITE_API_URL=https://autolistbackend.happyrock-8cdefed1.centralindia.azurecontainerapps.io
```

### Redeploy Frontend

After any code changes:
```bash
git add .
git commit -m "Update frontend"
git push
```

Vercel will auto-deploy from your GitHub repository.

Or manually:
```bash
cd frontend
vercel --prod
```

## Backend Deployment (Azure Container Apps)

**Live URL:** https://autolistbackend.happyrock-8cdefed1.centralindia.azurecontainerapps.io

### Redeploy Backend

After any code changes:

1. Rebuild and push Docker image:
```bash
cd backend
docker buildx build --platform linux/amd64 -t nish542/autolist-backend:latest --push .
```

2. Update Azure Container App (if not auto-configured):
```bash
az containerapp update \
  --name autolistbackend \
  --resource-group <your-resource-group> \
  --image nish542/autolist-backend:latest
```

Or it will auto-pull the new image on restart.

## Current Configuration

- **Frontend:** Vercel (https://auto-list.vercel.app/)
- **Backend:** Azure Container Apps (https://autolistbackend.happyrock-8cdefed1.centralindia.azurecontainerapps.io)
- **CORS:** Configured to allow Vercel frontend

## Testing Production

Visit: https://auto-list.vercel.app/

1. Go to Dashboard
2. Click "Fetch Instagram Posts" or use direct generation
3. Generate a listing - it should connect to Azure backend
4. Download in JSON/CSV/HTML/PDF formats

## Local Development

```bash
# Frontend (connects to Azure backend)
cd frontend
npm run dev

# Or connect to local backend
echo "VITE_API_URL=http://localhost:8000" > .env.local
npm run dev
```

## Troubleshooting

### CORS Errors
- Backend already configured with `allow_origins=["*"]`
- If issues persist, check Azure Container App logs

### Failed to Fetch
- Verify backend is running: `curl https://autolistbackend.happyrock-8cdefed1.centralindia.azurecontainerapps.io/categories`
- Check if latest image is deployed
- Restart Azure Container App

### Changes Not Reflecting
- **Frontend:** Clear browser cache or hard refresh (Cmd+Shift+R)
- **Backend:** Ensure new Docker image is pushed and pulled by Azure
