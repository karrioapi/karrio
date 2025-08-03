"use client";

import {
  Card,
  CardContent,
} from "@karrio/ui/components/ui/card";
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
  DropdownMenuCheckboxItem,
  DropdownMenuTrigger,
} from "@karrio/ui/components/ui/dropdown-menu";
import { useOrganizationAccounts, useOrganizationAccountMutation } from "@karrio/hooks/admin-accounts";
import { GetAccounts_accounts_edges_node as Account } from "@karrio/types/graphql/admin/types";
import { MoreHorizontal, Building2, Users, Package, DollarSign, Eye } from "lucide-react";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@karrio/ui/components/ui/dialog";
import {
  Badge
} from "@karrio/ui/components/ui/badge";

type Column = {
  id: string;
  label: string;
  accessor: (account: Account) => string | number | JSX.Element;
  defaultVisible?: boolean;
};

const COLUMNS: Column[] = [
  {
    id: "name",
    label: "Organization",
    accessor: (account) => (
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
          <Building2 className="h-4 w-4 text-purple-600" />
        </div>
        <div>
          <div className="font-medium">{account.name}</div>
          <div className="text-sm text-muted-foreground">
            ID: {account.id}
          </div>
        </div>
      </div>
    ),
    defaultVisible: true,
  },
  {
    id: "members",
    label: "Members",
    accessor: (account) => (
      <div className="flex items-center gap-2">
        <Users className="h-4 w-4 text-purple-600" />
        <span>{account.usage?.members || 0}</span>
      </div>
    ),
    defaultVisible: true,
  },
  {
    id: "total_shipments",
    label: "Shipments",
    accessor: (account) => (
      <div className="flex items-center gap-2">
        <Package className="h-4 w-4 text-purple-600" />
        <span>{(account.usage?.total_shipments || 0).toLocaleString()}</span>
      </div>
    ),
    defaultVisible: true,
  },
  {
    id: "total_shipping_spend",
    label: "Shipping Spend",
    accessor: (account) => (
      <div className="flex items-center gap-2">
        <DollarSign className="h-4 w-4 text-purple-600" />
        <span>${(account.usage?.total_shipping_spend || 0).toLocaleString()}</span>
      </div>
    ),
    defaultVisible: true,
  },
  {
    id: "total_requests",
    label: "API Requests",
    accessor: (account) => (account.usage?.total_requests || 0).toLocaleString(),
    defaultVisible: false,
  },
  {
    id: "total_trackers",
    label: "Trackers",
    accessor: (account) => (account.usage?.total_trackers || 0).toLocaleString(),
    defaultVisible: false,
  },
  {
    id: "unfulfilled_orders",
    label: "Pending Orders",
    accessor: (account) => {
      const unfulfilled = account.usage?.unfulfilled_orders || 0;
      return unfulfilled > 0 ? (
        <Badge variant="secondary" className="bg-purple-100 text-purple-800">
          {unfulfilled}
        </Badge>
      ) : (
        <span className="text-muted-foreground">0</span>
      );
    },
    defaultVisible: false,
  },
  {
    id: "total_errors",
    label: "Errors",
    accessor: (account) => {
      const errors = account.usage?.total_errors || 0;
      return errors > 0 ? (
        <Badge variant="destructive">
          {errors}
        </Badge>
      ) : (
        <span className="text-muted-foreground">0</span>
      );
    },
    defaultVisible: false,
  },
  {
    id: "status",
    label: "Status",
    accessor: (account) => (
      <Badge variant={account.is_active ? "default" : "secondary"}>
        {account.is_active ? "Active" : "Inactive"}
      </Badge>
    ),
    defaultVisible: true,
  },
  {
    id: "created",
    label: "Connected",
    accessor: (account) =>
      new Date(account.created || Date.now()).toLocaleDateString(),
    defaultVisible: true,
  },
];

const ITEMS_PER_PAGE = 25;

const generateSlug = (name: string) => {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
};

