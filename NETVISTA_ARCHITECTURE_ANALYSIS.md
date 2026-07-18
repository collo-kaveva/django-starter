# NetVista - Starter Project Architecture Analysis

## Phase 1 Analysis Summary

### Project Structure
- **Django Version**: Django 6.0+ (Python 3.14)
- **Project Type**: Django starter template inherited from SaaS Pegasus
- **Package Manager**: uv for Python, npm for JavaScript
- **Architecture**: Monolithic Django with modular apps structure

### Key Technologies & Packages

#### Backend
- **Django 6.0+**: Web framework
- **django-allauth**: Authentication system (email-based login, signup, password reset)
- **Django Rest Framework**: API framework
- **drf-spectacular**: OpenAPI schema generation
- **Celery**: Background tasks and scheduled jobs
- **django-celery-beat**: Database-backed periodic task scheduler
- **django-environ**: Environment variable management
- **django-htmx**: HTMX integration
- **django-vite**: Frontend asset integration
- **psycopg**: PostgreSQL adapter

#### Frontend
- **Tailwind CSS v4**: Utility-first CSS framework
- **DaisyUI**: Component library built on Tailwind
- **Alpine.js**: Lightweight JavaScript framework for reactivity
- **HTMX**: Enhanced HTML for dynamic interactions
- **Vite**: Frontend build tool and dev server
- **Chart.js**: Charting library (already included)
- **@fortawesome/fontawesome-free**: Icon library

#### Development Tools
- **ruff**: Python linting and formatting
- **mypy**: Static type checking
- **pre-commit**: Git hooks
- **django-debug-toolbar**: Debugging tool
- **django-browser-reload**: Auto-reload during development

### Authentication System

#### Custom User Model
- **Location**: `apps.users.models.CustomUser`
- **Base**: `AbstractUser` from Django
- **Additional Fields**: 
  - `avatar` (FileField with validation)
- **Features**:
  - Email-based authentication (username disabled)
  - Profile picture upload with Gravatar fallback
  - Email verification support (configurable)
  - Terms agreement during signup
  - Turnstile captcha integration (optional)

#### Authentication Flow
- **Library**: django-allauth
- **Login Methods**: Email only
- **Signup Fields**: Email, password
- **Built-in Views**:
  - Registration/Signup
  - Login/Logout
  - Password Reset
  - Password Change
  - Email Confirmation
- **Custom Views**:
  - Profile management (`apps.users.views.profile`)
  - Profile image upload (`apps.users.views.upload_profile_image`)

### Settings Configuration

#### Three-Tier Settings Structure
1. **base.py**: Shared settings for all environments
2. **dev.py**: Local development overrides (minimal, just imports base)
3. **prod.py**: Production-specific settings

#### Key Configuration Details
- **Development**: SQLite database, DummyCache, eager Celery
- **Production**: PostgreSQL, Redis cache/broker, real Celery worker
- **Static Files**: Django-vite integration with Vite dev server in DEBUG
- **Media Files**: FileSystemStorage to `/media` directory
- **Security**: WhiteNoise middleware, SSL headers in production

### Frontend Architecture

#### Asset Organization
- **JavaScript**: `assets/javascript/`
  - `site.js`: Main site-wide scripts
  - `app.js`: Application-specific scripts
  - `alpine.js`: Alpine.js initialization
  - `htmx.js`: HTMX configuration
  - `csrf.js`: CSRF token handling
  - `api.js`: API client integration
  - `logout.js`: Logout functionality

- **Styles**: `assets/styles/`
  - `site-base.css`: Base styles
  - `site-tailwind.css`: Tailwind + DaisyUI integration
  - `app/tailwind/`: App-specific components
  - `pegasus/`: Pegasus framework styles

#### Build System
- **Vite**: Modern build tool with HMR
- **Configuration**: `vite.config.ts`
- **Output**: `static/` directory with manifest.json
- **Dev Server**: Port 5173 (configurable)
- **Integration**: django-vite template tags

