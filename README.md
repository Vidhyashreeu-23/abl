# CampusConnect

A comprehensive Django web application for college students to discover, join, and participate in campus clubs, with event management and community features.

## Features

- **User Authentication**: Custom user model with profiles, skills, and interests
- **Club Management**: Create, join, and manage campus clubs with categories
- **Event System**: Organize and register for club events
- **Posts & Announcements**: Club admins can create posts and announcements
- **Reviews & Ratings**: Members can review clubs with star ratings
- **Admin Panel**: Full Django admin integration for all models
- **Responsive Design**: Bootstrap 5 frontend with crispy forms

## Tech Stack

- Django 4.2+
- Django REST Framework (optional for AJAX)
- SQLite (default, switchable to PostgreSQL)
- Bootstrap 5
- Pillow for image uploads
- django-crispy-forms with crispy-bootstrap5

## Installation

1. **Clone or download the project**
   ```bash
   cd /path/to/your/workspace
   # The project is already set up in d:\Django
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```
   Or use the pre-created admin account:
   - Username: `admin`
   - Email: `admin@example.com`
   - Password: `admin123`

5. **Seed sample data (optional)**
   ```bash
   python manage.py seed_data
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Homepage: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
campusconnect/
├── manage.py
├── requirements.txt
├── campusconnect/          # Main config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/               # User auth & profiles
├── clubs/                  # Club management
├── events/                  # Events management
├── posts/                  # Club posts/announcements
├── reviews/                # Ratings & reviews
├── templates/              # All HTML templates
├── static/                 # CSS, JS, images
└── media/                  # Uploaded files
```

## Key Features

### User Management
- Registration with college and graduation year
- Profile editing with skills, interests, and profile pictures
- Public profiles showing club memberships

### Club System
- Browse clubs by category or search
- Join/leave clubs with membership tracking
- Club admins can create events and posts
- Member management with roles (member, admin, president)

### Events
- Create events for clubs (admin only)
- Register for events
- Filter events by club, date, or search

### Posts & Comments
- Club admins can create posts/announcements
- Members can comment on posts
- Pinned posts for important announcements

### Reviews
- Members can review clubs with ratings (1-5 stars)
- Average rating calculation for clubs
- Review management (edit/delete own reviews)

## Admin Panel

Access the Django admin at `/admin/` with superuser credentials to manage:
- Users, clubs, events, posts, reviews
- Categories, skills, interests
- Memberships and registrations

## API Endpoints

The application includes RESTful URL patterns for all features:
- `/accounts/` - User management
- `/clubs/` - Club browsing and management
- `/events/` - Event listing and registration
- `/posts/` - Club posts and comments
- `/reviews/` - Club reviews

## Development Notes

- Uses Django's built-in authentication with custom user model
- Crispy forms for form rendering with Bootstrap 5
- Template tags for membership and admin checks
- Signals for automatic club creator assignment
- Pagination for large lists
- Star rating display in templates

## Production Deployment

For production:
1. Set `DEBUG = False`
2. Configure `ALLOWED_HOSTS`
3. Use PostgreSQL instead of SQLite
4. Set up static/media file serving
5. Use a production WSGI server (gunicorn, uwsgi)
6. Configure email settings for notifications

## License

This project is for educational purposes.