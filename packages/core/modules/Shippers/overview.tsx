"use client";
import { LineChart, Line, CartesianGrid, XAxis, Tooltip, ResponsiveContainer } from "recharts";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { SelectField } from "@karrio/ui/core/components";
import { useAdminSystemUsage } from "@karrio/hooks/admin-usage";
import { useOrganizationAccounts } from "@karrio/hooks/admin-accounts";
import { useUser } from "@karrio/hooks/user";
import { StatusBadge } from "@karrio/ui/components/status-badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from "@karrio/ui/components/ui/table";
import { Building2, Users, Package, DollarSign, MoreHorizontal, Eye } from "lucide-react";
import { Button } from "@karrio/ui/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@karrio/ui/components/ui/dropdown-menu";
import moment from "moment";

export default function ShippersOverview() {
  const {
    query: { data: { user } = {} },
  } = useUser();
  const {
    query: { data: { usage } = {} },
    setFilter,
    filter,
    USAGE_FILTERS,
    DAYS_LIST,
    currentFilter,
  } = useAdminSystemUsage();

  const { query: accountsQuery, accounts: accountsData } = useOrganizationAccounts();
  const accounts = accountsData?.edges || [];

  // Top 10 organizations by shipping spend
  const topOrganizations = accounts
    .sort((a, b) => (b.node.usage?.total_shipping_spend || 0) - (a.node.usage?.total_shipping_spend || 0))
    .slice(0, 10);

  // Shipping spend data for single-line chart
  const chartData = DAYS_LIST[currentFilter() || "15 days"].map((day) => ({
    name: day,
    spend: usage?.shipping_spend?.find(({ date }) => moment(date).format("MMM D") === day)?.count || 0,
  }));

  const totalSpend = usage?.total_shipping_spend || 0;
  const totalShipments = usage?.total_shipments || 0;
  const totalAddonsCharges = usage?.total_addons_charges || 0;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Shippers Overview</h1>
          <p className="text-sm text-gray-600 mt-1">
            Overview of shippers usage and spend.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <SelectField
            className="is-small"
            value={JSON.stringify(filter)}
            onChange={(e) => setFilter(JSON.parse(e.target.value))}
            style={{ minWidth: "140px" }}
          >
            {Object.entries(USAGE_FILTERS).map(([key, value]) => (
              <option key={key} value={JSON.stringify(value)}>
                {key}
              </option>
            ))}
          </SelectField>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg border shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Shipments</p>
              <p className="text-2xl font-bold text-gray-900">{totalShipments.toLocaleString()}</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-full">
              <Package className="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Addons Charges</p>
              <p className="text-2xl font-bold text-gray-900">${totalAddonsCharges.toLocaleString()}</p>
            </div>
            <div className="p-3 bg-green-100 rounded-full">
              <DollarSign className="h-6 w-6 text-green-600" />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Spend</p>
              <p className="text-2xl font-bold text-gray-900">${totalSpend.toLocaleString()}</p>
            </div>
            <div className="p-3 bg-purple-100 rounded-full">
              <DollarSign className="h-6 w-6 text-purple-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Main Chart - Full Width */}
      <div>
        {/* Legend */}
        <div className="flex items-center gap-4 mb-4">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-blue-500"></div>
            <span className="text-sm font-medium">${totalSpend.toLocaleString()} total spend</span>
          </div>
        </div>

        <div style={{ width: "100%", height: "300px" }}>
          {usage?.shipping_spend ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={chartData}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis
                  dataKey="name"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fontSize: 12, fill: '#64748b' }}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1e293b',
                    border: 'none',
                    borderRadius: '6px',
                    color: 'white',
                    fontSize: '12px'
                  }}
                  formatter={(value: any) => [`$${value.toLocaleString()}`, 'Spend']}
                />
                <Line
                  type="linear"
                  dataKey="spend"
                  stroke="#3b82f6"
                  strokeWidth={2}
                  dot={false}
                  name="spend"
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-full bg-gray-50 rounded">
              <div className="text-center">
                <Package className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                <p className="text-sm text-gray-500">No shipping data available</p>
              </div>
            </div>
          )}
        </div>
        <div className="text-right mt-2">
          <span className="text-xs text-gray-500">
            Updated today {new Date().toLocaleTimeString('en-US', {
              hour: 'numeric',
              minute: '2-digit',
              hour12: true
            })}
          </span>
        </div>
      </div>

      {/* Top Organizations Table */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-medium text-gray-900">Top organizations</h2>
          <AppLink href="/shippers/accounts" className="text-sm text-indigo-600 hover:text-indigo-500">
            All time data →
          </AppLink>
        </div>

        <div className="border-b">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Organization</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Members</TableHead>
                <TableHead className="text-right">Shipments</TableHead>
                <TableHead className="text-right">Addon Charges</TableHead>
                <TableHead className="text-right">API Requests</TableHead>
                <TableHead className="text-right">Shipping Spend</TableHead>
                <TableHead className="w-12"></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {topOrganizations.map(({ node: org }) => (
                <TableRow key={org.id}>
                  <TableCell>
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
                        <Building2 className="h-4 w-4 text-gray-600" />
                      </div>
                      <div>
                        <div className="font-medium text-gray-900">{org.name}</div>
                        <div className="text-sm text-gray-500">{org.slug}</div>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <StatusBadge status={org.is_active ? "active" : "inactive"} />
                  </TableCell>
                  <TableCell className="text-right text-sm text-gray-600">
                    {org.usage?.members || 0}
                  </TableCell>
                  <TableCell className="text-right text-sm text-gray-600">
                    {(org.usage?.total_shipments || 0).toLocaleString()}
                  </TableCell>
                  <TableCell className="text-right text-sm text-gray-600">
                    ${(org.usage?.total_addons_charges || 0).toLocaleString()}
                  </TableCell>
                  <TableCell className="text-right text-sm text-gray-600">
                    {(org.usage?.total_requests || 0).toLocaleString()}
                  </TableCell>
                  <TableCell className="text-right font-medium text-gray-900">
                    ${(org.usage?.total_shipping_spend || 0).toLocaleString()}
                  </TableCell>
                  <TableCell>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-8 w-8 p-0 hover:bg-muted"
                        >
                          <MoreHorizontal className="h-4 w-4" />
                          <span className="sr-only">Open menu</span>
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem asChild>
                          <AppLink href={`/shippers/accounts/${org.id}`}>
                            <Eye className="mr-2 h-4 w-4" />
                            View Details
                          </AppLink>
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          {topOrganizations.length === 0 && (
            <div className="text-center py-12">
              <Building2 className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-500 mb-2">
                No organizations yet
              </h3>
              <p className="text-sm text-gray-400">
                Organizations will appear here once they start shipping.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
