"use client";
import { TemplateEditor } from "@karrio/ui/components/template-editor";
import { useRouter, useSearchParams } from "next/navigation";

export default function TemplatePage(pageProps: any) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const templateId = searchParams.get("id") as string;

  const handleClose = () => {
    router.push('/settings/templates');
  };

  const handleSave = () => {
    // Save logic handled by TemplateEditor
  };

  const Component = (): JSX.Element => {
    return (
      <div className="min-h-screen bg-background">
        <TemplateEditor
          templateId={templateId}
          onClose={handleClose}
          onSave={handleSave}
        />
      </div>
    );
  };

  return <Component />;
}
