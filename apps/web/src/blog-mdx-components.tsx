import { useMDXComponents as nextUseMDXComponents } from 'nextra/mdx-components'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/cjs/styles/prism'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { CodeBlockClient } from '@/components/blog/code-block-client'
import { BackButton } from '@/components/blog/back-button'
import { Badge } from '@karrio/ui/components/ui/badge'
import { withGitHubAlert } from 'nextra/hocs/with-github-alert'
import { Callout } from 'nextra/components/callout'
import { formatDate } from '@/lib/utils'
import Image from 'next/image'
import Link from 'next/link'
import React from 'react'

// Map GitHub alert types to Callout types and their respective colors
const mapAlertTypeToCalloutType = (type: string) => {
  const typeMap = {
    'note': 'info',
    'tip': 'info',
    'important': 'default',
    'warning': 'warning',
    'caution': 'error'
  };
  return typeMap[type] || 'default';
};

// Create a Blockquote component with GitHub Alert syntax support
const Blockquote = withGitHubAlert(
  ({ type, ...props }) => {
    // This transforms GitHub alerts into Callout components with GitHub-like styling
    const alertType = mapAlertTypeToCalloutType(type);

    return (
      <div
        className="my-4 rounded-lg border p-3 nextra-callout"
        data-type={type}
        style={{
          backgroundColor: type === 'note' || type === 'tip'
            ? 'var(--callout-info-bg)'
            : type === 'warning'
              ? 'var(--callout-warning-bg)'
              : type === 'caution'
                ? 'var(--callout-error-bg)'
                : 'var(--callout-bg)',
          borderColor: type === 'note' || type === 'tip'
            ? 'var(--callout-info-border)'
            : type === 'warning'
              ? 'var(--callout-warning-border)'
              : type === 'caution'
                ? 'var(--callout-error-border)'
                : 'var(--callout-border)'
        }}
      >
        <Callout type={alertType} {...props} />
      </div>
    );
  },
  // This is your regular blockquote component for non-alert blockquotes with GitHub-like styling
  (props) => (
    <blockquote
      className="my-4 border-l-4 px-4 py-2.5 nextra-callout"
      style={{
        backgroundColor: 'var(--callout-bg)',
        borderColor: 'var(--callout-border)'
      }}
      {...props}
    />
  )
)

const CustomLink = (props) => {
  const href = props.href

  if (href.startsWith('/')) {
    return (
      <Link href={href} {...props}>
        {props.children}
      </Link>
    )
  }

  if (href.startsWith('#')) {
    return <a {...props} />
  }

  return <a target="_blank" rel="noopener noreferrer" {...props} />
}

// Custom code block component that supports line highlighting, filenames, etc.
const CustomCodeBlock = ({
  className,
  children,
  filename,
  showLineNumbers = true,
  ...props
}: {
  className?: string;
  children: React.ReactNode;
  filename?: string;
  showLineNumbers?: boolean;
  [key: string]: any;
}) => {
  // Extract language from className
  const match = /language-(\w+)/.exec(className || '')
  const language = match ? match[1] : ''

  // Extract line highlights from meta string (e.g. {1,4-5})
  const highlightLines = new Set<number>()
  const metaMatch = className?.match(/{([\d,-]+)}/)

  if (metaMatch && metaMatch[1]) {
    const ranges = metaMatch[1].split(',')
    ranges.forEach(range => {
      if (range.includes('-')) {
        const [start, end] = range.split('-').map(Number)
        for (let i = start; i <= end; i++) {
          highlightLines.add(i)
        }
      } else {
        highlightLines.add(Number(range))
      }
    })
  }

  // Convert children to string for highlighting
  const codeString = typeof children === 'string'
    ? children.trim()
    : (children && typeof children === 'object' && 'props' in children && children.props.children)
      ? typeof children.props.children === 'string'
        ? children.props.children.trim()
        : children.props.children
      : '';

  return (
    <div className="nextra-code-block not-prose border rounded-md overflow-hidden" style={{ borderColor: 'var(--code-border)' }}>
      {filename && (
        <div className="border-b px-3 py-1 text-xs font-medium rounded-t-md" style={{
          borderColor: 'var(--code-border)',
          backgroundColor: 'var(--code-header-bg)',
          color: 'var(--code-header-fg)'
        }}>
          {filename}
        </div>
      )}

      <CodeBlockClient codeString={codeString}>
        <SyntaxHighlighter
          PreTag="div"
          style={vscDarkPlus}
          language={language}
          showLineNumbers={showLineNumbers}
          wrapLines={true}
          lineProps={(lineNumber) => {
            const isHighlighted = highlightLines.has(lineNumber)
            return {
              style: {
                display: 'block',
                backgroundColor: isHighlighted ? 'rgba(255, 255, 255, 0.1)' : undefined,
              },
              className: isHighlighted ? 'highlighted-line' : undefined
            }
          }}
          customStyle={{
            margin: 0,
            padding: '0.75rem',
            fontSize: '0.9rem',
            background: 'var(--code-bg)',
            color: 'var(--code-fg)',
            borderRadius: filename ? '0 0 0.375rem 0.375rem' : '0.375rem',
          }}
          codeTagProps={{
            style: {
              fontFamily: 'var(--font-mono)'
            }
          }}
          {...props}
        >
          {codeString.trim()}
        </SyntaxHighlighter>
      </CodeBlockClient>
    </div>
  )
}

interface BlogWrapperProps {
  children: any
  toc?: any
  metadata?: any
  pageMap?: any[]
}

