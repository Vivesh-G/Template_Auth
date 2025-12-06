### Rate limiting
Integrate `slowapi` in FastAPI to limit the number of requests to endpoints like `/login` based on IP address.
Frontend should handle `429 Too Many Requests` responses by disabling buttons and showing a countdown. [DONE]

### Refresh token rotation
When a refresh token is used to get a new access token, issue a new refresh token and revoke the old one.
If a revoked token is used, invalidate the entire token family to prevent replay attacks.

### Token invalidation (Logout)
Implement a blocklist (using a database table) to store revoked tokens until their natural expiry.
Middleware checks this blocklist on every authenticated request to ensure the token is still valid. [DONE]

### Email verification
Generate a unique, time-limited token upon registration and send it via email using `fastapi-mail`.
Create a frontend route `/verify?token=...` that calls the backend to flip the user's `is_verified` status.

### Password reset flows
Create an endpoint to send a reset link with a signed token to the user's email.
Frontend provides a form to enter a new password. [DONE]

### Brute force protection
Track failed login attempts by email or IP in Redis or the database.
Temporarily lock the account or enforce a delay after a specific number of consecutive failures (e.g., 5 attempts).

### IP-based throttling
Use middleware to track request rates per IP address across the entire API.
Block IPs that exceed a high threshold (e.g., 100 req/min) to protect against scraping and DoS attacks.

### Session hijacking prevention
Store tokens in `HttpOnly`, `Secure`, `SameSite` cookies to prevent XSS attacks from stealing them.
Validate the `User-Agent` or IP address inside the token payload against the current request to detect session theft.

### Storage of tokens
**Frontend**: Do not store sensitive tokens in `localStorage`.
**Backend**: Send `refresh_token` and `access_token` as `HttpOnly` cookies so the browser handles storage securely.

### Cleanup of expired refresh tokens
Set up a background task (using `APScheduler` or a simple cron job) in FastAPI.
Periodically delete rows from the `refresh_tokens` database table where the `expires_at` timestamp is in the past.

### Audit logs
Create a `logging` table in the database.
Use a middleware or decorator to record critical actions (logins, data changes) with `user_id`, `timestamp`, `ip_address`, and `action_type`. [DONE]