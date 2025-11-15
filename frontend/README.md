# Welcome to your Lovable project

## Project info

**URL**: https://lovable.dev/projects/a29fe00f-99cf-4439-8659-16b5f3b57233

## How can I edit this code?

There are several ways of editing your application.

**Use Lovable**

Simply visit the [Lovable Project](https://lovable.dev/projects/a29fe00f-99cf-4439-8659-16b5f3b57233) and start prompting.

Changes made via Lovable will be committed automatically to this repo.

**Use your preferred IDE**

If you want to work locally using your own IDE, you can clone this repo and push changes. Pushed changes will also be reflected in Lovable.

The only requirement is having Node.js & npm installed - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

Follow these steps:

```sh
# Step 1: Clone the repository using the project's Git URL.
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory.
cd <YOUR_PROJECT_NAME>

# Step 3: Install the necessary dependencies.
npm i

# Step 4: Start the development server with auto-reloading and an instant preview.
npm run dev
```

**Edit a file directly in GitHub**

- Navigate to the desired file(s).
- Click the "Edit" button (pencil icon) at the top right of the file view.
- Make your changes and commit the changes.

**Use GitHub Codespaces**

- Navigate to the main page of your repository.
- Click on the "Code" button (green button) near the top right.
- Select the "Codespaces" tab.
- Click on "New codespace" to launch a new Codespace environment.
- Edit files directly within the Codespace and commit and push your changes once you're done.

## What technologies are used for this project?

This project is built with:

**Frontend:**
- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

**Backend:**
- FastAPI
- Google Gemini AI
- Python 3.8+

## Backend Setup

The backend is a FastAPI server that generates Amazon product listings from Instagram posts using Google's Gemini AI.

### Prerequisites

1. Python 3.8 or higher
2. Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. Navigate to the backend directory:
```sh
cd backend
```

2. Create a virtual environment:
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```sh
pip install -r requirements.txt
```

4. Create a `.env` file in the backend directory:
```sh
GEMINI_API_KEY=your_gemini_api_key_here
```

5. Run the server:
```sh
uvicorn main:app --reload --port 8000
```

Or use the provided script:
```sh
chmod +x run.sh
./run.sh
```

The API will be available at `http://localhost:8000`

Note: the frontend Vite dev server is configured to run on port 8080 in this project. During development the frontend will proxy requests to the backend so you can call /api/* from the client without CORS issues. You can override the backend base URL used by the frontend by creating a `.env` file at the project root (for Vite) with:

```ini
VITE_API_URL=http://localhost:8000
```

### API Endpoints

- `POST /api/generate-listing` - Generate Amazon listing from Instagram post
- `GET /health` - Health check endpoint
- `GET /` - API information

See `backend/README.md` for more detailed API documentation.

## How can I deploy this project?

Simply open [Lovable](https://lovable.dev/projects/a29fe00f-99cf-4439-8659-16b5f3b57233) and click on Share -> Publish.

## Can I connect a custom domain to my Lovable project?

Yes, you can!

To connect a domain, navigate to Project > Settings > Domains and click Connect Domain.

Read more here: [Setting up a custom domain](https://docs.lovable.dev/features/custom-domain#custom-domain)