#### Tailwind + DaisyUI Integration
- **Tailwind Version**: v4 (latest)
- **DaisyUI**: Component library
- **Custom Components**: Defined in `assets/styles/app/tailwind/app-components.css`
- **Theme**: Light/dark mode support via `data-theme` attribute
- **Font**: IBM Plex Mono (mono font for everything)

### Template Structure

#### Base Templates
- **base.html**: Main site template with navigation and footer
- **app/app_base.html**: Application-specific base with sidebar navigation
- **app_home.html**: Default logged-in home page

#### Component Templates
- **top_nav.html**: Main navigation with mobile drawer
- **top_nav_app.html**: App-specific navigation
- **app_nav.html**: Sidebar navigation
- **app_nav_menu_items.html**: Navigation menu items
- **messages.html**: Django messages display
- **footer.html**: Site footer
- **hero.html**: Hero section component
- **feature_highlight.html**: Feature showcase
- **cta.html**: Call-to-action component

#### Template Features
- **Alpine.js Integration**: Interactive components
- **HTMX Integration**: Dynamic content loading
- **DaisyUI Components**: Pre-built UI components
- **Responsive Design**: Mobile-first approach
- **Theme Support**: Light/dark mode switching

### URL Organization

#### Main URL Configuration
- **Location**: `config/urls.py`
- **Structure**:
  - `/admin/` → Django admin
  - `/accounts/` → django-allauth URLs
  - `/users/` → User profile URLs
  - `/` → Main web application
  - `/api/schema/` → API documentation
  - `/celery-progress/` → Celery progress tracking

#### App-Specific URLs
- **apps.web.urls**: Home, terms, error pages
- **apps.users.urls**: Profile, image upload

### Database Models

#### Base Model
- **Location**: `apps.utils.models.BaseModel`
- **Fields**: `created_at`, `updated_at`
- **Usage**: All project models should extend this

#### Custom User Model
- **Location**: `apps.users.models.CustomUser`
- **Inheritance**: `AbstractUser`
- **Additional**: Avatar field with validation

#### Model Conventions
- All models should extend `BaseModel`
- Use `CustomUser` for user references
- Timestamps automatic via `BaseModel`

### Static & Media File Handling

#### Static Files
- **Development**: Served by Vite dev server
- **Production**: Served by WhiteNoise middleware
- **Location**: `static/` directory
- **Build Output**: `static/js/`, `static/css/`, `static/assets/`
- **Manifest**: `static/.vite/manifest.json`

#### Media Files
- **Location**: `media/` directory (created on demand)
- **URL**: `/media/`
- **Storage**: FileSystemStorage
- **Upload**: Profile pictures go to `media/profile-pictures/`

### Deployment Configuration

#### Docker Setup
- **Multi-stage Build**: 
  - Stage 1: Node.js for frontend build
  - Stage 2: Python for application
- **Services**:
  - `web`: Gunicorn web server
  - `celery`: Celery worker + beat
  - `db`: PostgreSQL 17
  - `redis`: Redis 7 with persistence
- **Volumes**: PostgreSQL data, Redis data, media files
- **Configuration**: `.env.prod` file

#### Production Settings
- **Database**: PostgreSQL required
- **Cache**: Redis
- **Static Files**: WhiteNoise with compression
- **Security**: SSL headers, secure cookies
- **Workers**: Gunicorn (3 workers by default)
- **Process Management**: Docker Compose

### Existing Utilities & Helpers

#### User Helpers
- **Location**: `apps/users/helpers.py`
- **Functions**: Profile picture validation, email confirmation helpers

#### Context Processors
- **Location**: `apps/web/context_processors.py`
- **Provided**: Project metadata, CSRF settings, Google Analytics ID

#### Template Tags
- **Location**: `apps/web/templatetags/`
- **Available**: Meta tags, form tags

#### Management Commands
- **runserver**: Custom dev server with auto-superuser creation
- **send_test_email**: Email testing
- **bootstrap_celery_tasks**: Initialize scheduled tasks

