"use client";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@karrio/ui/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@karrio/ui/components/ui/table";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Shield, Key } from "lucide-react";
import {
  GetPermissionGroups_permission_groups_edges_node as PermissionGroup,
} from "@karrio/types/graphql/admin/types";

interface PermissionsTableProps {
  permissionGroups: Array<{ node: PermissionGroup }>;
  isLoading: boolean;
}

// Static permissions data based on typical Django/Karrio permissions
const KARRIO_PERMISSIONS = [
  {
    id: "view_user",
    name: "View User",
    description: "Can view user accounts and profiles",
    category: "User Management",
  },
  {
    id: "add_user",
    name: "Add User",
    description: "Can create new user accounts",
    category: "User Management",
  },
  {
    id: "change_user",
    name: "Change User",
    description: "Can modify user account details",
    category: "User Management",
  },
  {
    id: "delete_user",
    name: "Delete User",
    description: "Can remove user accounts",
    category: "User Management",
  },
  {
    id: "view_shipment",
    name: "View Shipment",
    description: "Can view shipment records",
    category: "Shipping",
  },
  {
    id: "add_shipment",
    name: "Add Shipment",
    description: "Can create new shipments",
    category: "Shipping",
  },
  {
    id: "change_shipment",
    name: "Change Shipment",
    description: "Can modify shipment details",
    category: "Shipping",
  },
  {
    id: "delete_shipment",
    name: "Delete Shipment",
    description: "Can remove shipments",
    category: "Shipping",
  },
  {
    id: "view_carrier",
    name: "View Carrier",
    description: "Can view carrier connections",
    category: "Carriers",
  },
  {
    id: "add_carrier",
    name: "Add Carrier",
    description: "Can create carrier connections",
    category: "Carriers",
  },
  {
    id: "change_carrier",
    name: "Change Carrier",
    description: "Can modify carrier settings",
    category: "Carriers",
  },
  {
    id: "delete_carrier",
    name: "Delete Carrier",
    description: "Can remove carrier connections",
    category: "Carriers",
  },
  {
    id: "view_tracker",
    name: "View Tracker",
    description: "Can view tracking information",
    category: "Tracking",
  },
  {
    id: "add_tracker",
    name: "Add Tracker",
    description: "Can create tracking records",
    category: "Tracking",
  },
  {
    id: "view_order",
    name: "View Order",
    description: "Can view order information",
    category: "Orders",
  },
  {
    id: "add_order",
    name: "Add Order",
    description: "Can create new orders",
    category: "Orders",
  },
  {
    id: "change_order",
    name: "Change Order",
    description: "Can modify order details",
    category: "Orders",
  },
  {
    id: "view_ratesheet",
    name: "View Rate Sheet",
    description: "Can view pricing rate sheets",
    category: "Pricing",
  },
  {
    id: "add_ratesheet",
    name: "Add Rate Sheet",
    description: "Can create pricing rate sheets",
    category: "Pricing",
  },
  {
    id: "change_ratesheet",
    name: "Change Rate Sheet",
    description: "Can modify pricing rate sheets",
    category: "Pricing",
  },
  {
    id: "view_webhook",
    name: "View Webhook",
    description: "Can view webhook configurations",
    category: "Integration",
  },
  {
    id: "add_webhook",
    name: "Add Webhook",
    description: "Can create webhook configurations",
    category: "Integration",
  },
  {
    id: "view_apikey",
    name: "View API Key",
    description: "Can view API key information",
    category: "API Access",
  },
  {
    id: "add_apikey",
    name: "Add API Key",
    description: "Can generate API keys",
    category: "API Access",
  },
];

function getCategoryBadgeVariant(category: string) {
  switch (category) {
    case "User Management": return "default";
    case "Shipping": return "secondary";
    case "Carriers": return "outline";
    case "Tracking": return "secondary";
    case "Orders": return "outline";
    case "Pricing": return "default";
    case "Integration": return "secondary";
    case "API Access": return "outline";
    default: return "secondary";
  }
}

export function PermissionsTable({ permissionGroups, isLoading }: PermissionsTableProps) {
  if (isLoading) {
    return (
      <div className="flex h-[calc(100vh-4rem)] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
      </div>
    );
  }

  // Group permissions by category
  const groupedPermissions = KARRIO_PERMISSIONS.reduce((acc, permission) => {
    if (!acc[permission.category]) {
      acc[permission.category] = [];
    }
    acc[permission.category].push(permission);
    return acc;
  }, {} as Record<string, typeof KARRIO_PERMISSIONS>);

  return (
    <div className="space-y-6">
      {/* Permission Groups */}
      {permissionGroups.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Key className="h-5 w-5" />
              Permission Groups ({permissionGroups.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Group Name</TableHead>
                  <TableHead>Members</TableHead>
                  <TableHead>Created</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {permissionGroups.map(({ node: group }) => (
                  <TableRow key={group.id}>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Shield className="h-4 w-4 text-muted-foreground" />
                        <span className="font-medium">{group.name}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="secondary">0 members</Badge>
                    </TableCell>
                    <TableCell>
                      <span className="text-sm text-muted-foreground">System default</span>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}

      {/* System Permissions by Category */}
      {Object.entries(groupedPermissions).map(([category, permissions]) => (
        <Card key={category}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              {category} Permissions ({permissions.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Permission</TableHead>
                  <TableHead>Description</TableHead>
                  <TableHead>Code</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {permissions.map((permission) => (
                  <TableRow key={permission.id}>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Badge variant={getCategoryBadgeVariant(category)}>
                          {permission.name}
                        </Badge>
                      </div>
                    </TableCell>
                    <TableCell>
                      <span className="text-sm text-muted-foreground">
                        {permission.description}
                      </span>
                    </TableCell>
                    <TableCell>
                      <code className="text-xs bg-muted px-2 py-1 rounded">
                        {permission.id}
                      </code>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}