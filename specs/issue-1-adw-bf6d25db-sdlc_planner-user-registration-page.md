# Feature: User Registration Page

## Metadata
issue_number: `1`
adw_id: `adw-bf6d25db`
issue_json: `{"body":"Create a Registartion page for my app.It should contain email and password.","number":1,"title":"Login Page"}`

## Feature Description
This feature adds a user registration page to the Natural Language SQL Interface application. The page will allow new users to create accounts by providing an email address and password. This is the foundational authentication feature that will enable user account management, data persistence per user, and secure access control. The registration page will include form validation, secure password handling, and proper error messaging to ensure a smooth user onboarding experience.

## User Story
As a new user
I want to create an account with my email and password
So that I can securely access and manage my own data in the Natural Language SQL Interface application

## Problem Statement
Currently, the Natural Language SQL Interface application has no user authentication or account management. All users share the same database instance, which creates security and privacy concerns. There is no way to:
- Distinguish between different users
- Protect user data and queries
- Provide personalized experiences
- Implement access control

## Solution Statement
Implement a user registration page that collects email and password credentials, validates the input, securely hashes passwords, stores user data in a dedicated users table in the SQLite database, and provides appropriate feedback for successful registration or validation errors. This will establish the foundation for a complete authentication system (login, session management, and protected routes will be added in future features).

## Relevant Files
Use these files to implement the feature:

### Backend Files
- `app/server/server.py` - Add new registration endpoint `/api/auth/register` that handles user registration requests
- `app/server/core/data_models.py` - Add Pydantic models for registration request/response (`RegisterRequest`, `RegisterResponse`)
- `app/server/pyproject.toml` - Dependencies are managed here; may need to add `passlib[bcrypt]` for password hashing

### Frontend Files
- `app/client/src/main.ts` - Add registration form initialization, event handlers, and API integration for the registration flow
- `app/client/src/style.css` - Add styles for registration form, input fields, validation messages, and layout matching existing design patterns
- `app/client/index.html` - Add registration form HTML structure (form fields, submit button, validation messages)
- `app/client/src/api/client.ts` - Add `register()` API client function to communicate with the backend registration endpoint
- `app/client/src/types.d.ts` - Add TypeScript types for registration request/response

### Database
- SQLite database (`app/server/db/database.db`) - Will store user credentials in a new `users` table with proper schema

### New Files
- `.claude/commands/e2e/test_registration.md` - E2E test specification to validate the registration page functionality end-to-end

## Implementation Plan
### Phase 1: Foundation
Set up the backend infrastructure for user authentication including:
- Install password hashing library (`passlib[bcrypt]`)
- Create database schema for users table with fields: id (primary key), email (unique), password_hash, created_at
- Define Pydantic data models for registration API
- Implement password hashing utility functions

### Phase 2: Core Implementation
Build the registration functionality on both backend and frontend:
- Create `/api/auth/register` endpoint that validates email format, checks for duplicate emails, hashes passwords, and stores user records
- Build registration form UI with email and password input fields following existing design patterns
- Implement client-side validation (email format, password requirements)
- Add API client function to communicate with registration endpoint
- Implement error handling and user feedback for both success and failure scenarios

### Phase 3: Integration
Connect all components and ensure proper flow:
- Wire up frontend form submission to backend API endpoint
- Test complete registration flow from form input to database storage
- Add navigation between registration and main application (placeholder for now)
- Ensure responsive design and accessibility
- Create comprehensive E2E test to validate the entire registration flow

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Install Dependencies
- Navigate to `app/server/` directory
- Run `uv add "passlib[bcrypt]"` to install password hashing library
- Verify installation by checking `pyproject.toml` and `uv.lock`

### Step 2: Create User Authentication Models
- Open `app/server/core/data_models.py`
- Add `RegisterRequest` model with fields: `email: str`, `password: str`
- Add `RegisterResponse` model with fields: `user_id: int`, `email: str`, `created_at: datetime`, `error: Optional[str]`
- Add validation to `RegisterRequest` for email format using Pydantic validators
- Add password strength requirements (minimum 8 characters)

