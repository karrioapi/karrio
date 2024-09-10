export function bundleContexts(
  contexts: React.FC<{ children?: React.ReactNode } & any>[],
) {
  const ContextProviders: React.FC<{ children?: React.ReactNode }> = ({
    children,
    ...props
  }) => {
    const NestedContexts = contexts.reduce(
      (_, Ctx) => <Ctx {...props}>{_}</Ctx>,
      children,
    );

    return <>{NestedContexts}</>;
  };

  return ContextProviders;
}
