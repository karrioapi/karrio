// icons.tsx — Karrio Studio stroke icon set (ported from the design handoff)
import type { ReactNode, CSSProperties } from "react";

type IconProps = {
  size?: number;
  stroke?: number;
  fill?: string;
  style?: CSSProperties;
  className?: string;
};

const Ic = ({
  d,
  size = 16,
  stroke = 1.6,
  fill = "none",
  style,
  className,
}: IconProps & { d: ReactNode }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill={fill}
    stroke="currentColor"
    strokeWidth={stroke}
    strokeLinecap="round"
    strokeLinejoin="round"
    style={style}
    className={className}
  >
    {typeof d === "string" ? <path d={d} /> : d}
  </svg>
);

export const Icon = {
  Home: (p: IconProps) => <Ic {...p} d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z" />,
  Box: (p: IconProps) => (
    <Ic {...p} d={<><path d="m3.5 7.5 8.5-4 8.5 4-8.5 4z" /><path d="M3.5 7.5V17l8.5 4 8.5-4V7.5" /><path d="M12 11.5V21" /></>} />
  ),
  Truck: (p: IconProps) => (
    <Ic {...p} d={<><path d="M2 16V6a1 1 0 0 1 1-1h10v11H2z" /><path d="M13 9h4l4 4v3h-8z" /><circle cx="7" cy="18.5" r="2" /><circle cx="17" cy="18.5" r="2" /></>} />
  ),
  Pin: (p: IconProps) => (
    <Ic {...p} d={<><path d="M12 22s7-7 7-12a7 7 0 1 0-14 0c0 5 7 12 7 12z" /><circle cx="12" cy="10" r="2.5" /></>} />
  ),
  Inbox: (p: IconProps) => (
    <Ic {...p} d={<><path d="M21 14H16l-1.5 2.5h-5L8 14H3" /><path d="M5 5h14l2 9v5a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-5z" /></>} />
  ),
  Plug: (p: IconProps) => (
    <Ic {...p} d={<><path d="M9 2v6M15 2v6" /><path d="M7 8h10v3a5 5 0 0 1-10 0z" /><path d="M12 16v6" /></>} />
  ),
  Grid: (p: IconProps) => (
    <Ic {...p} d={<><rect x="3" y="3" width="7" height="7" rx="1" /><rect x="14" y="3" width="7" height="7" rx="1" /><rect x="3" y="14" width="7" height="7" rx="1" /><rect x="14" y="14" width="7" height="7" rx="1" /></>} />
  ),
  Code: (p: IconProps) => (
    <Ic {...p} d={<><path d="m8 7-5 5 5 5" /><path d="m16 7 5 5-5 5" /><path d="m14 4-4 16" /></>} />
  ),
  Shield: (p: IconProps) => <Ic {...p} d="M12 22s7-3 7-10V5l-7-3-7 3v7c0 7 7 10 7 10z" />,
  Settings: (p: IconProps) => (
    <Ic {...p} d={<><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" /></>} />
  ),
  Search: (p: IconProps) => <Ic {...p} d={<><circle cx="11" cy="11" r="7" /><path d="m20 20-3.5-3.5" /></>} />,
  Plus: (p: IconProps) => <Ic {...p} d="M12 5v14M5 12h14" />,
  ChevronD: (p: IconProps) => <Ic {...p} d="m6 9 6 6 6-6" />,
  ChevronR: (p: IconProps) => <Ic {...p} d="m9 6 6 6-6 6" />,
  X: (p: IconProps) => <Ic {...p} d="M18 6 6 18M6 6l12 12" />,
  Check: (p: IconProps) => <Ic {...p} d="m5 12 5 5L20 7" />,
  Filter: (p: IconProps) => <Ic {...p} d="M3 5h18l-7 9v6l-4-2v-4z" />,
  Refresh: (p: IconProps) => (
    <Ic {...p} d={<><path d="M3 12a9 9 0 0 1 15.5-6.3L21 8" /><path d="M21 3v5h-5" /><path d="M21 12a9 9 0 0 1-15.5 6.3L3 16" /><path d="M3 21v-5h5" /></>} />
  ),
  Doc: (p: IconProps) => (
    <Ic {...p} d={<><path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8z" /><path d="M14 3v5h5" /><path d="M9 13h6M9 17h6" /></>} />
  ),
  Tag: (p: IconProps) => (
    <Ic {...p} d={<><path d="M20.5 13.5 13 21l-9-9V4l8 .5 8 9z" /><circle cx="8" cy="8" r="1.4" /></>} />
  ),
  User: (p: IconProps) => (
    <Ic {...p} d={<><circle cx="12" cy="8" r="4" /><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6" /></>} />
  ),
  Activity: (p: IconProps) => <Ic {...p} d="M3 12h4l3-8 4 16 3-8h4" />,
  Lock: (p: IconProps) => (
    <Ic {...p} d={<><rect x="4" y="11" width="16" height="10" rx="1.5" /><path d="M8 11V7a4 4 0 1 1 8 0v4" /></>} />
  ),
  Webhook: (p: IconProps) => (
    <Ic {...p} d={<><path d="M8 12a4 4 0 1 1 7 2.7" /><path d="M14 21a4 4 0 0 1-3.4-6" /><path d="M6 17a4 4 0 0 1 5-5.5" /></>} />
  ),
  Key: (p: IconProps) => (
    <Ic {...p} d={<><circle cx="8" cy="14" r="4" /><path d="m10.5 11.5 9-9" /><path d="m18 4 2 2" /><path d="m15 7 2 2" /></>} />
  ),
  Workspace: (p: IconProps) => (
    <Ic {...p} d={<><rect x="3" y="3" width="8" height="8" rx="1.5" /><rect x="13" y="3" width="8" height="8" rx="1.5" /><rect x="3" y="13" width="8" height="8" rx="1.5" /><rect x="13" y="13" width="8" height="8" rx="1.5" /></>} />
  ),
  Sun: (p: IconProps) => (
    <Ic {...p} d={<><circle cx="12" cy="12" r="4" /><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41" /></>} />
  ),
  Moon: (p: IconProps) => <Ic {...p} d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />,
  Terminal: (p: IconProps) => (
    <Ic {...p} d={<><path d="m4 8 4 4-4 4" /><path d="M12 16h7" /><rect x="2" y="3" width="20" height="18" rx="1.5" /></>} />
  ),
  Sidebar: (p: IconProps) => (
    <Ic {...p} d={<><rect x="3" y="4" width="18" height="16" rx="1.5" /><path d="M9 4v16" /></>} />
  ),
  Pkg: (p: IconProps) => (
    <Ic {...p} d={<><path d="M3 7.5 12 3l9 4.5v9L12 21 3 16.5z" /><path d="M3 7.5 12 12l9-4.5M12 12v9" /></>} />
  ),
};

export type IconName = keyof typeof Icon;
