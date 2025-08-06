"use client";

import { useParams } from "next/navigation";
import { useState } from "react";
import { useOrganizationAccounts, useOrganizationAccountMutation } from "@karrio/hooks/admin-accounts";
import { useToast } from "@karrio/ui/hooks/use-toast";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@karrio/ui/components/ui/card";
import { Button } from "@karrio/ui/components/ui/button";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@karrio/ui/components/ui/tabs";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@karrio/ui/components/ui/table";
import {
  ArrowLeft,
  Activity,
  TrendingUp,
  TrendingDown,
  DollarSign,
  Package,
  Users,
  AlertTriangle,
  Settings,
  CreditCard,
  Truck,
  FileText,
  Calendar,
  MoreHorizontal,
} from "lucide-react";
import { formatDistanceToNow } from "date-fns";

interface AccountDetailProps {
  accountId: string;
}

export default function OrganizationAccountDetail() {
  const params = useParams();
  const accountId = params.accountId as string;
  const { toast } = useToast();
  const [selectedTimeRange, setSelectedTimeRange] = useState("30d");

  // Fetch account details - using the list hook with filter for now
  const { query, accounts } = useOrganizationAccounts({ id: accountId });
  const account = accounts?.edges?.[0]?.node;
  const isLoading = query.isLoading;

  // Note: These would need to be implemented in the backend
  const transactions = null; // Placeholder for transactions data
  const analytics = null; // Placeholder for analytics data

  const { updateOrganizationAccount } = useOrganizationAccountMutation();

  const handleToggleStatus = () => {
    if (!account) return;

    updateOrganizationAccount.mutate(
      {
        id: account.id,
        is_active: !account.is_active,
      },
      {
        onSuccess: () => {
          toast({ title: "Account status updated successfully" });
        },
        onError: (error: any) => {
          toast({
            title: "Failed to update account status",
            description: error.message || "An error occurred",
            variant: "destructive",
          });
        },
      },
    );
  };

  if (isLoading) {
    return (
      <div className="flex h-[calc(100vh-4rem)] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
      </div>
    );
  }

  if (!account) {
    return (
      <div className="p-6">
        <div className="text-center">
          <h2 className="text-lg font-semibold">Account not found</h2>
          <p className="text-muted-foreground">The requested account could not be found.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button variant="ghost" size="icon" onClick={() => window.history.back()}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-2xl font-semibold tracking-tight">{account.name}</h1>
            <p className="text-muted-foreground">Account ID: {account.id}</p>
          </div>
          <Badge variant={account.is_active ? "default" : "secondary"}>
            {account.is_active ? "Active" : "Inactive"}
          </Badge>
        </div>
        <div className="flex items-center space-x-2">
          <Button onClick={handleToggleStatus} variant="outline">
            {account.is_active ? "Disable Account" : "Enable Account"}
          </Button>
          <Button variant="outline">
            <Settings className="h-4 w-4 mr-2" />
            Configure
          </Button>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Shipments</CardTitle>
            <Package className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{account.usage?.total_shipments || 0}</div>
            <p className="text-xs text-muted-foreground">
              +12% from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Shipping Spend</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${(account.usage?.total_shipping_spend || 0).toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              +8% from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">API Requests</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{account.usage?.total_requests || 0}</div>
            <p className="text-xs text-muted-foreground">
              +5% from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Error Rate</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {account.usage?.total_errors || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              -2% from last month
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Tabs */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="transactions">Transactions</TabsTrigger>
          <TabsTrigger value="team">Team</TabsTrigger>
          <TabsTrigger value="carriers">Carriers</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Recent Activity */}
            <Card>
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
                <CardDescription>Latest shipments and API calls</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {/* Mock recent activity items */}
                  <div className="flex items-center space-x-3">
                    <div className="flex-shrink-0">
                      <Package className="h-5 w-5 text-blue-500" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium">Shipment created</p>
                      <p className="text-sm text-muted-foreground">Tracking: UPS123456789</p>
                    </div>
                    <div className="text-sm text-muted-foreground">
                      2 hours ago
                    </div>
                  </div>

                  <div className="flex items-center space-x-3">
                    <div className="flex-shrink-0">
                      <Activity className="h-5 w-5 text-green-500" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium">Rate quoted</p>
                      <p className="text-sm text-muted-foreground">FedEx Ground - $12.45</p>
                    </div>
                    <div className="text-sm text-muted-foreground">
                      4 hours ago
                    </div>
                  </div>

                  <div className="flex items-center space-x-3">
                    <div className="flex-shrink-0">
                      <Users className="h-5 w-5 text-purple-500" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium">Team member added</p>
                      <p className="text-sm text-muted-foreground">john@company.com</p>
                    </div>
                    <div className="text-sm text-muted-foreground">
                      1 day ago
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Account Information */}
            <Card>
              <CardHeader>
                <CardTitle>Account Information</CardTitle>
                <CardDescription>Organization details and metadata</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium">Created</label>
                    <p className="text-sm text-muted-foreground">
                      {formatDistanceToNow(new Date(account.created), { addSuffix: true })}
                    </p>
                  </div>
                  <div>
                    <label className="text-sm font-medium">Last Modified</label>
                    <p className="text-sm text-muted-foreground">
                      {formatDistanceToNow(new Date(account.modified), { addSuffix: true })}
                    </p>
                  </div>
                  <div>
                    <label className="text-sm font-medium">Slug</label>
                    <p className="text-sm text-muted-foreground">{account.slug}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium">Members</label>
                    <p className="text-sm text-muted-foreground">
                      {account.usage?.members || 0} members
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="transactions" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Transaction History</CardTitle>
              <CardDescription>Detailed shipment and payment transactions</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Date</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Description</TableHead>
                    <TableHead>Amount</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {/* Mock transaction data */}
                  <TableRow>
                    <TableCell>Dec 15, 2024</TableCell>
                    <TableCell>
                      <Badge variant="outline">Shipment</Badge>
                    </TableCell>
                    <TableCell>UPS Ground - Package delivery</TableCell>
                    <TableCell>$12.45</TableCell>
                    <TableCell>
                      <Badge variant="default">Completed</Badge>
                    </TableCell>
                    <TableCell>
                      <Button variant="ghost" size="icon">
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </TableCell>
                  </TableRow>

                  <TableRow>
                    <TableCell>Dec 14, 2024</TableCell>
                    <TableCell>
                      <Badge variant="outline">Refund</Badge>
                    </TableCell>
                    <TableCell>Cancelled shipment refund</TableCell>
                    <TableCell>-$8.20</TableCell>
                    <TableCell>
                      <Badge variant="secondary">Processing</Badge>
                    </TableCell>
                    <TableCell>
                      <Button variant="ghost" size="icon">
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="team" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Team Members</CardTitle>
              <CardDescription>Users with access to this organization</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8">
                <Users className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">Team management interface would go here</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="carriers" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Configured Carriers</CardTitle>
              <CardDescription>Shipping carriers available to this organization</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8">
                <Truck className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">Carrier configuration interface would go here</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="settings" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Account Settings</CardTitle>
              <CardDescription>Configuration and preferences for this organization</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8">
                <Settings className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">Settings interface would go here</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
