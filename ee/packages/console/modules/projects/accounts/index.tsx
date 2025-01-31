"use client";

import { useParams } from "next/navigation";
import { trpc } from "@karrio/console/trpc/client";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@karrio/insiders/components/ui/table";
import { Badge } from "@karrio/insiders/components/ui/badge";
import { Alert, AlertDescription } from "@karrio/insiders/components/ui/alert";
import { DashboardHeader } from "@karrio/console/components/dashboard-header";
import { AlertTriangle, Settings2, Search, RefreshCw } from "lucide-react";
import moment from "moment";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@karrio/insiders/components/ui/card";
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@karrio/insiders/components/ui/dropdown-menu";
import { Button } from "@karrio/insiders/components/ui/button";
import { Input } from "@karrio/insiders/components/ui/input";
import { useState } from "react";
import { Pagination } from "@karrio/insiders/components/ui/pagination";

interface Column {
  id: string;
  label: string;
  visible: boolean;
  render: (account: any) => React.ReactNode;
}

const PAGE_SIZE = 10;

export default function ConnectedAccounts() {
  const params = useParams<{ projectId: string; orgId: string }>();
  const [page, setPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState("");
  const [columns, setColumns] = useState<Column[]>([
    {
      id: "name",
      label: "Account",
      visible: true,
      render: (account) => (
        <div className="flex items-center gap-3">
          <span className="font-medium">{account.name}</span>
        </div>
      ),
    },
    {
      id: "status",
      label: "Status",
      visible: true,
      render: (account) => (
        <Badge
          variant={account.is_active ? "default" : "destructive"}
          className="px-4 py-1"
        >
          {account.is_active ? "Active" : "Inactive"}
        </Badge>
      ),
    },
    {
      id: "volume",
      label: "Volume",
      visible: true,
      render: (account) => (
        <div className="text-right">
          <span className="font-semibold">
            ${account.usage?.total_shipping_spend?.toFixed(2) || "0.00"}
          </span>
          <p className="text-xs text-muted-foreground">Total Spend</p>
        </div>
      ),
    },
    {
      id: "shipments",
      label: "Shipments",
      visible: true,
      render: (account) => (
        <div className="text-right">
          <span className="font-semibold">
            {account.usage?.total_shipments || 0}
          </span>
          <p className="text-xs text-muted-foreground">Total Shipments</p>
        </div>
      ),
    },
    {
      id: "trackers",
      label: "Trackers",
      visible: true,
      render: (account) => (
        <div className="text-right">
          <span className="font-semibold">
            {account.usage?.total_trackers || 0}
          </span>
          <p className="text-xs text-muted-foreground">Total Trackers</p>
        </div>
      ),
    },
    {
      id: "members",
      label: "Members",
      visible: true,
      render: (account) => (
        <div className="text-right">
          <span className="font-semibold">{account.usage?.members || 0}</span>
          <p className="text-xs text-muted-foreground">Active Users</p>
        </div>
      ),
    },
    {
      id: "connected",
      label: "Connected",
      visible: true,
      render: (account) => (
        <div className="text-right">
          <span>{moment(account.created).format("MMM D, YYYY")}</span>
          <p className="text-xs text-muted-foreground">
            {moment(account.created).fromNow()}
          </p>
        </div>
      ),
    },
  ]);

  const { data: project, isLoading: isProjectLoading } =
    trpc.projects.get.useQuery({
      id: params.projectId,
      orgId: params.orgId as string,
    });

  const { data: accounts, refetch } =
    trpc.projects.tenant.getConnectedAccounts.useQuery(
      {
        projectId: params.projectId,
      },
      {
        enabled: project?.status === "ACTIVE",
      },
    );

  const visibleColumns = columns.filter((col) => col.visible);
  const filteredAccounts = accounts?.edges?.filter((edge) =>
    edge.node.name.toLowerCase().includes(searchQuery.toLowerCase()),
  );
  const totalPages = Math.ceil((filteredAccounts?.length || 0) / PAGE_SIZE);
  const paginatedAccounts = filteredAccounts?.slice(
    (page - 1) * PAGE_SIZE,
    page * PAGE_SIZE,
  );

  const toggleColumn = (columnId: string) => {
    setColumns(
      columns.map((col) =>
        col.id === columnId ? { ...col, visible: !col.visible } : col,
      ),
    );
  };

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader
        title="Connected Accounts"
        description="Manage your carrier accounts and track their usage"
      />

      <div className="container mx-auto py-8">
        <div className="max-w-7xl mx-auto space-y-6">
          {isProjectLoading ? (
            <Card>
              <CardContent className="h-24 flex items-center justify-center">
                <RefreshCw className="h-5 w-5 animate-spin text-muted-foreground" />
              </CardContent>
            </Card>
          ) : project?.status !== "ACTIVE" ? (
            <Alert variant="destructive" className="border-2">
              <AlertTriangle className="h-5 w-5" />
              <AlertDescription className="font-medium">
                Project tenant is not healthy. Please check your project status.
              </AlertDescription>
            </Alert>
          ) : (
            <Card className="shadow-md">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-6">
                <div className="space-y-1">
                  <CardTitle className="text-2xl">Connected Accounts</CardTitle>
                  <p className="text-sm text-muted-foreground">
                    Showing {paginatedAccounts?.length || 0} of{" "}
                    {accounts?.edges?.length || 0} accounts
                  </p>
                </div>
                <div className="flex items-center gap-4">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Search accounts..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-9 w-[250px]"
                    />
                  </div>
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={() => refetch()}
                  >
                    <RefreshCw className="h-4 w-4" />
                  </Button>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="outline" size="icon">
                        <Settings2 className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end" className="w-48">
                      {columns.map((column) => (
                        <DropdownMenuCheckboxItem
                          key={column.id}
                          checked={column.visible}
                          onCheckedChange={() => toggleColumn(column.id)}
                        >
                          {column.label}
                        </DropdownMenuCheckboxItem>
                      ))}
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </CardHeader>
              <CardContent>
                <div className="rounded-lg border">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        {visibleColumns.map((column) => (
                          <TableHead
                            key={column.id}
                            className={
                              column.id === "volume" ||
                                column.id === "members" ||
                                column.id === "connected" ||
                                column.id === "shipments" ||
                                column.id === "trackers"
                                ? "text-right"
                                : ""
                            }
                          >
                            {column.label}
                          </TableHead>
                        ))}
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {paginatedAccounts?.map((edge) => (
                        <TableRow
                          key={edge.node.id}
                          className="hover:bg-muted/50"
                        >
                          {visibleColumns.map((column) => (
                            <TableCell
                              key={`${edge.node.id}-${column.id}`}
                              className={
                                column.id === "volume" ||
                                  column.id === "members" ||
                                  column.id === "connected" ||
                                  column.id === "shipments" ||
                                  column.id === "trackers"
                                  ? "text-right"
                                  : ""
                              }
                            >
                              {column.render(edge.node)}
                            </TableCell>
                          ))}
                        </TableRow>
                      ))}
                      {(!paginatedAccounts ||
                        paginatedAccounts.length === 0) && (
                          <TableRow>
                            <TableCell
                              colSpan={visibleColumns.length}
                              className="h-32 text-center"
                            >
                              <div className="flex flex-col items-center gap-2 text-muted-foreground">
                                <AlertTriangle className="h-8 w-8" />
                                <p>No connected accounts found</p>
                              </div>
                            </TableCell>
                          </TableRow>
                        )}
                    </TableBody>
                  </Table>
                </div>

                {totalPages > 1 && (
                  <div className="mt-6">
                    <Pagination
                      currentPage={page}
                      totalPages={totalPages}
                      onPageChange={setPage}
                    />
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
