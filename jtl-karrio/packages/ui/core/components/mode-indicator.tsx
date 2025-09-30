"use client";
import { useAppMode } from "@karrio/hooks/app-mode";

export const ModeIndicator = (): JSX.Element => {
  const { testMode } = useAppMode();

  return (
    <>
      {testMode && (
        <div className="mode-indicator">
          <span className="mode-indicator-label has-text-weight-bold">
            TEST DATA
          </span>
        </div>
      )}
    </>
  );
};
