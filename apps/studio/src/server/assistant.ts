// assistant.ts — AI Assistant server function (F1). Calls the Claude API when
// ANTHROPIC_API_KEY is set; otherwise returns a deterministic stub so the
// Editor remains usable/testable without a key.
import { createServerFn } from "@tanstack/react-start";
import { z } from "zod";

const input = z.object({
  message: z.string().min(1),
  model: z.string().optional(),
  mode: z.string().optional(),
});

export const sendAssistantMessage = createServerFn({ method: "POST" })
  .inputValidator((data: unknown) => input.parse(data))
  .handler(async ({ data }) => {
    const key = process.env.ANTHROPIC_API_KEY;
    if (!key) {
      return {
        reply:
          `**[stub reply]** I received: “${data.message}”.\n\n` +
          `Set ANTHROPIC_API_KEY to enable live Claude responses. ` +
          `In ${data.mode ?? "assistant"} mode I can scaffold connectors, edit plugin files, and run Karrio tools via MCP.`,
      };
    }
    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "x-api-key": key,
          "anthropic-version": "2023-06-01",
          "content-type": "application/json",
        },
        body: JSON.stringify({
          model: data.model || "claude-opus-4-8",
          max_tokens: 1024,
          messages: [{ role: "user", content: data.message }],
        }),
      });
      const json = await res.json();
      const reply = json?.content?.[0]?.text ?? "(no response)";
      return { reply };
    } catch {
      return { reply: "The assistant is temporarily unavailable. Please try again." };
    }
  });
