export function bundleContexts(
  contexts: React.FC<{ children?: React.ReactNode } & any>[],
) {
  const ContextProviders = ({
    children,
    ...props
  }: {
    children?: React.ReactNode;
  }): JSX.Element => {
    const NestedContexts = contexts.reduce(
      (_, Ctx) => <Ctx {...props}>{_}</Ctx>,
      children,
    );

    return <>{NestedContexts}</>;
  };

  return ContextProviders;
}
