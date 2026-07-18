# NetVista - Modern Network Management Dashboard Simulator

> A modern, responsive network management dashboard simulator inspired by professional router interfaces like Tenda, TP-Link Omada, UniFi Network, and Cisco Meraki.

NetVista is a **simulation-only** application designed for demonstration and educational purposes. It does not access, scan, or control real networks. All devices, analytics, traffic data, and statistics are generated from the application's database.

## Features

### Core Functionality
- **Interactive Dashboard**: Real-time network statistics with charts and widgets
- **Device Management**: Full CRUD operations for network devices
- **Device Groups**: Organize devices into logical groups (Office, Home, Guests, IoT, etc.)
- **Network Settings**: Simulated WiFi, DHCP, DNS, and LAN configuration
- **Alerts System**: Real-time network alerts with severity levels
- **Traffic Analytics**: Historical traffic logs with Chart.js visualization
- **Search & Filtering**: Advanced device search with multiple filter options
- **Role-Based Access Control**: Administrator and Technician user roles

### User Management
- **Complete Authentication Flow**: Registration, login, logout, password reset
- **Profile Management**: Update profile information and avatar
- **User Roles**: 
  - **Network Administrator**: Full access to all features
  - **Network Technician**: Read-only access with limited device management

### Technical Features
- **Progressive Web App (PWA)**: Installable with offline support
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Modern UI**: Built with Tailwind CSS v4 and DaisyUI
- **Real-time Updates**: HTMX for dynamic content loading
- **Interactive Components**: Alpine.js for client-side interactivity
- **Data Visualization**: Chart.js for traffic analytics and network statistics

## Technology Stack

### Backend
- **Django 6.0+**: Python web framework
- **django-allauth**: Authentication system
- **Django Rest Framework**: API framework
- **Celery**: Background tasks and scheduled jobs
- **PostgreSQL**: Production database (SQLite for development)

### Frontend
- **Tailwind CSS v4**: Utility-first CSS framework
- **DaisyUI**: Component library for Tailwind
- **Alpine.js**: Lightweight JavaScript framework
- **HTMX**: Enhanced HTML for dynamic interactions
- **Chart.js**: Data visualization library
- **Vite**: Frontend build tool and dev server

### Development Tools
- **uv**: Python package manager
- **npm**: JavaScript package manager
- **ruff**: Python linting and formatting
- **mypy**: Static type checking
- **Docker**: Containerization for production

## Installation

### Prerequisites

Install these once on your machine:

- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** — Python package manager
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **[Node.js](https://nodejs.org/) 20+** — JavaScript runtime
- **`make`** — Build automation tool (preinstalled on macOS/Linux)

### First-time Setup

From the project root:

```bash
make init
```

This single command:
1. Copies `.env.example` → `.env` (if it doesn't exist)
2. Installs Python dependencies with `uv sync`
3. Installs front-end dependencies with `npm install`
4. Creates the SQLite database and applies migrations
5. Sets up Django groups for user roles
6. Creates demo accounts for development

### Database Setup

The project uses **SQLite** for local development (no setup required). For production, configure PostgreSQL via the `DATABASE_URL` environment variable.

### Running the Application

Local development needs **two terminals running simultaneously**:

**Terminal 1 — Django backend (port 8000):**
```bash
make start
```

**Terminal 2 — Vite front-end server (port 5173):**
```bash
make npm-dev
```

Visit **[http://localhost:8000](http://localhost:8000/)** to access the application.

> **Note**: The Vite dev server is required for styling. Without it, pages will load unstyled.

## Initial Setup

### 1. Create User Roles

Set up the administrator and technician groups with appropriate permissions:

```bash
make manage ARGS='setup_roles'
```

### 2. Generate Sample Data

Populate the dashboard with realistic demo data:

```bash
make manage ARGS='generate_sample_data'
```

This creates:
- 6 device groups (Office, Home, Guests, Security, IoT, Gaming)
- 50 network devices with realistic data
- Traffic logs for the past 7 days
- 30 network alerts
- Network settings configuration

### 3. Demo Accounts

Demo accounts are automatically created during `make init` for development and testing purposes:

**Administrator**
- Username: `admin`
- Email: `admin@netvista.local`
- Password: `Admin123!`
- Role: Network Administrator (full access to all features)

**Standard User**
- Username: `user`
- Email: `user@netvista.local`
- Password: `User123!`
- Role: Network Technician (read-only access with limited device management)

> **Note**: These accounts are automatically created during project setup and are intended for local development and demo purposes only.

To recreate demo accounts at any time, run:

```bash
make manage ARGS='create_demo_accounts'
```

### 4. Create Additional User Accounts (Optional)

To create additional user accounts manually:

1. Sign up at [http://localhost:8000/accounts/signup/](http://localhost:8000/accounts/signup/)
2. Log in with your credentials
3. The first user is automatically assigned the Technician role
4. Use Django admin to assign Administrator role: [http://localhost:8000/admin/](http://localhost:8000/admin/)

### 5. Assign User Roles (Optional)

To assign a user to a specific role, use the Django shell:

```bash
make shell
```

```python
from django.contrib.auth.models import User, Group

# Get user and group
user = User.objects.get(email="user@example.com")
admin_group = Group.objects.get(name="Administrators")

# Add user to group
user.groups.add(admin_group)
```

## User Roles and Permissions

### Network Administrator
Full access to all features:
- ✅ View and edit all devices
- ✅ Create, update, delete devices
- ✅ Connect, disconnect, block devices
- ✅ Configure network settings
- ✅ Manage device groups
- ✅ View and manage alerts
- ✅ Manage users and permissions

### Network Technician
Limited access for monitoring and basic operations:
- ✅ View all devices and analytics
- ✅ Edit device names
- ✅ View network settings (read-only)
- ✅ View and acknowledge alerts
- ✅ View device groups
- ❌ Cannot change global network settings
- ❌ Cannot manage users
- ❌ Cannot delete devices

## Project Structure

```
django-starter/
├── apps/
│   ├── network/          # NetVista main application
│   │   ├── models.py     # Device, Alert, TrafficLog models
│   │   ├── views.py      # Dashboard, device management views
│   │   ├── forms.py      # Django forms
│   │   ├── admin.py      # Django admin configuration
│   │   ├── urls.py       # URL routing
│   │   ├── decorators.py # Role-based access control
│   │   └── management/   # Django management commands
│   ├── users/            # User authentication and profiles
│   ├── utils/            # Shared utilities and base models
│   └── web/              # Landing pages and base templates
├── config/               # Django settings
│   ├── settings/
│   │   ├── base.py       # Shared settings
│   │   ├── dev.py        # Development settings
│   │   └── prod.py       # Production settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── templates/            # Django templates
│   ├── network/          # NetVista-specific templates
│   └── web/              # Base templates and components
├── static/               # Static files
│   ├── manifest.json     # PWA manifest
│   ├── service-worker.js # Service worker for offline support
│   └── images/           # Images and icons
├── assets/               # Frontend source files
│   ├── javascript/       # JavaScript source
│   └── styles/           # CSS source
└── requirements.txt     # Python dependencies
```

## Common Commands

### Development
```bash
make start                # Run Django dev server
make npm-dev              # Run Vite dev server
make shell                # Open Django shell
make dbshell              # Open database shell
make migrate              # Apply database migrations
make migrations           # Create new migrations
make test                 # Run tests
make ruff                 # Format and lint Python code
```

### Database
```bash
make migrations           # Create migrations
make migrate              # Apply migrations
make dbshell              # Open database shell
```

### Frontend
```bash
make npm-dev              # Run Vite dev server
make npm-build            # Build for production
make npm-install          # Install npm packages
```

### NetVista Specific
```bash
make manage ARGS='setup_roles'         # Set up user roles and permissions
make manage ARGS='generate_sample_data' # Generate sample data
```

## PWA Features

NetVista includes Progressive Web App functionality:

### Installation
- The app can be installed on desktop and mobile devices
- Supports "Add to Home Screen" on iOS and Android
- Provides app-like experience with dedicated icon

### Offline Support
- Service worker caches static assets
- Offline page displays when network is unavailable
- Core functionality remains accessible without internet

### PWA Configuration
- **Manifest**: `/static/manifest.json`
- **Service Worker**: `/static/service-worker.js`
- **Offline Page**: `/network/offline/`

## Deployment

### Production Setup

1. **Configure Environment Variables**
   ```bash
   cp .env.prod.example .env.prod
   # Edit .env.prod with your production values
   ```

2. **Build Production Image**
   ```bash
   make prod-build
   ```

3. **Start Production Stack**
   ```bash
   make prod-start      # Foreground
   make prod-start-bg   # Background
   ```

4. **Stop Production Stack**
   ```bash
   make prod-stop
   ```

### Production Architecture

The production stack uses Docker Compose with:
- **PostgreSQL 17**: Database
- **Redis 7**: Cache and Celery broker
- **Gunicorn**: WSGI HTTP server
- **Celery**: Background task processing
- **WhiteNoise**: Static file serving

### Hosting Platforms

NetVista is compatible with free hosting platforms:
- **Render**: Full-stack deployment
- **Fly.io**: Container deployment
- **Railway**: Container deployment
- **Heroku**: Container deployment (with add-ons)

## Environment Variables

### Required for Production
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Optional
- `DEBUG`: Enable/disable debug mode
- `EMAIL_BACKEND`: Email configuration
- `GOOGLE_ANALYTICS_ID`: Google Analytics tracking ID

## Email Configuration for Password Reset

NetVista uses Django's built-in email framework for password reset functionality. To enable password reset emails, configure the following environment variables in your `.env` file:

### Basic Email Settings

```bash
# Default sender email address
DEFAULT_FROM_EMAIL="noreply@netvista.local"
SERVER_EMAIL="noreply@netvista.local"

# Email backend
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
```

### SMTP Configuration

**For Gmail:**
```bash
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER="your-email@gmail.com"
EMAIL_HOST_PASSWORD="your-app-password"
```

**For SendGrid:**
```bash
EMAIL_HOST="smtp.sendgrid.net"
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER="apikey"
EMAIL_HOST_PASSWORD="SG.your-sendgrid-api-key"
```

**For Resend:**
```bash
EMAIL_HOST="smtp.resend.com"
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER="resend"
EMAIL_HOST_PASSWORD="your-resend-api-key"
```

### Development Mode

For local development without a real email server, use the console backend (default):

```bash
EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend"
```

This will print emails to the console instead of sending them.

### Testing Password Reset

1. Configure email settings in `.env`
2. Restart the Django server
3. Go to the login page: [http://localhost:8000/accounts/login/](http://localhost:8000/accounts/login/)
4. Click "Forgot your password?"
5. Enter your email address
6. Check your email (or console if using console backend) for the reset link

## Testing

Run the test suite:

```bash
make test                              # Run all tests
make test ARGS='apps.network.tests'    # Run specific app tests
make test ARGS='--keepdb'              # Reuse test database (faster)
```

## Code Quality

Maintain code quality with automated tools:

```bash
make ruff                 # Format and lint Python code
make ruff-format          # Format code only
make ruff-lint            # Lint code only
```

## Troubleshooting

### Styles Not Loading
- Ensure Vite dev server is running: `make npm-dev`
- Check that `node_modules` exists: `make npm-install`
- Verify browser console for errors

### Database Locked
- Close any database connections
- Restart the Django server
- If persistent, delete `db.sqlite3` and run `make init`

### Permission Denied Errors
- Verify user role assignment
- Check group permissions in Django admin
- Ensure `setup_roles` command was run

## Security Notes

- NetVista is a **simulation only** - it does not interact with real networks
- All data is stored locally in the database
- No external network scanning or control is performed
- User authentication follows Django security best practices
- Production deployment requires proper SSL/TLS configuration

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Code Style**: Follow PEP 8 with 120 character line limit
2. **Testing**: Write tests for new features
3. **Documentation**: Update documentation for changes
4. **Commit Messages**: Use clear, descriptive commit messages

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- UI components from [DaisyUI](https://daisyui.com/)
- Authentication powered by [django-allauth](https://django-allauth.readthedocs.io/)
- Icons from [Font Awesome](https://fontawesome.com/)
- Charts powered by [Chart.js](https://www.chartjs.org/)

## Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Check existing documentation
- Review Django and framework documentation

---

**NetVista** - Modern Network Management Dashboard Simulator

*Built for demonstration and educational purposes only.*