export default function ShippersAccounts() {
  const { toast } = useToast();
  const [visibleColumns, setVisibleColumns] = useState<string[]>(
    COLUMNS.filter((col) => col.defaultVisible !== false).map((col) => col.id),
  );
  const [currentPage, setCurrentPage] = useState(1);
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isDisableOpen, setIsDisableOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [selectedAccount, setSelectedAccount] = useState<Account | null>(null);

  // Fetch accounts
  const { query, accounts: accountsData } = useOrganizationAccounts();
  const isLoading = query.isLoading;

  // Mutations
  const {
    createOrganizationAccount,
    updateOrganizationAccount,
    disableOrganizationAccount,
    deleteOrganizationAccount,
  } = useOrganizationAccountMutation();

  const handleCreateSuccess = () => {
    toast({ title: "Organization created successfully" });
    setIsCreateOpen(false);
  };

  const handleUpdateSuccess = () => {
    toast({ title: "Organization updated successfully" });
    setIsEditOpen(false);
    setSelectedAccount(null);
  };

  const handleDisableSuccess = () => {
    toast({ title: "Organization disabled successfully" });
    setIsDisableOpen(false);
    setSelectedAccount(null);
  };

  const handleDeleteSuccess = () => {
    toast({ title: "Organization deleted successfully" });
    setIsDeleteOpen(false);
    setSelectedAccount(null);
  };

  const handleError = (error: any, action: string) => {
    toast({
      title: `Failed to ${action} organization`,
      description: error.message || "An error occurred",
      variant: "destructive",
    });
  };

  const accounts = accountsData?.edges || [];
  const totalAccounts = accounts.length;
  const totalPages = Math.ceil(totalAccounts / ITEMS_PER_PAGE);

  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const endIndex = startIndex + ITEMS_PER_PAGE;

  const processedAccounts = accounts.map(({ node }) => {
    const account: Account = {
      ...node,
      created: node.created || new Date().toISOString(),
      modified: node.modified || new Date().toISOString(),
      usage: {
        members: node.usage?.members || 0,
        total_errors: node.usage?.total_errors || 0,
        order_volume: node.usage?.order_volume || 0,
        total_requests: node.usage?.total_requests || 0,
        total_trackers: node.usage?.total_trackers || 0,
        total_shipments: node.usage?.total_shipments || 0,
        unfulfilled_orders: node.usage?.unfulfilled_orders || 0,
        total_shipping_spend: node.usage?.total_shipping_spend || 0,
      },
    };
    return account;
  });

  const currentAccounts = processedAccounts.slice(startIndex, endIndex);

  const toggleColumn = (columnId: string) => {
    setVisibleColumns((prev) =>
      prev.includes(columnId)
        ? prev.filter((id) => id !== columnId)
        : [...prev, columnId],
    );
  };

  const handleCreate = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const name = formData.get("name") as string;
    createOrganizationAccount.mutate({
      name: name,
      slug: generateSlug(name),
    }, {
      onSuccess: handleCreateSuccess,
      onError: (error) => handleError(error, "create")
    });
  };

  const handleUpdate = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!selectedAccount) return;
    const formData = new FormData(e.currentTarget);
    const name = formData.get("name") as string;
    updateOrganizationAccount.mutate({
      id: String(selectedAccount.id),
      name: name,
      slug: generateSlug(name),
    }, {
      onSuccess: handleUpdateSuccess,
      onError: (error) => handleError(error, "update")
    });
  };

  const handleDisable = async () => {
    if (!selectedAccount) return;
    disableOrganizationAccount.mutate({
      id: String(selectedAccount.id),
    }, {
      onSuccess: handleDisableSuccess,
      onError: (error) => handleError(error, "disable")
    });
  };

  const handleDelete = async () => {
    if (!selectedAccount) return;
    deleteOrganizationAccount.mutate({
      id: String(selectedAccount.id),
    }, {
      onSuccess: handleDeleteSuccess,
      onError: (error) => handleError(error, "delete")
    });
  };

  if (isLoading) {
    return (
      <div className="flex h-[calc(100vh-4rem)] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
      </div>
    );
  }

  // Calculate summary stats
  const summaryStats = processedAccounts.reduce((acc, account) => ({
    totalShipments: acc.totalShipments + (account.usage?.total_shipments || 0),
    totalSpend: acc.totalSpend + (account.usage?.total_shipping_spend || 0),
    totalMembers: acc.totalMembers + (account.usage?.members || 0),
    activeOrgs: acc.activeOrgs + (account.is_active ? 1 : 0)
  }), { totalShipments: 0, totalSpend: 0, totalMembers: 0, activeOrgs: 0 });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Connected Organizations
          </h1>
          <p className="text-muted-foreground">
            Manage and monitor all organizations using your shipping platform
          </p>
        </div>
        <Button asChild>
          <AppLink href="/shippers/overview">
            <Eye className="h-4 w-4 mr-2" />
            System Overview
          </AppLink>
        </Button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="border-2 shadow-none">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Building2 className="h-5 w-5 text-purple-600" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Organizations</p>
                <p className="text-xl font-semibold">
                  {summaryStats.activeOrgs} / {totalAccounts}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-2 shadow-none">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Users className="h-5 w-5 text-purple-600" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Total Members</p>
                <p className="text-xl font-semibold">{summaryStats.totalMembers.toLocaleString()}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-2 shadow-none">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Package className="h-5 w-5 text-purple-600" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Total Shipments</p>
                <p className="text-xl font-semibold">{summaryStats.totalShipments.toLocaleString()}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-2 shadow-none">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <DollarSign className="h-5 w-5 text-purple-600" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Total Spend</p>
                <p className="text-xl font-semibold">${summaryStats.totalSpend.toLocaleString()}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="border-2 shadow-none">
        <CardContent className="p-6">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold">Organizations</h2>
            <div className="flex items-center space-x-2">
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" size="sm">
                    <span className="mr-2">Columns</span>
                    <span className="w-4 h-4">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                      >
                        <path
                          fillRule="evenodd"
                          d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                          clipRule="evenodd"
                        />
                      </svg>
                    </span>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  {COLUMNS.map((column) => (
                    <DropdownMenuCheckboxItem
                      key={column.id}
                      checked={visibleColumns.includes(column.id)}
                      onCheckedChange={() => toggleColumn(column.id)}
                    >
                      {column.label}
                    </DropdownMenuCheckboxItem>
                  ))}
                </DropdownMenuContent>
              </DropdownMenu>

              <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
                <DialogTrigger asChild>
                  <Button size="sm">Add Organization</Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Create New Organization</DialogTitle>
                    <DialogDescription>
                      Create a new organization account on your platform.
                    </DialogDescription>
                  </DialogHeader>
                  <form onSubmit={handleCreate} className="space-y-4">
                    <div className="space-y-2 p-4 pb-8">
                      <Label htmlFor="name">Organization Name</Label>
                      <Input id="name" name="name" required placeholder="Enter organization name" />
                    </div>
                    <DialogFooter>
                      <Button
                        type="submit"
                        disabled={createOrganizationAccount.isLoading}
                      >
                        {createOrganizationAccount.isLoading
                          ? "Creating..."
                          : "Create Organization"}
                      </Button>
                    </DialogFooter>
                  </form>
                </DialogContent>
              </Dialog>
            </div>
          </div>

          {currentAccounts.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <Building2 className="h-12 w-12 text-muted-foreground mb-4" />
              <p className="text-lg font-medium text-muted-foreground mb-2">No organizations found</p>
              <p className="text-sm text-muted-foreground">Create an organization to get started</p>
            </div>
          ) : (
            <>
              <Table>
                <TableHeader>
                  <TableRow>
                    {COLUMNS.filter((col) => visibleColumns.includes(col.id)).map(
                      (column) => (
                        <TableHead key={column.id}>{column.label}</TableHead>
                      ),
                    )}
                    <TableHead className="w-[50px]" />
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {currentAccounts.map((account) => (
                    <TableRow key={account.id}>
                      {COLUMNS.filter((col) => visibleColumns.includes(col.id)).map(
                        (column) => (
                          <TableCell key={column.id}>
                            {column.accessor(account)}
                          </TableCell>
                        ),
                      )}
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-slate-100">
                              <MoreHorizontal className="h-4 w-4 p-0" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem asChild>
                              <AppLink href={`/shippers/accounts/${account.id}`}>
                                View Details
                              </AppLink>
                            </DropdownMenuItem>
                            <DropdownMenuItem
                              onClick={() => {
                                setSelectedAccount(account);
                                setIsEditOpen(true);
                              }}
                            >
                              Edit
                            </DropdownMenuItem>
                            <DropdownMenuItem
                              onClick={() => {
                                setSelectedAccount(account);
                                setIsDisableOpen(true);
                              }}
                              className="text-yellow-600"
                            >
                              {account.is_active ? "Disable" : "Enable"}
                            </DropdownMenuItem>
                            <DropdownMenuItem
                              onClick={() => {
                                setSelectedAccount(account);
                                setIsDeleteOpen(true);
                              }}
                              className="text-destructive"
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

              <div className="mt-4 flex items-center justify-between">
                <p className="text-sm text-muted-foreground">
                  Showing {startIndex + 1} to {Math.min(endIndex, totalAccounts)} of{" "}
                  {totalAccounts} organizations
                </p>
                <div className="flex items-center space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1}
                  >
                    Previous
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() =>
                      setCurrentPage((prev) => Math.min(prev + 1, totalPages))
                    }
                    disabled={currentPage === totalPages}
                  >
                    Next
                  </Button>
                </div>
              </div>
            </>
          )}
        </CardContent>
      </Card>

      {/* Dialogs for Edit, Disable, Delete remain the same as original */}
      <Dialog
        open={isEditOpen}
        onOpenChange={(open) => {
          setIsEditOpen(open);
          if (!open) {
            requestAnimationFrame(() => {
              setSelectedAccount(null);
            });
          }
        }}
      >
        <DialogContent>
          {selectedAccount && (
            <>
              <DialogHeader className="p-4 pb-2">
                <DialogTitle>Edit Organization</DialogTitle>
                <DialogDescription>
                  Update organization details.
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleUpdate} className="space-y-4">
                <div className="space-y-2 p-4 pb-8">
                  <Label htmlFor="edit_name">Name</Label>
                  <Input
                    id="edit_name"
                    name="name"
                    defaultValue={selectedAccount?.name}
                    required
                  />
                </div>
                <DialogFooter>
                  <Button
                    type="submit"
                    disabled={updateOrganizationAccount.isLoading}
                  >
                    {updateOrganizationAccount.isLoading
                      ? "Saving..."
                      : "Save Changes"}
                  </Button>
                </DialogFooter>
              </form>
            </>
          )}
        </DialogContent>
      </Dialog>

      <Dialog
        open={isDisableOpen}
        onOpenChange={(open) => {
          setIsDisableOpen(open);
          if (!open) {
            requestAnimationFrame(() => {
              setSelectedAccount(null);
            });
          }
        }}
      >
        <DialogContent>
          {selectedAccount && (
            <>
              <DialogHeader>
                <DialogTitle>
                  {selectedAccount.is_active ? "Disable" : "Enable"} Organization
                </DialogTitle>
                <DialogDescription>
                  Are you sure you want to {selectedAccount.is_active ? "disable" : "enable"} {selectedAccount.name}?
                  {selectedAccount.is_active && " This will prevent the organization from accessing the platform."}
                </DialogDescription>
              </DialogHeader>
              <DialogFooter>
                <Button
                  variant="outline"
                  onClick={() => setIsDisableOpen(false)}
                >
                  Cancel
                </Button>
                <Button
                  variant={selectedAccount.is_active ? "destructive" : "default"}
                  onClick={handleDisable}
                  disabled={disableOrganizationAccount.isLoading}
                >
                  {disableOrganizationAccount.isLoading
                    ? `${selectedAccount.is_active ? "Disabling" : "Enabling"}...`
                    : `${selectedAccount.is_active ? "Disable" : "Enable"} Organization`}
                </Button>
              </DialogFooter>
            </>
          )}
        </DialogContent>
      </Dialog>

      <Dialog
        open={isDeleteOpen}
        onOpenChange={(open) => {
          setIsDeleteOpen(open);
          if (!open) {
            requestAnimationFrame(() => {
              setSelectedAccount(null);
            });
          }
        }}
      >
        <DialogContent>
          {selectedAccount && (
            <>
              <DialogHeader>
                <DialogTitle>Delete Organization</DialogTitle>
                <DialogDescription>
                  Are you sure you want to delete {selectedAccount.name}? This
                  action cannot be undone and will permanently remove all data.
                </DialogDescription>
              </DialogHeader>
              <DialogFooter>
                <Button
                  variant="outline"
                  onClick={() => setIsDeleteOpen(false)}
                >
                  Cancel
                </Button>
                <Button
                  variant="destructive"
                  onClick={handleDelete}
                  disabled={deleteOrganizationAccount.isLoading}
                >
                  {deleteOrganizationAccount.isLoading
                    ? "Deleting..."
                    : "Delete Organization"}
                </Button>
              </DialogFooter>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
