import { PLATFORM_API_URL, PLATFORM_API_KEY, AUTH_SECRET, DATABASE_URL, TENANT_DASHBOARD_DOMAIN, STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY, TENANT_API_DOMAIN } from "./constants";

// Environment validation and diagnostics
export interface EnvironmentStatus {
  isValid: boolean;
  issues: string[];
  warnings: string[];
  info: Record<string, any>;
}

export function validateEnvironment(): EnvironmentStatus {
  const issues: string[] = [];
  const warnings: string[] = [];
  const info: Record<string, any> = {};

  // Required environment variables
  const required = {
    KARRIO_PLATFORM_API_URL: PLATFORM_API_URL,
    KARRIO_PLATFORM_API_KEY: PLATFORM_API_KEY,
    NEXTAUTH_SECRET: AUTH_SECRET,
    DATABASE_URL: DATABASE_URL,
  };

  // Optional but recommended
  const optional = {
    TENANT_API_DOMAIN: TENANT_API_DOMAIN,
    TENANT_DASHBOARD_DOMAIN: TENANT_DASHBOARD_DOMAIN,
    STRIPE_SECRET_KEY: STRIPE_SECRET_KEY,
    STRIPE_PUBLISHABLE_KEY: STRIPE_PUBLISHABLE_KEY,
  };

  // Check required variables
  Object.entries(required).forEach(([key, value]) => {
    if (!value) {
      issues.push(`Missing required environment variable: ${key}`);
    } else {
      info[key] = key.includes('KEY') || key.includes('SECRET')
        ? `${value.substring(0, 8)}...`
        : value;
    }
  });

  // Check optional variables
  Object.entries(optional).forEach(([key, value]) => {
    if (!value) {
      warnings.push(`Missing optional environment variable: ${key}`);
    } else {
      info[key] = key.includes('KEY') || key.includes('SECRET')
        ? `${value.substring(0, 8)}...`
        : value;
    }
  });

  // Validate API URL format
  if (required.KARRIO_PLATFORM_API_URL) {
    try {
      new URL(required.KARRIO_PLATFORM_API_URL);
      info.api_url_valid = true;
    } catch (error) {
      issues.push(`Invalid KARRIO_PLATFORM_API_URL format: ${required.KARRIO_PLATFORM_API_URL}`);
      info.api_url_valid = false;
    }
  }

  // Validate API key format (should be a valid token)
  if (required.KARRIO_PLATFORM_API_KEY) {
    if (required.KARRIO_PLATFORM_API_KEY.length < 20) {
      warnings.push('KARRIO_PLATFORM_API_KEY seems too short, verify it\'s correct');
    }
    info.api_key_length = required.KARRIO_PLATFORM_API_KEY.length;
  }

  // Check database connection string
  if (required.DATABASE_URL) {
    if (!required.DATABASE_URL.startsWith('postgresql://') && !required.DATABASE_URL.startsWith('postgres://')) {
      warnings.push('DATABASE_URL should start with postgresql:// or postgres://');
    }
  }

  return {
    isValid: issues.length === 0,
    issues,
    warnings,
    info,
  };
}

export function logEnvironmentStatus(): void {
  const status = validateEnvironment();

  console.log('\n=== Environment Configuration Status ===');

  if (status.isValid) {
    console.log('✅ Environment configuration is valid');
  } else {
    console.log('❌ Environment configuration has issues');
  }

  if (status.issues.length > 0) {
    console.log('\n🚨 Issues (must be fixed):');
    status.issues.forEach(issue => console.log(`  - ${issue}`));
  }

  if (status.warnings.length > 0) {
    console.log('\n⚠️  Warnings (recommended to fix):');
    status.warnings.forEach(warning => console.log(`  - ${warning}`));
  }

  console.log('\n📋 Configuration Info:');
  Object.entries(status.info).forEach(([key, value]) => {
    console.log(`  ${key}: ${value}`);
  });

  console.log('=========================================\n');
}

// Auto-run on import in development
if (process.env.NODE_ENV === 'development') {
  logEnvironmentStatus();
}
