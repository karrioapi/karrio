import type { NextRequest } from "next/server";

/**
 * Generated carrier logo / icon (SVG placeholder).
 *
 * Everything that ends up in the SVG comes from the request URL, so it is
 * treated as untrusted:
 *  - the name must match a strict allowlist (`<slug>_logo.svg` / `<slug>_icon.svg`),
 *  - colours must be a hex, rgb()/hsl() value or a plain colour keyword,
 *  - the text is XML-escaped before it is written into the document,
 *  - the response is sent with `nosniff` and a CSP that disables scripts, so
 *    even a future templating mistake cannot execute when the URL is opened
 *    directly in a browser tab.
 *
 * This file intentionally has no runtime imports so it can be unit tested with
 * the Node.js built-in test runner (see apps/dashboard/tests).
 */

const NAME_PATTERN = /^([a-z0-9][a-z0-9_-]{0,63})_(logo|icon)\.svg$/i;
const COLOR_PATTERN =
  /^(?:#(?:[0-9a-f]{3,4}|[0-9a-f]{6}|[0-9a-f]{8})|[a-z]{3,20}|(?:rgb|hsl)a?\(\s*[0-9.,%\s/]{1,40}\))$/i;

const DEFAULT_TEXT_COLOR = "#ddd";
const DEFAULT_BACKGROUND = "#7e51e1";

const SECURITY_HEADERS = {
  "X-Content-Type-Options": "nosniff",
  "Content-Security-Policy":
    "default-src 'none'; style-src 'unsafe-inline'; sandbox",
};

function escapeXml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

function safeColor(raw: string | null, fallback: string): string {
  if (!raw) return fallback;

  let value = raw;
  try {
    // the UI encodes the colour once more before adding it to the query string
    value = decodeURIComponent(raw);
  } catch {
    return fallback;
  }

  return COLOR_PATTERN.test(value.trim()) ? value.trim() : fallback;
}

function getInitials(text: string): string {
  return text
    .split(/[-_ ]/)
    .map((n) => n[0] ?? "")
    .join("");
}

function formatCarrierSlug(text: string): string {
  const short = text.length > 10 ? `${text.slice(0, 9)}.` : text;
  return short.toUpperCase();
}

function notFound(): Response {
  return new Response("Not found", {
    status: 404,
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      ...SECURITY_HEADERS,
    },
  });
}

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ name: string }> },
) {
  const { name } = await params;
  const match = NAME_PATTERN.exec(name);

  if (!match) return notFound();

  const [, slug, kind] = match;
  const isIcon = kind.toLowerCase() === "icon";
  const searchParams = new URL(request.url).searchParams;
  const carrier_name = escapeXml(
    isIcon ? getInitials(slug).substring(0, 2) : formatCarrierSlug(slug),
  );
  const text_color = safeColor(searchParams.get("text_color"), DEFAULT_TEXT_COLOR);
  const background = safeColor(searchParams.get("background"), DEFAULT_BACKGROUND);
  const props = isIcon ? 'viewBox="0 0 512 512"' : 'viewBox="0 0 125 25"';
  const path = isIcon
    ? `<path xmlns="http://www.w3.org/2000/svg" style="fill-rule:evenodd;clip-rule:evenodd;fill:${background};" d="M512,472c0,22.1-17.9,40-40,40H40c-22.1,0-40-17.9-40-40V40C0,17.9,17.9,0,40,0h432c22.1,0,40,17.9,40,40V472z"/>`
    : `<path xmlns="http://www.w3.org/2000/svg" style="fill-rule:evenodd;clip-rule:evenodd;fill:${background};" d="M125,0v25H0V0H125z"/>`;

  const content = `<svg ${props} x="0px" y="0px" xmlns="http://www.w3.org/2000/svg">
    <g>
      ${path}

      <text x="50%" y="55%" alignment-baseline="middle" text-anchor="middle" fill="${text_color}" font-weight="bold" font-family="arial"
        font-size="${isIcon ? "16em" : ".95em"}" style="text-transform: uppercase; ${isIcon ? "border-radius: 40px;" : ""}">
        ${carrier_name}
      </text>
    </g>
  </svg>
  `;

  return new Response(content, {
    headers: {
      "Content-Type": "image/svg+xml; charset=utf-8",
      ...SECURITY_HEADERS,
    },
  });
}
