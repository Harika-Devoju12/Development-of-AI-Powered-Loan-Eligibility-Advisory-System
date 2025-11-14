# 🚀 Quick Reference Card

## Start Development in 5 Minutes

### Frontend
```bash
# Terminal 1: Frontend
npm install
npm run dev
# Visit: http://localhost:5173
```

### Backend
```bash
# Terminal 2: Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
# Visit: http://localhost:8000/docs
```

### Database
1. Create Supabase project at supabase.com
2. Copy URL and Key to `.env` files
3. Run migration in Supabase SQL Editor
4. Done! ✅

---

## Environment Variables Checklist

### Must Configure
```
# Frontend (.env)
VITE_API_URL=http://localhost:8000

# Backend (backend/.env)
SUPABASE_URL=your-url
SUPABASE_KEY=your-key
JWT_SECRET=your-secret
```

### AWS Services (Optional)
```
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-v2
```

---

## API Quick Test

```bash
# Start session
curl -X POST http://localhost:8000/start-session \
  -H "Content-Type: application/json" \
  -d '{"channel": "chat"}'

# Chat
curl -X POST http://localhost:8000/chat-input \
  -H "Content-Type: application/json" \
  -d '{"session_id": "xxx", "message": "John Doe"}'

# Manager login
curl -X POST http://localhost:8000/manager/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@loanbank.com", "password": "admin123"}'
```

Or use: http://localhost:8000/docs (Swagger UI)

---

## File Structure Overview

```
project/
├── Frontend (React)
│   ├── src/pages/       ← Chat, Upload, Manager pages
│   ├── src/services/    ← API client
│   └── .env             ← Your config
│
├── Backend (FastAPI)
│   ├── main.py          ← API endpoints
│   ├── chat_service.py  ← Chat logic
│   ├── aws_services.py  ← AWS integration ← NEW
│   ├── config.py        ← Configuration ← UPDATED
│   └── .env             ← Your config
│
├── Database
│   └── supabase/        ← Migrations
│
└── Docs
    ├── README.md                ← Start here
    ├── SETUP_GUIDE.md           ← Step-by-step ← NEW
    ├── INTEGRATION_GUIDE.md      ← AWS services ← NEW
    └── UPDATES_SUMMARY.md       ← What changed ← NEW
```

---

## Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/start-session` | POST | Start new app |
| `/chat-input` | POST | Send chat |
| `/verify-aadhaar` | POST | Verify doc |
| `/predict` | POST | Get score |
| `/manager/login` | POST | Manager login |
| `/manager/applications` | GET | List apps |
| `/manager/approve` | POST | Approve app |

---

## Default Credentials (Development Only)

```
Manager Email: admin@loanbank.com
Manager Password: admin123
```

⚠️ Change in production!

---

## Common Commands

```bash
# Development
npm run dev              # Frontend
npm run typecheck       # Type check
npm run lint           # Linting

# Backend
uvicorn main:app --reload    # Dev server
python -m pytest            # Tests (if available)

# Database
# In Supabase SQL Editor:
# Paste migration file

# Docker (optional)
docker build -t loan-api .
docker run -p 8000:8000 --env-file .env loan-api
```

---

## Troubleshooting Fast

```bash
# Can't connect to backend?
curl http://localhost:8000/

# Can't connect to Supabase?
python3 -c "from database import get_supabase; print('OK')"

# Module not found?
pip install -r requirements.txt

# Port already in use?
lsof -i :8000  # Check who uses port
kill -9 <PID>  # Kill process
```

---

## AWS Services Toggle

### Enable Mocks (Default)
```
USE_MOCK_BEDROCK=True
USE_MOCK_TEXTRACT=True
USE_MOCK_SAGEMAKER=True
USE_MOCK_S3=True
```

### Enable Real Services
```
USE_MOCK_BEDROCK=False      # When Bedrock is set up
USE_MOCK_TEXTRACT=False     # When Textract is set up
USE_MOCK_SAGEMAKER=False    # When SageMaker is set up
USE_MOCK_S3=False           # When S3 is set up
```

---

## Important Files to Update

1. ✅ `.env` - Your config
2. ✅ `backend/.env` - Your AWS credentials
3. ✅ `supabase/migrations/*.sql` - Database schema (already in place)
4. ✅ `backend/config.py` - Application settings (already updated)
5. ✅ `backend/aws_services.py` - AWS integration (already created)

---

## Next Actions

- [ ] Copy `.env.example` to `.env`
- [ ] Copy `backend/.env.example` to `backend/.env`
- [ ] Set up Supabase
- [ ] Run migration
- [ ] Start frontend: `npm run dev`
- [ ] Start backend: `uvicorn main:app --reload`
- [ ] Test at http://localhost:5173

---

## Documentation Map

```
README.md
├── Overview & Features
├── Quick Start
└── → SETUP_GUIDE.md (detailed steps)
    └── → INTEGRATION_GUIDE.md (AWS services)
        └── → copilot/context.md (architecture)
```

---

## Resources

- 📚 [FastAPI Docs](https://fastapi.tiangolo.com)
- 🗄️ [Supabase Docs](https://supabase.com/docs)
- ☁️ [AWS Documentation](https://docs.aws.amazon.com)
- ⚛️ [React Docs](https://react.dev)
- 🎨 [Tailwind CSS](https://tailwindcss.com)

---

**Ready to start? Open SETUP_GUIDE.md now! 🚀**
