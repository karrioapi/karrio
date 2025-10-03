"use client";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useSyncedSession } from "@karrio/hooks/session";
import SwaggerUI from "swagger-ui-react";
import "swagger-ui-react/swagger-ui.css";
import { url$ } from "@karrio/lib";
import "./swagger-ui-custom.css";
import React from "react";


export default function Page(pageProps: any) {
  const Component = (): JSX.Element => {
    const { references } = useAPIMetadata();
    const { query: { data: session } } = useSyncedSession();

    // Configure request interceptor to add Bearer token
    const requestInterceptor = (request: any) => {
      if (session?.accessToken) {
        request.headers.Authorization = `Bearer ${session.accessToken}`;
      }
      if (session?.orgId) {
        request.headers["x-org-id"] = session.orgId;
      }
      if (session?.testMode) {
        request.headers["x-test-mode"] = session.testMode;
      }
      return request;
    };

    return (
      <div className="swagger-ui-container">
        <SwaggerUI
          url={url$`${references?.HOST}/shipping-openapi`}
          docExpansion="none"
          defaultModelsExpandDepth={1}
          defaultModelExpandDepth={1}
          displayRequestDuration={true}
          filter={false}
          showExtensions={true}
          showCommonExtensions={true}
          requestInterceptor={requestInterceptor}
          onComplete={(swaggerApi: any) => {
            // Auto-authorize with Bearer token if available
            if (session?.accessToken) {
              swaggerApi.preauthorizeApiKey('Bearer', session.accessToken);
            }
          }}
        />
      </div>
    );
  };

  return (
    <>
      <Component />
    </>
  );
}
