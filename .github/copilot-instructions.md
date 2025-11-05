# Copilot Instructions - Referral Body Automation

## Project Overview
This is a Python automation project that processes referral links through automated account creation using temporary email APIs. The system navigates to target URLs, completes registration flows, and authenticates to perform follow-up activities.

**Primary Language:** Python (Swedish documentation)  
**Core Technology:** Playwright for browser automation  
**External Services:** Oxylabs Residential Proxies, 2Captcha for CAPTCHA solving

## Project Structure & Organization

### Directory Layout
- `main.py` - Main entry point (currently empty - project in early setup)
- `docs/` - All documentation and specification files
  - `oxlabs dokumentasjon.md` - Complete Oxylabs Residential Proxy API reference
  - `status.md` - **CRITICAL**: Must be updated after EVERY code change
- `tests/` - Test files (when created, keep separate from source)

### Structural Rules (Enforced)
1. **No duplicate files** - Maximum one `.bak` file if needed, delete unused files immediately
2. **Organized separation** - Tests in `tests/`, documentation in `docs/`
3. **Status tracking** - Update `docs/status.md` after each modification
4. **Clean structure** - "Hålla ren och städad struktur" (keep clean and tidy structure)

## Key Technical Integrations

### Oxylabs Residential Proxy API
**Base URL:** `/v1` | **Auth:** Bearer token from `POST /login`

**Critical API Details:**
- Sub-user management with UUID-based userId endpoints
- Password requirements: 12-64 chars, must include lowercase, uppercase, digit, and one of: `# _ ~ + =`
- Username: letters, digits, underscores only
- Traffic limits: `null` (unlimited), numeric (GB limit), `0` (no traffic)
- Custom date ranges with hours limited to 7-day range
- Last 30 days only for target stats

**Common Workflow:**
```python
# 1. POST /login → get Bearer token
# 2. POST /users/{userId}/sub-users → create proxy sub-user
# 3. Use sub-user credentials for Playwright proxy configuration
```

### 2Captcha Integration
Use when CAPTCHA challenges appear during automation flows.

### Gmailnator (Emailnator) Temporary Email API
**Host:** `gmailnator.p.rapidapi.com` | **Auth:** RapidAPI headers

**Critical API Details:**
- Generates temporary Gmail addresses (public/private, plus/dot variants)
- Email options: `[1,2,3,4,5,6,8,9]` - see `docs/gmailnator_api.md` for details
- Inbox polling with max 20 messages per request
- Message IDs are encrypted JWT-like strings
- Bulk generation supports up to 500 emails

**Common Workflow:**
```python
# 1. POST /generate-email with options=[1] → get temp email
# 2. Use email in registration form
# 3. POST /inbox with email parameter → poll for messages
# 4. GET /messageid with message ID → extract verification link
# 5. GET /delete with message ID → cleanup
```

**Integration Pattern:**
- Generate email before registration
- Poll inbox after form submission (use async sleep)
- Extract verification URLs from message content
- Navigate to verification link with Playwright
- Delete messages after use

## Development Patterns

### Code Quality Standards
- **Comments:** Write logical, meaningful comments in Swedish or English
- **Modularity:** Build with modular structure - separate concerns into distinct modules
- **No placeholder code:** Always implement complete, working solutions

### Browser Automation with Playwright
- Configure Oxylabs residential proxies for each browser context
- Handle registration forms with temporary email addresses
- Implement authentication flows for target platforms
- Prepare for CAPTCHA solving integration points

### Error Handling
- Plan for 400/401/404 responses from Oxylabs API (validation errors, auth issues, missing resources)
- Handle browser automation failures gracefully
- Account for CAPTCHA appearance in flows

## Critical Workflows

### Status Documentation
**After every change:**
1. Update `docs/status.md` with:
   - What was changed
   - Why it was changed
   - Current state of implementation
   - Next steps or blockers

### File Management
Before creating new files:
1. Check if similar functionality exists
2. Remove unused/obsolete files
3. Ensure proper directory placement

## API Reference Quick Guide

**Oxylabs Sub-User Creation:**
```json
POST /users/{userId}/sub-users
{
  "username": "valid_user_123",
  "password": "Strong_Pass#123",
  "traffic_limit": 2000.68,
  "lifetime": true,
  "auto_disable": true
}
```

**Traffic Stats Query:**
```
GET /users/{userId}/sub-users/{subUserId}?type=24h
Types: 24h, week, month, current_month, lifetime, custom
```

## Next Steps for Implementation
1. Set up Playwright browser automation framework
2. Implement Oxylabs proxy integration (auth + sub-user creation)
3. Create temporary email service integration
4. Build registration flow navigation
5. Add 2Captcha solving when needed
6. Implement authentication and follow-up activities
