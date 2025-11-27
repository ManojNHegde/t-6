# Implementation Plan: Login/Registration Page (Issue #1)

## Issue Details
- **Issue Number**: #1
- **Title**: Login Page
- **Description**: Create a Registration page for my app. It should contain email and password.
- **Type**: FEATURE
- **Branch**: feature/issue-1-login-page

## Overview
Implement a complete authentication system with login and registration pages for the Natural Language SQL Interface application. This will include both frontend UI components and backend API endpoints to handle user authentication.

## Current State Analysis
- Application currently has no authentication system
- Frontend is a single-page TypeScript/Vite application (app/client)
- Backend is FastAPI with SQLite database (app/server)
- No user management or session handling exists
- CORS configured for localhost:5173

## Implementation Steps

### Phase 1: Backend - Database & Models

#### 1.1 Create User Database Schema
**Files to create/modify**:
- `app/server/core/auth_models.py` (new)
- `app/server/db/init_auth.py` (new)

**Tasks**:
- Create a `users` table with fields:
  - id (INTEGER PRIMARY KEY AUTOINCREMENT)
  - email (TEXT UNIQUE NOT NULL)
  - password_hash (TEXT NOT NULL)
  - created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
  - last_login (TIMESTAMP)
- Add indexes on email for faster lookups
- Create database initialization script
- Use SQLite as the database (consistent with existing architecture)

#### 1.2 Implement Password Security
**Files to create**:
- `app/server/core/auth_security.py` (new)

**Tasks**:
- Implement password hashing using `passlib` with bcrypt
- Add password validation (minimum 8 characters, at least one letter and one number)
- Create functions for:
  - `hash_password(password: str) -> str`
  - `verify_password(plain_password: str, hashed_password: str) -> bool`

#### 1.3 Session Management
**Files to create**:
- `app/server/core/session_manager.py` (new)

**Tasks**:
- Implement JWT-based session tokens using `python-jose`
- Create token generation and validation functions
- Set token expiration (e.g., 24 hours)
- Functions needed:
  - `create_access_token(user_id: int, email: str) -> str`
  - `decode_token(token: str) -> dict`
  - `verify_token(token: str) -> bool`

### Phase 2: Backend - API Endpoints

#### 2.1 Authentication Endpoints
**Files to modify**:
- `app/server/server.py`

**New endpoints to add**:

1. **POST /api/auth/register**
   - Input: `{ email: string, password: string }`
   - Validation:
     - Email format validation
     - Email uniqueness check
     - Password strength validation
   - Creates new user with hashed password
   - Returns: `{ success: boolean, message: string, user: { id, email } }`

2. **POST /api/auth/login**
   - Input: `{ email: string, password: string }`
   - Validates credentials
   - Generates JWT token
   - Updates last_login timestamp
   - Returns: `{ success: boolean, token: string, user: { id, email } }`

3. **POST /api/auth/logout**
   - Input: Authorization header with JWT token
   - Invalidates token (add to blacklist if needed)
   - Returns: `{ success: boolean, message: string }`

4. **GET /api/auth/me**
   - Input: Authorization header with JWT token
   - Returns current user info
   - Returns: `{ user: { id, email, created_at } }`

#### 2.2 Data Models
**Files to create**:
- `app/server/core/data_models.py` (modify existing)

**Models to add**:
```python
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[dict] = None

class UserInfo(BaseModel):
    id: int
    email: str
    created_at: datetime
```

#### 2.3 Middleware & Authentication
**Files to create**:
- `app/server/core/auth_middleware.py` (new)

**Tasks**:
- Create authentication dependency for protected routes
- Add `get_current_user()` dependency function
- Implement token validation from headers

### Phase 3: Frontend - Components

#### 3.1 Create Login Component
**Files to create**:
- `app/client/src/components/Login.ts` (new)
- `app/client/src/styles/auth.css` (new)

**Tasks**:
- Create login form with:
  - Email input (type="email")
  - Password input (type="password")
  - Submit button
  - Link to registration page
  - Error message display
- Add client-side validation
- Handle form submission
- Store JWT token in localStorage
- Redirect to main app on success

#### 3.2 Create Registration Component
**Files to create**:
- `app/client/src/components/Register.ts` (new)

**Tasks**:
- Create registration form with:
  - Email input (type="email")
  - Password input (type="password")
  - Confirm password input
  - Submit button
  - Link to login page
  - Success/error message display
- Add client-side validation:
  - Email format
  - Password strength
  - Password confirmation match
- Handle form submission
- Show success message
- Redirect to login page on success

#### 3.3 Authentication State Management
**Files to create**:
- `app/client/src/utils/auth.ts` (new)

**Tasks**:
- Create authentication utility functions:
  - `saveToken(token: string): void`
  - `getToken(): string | null`
  - `removeToken(): void`
  - `isAuthenticated(): boolean`
  - `getCurrentUser(): Promise<UserInfo>`
