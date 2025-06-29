"use client";

import { useSurcharges, useSurchargeMutation } from "@karrio/hooks/admin-surcharges";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@karrio/ui/components/ui/table";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@karrio/ui/components/ui/dropdown-menu";
import { Button } from "@karrio/ui/components/ui/button";
import { Switch } from "@karrio/ui/components/ui/switch";
import { Badge } from "@karrio/ui/components/ui/badge";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { MoreVertical } from "lucide-react";
import { useState } from "react";
import { DeleteConfirmationDialog } from "@karrio/ui/components/delete-confirmation-dialog";
import { SurchargeDialog } from "@karrio/ui/components/surcharge-dialog";
import {
  GetSurcharges_surcharges_edges_node as Surcharge,
  SurchargeTypeEnum,
} from "@karrio/types/graphql/admin/types";

interface FormValues {
  id?: string;
  name: string;
  amount: number;
  surcharge_type: SurchargeTypeEnum;
  active: boolean;
  carriers?: string[];
  services?: string[];
  carrier_accounts?: string[];
}

export default function Page() {
  const { toast } = useToast();
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [selectedSurcharge, setSelectedSurcharge] = useState<Surcharge | null>(null);
  const [page, setPage] = useState(1);

  const { query, surcharges } = useSurcharges();
  const isLoading = query.isLoading;

  const { createSurcharge, updateSurcharge, deleteSurcharge } = useSurchargeMutation();

  const handleCreateSuccess = () => {
    toast({ title: "Surcharge created successfully" });
    setIsCreateOpen(false);
  };

  const handleUpdateSuccess = () => {
    toast({ title: "Surcharge updated successfully" });
    setIsEditOpen(false);
    setSelectedSurcharge(null);
  };

  const handleDeleteSuccess = () => {
    toast({ title: "Surcharge deleted successfully" });
    setIsDeleteOpen(false);
    setSelectedSurcharge(null);
  };

  const handleError = (error: any, action: string) => {
    toast({
      title: `Failed to ${action} surcharge`,
      description: error.message || "An error occurred",
      variant: "destructive",
    });
  };

  const handleCreate = async (values: FormValues) => {
    const { carrier_accounts: _, id: __, ...input } = values;
    createSurcharge.mutate({
      name: input.name,
      amount: input.amount,
      surcharge_type: input.surcharge_type,
      active: input.active,
      carriers: input.carriers,
      services: input.services,
    }, {
      onSuccess: handleCreateSuccess,
      onError: (error) => handleError(error, "create")
    });
  };

  const handleUpdate = async (values: FormValues) => {
    if (!values.id) return;
    const { carrier_accounts: _, ...input } = values;
    updateSurcharge.mutate({
      id: values.id,
      name: input.name,
      amount: input.amount,
      surcharge_type: input.surcharge_type,
      active: input.active,
      carriers: input.carriers,
      services: input.services,
    }, {
      onSuccess: handleUpdateSuccess,
      onError: (error) => handleError(error, "update")
    });
  };

  const handleDelete = async () => {
    if (!selectedSurcharge) return;
    deleteSurcharge.mutate({
      id: selectedSurcharge.id,
    }, {
      onSuccess: handleDeleteSuccess,
      onError: (error) => handleError(error, "delete")
    });
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight">
          Surcharge Management
        </h1>
      </div>

      <Card>
        <CardContent className="p-6">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold">Surcharges</h2>
            <Button onClick={() => setIsCreateOpen(true)}>Add Surcharge</Button>
          </div>

          {surcharges?.edges.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <p className="text-sm text-muted-foreground">No surcharges found</p>
              <p className="text-sm text-muted-foreground">Add a surcharge to get started</p>
            </div>
          ) : (
            <>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>NAME</TableHead>
                    <TableHead>TYPE</TableHead>
                    <TableHead>AMOUNT</TableHead>
                    <TableHead>STATUS</TableHead>
                    <TableHead className="w-[50px]"></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {surcharges?.edges?.map(({ node: surcharge }) => (
                    <TableRow key={surcharge.id}>
                      <TableCell>{surcharge.name}</TableCell>
                      <TableCell>
                        <Badge variant="outline">{surcharge.surcharge_type}</Badge>
                      </TableCell>
                      <TableCell>
                        {surcharge.surcharge_type === SurchargeTypeEnum.PERCENTAGE
                          ? `${surcharge.amount}%`
                          : `$${surcharge.amount}`}
                      </TableCell>
                      <TableCell>
                        <Switch checked={surcharge.active} disabled />
                      </TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="h-8 w-8 p-0">
                              <MoreVertical className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem
                              onClick={() => {
                                setSelectedSurcharge(surcharge);
                                setIsEditOpen(true);
                              }}
                            >
                              Edit
                            </DropdownMenuItem>
                            <DropdownMenuItem
                              className="text-destructive"
                              onClick={() => {
                                setSelectedSurcharge(surcharge);
                                setIsDeleteOpen(true);
                              }}
                            >
                              Delete
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>

              {surcharges?.page_info && (
                <div className="mt-4 flex items-center justify-between">
                  <p className="text-sm text-muted-foreground">
                    Showing {surcharges.edges.length} of {surcharges.page_info.count} surcharges
                  </p>
                  <div className="flex items-center space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setPage(page - 1)}
                      disabled={!surcharges.page_info.has_previous_page}
                    >
                      Previous
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setPage(page + 1)}
                      disabled={!surcharges.page_info.has_next_page}
                    >
                      Next
                    </Button>
                  </div>
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>

      <SurchargeDialog
        open={isCreateOpen}
        onOpenChange={setIsCreateOpen}
        onSubmit={handleCreate}
      />

      <SurchargeDialog
        open={isEditOpen}
        onOpenChange={setIsEditOpen}
        onSubmit={handleUpdate}
        defaultValues={selectedSurcharge || undefined}
      />

      <DeleteConfirmationDialog
        open={isDeleteOpen}
        onOpenChange={setIsDeleteOpen}
        onConfirm={handleDelete}
        title="Delete Surcharge"
        description="Are you sure you want to delete this surcharge? This action cannot be undone."
      />
    </div>
  );
}
