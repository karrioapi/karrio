interface PageHeaderProps {
  title: string;
  description?: string;
}

export function PageHeader({ title, description }: PageHeaderProps) {
  return (
    <div className="mb-8">
      <h1 className="text-4xl font-bold mb-2">{title}</h1>
      {description && (
        <p className="text-xl text-muted-foreground">{description}</p>
      )}
    </div>
  );
}
