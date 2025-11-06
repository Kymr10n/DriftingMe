# Security and Environment Configuration

## Important Security Notes

### Environment Variables (.env)
- **NEVER** commit `.env` files to version control
- The `.env` file may contain sensitive information like hostnames, API keys, or server details
- Always use `.env.template` as a template and create your own `.env` file locally

### Sensitive Information
The following information should be kept in `.env` files only:
- Remote server hostnames or IP addresses
- SSH usernames 
- API endpoints (if they contain sensitive paths)
- Any custom configuration that reveals your infrastructure

### Git Configuration
The `.gitignore` file is configured to exclude:
- `.env` (main environment file)
- `.env.local`
- `.env.development.local` 
- `.env.test.local`
- `.env.production.local`
- `config/*.secret` (any secret files)

### Best Practices
1. **Use .env.template**: Copy and customize for your environment
2. **Review before committing**: Always check that no sensitive data is hardcoded
3. **Environment-specific configs**: Use different .env files for different environments
4. **Documentation**: Keep examples generic (e.g., `user@server.com` instead of real hostnames)

### Default Values
All scripts use safe defaults when environment variables are not set:
- `A1111_URL`: `http://localhost:7860`
- `COMFYUI_URL`: `http://localhost:8188` 
- `REMOTE_HOST`: `user@remote-server.com`
- `REMOTE_PROJECT_DIR`: `~/DriftingMe`

This ensures the project works out-of-the-box while allowing full customization through environment variables.