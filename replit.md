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
- **Authentication**: Email-based OTP verification for admins and contributors with rate limiting and lockout mechanisms.
- **Role-Based Access**: Three-tier role system (Admin, Contributor, Guest) with granular permission controls.

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

## Deployment Strategy

### Current Deployment
- **Platform**: Replit with autoscale deployment target
- **Server**: Gunicorn binding to 0.0.0.0:5000
- **Port Mapping**: Internal 5000 → External 80
- **Process Management**: Replit workflows with automatic restart and reload capabilities

### Production Considerations
- **Database Migration**: Prepared SQLAlchemy models for PostgreSQL migration
- **File Storage**: Current local storage can be migrated to cloud storage (AWS S3, etc.)
- **Environment Variables**: Session secret and database URL configuration
- **Scaling**: Stateless design allows horizontal scaling with shared storage

### Security Measures
- **File Upload**: Werkzeug secure filename handling
- **Input Validation**: Form validation for all user inputs
- **Session Security**: Configurable secret key for session management
- **OTP Verification**: SHA256 hashed 6-digit codes with 10-minute expiry, 5-attempt rate limiting, 15-minute lockouts
- **Email Verification**: Secure email verification for admins and @ssn.edu.in contributors
- **Role-Based Access**: Three-tier system (Admin, Contributor, Guest) with specific permissions for each role
- **Admin Security**: Admin accounts require OTP verification every login with dedicated dashboard access

## Changelog

- November 8, 2025. **Three-Role Authentication System**: Implemented comprehensive role-based access control with three distinct user roles - Admin (full access with mandatory OTP every login), Contributor (@ssn.edu.in emails with upload permissions), and Guest (view-only access). Admin role is restricted to specific email address (sharruk.cse@gmail.com) with dedicated admin dashboard featuring user statistics, recent activity, and management tools. Updated User model with is_admin property, created get_user_role() function for dynamic role assignment based on email, implemented admin_required decorator for protected routes, modified login flows to assign correct roles on user creation and verification, added role-based redirect logic (admin → dashboard, others → home). Removed hardcoded location details from canteen page (Main Canteen Building address and directions). All permission decorators updated to support three-role hierarchy with admin having full privileges, contributors limited to uploads, and guests restricted to viewing/downloading.
- November 8, 2025. **SSN Canteen Form Update**: Restored "Add New Canteen" form at the top of the page with updated fields - added Google Maps Link field (required), kept Canteen Name (required), Description (optional), and Photo Upload (JPG/PNG only, required), removed Popular Items section per user request, maintained all existing sections (About, Operating Hours, Location with Google Maps button, View Menu & Prices button, Coming Soon features), updated backend to capture and store maps_link field in canteen.json, preserved green food theme and mobile responsive design
- November 8, 2025. **SSN Canteen MVP Update**: Redesigned canteen page to comprehensive MVP version - added About section with canteen description and feature highlights (hygienic food, affordable prices, variety menu), implemented detailed Operating Hours section with breakfast/lunch/snacks timings, integrated Google Maps navigation button for location access, created Popular Items showcase with 4 student favorites (Masala Dosa, Chicken Biriyani, Paneer Paratha, Filter Coffee), added "View Menu & Prices" button placeholder for future food website integration, built Coming Soon section featuring 6 planned features (Ratings & Reviews, Discussion Forum, Live Crowd Status, Pre-Order System, Nutritional Info, Daily Specials Board), added smooth animations and hover effects, implemented admin management section for contributors, modern gradient design with responsive layout
- November 8, 2025. **Replit Import Update**: Refreshed Replit environment setup - installed Python 3.11 with all required dependencies (Flask 3.1+, SQLAlchemy 2.0+, psycopg2-binary, Gunicorn, Flask-Login, Flask-Mail, etc.), configured Flask development workflow on port 5000 with 0.0.0.0 binding and webview output, set up autoscale deployment with Gunicorn (2 workers, port 5000, reuse-port enabled), updated .gitignore to preserve Replit config files, verified server running successfully with all routes accessible