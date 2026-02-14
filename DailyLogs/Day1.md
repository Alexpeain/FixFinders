# Fix Finder - Development Log

## Day 1: Architecture & Backend Foundation
**Goal:** Setup a professional Django environment for a localized directory app.

### Key Technical Decisions:
1.  **Project Structure:** 
    - Used a split structure (`config/` vs `src/`) to separate settings from logic.
    - This makes the codebase cleaner and easier to containerize later.
2.  **User Model:** 
    - Implemented a Custom User Model (`users.User`) inheriting from `AbstractUser`.
    - *Reason:* Django recommends this to avoid painful migrations if we need to add fields (like `is_provider`) later.
3.  **Provider Data Model:**
    - Designed `ProviderProfile` with `OneToOneField` to User.
    - Added `db_index=True` to `township` and `category` fields to optimize search performance for the directory.
    - **Identity Verification:** Added logic to support both Pink Cards (NRC) and Smart Cards without exposing sensitive images to the public.

### Challenges Solved:
- Fixed circular dependency in `AUTH_USER_MODEL` during initial migration.
- Resolved `AppRegistryNotReady` error caused by importing models inside `apps.py`.

### Next Steps:
- Build the Public Views (Search, Detail Page).
- Create HTML Templates with Bootstrap.
- Implement Township filtering.
