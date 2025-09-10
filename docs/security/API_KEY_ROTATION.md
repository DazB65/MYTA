# API Key Rotation Guide for MYTA

This document provides comprehensive guidance for rotating API keys in the MYTA application to maintain security compliance.

## Overview

API key rotation is a critical security practice that involves:
- Regularly replacing API keys with new ones
- Ensuring zero-downtime during rotation
- Maintaining audit trails of all rotations
- Following service-specific rotation procedures

## Rotation Schedule

### Recommended Rotation Frequency

| Key Type | Frequency | Risk Level | Automation |
|----------|-----------|------------|------------|
| Internal Keys (Session, JWT) | 90 days | Low | ✅ Automated |
| OpenAI API Key | 90 days | High | ⚠️ Manual |
| Anthropic API Key | 90 days | High | ⚠️ Manual |
| Google/YouTube API Key | 180 days | Medium | ⚠️ Manual |
| OAuth Credentials | 365 days | Medium | ⚠️ Manual |

### Emergency Rotation

Immediate rotation required if:
- Key suspected to be compromised
- Key accidentally exposed in logs/code
- Security incident detected
- Employee with key access leaves

## Automated Rotation

### Internal Keys

Internal application keys can be rotated automatically:

```bash
# Rotate only internal keys
python scripts/security/rotate_api_keys.py --internal-only

# Rotate all keys (provides manual instructions for external services)
python scripts/security/rotate_api_keys.py

# Rotate specific services
python scripts/security/rotate_api_keys.py --services openai anthropic
```

### What Gets Rotated Automatically

1. **BOSS_AGENT_SECRET_KEY** - Used for internal agent authentication
2. **SESSION_SECRET_KEY** - Used for session management

## Manual Rotation Procedures

### OpenAI API Key

1. **Generate New Key**:
   - Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Click "Create new secret key"
   - Copy the new key immediately (it won't be shown again)

2. **Update Environment**:
   ```bash
   # Update .env file
   OPENAI_API_KEY=sk-proj-your_new_key_here
   ```

3. **Test New Key**:
   ```bash
   # Test the new key
   python scripts/security/test_api_keys.py --service openai
   ```

4. **Delete Old Key**:
   - Return to OpenAI dashboard
   - Delete the old key
   - Verify deletion

### Anthropic API Key

1. **Generate New Key**:
   - Go to [Anthropic Console](https://console.anthropic.com/)
   - Navigate to API Keys section
   - Create new key

2. **Update Environment**:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-api03-your_new_key_here
   ```

3. **Test and Delete Old Key** (same process as OpenAI)

### Google/YouTube API Key

1. **Generate New Key**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Click "Create Credentials" → "API Key"
   - Restrict the key to YouTube Data API v3

2. **Update Environment**:
   ```bash
   GOOGLE_API_KEY=your_new_google_key_here
   YOUTUBE_API_KEY=your_new_google_key_here  # Usually same key
   YT_API_KEY=your_new_google_key_here       # Alias
   ```

3. **Test and Delete Old Key**

### OAuth Credentials

1. **Google OAuth**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Edit existing OAuth 2.0 Client ID or create new one
   - Update redirect URIs if needed

2. **Update Environment**:
   ```bash
   GOOGLE_CLIENT_ID=your_new_client_id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your_new_client_secret
   ```

## Zero-Downtime Rotation

### For Production Systems

1. **Preparation Phase**:
   ```bash
   # Create backup
   cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
   
   # Generate new internal keys
   python scripts/security/rotate_api_keys.py --internal-only
   ```

2. **External Key Rotation**:
   - Generate new external API keys
   - Keep old keys active initially
   - Update environment with new keys
   - Test all functionality
   - Delete old keys only after confirmation

3. **Verification**:
   ```bash
   # Run health checks
   curl http://localhost:8000/health
   
   # Test API functionality
   python scripts/security/test_api_keys.py --all
   ```

## Security Best Practices

### During Rotation

1. **Never commit keys to version control**
2. **Use secure channels for key transmission**
3. **Rotate keys during low-traffic periods**
4. **Have rollback plan ready**
5. **Monitor for errors after rotation**

### Key Storage

1. **Development**:
   - Use `.env` file (gitignored)
   - Never share keys in plain text

2. **Production**:
   - Use environment variables
   - Consider secret management services:
     - AWS Secrets Manager
     - Azure Key Vault
     - HashiCorp Vault
     - Google Secret Manager

### Monitoring

1. **Set up alerts for**:
   - API key usage anomalies
   - Authentication failures
   - Rate limit exceeded errors

2. **Log rotation events**:
   - Who performed the rotation
   - When it was performed
   - Which keys were rotated

## Automation Scripts

### Available Scripts

1. **`rotate_api_keys.py`** - Main rotation script
2. **`test_api_keys.py`** - Key validation script
3. **`backup_keys.py`** - Backup management script

### Usage Examples

```bash
# Full rotation with backup
python scripts/security/rotate_api_keys.py --backup-dir ./backups/keys

# Test all keys after rotation
python scripts/security/test_api_keys.py --all --verbose

# Emergency rotation (force even if not due)
python scripts/security/rotate_api_keys.py --force
```

## Troubleshooting

### Common Issues

1. **Key Validation Fails**:
   - Check key format
   - Verify service-specific requirements
   - Ensure key has proper permissions

2. **Service Unavailable After Rotation**:
   - Check logs for authentication errors
   - Verify new keys are properly saved
   - Rollback to backup if needed

3. **Rate Limiting Issues**:
   - Some services have rate limits on key generation
   - Wait before generating new keys
   - Contact service support if needed

### Emergency Rollback

```bash
# Restore from backup
cp .env.backup.YYYYMMDD_HHMMSS .env

# Restart services
systemctl restart myta-backend  # or your service manager

# Verify functionality
curl http://localhost:8000/health
```

## Compliance and Auditing

### Audit Trail

All rotations are logged with:
- Timestamp of rotation
- User who performed rotation
- Keys that were rotated
- Backup file locations

### Compliance Requirements

1. **SOC 2**: Regular key rotation required
2. **ISO 27001**: Key management procedures documented
3. **GDPR**: Secure handling of authentication credentials

### Reporting

Monthly rotation reports include:
- Keys rotated in the period
- Keys due for rotation
- Any security incidents
- Compliance status

## Contact Information

For security-related issues:
- **Security Team**: security@myta.com
- **Emergency**: security-emergency@myta.com
- **Documentation**: This file and `/docs/security/`

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2024-01-XX | 1.0 | Initial documentation |
| 2024-01-XX | 1.1 | Added automation scripts |
