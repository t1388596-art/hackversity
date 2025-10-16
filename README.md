# Django GenAI Application - Development Environment

A Django-based generative AI application with user authentication and conversation management, **optimized specifically for local development**.

## 🚀 Features

- **Simple Setup**: SQLite database, no external dependencies
- **User Authentication**: Registration, login with django-allauth
- **AI Chat Interface**: Powered by Euron API (GPT-4.1-nano)
- **Learning Modules**: Dynamic learning content system with video tutorials
- **Admin-Managed Content**: Create and manage learning modules through admin panel
- **Development Optimized**: Debug mode, console logging, relaxed security
- **Responsive Design**: Works on desktop and mobile
- **Admin Interface**: Full Django admin panel

## 🔧 Quick Development Setup

### Prerequisites
- Python 3.9+ (tested with Python 3.13.5)

### 1. Setup Environment
```cmd
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key
```cmd
# Create .env file from example
copy .env.example .env

# Edit .env file and add your Euron API key:
# EURON_API_KEY=your-api-key-here
```

### 3. Initialize Database
```cmd
# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

### 4. Start Development Server
```cmd
python manage.py runserver
```

## 🌐 Application URLs

- **Homepage**: http://127.0.0.1:8000/
- **Chat Interface**: http://127.0.0.1:8000/chat/
- **Learning Hub**: http://127.0.0.1:8000/chat/learning/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **User Registration**: http://127.0.0.1:8000/accounts/signup/
- **API Endpoints**: http://127.0.0.1:8000/api/

## 🛠️ Development Features

### Optimized for Development
- **SQLite Database**: Fast, file-based database
- **Debug Mode**: Always enabled with detailed error pages
- **Console Email**: Emails print to terminal (no SMTP needed)
- **Simple Auth**: Username-based authentication
- **Relaxed Passwords**: Allows simple passwords like "test123"
- **Verbose Logging**: Detailed console output

### Learning Module System
- **Dynamic Content**: Create learning modules through admin panel
- **Video Integration**: YouTube video embedding
- **Custom Icons**: Font Awesome icon selection
- **Flexible Ordering**: Control module and video display order
- **Active/Inactive Toggle**: Show/hide content without deletion

### Available Commands
```cmd
# Start development server
python manage.py runserver

# Database operations
python manage.py migrate
python manage.py createsuperuser

# Django shell
python manage.py shell

# Check for issues
python manage.py check
```

## 📁 Clean Project Structure

```
Hackversity 2.0/
├── genai_project/          # Django settings (development-optimized)
├── chat/                   # AI chat functionality
├── accounts/               # User authentication
├── static/                 # CSS, JavaScript, images
├── templates/              # HTML templates
├── db.sqlite3             # SQLite database
├── .env                   # Environment variables
├── requirements.txt       # Development dependencies only
└── manage.py              # Django management
```

## ⚠️ Development Only

**This configuration is optimized for development only:**
- Debug mode always enabled
- Simple SQLite database
- No production security settings
- Console email backend
- Relaxed authentication

## 🐛 Troubleshooting

**Database Issues**: Delete `db.sqlite3` and run `python manage.py migrate`  
**Module Errors**: Ensure virtual environment is activated  
**API Errors**: Check your Euron API key in `.env` file  
**Learning Modules Not Showing**: 
- Check if modules are marked as "Active" in admin
- Visit http://127.0.0.1:8000/admin/chat/learningmodule/
- Ensure at least one module exists and is active

## 🎓 Managing Learning Modules

### Creating a Learning Module:
1. Login to admin: http://127.0.0.1:8000/admin/
2. Navigate to: **Chat** > **Learning modules** > **Add learning module**
3. Fill in the details:
   - **Title**: Module name
   - **Slug**: URL-friendly name (auto-generated)
   - **Description**: Brief overview
   - **Icon**: Choose Font Awesome icon
   - **Order**: Display order (lower = first)
   - **Is active**: Check to make visible
4. Add videos using the inline form (YouTube ID required)
5. Save and visit: http://127.0.0.1:8000/chat/learning/

Your module will appear immediately on the learning page!

## 📝 License

This project is configured for development and learning purposes.