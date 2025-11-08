# College Materials & PYQs Portal

## Overview
A comprehensive Flask-based web portal designed for college students to upload, organize, and download study materials, previous year question papers (PYQs), and academic resources. The application features a hierarchical navigation system organized by course types, departments, semesters, and categories. It also includes a calculator suite and features for managing student clubs, bus routes, canteens, campus places, hostels, upcoming events, and community discussions. The project aims to provide a centralized hub for academic and campus-related information.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### UI/UX Decisions
- **CSS Framework**: Bootstrap 5.3 for responsive design.
- **Icons**: Font Awesome 6.4 for consistent iconography.
- **JavaScript**: Vanilla JavaScript for client-side functionality.
- **Template Engine**: Jinja2.
- **UI Components**: Card-based layouts with table and card view toggles, smooth animations, and hover effects.
- **Design Approach**: Mobile-first responsive design, modern gradient design.

### Technical Implementations
- **Backend Framework**: Flask 3.0+ (Python).
- **Data Storage**: JSON-based file storage (`data.json`, `community.json`, `clubs.json`, `transportation.json`, `canteen.json`, `places.json`, `hostels.json`, `events.json`).
- **File Storage**: Local filesystem (`uploads/` directory with organized structure).
- **Session Management**: Flask's built-in session handling.
- **Web Server**: Gunicorn WSGI server for production.
- **File Management**: Upload, view, download, and delete functionality with secure filename handling.
- **Search**: Comprehensive smart search with live filtering and advanced filter options.
- **Calculators**: GPA, CGPA, Percentage, and Internal Marks calculators.
- **Authentication**: Email-based OTP verification for `@ssn.edu.in` addresses with rate limiting and lockout mechanisms.
- **Role-Based Access**: Database-driven contributor permissions.

### Feature Specifications
- **Hierarchical Navigation**: Course Type → Department → Semester → Category → Files.
- **File Previews**: Integrated viewers for PDF, images, DOCX (via Office Online), and text files.
- **Social Features**: Like/dislike buttons, comment systems, and share functionality for files and community discussions.
- **Community Discussion System**: Create discussions, reply, and sort by various criteria.
- **Campus Management**: Systems for Student Clubs, Bus Routes, Canteens, Campus Places, Hostels, and Upcoming Events, all with admin management and display features.

### System Design Choices
- **JSON over Database**: Chosen for simplicity and rapid prototyping, with prepared SQLAlchemy models for future database migration.
- **File-based Storage**: Direct filesystem storage for uploaded files.
- **Stateless Design**: Allows for horizontal scaling.
- **Security**: Werkzeug secure filename handling, input validation, secure session management, and robust OTP verification.

## External Dependencies

### Python Dependencies
- **Flask**: Web framework.
- **Flask-Mail**: Email service.
- **SQLAlchemy**: Database ORM (for user management and OTP verification).
- **Werkzeug**: File upload security and utilities.
- **Gunicorn**: Production WSGI server.
- **psycopg2-binary**: PostgreSQL database adapter.

### Frontend Dependencies
- **Bootstrap 5.3**: CSS framework (CDN).
- **Font Awesome 6.4**: Icon library (CDN).
- **PDF.js**: For interactive PDF viewing.
- **Microsoft Office Online Viewer**: For DOCX/PPT file previews.

### Development Environment
- **Replit Configuration**: Multi-language support (Python 3.11, Node.js 20, web modules).
- **Nix Packages**: System-level dependencies.