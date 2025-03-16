import { useMDXComponents as getNextraComponents } from 'nextra/mdx-components'

const defaultComponents = getNextraComponents({
  wrapper({ children, toc }) {
    return (
      <>
        <div style={{ flexGrow: 1, padding: 20 }}>{children}</div>
      </>
    )
  }
})

export const useMDXComponents = components => ({
  ...defaultComponents,
  ...components
})
