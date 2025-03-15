/**
 * Custom type declarations to make Docusaurus components compatible with React 19
 */

declare module '@theme/Layout' {
  import type { ReactNode } from 'react';

  export interface Props {
    children?: ReactNode;
    title?: string;
    description?: string;
    wrapperClassName?: string;
    pageClassName?: string;
    noFooter?: boolean;
    searchMetadatas?: {
      version?: string;
      tag?: string;
    };
  }

  export default function Layout(props: Props): JSX.Element;
}

declare module '@docusaurus/Link' {
  import type { ComponentProps, ReactNode } from 'react';

  export interface Props extends ComponentProps<'a'> {
    to?: string;
    activeClassName?: string;
    isNavLink?: boolean;
    exact?: boolean;
    href?: string;
    children?: ReactNode;
  }

  export default function Link(props: Props): JSX.Element;
}

declare module '@docusaurus/useDocusaurusContext' {
  export interface DocusaurusContext {
    siteConfig: {
      title: string;
      tagline: string;
      url: string;
      baseUrl: string;
      favicon: string;
      organizationName: string;
      projectName: string;
      customFields?: Record<string, any>;
      themeConfig: Record<string, any>;
      [key: string]: any;
    };
    siteMetadata: {
      docusaurusVersion: string;
      siteVersion?: string;
      pluginVersions: Record<string, string>;
    };
    globalData: Record<string, any>;
    isClient: boolean;
    i18n: {
      currentLocale: string;
      locales: string[];
      defaultLocale: string;
      localeConfigs: Record<string, { label: string; direction: string }>;
    };
  }

  export default function useDocusaurusContext(): DocusaurusContext;
}

declare module '@theme/DocSidebar' {
  import type { ReactNode } from 'react';

  export interface Props {
    path: string;
    sidebar: any;
    sidebarCollapsible?: boolean;
    onCollapse?: () => void;
    isHidden?: boolean;
    children?: ReactNode;
  }

  export default function DocSidebar(props: Props): JSX.Element;
}

declare module '@theme/Navbar' {
  import type { ReactNode } from 'react';

  export interface Props {
    items: any[];
    children?: ReactNode;
  }

  export default function Navbar(props: Props): JSX.Element;
}
