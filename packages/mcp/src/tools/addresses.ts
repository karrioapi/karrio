import { z } from "zod";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { KarrioClient } from "../client.js";

export function registerAddressTools(
  server: McpServer,
  client: KarrioClient,
): void {
  server.tool(
    "validate_address",
    "Validate and correct a shipping address. Returns the validated address with any corrections applied, plus a validation score. Use this to verify addresses before creating shipments.",
    {
      address_line1: z.string().describe("Street address line 1"),
      address_line2: z
        .string()
        .optional()
        .describe("Street address line 2"),
      city: z.string().optional().describe("City name"),
      state: z
        .string()
        .optional()
        .describe("State/province code"),
      postal_code: z.string().describe("Postal/zip code"),
      country_code: z
        .string()
        .describe("ISO 2-letter country code"),
      person_name: z
        .string()
        .optional()
        .describe("Person name at the address"),
      company_name: z
        .string()
        .optional()
        .describe("Company name at the address"),
    },
    {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true,
    },
    async (params) => {
      try {
        const address: Record<string, string> = {
          address_line1: params.address_line1,
          postal_code: params.postal_code,
          country_code: params.country_code,
        };
        if (params.address_line2) address.address_line2 = params.address_line2;
        if (params.city) address.city = params.city;
        if (params.state) address.state_code = params.state;
        if (params.person_name) address.person_name = params.person_name;
        if (params.company_name) address.company_name = params.company_name;

        const response = await client.validateAddress({ address });

        return {
          content: [
            { type: "text", text: JSON.stringify(response, null, 2) },
          ],
        };
      } catch (error: any) {
        return {
          content: [
            {
              type: "text",
              text: `Error validating address: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    },
  );
}
