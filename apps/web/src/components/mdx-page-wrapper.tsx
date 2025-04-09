export const MDXPageWrapper = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="container mx-auto py-4 md:py-8">
      <div className="mx-auto px-4 sm:px-6 lg:px-0 max-w-6xl overflow-x-hidden">
        {/* Main content */}
        <div className="prose prose-lg dark:prose-invert mx-auto max-w-none overflow-x-scroll">
          {children}
        </div>
      </div>
    </div>
  )
}


