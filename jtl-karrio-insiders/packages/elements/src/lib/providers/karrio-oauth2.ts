import type { OAuthConfig, OAuthUserConfig } from "next-auth/providers";
import { KARRIO_API } from "@karrio/lib";

/**
 * <div style={{display: "flex", justifyContent: "space-between", alignItems: "center", padding: 16}}>
 * <span>Karrio OAuth2 provider for authentication with your Karrio instance</span>
 * </div>
 *
 * @module providers/karrio-oauth2
 */

export interface KarrioProfile {
  sub: string;
  name: string;
  email: string;
  picture?: string;
  orgId?: string;
  testMode?: boolean;
  [key: string]: any;
}

export interface KarrioOAuth2Config {
  clientId: string;
  clientSecret: string;
  apiUrl?: string;
  authorizationUrl?: string;
  tokenUrl?: string;
  profileUrl?: string;
}

/**
 * Add Karrio OAuth 2.0 login to your application.
 *
 * @param options - The configuration options for the Karrio OAuth2 provider
 * @returns The configured Karrio OAuth2 provider
 */
export default function KarrioOAuth2(
  options: OAuthUserConfig<KarrioProfile> & KarrioOAuth2Config
): OAuthConfig<KarrioProfile> {
  const {
    clientId,
    clientSecret,
    apiUrl = KARRIO_API,
    authorizationUrl,
    tokenUrl,
    profileUrl,
    ...rest
  } = options;

  return {
    id: "karrio-oauth2",
    name: "Karrio OAuth",
    type: "oauth",
    wellKnown: `${apiUrl}/.well-known/openid-configuration`,
    authorization: {
      url: authorizationUrl || `${apiUrl}/oauth/authorize`,
      params: { scope: "openid profile email" }
    },
    token: tokenUrl || `${apiUrl}/oauth/token`,
    userinfo: profileUrl || `${apiUrl}/oauth/userinfo`,
    clientId,
    clientSecret,
    profile(profile: KarrioProfile) {
      return {
        id: profile.sub,
        name: profile.name || profile.email?.split('@')[0] || 'Unknown',
        email: profile.email,
        image: profile.picture,
        orgId: profile.orgId,
        testMode: profile.testMode,
      };
    },
    checks: ["pkce", "state"],
    style: {
      logo: "/karrio-logo.svg",
      bg: "#fff",
      text: "#000",
    },
    options: rest,
  };
}
