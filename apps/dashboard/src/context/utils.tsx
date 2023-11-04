

export function bundleContexts(contexts: React.FC<any>[]) {
  const ContextProviders: React.FC = ({ children, ...props }) => {
    const NestedContexts = contexts.reduce((_, Ctx) => <Ctx {...props}>{_}</Ctx>, children);

    return (
      <>{NestedContexts}</>
    );
  };

  return ContextProviders;
}
