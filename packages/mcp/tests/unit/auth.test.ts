import { describe, it, expect } from "vitest";
import { validateApiKey, parseAuthHeader } from "../../src/auth.js";

describe("auth", () => {
  describe("validateApiKey", () => {
    it("returns trimmed key when valid", () => {
      const result = validateApiKey("  my_api_key  ");
      console.log(result);
      expect(result).toBe("my_api_key");
    });

    it("returns key as-is when no surrounding whitespace", () => {
      const result = validateApiKey("clean_key");
      console.log(result);
      expect(result).toBe("clean_key");
    });

    it("throws when key is undefined", () => {
      expect(() => validateApiKey(undefined)).toThrow(/required/i);
    });

    it("throws when key is empty string", () => {
      expect(() => validateApiKey("")).toThrow(/required/i);
    });

    it("throws when key is whitespace only", () => {
      expect(() => validateApiKey("   ")).toThrow(/required/i);
    });

    it("throws with descriptive message mentioning KARRIO_API_KEY", () => {
      expect(() => validateApiKey(undefined)).toThrow(/KARRIO_API_KEY/);
    });
  });

  describe("parseAuthHeader", () => {
    it("parses Token format", () => {
      const result = parseAuthHeader("Token my_token");
      console.log(result);
      expect(result).toBe("my_token");
    });

    it("parses Bearer format", () => {
      const result = parseAuthHeader("Bearer my_bearer");
      console.log(result);
      expect(result).toBe("my_bearer");
    });

    it("parses case-insensitive Token format", () => {
      const result = parseAuthHeader("token my_token");
      console.log(result);
      expect(result).toBe("my_token");
    });

    it("parses case-insensitive Bearer format", () => {
      const result = parseAuthHeader("bearer my_bearer");
      console.log(result);
      expect(result).toBe("my_bearer");
    });

    it("returns null for missing header", () => {
      const result = parseAuthHeader(undefined);
      console.log(result);
      expect(result).toBeNull();
    });

    it("returns null for empty string", () => {
      const result = parseAuthHeader("");
      console.log(result);
      expect(result).toBeNull();
    });

    it("returns null for invalid format", () => {
      const result = parseAuthHeader("Invalid header");
      console.log(result);
      expect(result).toBeNull();
    });

    it("returns null for key-only (no prefix)", () => {
      const result = parseAuthHeader("just_a_key");
      console.log(result);
      expect(result).toBeNull();
    });

    it("handles token with special characters", () => {
      const result = parseAuthHeader("Token abc123-def_456.xyz");
      console.log(result);
      expect(result).toBe("abc123-def_456.xyz");
    });
  });
});
