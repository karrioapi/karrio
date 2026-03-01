export function validateApiKey(apiKey: string | undefined): string {
  if (!apiKey || apiKey.trim() === "") {
    throw new Error(
      "Karrio API key is required. Set KARRIO_API_KEY environment variable or pass --api-key argument.",
    );
  }
  return apiKey.trim();
}

export function parseAuthHeader(header: string | undefined): string | null {
  if (!header) return null;

  const match = header.match(/^(?:Token|Bearer)\s+(.+)$/i);
  return match ? match[1] : null;
}
