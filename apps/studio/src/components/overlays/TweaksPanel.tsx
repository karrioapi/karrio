// TweaksPanel.tsx — self-editable appearance (G1). Accent / density / font /
// theme, applied live via CSS variables and persisted via preferences.ts
// (localStorage + async backend sync via update_user GraphQL mutation).
import { useState } from "react";
import { Sheet } from "~/components/ui/Sheet";
import { Section } from "~/components/ui/detail";
import {
  applyAccent,
  applyDensity,
  applyFont,
  applyTheme,
  loadPrefs,
  savePrefs,
  syncToBackend,
  type Density,
  type FontStack,
} from "~/lib/karrio/preferences";
import { useKarrioCtx } from "~/lib/karrio/session";

// Canonical accent palette (kept here so the constant is co-located with the UI).
export const ACCENTS = ["#8B5CF6", "#3B82F6", "#10B981", "#F97316", "#E11D48"] as const;

export function TweaksPanel({
  open,
  onClose,
  theme,
  onTheme,
}: {
  open: boolean;
  onClose: () => void;
  theme: "dark" | "light";
  onTheme: () => void;
}) {
  const ctx = useKarrioCtx();
  const stored = loadPrefs();
  const [accent, setAccent] = useState(stored.accent);
  const [density, setDensity] = useState<Density>(stored.density);
  const [font, setFont] = useState<FontStack>(stored.font_stack);

  if (!open) return null;

  return (
    <Sheet open={open} onClose={onClose} size="sm" crumb="Appearance" title="Customize Studio">
      <div className="sheet-body-pad" data-testid="tweaks-panel">
        <Section title="Theme">
          <div style={{ display: "flex", gap: 8 }}>
            {(["dark", "light"] as const).map((t) => (
              <button
                key={t}
                className={"btn" + (theme === t ? " btn-primary" : "")}
                onClick={() => {
                  if (theme !== t) {
                    applyTheme(t);
                    savePrefs({ theme: t });
                    void syncToBackend(ctx, { ...loadPrefs(), theme: t });
                    onTheme();
                  }
                }}
                data-testid={`tweak-theme-${t}`}
              >
                {t[0].toUpperCase() + t.slice(1)}
              </button>
            ))}
          </div>
        </Section>

        <Section title="Accent">
          <div style={{ display: "flex", gap: 8 }} data-testid="tweak-accents">
            {ACCENTS.map((c) => (
              <button
                key={c}
                aria-label={`Accent ${c}`}
                onClick={() => {
                  setAccent(c);
                  applyAccent(c);
                  savePrefs({ accent: c });
                  void syncToBackend(ctx, { ...loadPrefs(), accent: c });
                }}
                data-testid={`tweak-accent-${c.replace("#", "")}`}
                style={{
                  width: 26,
                  height: 26,
                  borderRadius: "var(--r-sm)",
                  background: c,
                  border: accent === c ? "2px solid var(--fg)" : "2px solid transparent",
                  cursor: "pointer",
                }}
              />
            ))}
          </div>
        </Section>

        <Section title="Density">
          <select
            className="select-sm"
            value={density}
            onChange={(e) => {
              const d = e.target.value as Density;
              setDensity(d);
              applyDensity(d);
              savePrefs({ density: d });
              void syncToBackend(ctx, { ...loadPrefs(), density: d });
            }}
            data-testid="tweak-density"
            aria-label="Density"
          >
            <option value="compact">Compact</option>
            <option value="regular">Regular</option>
            <option value="comfy">Comfortable</option>
          </select>
        </Section>

        <Section title="Font">
          <select
            className="select-sm"
            value={font}
            onChange={(e) => {
              const f = e.target.value as FontStack;
              setFont(f);
              applyFont(f);
              savePrefs({ font_stack: f });
              void syncToBackend(ctx, { ...loadPrefs(), font_stack: f });
            }}
            data-testid="tweak-font"
            aria-label="Font"
          >
            <option value="Inter">Inter</option>
            <option value="IBM Plex">IBM Plex Sans</option>
            <option value="System">System</option>
          </select>
        </Section>
      </div>
    </Sheet>
  );
}
