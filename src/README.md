# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities. Teachers can manage announcements and activities.

## Features

- View all available extracurricular activities
- Sign up for activities
- **NEW: Database-driven announcements system**
  - Create, read, update, and delete announcements
  - Set start and expiration dates for announcements
  - Priority levels (low, normal, high)
  - Real-time banner display for active announcements
  - Admin management interface for signed-in users

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - Web interface: http://localhost:8000/static/index.html
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

### Activities

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |

### Announcements

| Method | Endpoint                   | Description                                                  | Authentication |
| ------ | -------------------------- | ------------------------------------------------------------ | --------------- |
| GET    | `/announcements/`          | Get all visible announcements (public)                       | No              |
| GET    | `/announcements/all`       | Get all announcements including hidden ones (admin view)     | No*             |
| POST   | `/announcements/`          | Create a new announcement                                    | Recommended     |
| PUT    | `/announcements/{id}`      | Update an existing announcement                              | Recommended     |
| DELETE | `/announcements/{id}`      | Delete an announcement                                       | Recommended     |

*Note: Currently, the API does not enforce authentication server-side, but the UI hides management features from non-authenticated users.

### Announcement Fields

- **title** (string, required): Announcement title
- **message** (string, required): Announcement content
- **start_date** (date, optional): When the announcement becomes visible (YYYY-MM-DD)
- **expiration_date** (date, required): When the announcement stops being displayed (YYYY-MM-DD)
- **priority** (string, optional): Priority level - "low", "normal", or "high" (default: "normal")
- **visible** (boolean, optional): Whether the announcement is visible (default: true)

### Authentication

| Method | Endpoint              | Description                    |
| ------ | --------------------- | ------------------------------ |
| POST   | `/auth/login`         | Login with username and password |
| GET    | `/auth/check-session` | Verify a user session          |

## Data Model

The application uses MongoDB to store the following:

1. **Activities** - Activity name as identifier:
   - Description
   - Schedule and schedule details
   - Maximum number of participants
   - List of enrolled student emails

2. **Teachers** - Username as identifier:
   - Display name
   - Hashed password (Argon2)
   - Role (teacher or admin)

3. **Announcements** - MongoDB ObjectId as identifier:
   - Title
   - Message
   - Start date (optional)
   - Expiration date (required)
   - Priority level
   - Visibility flag
   - Creation timestamp

## Features

### Announcement Management UI

Signed-in users can access the announcements management interface by clicking the 📢 button in the header. The interface includes:

- **Announcements List**: View all announcements with their details and priority levels
- **Add New Announcement**: Form to create new announcements
- **Edit Announcement**: Click the "Edit" button on any announcement to modify it
- **Delete Announcement**: Remove announcements with a confirmation dialog
- **Date Filtering**: Announcements are automatically hidden based on start/expiration dates

### Announcement Banner

Valid announcements are displayed as banners on the main page:
- Shows only announcements that haven't expired
- Respects optional start dates
- Color-coded by priority level
- Updates in real-time

## Default Credentials

For testing, the following credentials are pre-loaded:

- **Username**: `principal` | **Password**: `admin789`
- **Username**: `mrodriguez` | **Password**: `art123`
- **Username**: `mchen` | **Password**: `chess456`

