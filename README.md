# JTL Shipping Platform

Enterprise shipping integration platform built on [Karrio](https://github.com/karrioapi/karrio).

## Quick Deployment

### One-Line Cloud Deployment

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/jtlshipping/shipping-platform/main/bin/deploy-jtl)"
```

**Requirements:**
- Ubuntu 22.04+ with 4GB+ RAM  
- Domain with DNS A records for `api.domain.com` and `app.domain.com`
- GitHub PAT with `read:packages` scope

That's it! The script handles everything else.

---

## Local Development

```bash
git clone https://github.com/jtlshipping/shipping-platform.git
cd shipping-platform

# Login to GitHub Container Registry
echo YOUR_PAT | docker login ghcr.io -u YOUR_USERNAME --password-stdin

# Start services
docker compose up -d
```

Access: http://localhost:3102 (Dashboard) | http://localhost:5002 (API)

---

## Support

Issues: https://github.com/jtlshipping/shipping-platform/issues