- Add token to API client requests

#### 3.4 Update API Client
**Files to modify**:
- `app/client/src/api/client.ts`

**Tasks**:
- Add authentication methods:
  - `register(email, password)`
  - `login(email, password)`
  - `logout()`
  - `getCurrentUser()`
- Add Authorization header to all API requests
- Handle 401 unauthorized responses

### Phase 4: Frontend - Routing & Protection

#### 4.1 Implement Routing
**Files to create**:
- `app/client/src/router.ts` (new)

**Tasks**:
- Set up simple routing system (or use a library like page.js)
- Routes:
  - `/` - Main app (protected)
  - `/login` - Login page
  - `/register` - Registration page
- Implement route guards for protected routes

#### 4.2 Update Main Application
**Files to modify**:
- `app/client/index.html`
- `app/client/src/main.ts`

**Tasks**:
- Add container div for auth components
- Check authentication on app load
- Redirect to login if not authenticated
- Add logout button to main interface
- Show current user email in header

### Phase 5: Styling

#### 5.1 Create Authentication Styles
**Files to create**:
- `app/client/src/styles/auth.css` (new)

**Tasks**:
- Design clean, modern login/registration forms
- Match existing application style (refer to app/client/src/style.css)
- Responsive design for mobile devices
- Form validation error states
- Loading states for form submission

#### 5.2 Update Main Styles
**Files to modify**:
- `app/client/src/style.css`

**Tasks**:
- Add styles for user info header
- Add styles for logout button
- Ensure consistent theme across auth and main app

### Phase 6: Testing & Security

#### 6.1 Backend Tests
**Files to create**:
- `app/server/tests/test_auth.py` (new)

**Test cases**:
- User registration with valid data
- User registration with duplicate email (should fail)
- User registration with weak password (should fail)
- User login with valid credentials
- User login with invalid credentials
- Token generation and validation
- Protected endpoint access without token (should fail)
- Protected endpoint access with valid token

#### 6.2 Security Considerations
- Implement rate limiting for login/register endpoints (optional for v1)
- Add CSRF protection if needed
- Ensure password hashing is strong (bcrypt with appropriate rounds)
- Validate all user inputs
- Sanitize error messages (don't reveal if email exists)
- Use HTTPS in production (configuration note)

### Phase 7: Documentation

#### 7.1 Update README
**Files to modify**:
- `README.md`

**Tasks**:
- Document new authentication system
- Add setup instructions for initial admin user (if needed)
- Update API endpoints section
- Add authentication flow diagram (optional)

#### 7.2 Add Environment Variables
**Files to modify**:
- `app/server/.env.sample`

**Add**:
```
# Authentication
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

## Dependencies to Add

### Backend
```bash
cd app/server
uv add passlib[bcrypt]  # Password hashing
uv add python-jose[cryptography]  # JWT tokens
uv add python-multipart  # Form data parsing
```

### Frontend
- No additional dependencies needed (vanilla TypeScript)
- Optional: Consider adding a routing library

## Database Migration

### Initial Setup
Since this is the first time adding authentication:
1. Create auth database initialization script
2. Run migration to create users table
3. Optionally seed with a default admin user

## Success Criteria

- [ ] Users can register with email and password
- [ ] Registration validates email format and password strength
- [ ] Passwords are securely hashed
- [ ] Users can login with valid credentials
- [ ] Login generates a JWT token
- [ ] Main application is only accessible when authenticated
- [ ] Token is included in all API requests
- [ ] Users can logout
- [ ] Invalid credentials show appropriate error messages
- [ ] All tests pass
- [ ] Documentation is updated

## Risks & Considerations

1. **Session Management**: Using JWT means tokens can't be invalidated before expiration. Consider adding token blacklist if needed.

2. **Password Reset**: Not included in this initial implementation. Should be added in future iteration.

3. **Email Verification**: Not included. Consider adding email verification in future.

4. **Remember Me**: Not included. Could be added with refresh tokens.

5. **Multi-factor Authentication**: Not included in v1.

6. **CORS**: Ensure CORS configuration allows authentication headers.

## Future Enhancements

- Password reset functionality
- Email verification
- OAuth2 social login (Google, GitHub)
- User profile management
- Remember me / refresh tokens
- Admin user roles and permissions
- Rate limiting on auth endpoints
- Audit logging for authentication events

## Estimated Complexity

- **Backend**: Medium complexity (3-4 hours)
- **Frontend**: Medium complexity (3-4 hours)
- **Testing**: Low-medium complexity (1-2 hours)
- **Total**: ~8-10 hours

## Notes

- The issue description mentions "Registration page" but the title says "Login Page". This plan implements both login and registration, as both are necessary for a complete authentication system.
- Using JWT tokens for simplicity; can be upgraded to OAuth2 with refresh tokens later.
- Following existing patterns in the codebase (FastAPI, SQLite, TypeScript).
- Maintaining consistency with current code style and architecture.
