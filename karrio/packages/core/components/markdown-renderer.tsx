"use client";
import React from 'react';

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

// Error boundary for markdown rendering
class MarkdownErrorBoundary extends React.Component<
  { children: React.ReactNode; fallback: React.ReactNode },
  { hasError: boolean }
> {
  constructor(props: { children: React.ReactNode; fallback: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.warn('Markdown rendering failed:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }

    return this.props.children;
  }
}

// Fallback markdown renderer using simple regex replacements
function SimplifiedMarkdownRenderer({ content, className = '' }: MarkdownRendererProps) {
  const processMarkdown = (text: string): string => {
    return text
      // Headers
      .replace(/^### (.*$)/gim, '<h3 class="text-lg font-semibold text-slate-900 mb-2 mt-4">$1</h3>')
      .replace(/^## (.*$)/gim, '<h2 class="text-xl font-semibold text-slate-900 mb-3 mt-5">$1</h2>')
      .replace(/^# (.*$)/gim, '<h1 class="text-2xl font-bold text-slate-900 mb-4 mt-6 first:mt-0">$1</h1>')

      // Bold and italic
      .replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-slate-900">$1</strong>')
      .replace(/\*(.*?)\*/g, '<em class="italic">$1</em>')

      // Code blocks
      .replace(/```([\s\S]*?)```/g, '<pre class="bg-slate-100 border border-slate-200 rounded-md p-3 my-3 overflow-x-auto"><code class="text-sm text-slate-800">$1</code></pre>')
      .replace(/`([^`]+)`/g, '<code class="bg-slate-100 px-1.5 py-0.5 rounded text-sm text-slate-800 font-mono">$1</code>')

      // Links
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-blue-600 hover:text-blue-800 underline" target="_blank" rel="noopener noreferrer">$1</a>')

      // Lists
      .replace(/^\* (.*$)/gim, '<li class="ml-4 list-disc">$1</li>')
      .replace(/^- (.*$)/gim, '<li class="ml-4 list-disc">$1</li>')
      .replace(/^\d+\. (.*$)/gim, '<li class="ml-4 list-decimal">$1</li>')

      // Line breaks
      .replace(/\n\n/g, '</p><p class="mb-3 text-slate-700 leading-relaxed">')
      .replace(/\n/g, '<br>');
  };

  const processedContent = processMarkdown(content);

  return (
    <div
      className={`markdown-content prose prose-sm max-w-none ${className}`}
      dangerouslySetInnerHTML={{
        __html: `<p class="mb-3 text-slate-700 leading-relaxed">${processedContent}</p>`
      }}
    />
  );
}

// Advanced markdown renderer using react-markdown (with error boundary)
function AdvancedMarkdownRenderer({ content, className = '' }: MarkdownRendererProps) {
  const [ReactMarkdown, setReactMarkdown] = React.useState<any>(null);
  const [remarkGfm, setRemarkGfm] = React.useState<any>(null);
  const [loadError, setLoadError] = React.useState(false);

  React.useEffect(() => {
    const loadMarkdownLibs = async () => {
      try {
        const [reactMarkdownModule, remarkGfmModule] = await Promise.all([
          import('react-markdown'),
          import('remark-gfm')
        ]);

        setReactMarkdown(() => reactMarkdownModule.default);
        setRemarkGfm(() => remarkGfmModule.default);
      } catch (error) {
        console.warn('Failed to load markdown libraries:', error);
        setLoadError(true);
      }
    };

    loadMarkdownLibs();
  }, []);

  if (loadError || !ReactMarkdown || !remarkGfm) {
    return <SimplifiedMarkdownRenderer content={content} className={className} />;
  }

  const components = {
    // Headers
    h1: ({ children }: any) => (
      <h1 className="text-2xl font-bold text-slate-900 mb-4 mt-6 first:mt-0">
        {children}
      </h1>
    ),
    h2: ({ children }: any) => (
      <h2 className="text-xl font-semibold text-slate-900 mb-3 mt-5">
        {children}
      </h2>
    ),
    h3: ({ children }: any) => (
      <h3 className="text-lg font-semibold text-slate-900 mb-2 mt-4">
        {children}
      </h3>
    ),
    h4: ({ children }: any) => (
      <h4 className="text-base font-semibold text-slate-900 mb-2 mt-3">
        {children}
      </h4>
    ),
    h5: ({ children }: any) => (
      <h5 className="text-sm font-semibold text-slate-900 mb-1 mt-2">
        {children}
      </h5>
    ),
    h6: ({ children }: any) => (
      <h6 className="text-xs font-semibold text-slate-900 mb-1 mt-2">
        {children}
      </h6>
    ),

    // Paragraphs and text
    p: ({ children }: any) => (
      <p className="mb-3 text-slate-700 leading-relaxed">
        {children}
      </p>
    ),
    strong: ({ children }: any) => (
      <strong className="font-semibold text-slate-900">
        {children}
      </strong>
    ),
    em: ({ children }: any) => (
      <em className="italic">
        {children}
      </em>
    ),

    // Links
    a: ({ href, children }: any) => (
      <a
        href={href}
        className="text-blue-600 hover:text-blue-800 underline"
        target="_blank"
        rel="noopener noreferrer"
      >
        {children}
      </a>
    ),

    // Lists
    ul: ({ children }: any) => (
      <ul className="mb-3 ml-4 space-y-1">
        {children}
      </ul>
    ),
    ol: ({ children }: any) => (
      <ol className="mb-3 ml-4 space-y-1 list-decimal">
        {children}
      </ol>
    ),
    li: ({ children }: any) => (
      <li className="text-slate-700 list-disc">
        {children}
      </li>
    ),

    // Code
    code: ({ inline, children }: any) => {
      if (inline) {
        return (
          <code className="bg-slate-100 px-1.5 py-0.5 rounded text-sm text-slate-800 font-mono">
            {children}
          </code>
        );
      }
      return (
        <code className="text-sm text-slate-800">
          {children}
        </code>
      );
    },
    pre: ({ children }: any) => (
      <pre className="bg-slate-100 border border-slate-200 rounded-md p-3 my-3 overflow-x-auto">
        {children}
      </pre>
    ),

    // Blockquotes
    blockquote: ({ children }: any) => (
      <blockquote className="border-l-4 border-slate-300 pl-4 my-3 italic text-slate-600">
        {children}
      </blockquote>
    ),

    // Tables
    table: ({ children }: any) => (
      <div className="my-3 overflow-x-auto">
        <table className="min-w-full border border-slate-200 rounded-md">
          {children}
        </table>
      </div>
    ),
    thead: ({ children }: any) => (
      <thead className="bg-slate-50">
        {children}
      </thead>
    ),
    tbody: ({ children }: any) => (
      <tbody className="divide-y divide-slate-200">
        {children}
      </tbody>
    ),
    tr: ({ children }: any) => (
      <tr>
        {children}
      </tr>
    ),
    th: ({ children }: any) => (
      <th className="px-3 py-2 text-left text-xs font-semibold text-slate-900 border-b border-slate-200">
        {children}
      </th>
    ),
    td: ({ children }: any) => (
      <td className="px-3 py-2 text-sm text-slate-700 border-b border-slate-200">
        {children}
      </td>
    ),

    // Horizontal rule
    hr: () => (
      <hr className="my-4 border-slate-200" />
    ),
  };

  return (
    <div className={`markdown-content prose prose-sm max-w-none ${className}`}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={components}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}

export function MarkdownRenderer({ content, className = '' }: MarkdownRendererProps) {
  return (
    <MarkdownErrorBoundary
      fallback={<SimplifiedMarkdownRenderer content={content} className={className} />}
    >
      <AdvancedMarkdownRenderer content={content} className={className} />
    </MarkdownErrorBoundary>
  );
}