### Development Workflow

#### First-time Setup
```bash
make init  # Copy .env, install dependencies, create database
```

#### Running Development
```bash
# Terminal 1
make start  # Django dev server

# Terminal 2
make npm-dev  # Vite dev server
```

#### Common Commands
- `make migrations`: Create migrations
- `make migrate`: Apply migrations
- `make test`: Run tests
- `make ruff`: Format and lint
- `make shell`: Django shell
- `make npm-build`: Build frontend assets

### Architectural Decisions for NetVista

#### What to Reuse
1. **Authentication System**: Complete django-allauth setup fits requirements perfectly
2. **Custom User Model**: Already has avatar field, can extend with role/bio
3. **Template Structure**: Base templates and components provide solid foundation
4. **Frontend Stack**: Tailwind + DaisyUI + Alpine.js + HTMX is ideal for requirements
5. **Settings Architecture**: Three-tier settings perfect for dev/prod split
6. **Deployment Setup**: Docker Compose ready for production deployment
7. **Base Model**: Use for all NetVista models
8. **Chart.js**: Already included for dashboard charts

#### What to Extend
1. **User Model**: Add role field, bio, full name requirements
2. **Authentication**: Add role-based access control
3. **Templates**: Create NetVista-specific dashboard layouts
4. **URL Structure**: Add NetVista app URLs
5. **Models**: Create device, network, alert, traffic models
6. **Views**: Implement dashboard, device management, settings views
7. **API**: Add DRF endpoints for AJAX interactions
8. **Sample Data**: Create management command for demo data generation

#### What to Add
1. **New Django App**: `apps.network` for NetVista-specific functionality
2. **PWA Support**: manifest.json, service worker, offline functionality
3. **Role System**: Django groups or custom role field
4. **Dashboard Widgets**: Custom components for network stats
5. **Device Management**: CRUD operations with search/filter
6. **Charts Integration**: Chart.js for traffic analytics
7. **Sample Data Generator**: Custom management command
8. **PWA Assets**: Icons, theme colors, manifest

### Technology Fit Assessment

#### Perfect Match
- **Django**: Ideal for complex business logic and admin interface
- **django-allauth**: Meets all authentication requirements
- **Tailwind + DaisyUI**: Perfect for modern, responsive UI
- **Alpine.js**: Great for client-side interactivity
- **HTMX**: Excellent for progressive enhancement
- **Chart.js**: Perfect for dashboard analytics
- **SQLite/PostgreSQL**: Meets database requirements

#### Needs Addition
- **PWA Tools**: Need to add service worker and manifest
- **Role Management**: Extend existing auth system
- **Sample Data**: Create custom management command

#### No Changes Needed
- **Build System**: Vite integration is excellent
- **Deployment**: Docker setup is production-ready
- **Development Workflow**: Make commands are comprehensive
- **Code Quality**: Ruff, mypy, pre-commit hooks configured

### Next Steps for NetVista Implementation

1. **Create Network App**: Set up `apps.network` with models for devices, alerts, traffic
2. **Extend User Model**: Add role field and additional profile fields
3. **Implement RBAC**: Set up Django groups for Administrator/Technician roles
4. **Create Dashboard**: Build main dashboard with widgets and charts
5. **Device Management**: Implement CRUD with search/filter functionality
6. **Add PWA Support**: Create manifest, service worker, offline page
7. **Generate Sample Data**: Create management command for demo data
8. **Test Authentication**: Verify all auth flows work with role restrictions
9. **Build Deployment**: Configure for chosen hosting platform
10. **Documentation**: Update README with NetVista-specific information

### Conclusion

The starter template provides an excellent foundation for NetVista:

- **Strengths**: Modern tech stack, solid architecture, deployment-ready, comprehensive auth
- **Fit**: 95% match with NetVista requirements
- **Effort**: Minimal architectural changes required, mostly feature additions
- **Risk**: Low - reusing proven patterns and technologies

The main work will be building NetVista-specific features rather than restructuring the foundation.