const BlogWrapper = ({ children, toc, metadata, pageMap }: BlogWrapperProps) => {
  const { title, date, description, tags, author, image, category, draft } = metadata || {};

  // Use default blog configuration
  const typesetting = 'article'
  const timestamp = true

  // Check if we should show draft indicator
  const isDraft = draft === true
  const isDevelopment = process.env.NODE_ENV === 'development'

  // Default blog layout
  return (
    <div className="py-8">
      <BackButton className="mb-4" />

      {/* Draft indicator - only show in development */}
      {isDraft && isDevelopment && (
        <div className="mb-6 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
            <span className="text-sm font-medium text-yellow-800 dark:text-yellow-200">
              Draft Post - Only visible in development
            </span>
          </div>
        </div>
      )}

      <div className="container mx-auto px-2 sm:px-4 lg:px-0 max-w-6xl bg-background dark:bg-inherit">
        {/* Featured Image */}
        {image && (
          <div className="mb-8 overflow-hidden rounded-xl">
            <div className="relative aspect-[21/9] w-full">
              <Image
                src={image}
                alt={title || 'Blog post featured image'}
                className="object-cover"
                fill
                priority
                sizes="(max-width: 768px) 100vw, (max-width: 1200px) 90vw, 800px"
              />
            </div>
          </div>
        )}

        {/* Category/Tag badge - if available */}
        {category && (
          <div className="mb-3">
            <Badge variant="secondary" className="text-xs font-medium uppercase tracking-wider">
              {category}
            </Badge>
          </div>
        )}

        {/* Title */}
        {title && (
          <h1 className="text-4xl font-bold mb-4 text-foreground">{title}</h1>
        )}

        {/* Meta information row */}
        <div className="flex flex-wrap items-center gap-3 mb-8 text-sm text-muted-foreground">
          {timestamp && date && (
            <time dateTime={date} className="flex items-center">
              {formatDate(date)}
            </time>
          )}

          {author && (
            <>
              <span className="text-muted-foreground/60">•</span>
              <span className="font-medium">{author}</span>
            </>
          )}

          {tags && tags.length > 0 && (
            <>
              <span className="text-muted-foreground/60">•</span>
              <div className="flex flex-wrap gap-2">
                {tags.map(tag => (
                  <Badge key={tag} variant="outline" className="hover:bg-primary/10 dark:hover:bg-primary/20">
                    {tag}
                  </Badge>
                ))}
              </div>
            </>
          )}
        </div>

        {/* Main content */}
        <div className={`prose ${typesetting === 'article' ? 'prose-lg' : 'prose-lg'} dark:prose-invert mx-auto max-w-none`}>
          {children}
        </div>
      </div>
    </div>
  )
}

// Create an enhanced Callout component that enforces proper styling
const EnhancedCallout = ({ type, children, ...props }) => {
  return (
    <div className={`nextra-callout`} data-type={type || 'default'}>
      <Callout type={type} {...props}>
        {children}
      </Callout>
    </div>
  );
};

export function useMDXComponents() {
  const components = nextUseMDXComponents({
    // Customize how markdown elements are rendered
    h1: (props) => <h1 className="text-3xl font-bold mt-8 mb-4" {...props} />,
    h2: (props) => <h2 className="text-2xl font-bold mt-8 mb-3" {...props} />,
    h3: (props) => <h3 className="text-xl font-bold mt-6 mb-3" {...props} />,
    h4: (props) => <h4 className="text-lg font-bold mt-4 mb-2" {...props} />,
    p: (props) => <p className="my-4" {...props} />,
    ul: (props) => <ul className="list-disc pl-6 my-4" {...props} />,
    ol: (props) => <ol className="list-decimal pl-6 my-4" {...props} />,
    blockquote: Blockquote,

    // Add syntax highlighting for code blocks
    code: ({ className, children, ...props }: { className?: string; children: React.ReactNode;[key: string]: any }) => {
      // Extract filename from meta string
      let filename: string | undefined = undefined

      // Method 1: Extract from props
      if (props.filename) {
        filename = props.filename as string
      }

      // Method 2: Extract from className
      if (!filename && className) {
        const filenameMatch = className.match(/filename="([^"]+)"/)
        if (filenameMatch) {
          filename = filenameMatch[1]
        }
      }

      // Method 3: Extract from content (first line comment)
      if (!filename && typeof children === 'string') {
        const firstLine = children.split('\n')[0]
        if (firstLine.startsWith('// ') || firstLine.startsWith('/* ') || firstLine.startsWith('# ')) {
          filename = firstLine.replace(/^(\/\/|\/\*|#)\s+/, '').trim()
          // Remove the first line from the code if it's a filename comment
          children = children.split('\n').slice(1).join('\n').trim()
        }
      }

      // For inline code (no language specified)
      if (!className || !className.startsWith('language-')) {
        return (
          <code
            className="rounded px-1 py-0.5 font-mono text-sm border"
            style={{
              backgroundColor: 'var(--code-bg)',
              color: 'var(--code-fg)',
              borderColor: 'var(--code-border)'
            }}
            {...props}
          >
            {children}
          </code>
        )
      }

      // For code blocks with language
      return (
        <CustomCodeBlock
          className={className}
          filename={filename}
          {...props}
        >
          {children}
        </CustomCodeBlock>
      )
    },

    // Custom components with proper styling
    Callout: EnhancedCallout,
    a: CustomLink,
    img: (props) => (
      <Image
        className="rounded-lg my-8"
        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        {...props}
      />
    )
  })

  // Return just the components without the wrapper
  return components
}

// Export BlogWrapper separately so it can be used only for blog pages
export { BlogWrapper }