### Step 3: Create Database Schema and Utilities
- Create new file `app/server/core/auth.py` for authentication utilities
- Implement `hash_password(password: str) -> str` function using `passlib.hash.bcrypt`
- Implement `verify_password(plain_password: str, hashed_password: str) -> bool` function
- Implement `create_users_table()` function to create users table with schema:
  - `id` INTEGER PRIMARY KEY AUTOINCREMENT
  - `email` TEXT UNIQUE NOT NULL
  - `password_hash` TEXT NOT NULL
  - `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- Implement `check_email_exists(email: str) -> bool` function to check for duplicate emails

### Step 4: Implement Registration Endpoint
- Open `app/server/server.py`
- Import auth utilities from `core.auth`
- Add startup event handler to ensure users table exists
- Create `POST /api/auth/register` endpoint with the following logic:
  - Validate request using `RegisterRequest` model
  - Check if email already exists in database
  - Hash the password using `hash_password()`
  - Insert new user record into users table
  - Return `RegisterResponse` with user details or error message
- Add comprehensive error handling for database errors, duplicate emails, and validation failures
- Add logging for registration attempts (success and failure)

### Step 5: Create E2E Test Specification
- Create `.claude/commands/e2e/test_registration.md` following the pattern in `test_basic_query.md`
- Define user story: registering a new account
- List test steps:
  1. Navigate to application
  2. Locate registration form
  3. Enter valid email and password
  4. Submit form
  5. Verify success message
  6. Verify error handling for duplicate email
  7. Verify validation for invalid email format
  8. Verify validation for weak password
- Define success criteria
- Specify 4-5 screenshots to capture

### Step 6: Update Frontend Types
- Open `app/client/src/types.d.ts`
- Add `RegisterRequest` interface matching backend model
- Add `RegisterResponse` interface matching backend model
- Ensure types are exported properly

### Step 7: Create API Client Function
- Open `app/client/src/api/client.ts`
- Add `register(email: string, password: string): Promise<RegisterResponse>` function
- Implement POST request to `/api/auth/register` endpoint
- Add proper error handling and response parsing
- Follow existing patterns in the file for consistency

### Step 8: Design Registration Form HTML
- Open `app/client/index.html`
- Add registration form section before or after the main query section (following existing structure)
- Create form with:
  - Email input field (type="email", id="register-email", required)
  - Password input field (type="password", id="register-password", required, minlength="8")
  - Submit button (id="register-button")
  - Success message container (id="register-success", hidden initially)
  - Error message container (id="register-error", hidden initially)
- Use semantic HTML and accessibility attributes (labels, aria-labels, etc.)
- Initially hide the registration form or place it in a modal similar to the upload modal

### Step 9: Style Registration Form
- Open `app/client/src/style.css`
- Add styles for `.registration-form` container matching existing `.query-section` design
- Style input fields for email and password using existing input patterns
- Add styles for `.register-button` using existing `.primary-button` styles
- Add success message styles (green theme, similar to upload success)
- Add error message styles (red theme, using existing `.error-message` patterns)
- Ensure responsive design for mobile devices
- Add focus states and validation feedback styling

### Step 10: Implement Registration Form Logic
- Open `app/client/src/main.ts`
- Create `initializeRegistration()` function
- Get references to form elements (email input, password input, submit button)
- Add submit event handler that:
  - Prevents default form submission
  - Validates email format client-side
  - Validates password strength (minimum 8 characters)
  - Disables form during submission
  - Calls `api.register()` with email and password
  - Displays success message on successful registration
  - Displays error message on failure (duplicate email, server error, etc.)
  - Re-enables form after completion
- Call `initializeRegistration()` in the `DOMContentLoaded` event listener
- Add debouncing to prevent double submissions

### Step 11: Add Navigation Between Registration and Main App
- Update `app/client/index.html` to add navigation links
- Add "Already have an account? Login" link (placeholder for now)
- Add "Create an account" link in the main interface to show registration form
- Update `app/client/src/main.ts` to handle showing/hiding registration form
- Implement simple toggle between registration view and main application view

### Step 12: Run Validation Commands
- Execute all validation commands listed in the `Validation Commands` section to ensure:
  - Backend tests pass with zero regressions
  - Frontend compiles without TypeScript errors
  - Frontend builds successfully for production
  - E2E test validates the registration flow works end-to-end

## Testing Strategy
### Unit Tests
Create unit tests for backend authentication functionality:
- Test `hash_password()` generates valid bcrypt hashes
- Test `verify_password()` correctly validates passwords against hashes
- Test `create_users_table()` creates proper schema
- Test `check_email_exists()` returns correct boolean values
- Test registration endpoint with valid inputs returns success
- Test registration endpoint rejects duplicate emails
- Test registration endpoint rejects invalid email formats
- Test registration endpoint rejects weak passwords
- Test registration endpoint handles database errors gracefully

Create unit tests for frontend validation:
- Test email format validation
- Test password strength validation
- Test API client error handling

### Edge Cases
Test and handle the following edge cases:
- Empty email or password fields
- Email without @ symbol or domain
- Password shorter than 8 characters
- Very long email addresses (255+ characters)
- SQL injection attempts in email field
- Special characters in passwords (should be allowed)
- Concurrent registration attempts with same email
- Database connection failures during registration
- Network errors during API requests
- Form submission while another submission is in progress (debouncing)
- Case sensitivity in email addresses (normalize to lowercase)

## Acceptance Criteria
- User can navigate to registration page/form from main interface
- Registration form contains email input field with type="email"
- Registration form contains password input field with type="password" and minimum length requirement
- Email field validates format client-side before submission
- Password field requires minimum 8 characters
- Submit button is disabled during registration process to prevent double submissions
- Backend endpoint `/api/auth/register` accepts POST requests with email and password
- Backend validates email format and password requirements
- Backend checks for duplicate email addresses before creating account
- Passwords are hashed using bcrypt before storage (never stored in plain text)
- Users table is created in SQLite database with proper schema
- Successful registration returns user details (id, email, created_at) without password
- Duplicate email registration returns clear error message
- Invalid email format returns validation error
- Weak password returns validation error with requirements
- Success message displays on successful registration
- Error messages display for all failure scenarios
- E2E test passes validating complete registration flow
- All existing tests continue to pass (zero regressions)
- Frontend builds without TypeScript errors
- Code follows existing patterns and conventions in the codebase

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

Read `.claude/commands/test_e2e.md`, then read and execute the new E2E `.claude/commands/e2e/test_registration.md` test file to validate the registration functionality works end-to-end.

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend tests to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes
- This implementation focuses solely on registration (creating new accounts). Login functionality, session management, and protected routes will be added in separate features.
- Passwords must be hashed using bcrypt with appropriate salt rounds (default 12). Never store plain text passwords.
- Email addresses should be normalized to lowercase before storage to prevent case-sensitivity issues.
- The registration endpoint should use rate limiting in production to prevent abuse (not implemented in this feature, but noted for future enhancement).
- Consider adding email verification in future iterations (send confirmation email with verification link).
- The users table should use SQLite's built-in AUTOINCREMENT for the id field to ensure unique user IDs.
- Use the existing `sql_security.py` module for any database operations to prevent SQL injection.
- The registration form should be accessible via keyboard navigation and screen readers.
- Consider adding a "Show/Hide Password" toggle in future iterations for better UX.
- The implementation should follow the existing architecture pattern: FastAPI backend with Pydantic models, TypeScript frontend with fetch API, and SQLite for data persistence.
- Since this is the first authentication feature, ensure the foundation is solid and extensible for future auth features (login, logout, session management, password reset, etc.).
