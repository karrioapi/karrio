"use client";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@karrio/ui/components/ui/dialog";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { useOrganizationMutation } from "@karrio/hooks/organization";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { createContext, useContext, useState } from "react";

type OperationType = {
  onChange: (orgId: string) => Promise<any>;
};

interface CreateOrganizationDialogContextType {
  createOrganization: (operation: OperationType) => void;
}

const CreateOrganizationDialogContext = createContext<CreateOrganizationDialogContextType>(
  {} as CreateOrganizationDialogContextType,
);

export const CreateOrganizationDialogProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { createOrganization: mutation } = useOrganizationMutation();
  const { toast } = useToast();
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [operation, setOperation] = useState<OperationType | undefined>();
  const [name, setName] = useState<string>("");

  const createOrganization = (operation: OperationType) => {
    setOperation(operation);
    setIsOpen(true);
  };

  const close = () => {
    setIsOpen(false);
    setOperation(undefined);
    setName("");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name) return;

    try {
      const { createOrganization: result } = await mutation.mutateAsync({
        name,
      }) as any;

      if (result?.errors && result.errors.length > 0) {
        throw new Error(result.errors.map((e: any) => e.messages).join(', '));
      }

      const orgId = result?.organization?.id;
      if (orgId && operation?.onChange) {
        await operation.onChange(orgId);
      }
      toast({
        title: "Success",
        description: "Organization created successfully",
      });
      close();
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error creating organization",
        description: error.message,
      });
    }
  };

  return (
    <CreateOrganizationDialogContext.Provider value={{ createOrganization }}>
      {children}
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Create New Organization</DialogTitle>
            <DialogDescription>
              Create a new organization to manage your shipments.
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleSubmit}>
            <div className="grid gap-4 py-4">
              <div className="items-center gap-4 p-4 pb-8">
                <Label htmlFor="name" className="text-right">
                  Name
                </Label>
                <Input
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="col-span-3"
                  required
                />
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="ghost" onClick={close}>
                Cancel
              </Button>
              <Button type="submit" disabled={mutation.isLoading}>
                {mutation.isLoading ? "Creating..." : "Create"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </CreateOrganizationDialogContext.Provider>
  );
};

export function useCreateOrganizationDialog() {
  return useContext(CreateOrganizationDialogContext);
}
