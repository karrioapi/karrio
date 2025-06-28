"use client";

import React, { useState } from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { LineChart, Line, CartesianGrid, XAxis, Tooltip, ResponsiveContainer } from "recharts";
import { useDeveloperTools } from "@karrio/developers/context/developer-tools-context";
import { CopiableLink } from "@karrio/ui/core/components/copiable-link";
import { Eye, EyeOff, Copy, AlertCircle } from "lucide-react";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { Button } from "@karrio/ui/components/ui/button";
import { Badge } from "@karrio/ui/components/ui/badge";
import { useAPIToken } from "@karrio/hooks/api-token";
import { useAPIUsage } from "@karrio/hooks/usage";
import { formatDateTimeLong } from "@karrio/lib";
import { useLogs } from "@karrio/hooks/log";
import moment from "moment";

export function ActivityView() {
  const [showSecretKey, setShowSecretKey] = useState(false);
  const { setCurrentView } = useDeveloperTools();

  // Fetch API metadata, usage, token, and logs data
  const { references, metadata } = useAPIMetadata();
  const {
    query: { data: { usage } = {} },
    setFilter,
    filter,
    USAGE_FILTERS,
    DAYS_LIST,
    currentFilter,
  } = useAPIUsage();

  const { query: { data: { token } = {} } } = useAPIToken();

  // Fetch recent error logs
  const { query: { data: { logs } = {} } } = useLogs({
    status: "failed",
    first: 5 // Get only 5 recent errors
  });

  // Combine requests and errors data for unified chart
  const combinedChartData = DAYS_LIST[currentFilter() || "15 days"].map((_, i) => {
    const dayLabel = i === 0 || i === DAYS_LIST[currentFilter() || "15 days"].length - 1 ? _ : "";
    return {
      name: dayLabel,
      requests: usage?.api_requests?.find(({ date }) => moment(date).format("MMM D") === _)?.count || 0,
      errors: usage?.api_errors?.find(({ date }) => moment(date).format("MMM D") === _)?.count || 0,
    };
  });

  const totalRequests = usage?.total_requests || 0;
  const totalErrors = usage?.total_errors || 0;

  // Get real API token data
  const isTestMode = token?.key?.startsWith('test_') || token?.key?.includes('test');
  const publicKey = `pk_${isTestMode ? 'test' : 'live'}_...${token?.key?.slice(-4) || 'k4$0'}`;
  const secretKey = token?.key || "sk_test_...bH2E";

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const handleManageAPIKeys = () => {
    setCurrentView("api-keys");
  };

  const handleViewAllRequests = () => {
    setCurrentView("logs");
  };

  // Get recent error logs
  const recentErrors = logs?.edges?.slice(0, 3) || [];

  return (
    <div className="h-full overflow-auto">
      <div className="p-2 sm:p-4 space-y-4 sm:space-y-6">
        {/* Top Row: API Requests Chart + API Keys */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-6">
          {/* API Requests Chart - Full width on mobile, 2/3 on desktop */}
          <div className="lg:col-span-2">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-slate-900">API requests</h3>
              <Select
                value={JSON.stringify(filter)}
                onValueChange={(value) => setFilter(JSON.parse(value))}
              >
                <SelectTrigger className="w-20 sm:w-24 h-7 text-xs">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(USAGE_FILTERS).map(([key, value]) => (
                    <SelectItem key={key} value={JSON.stringify(value)}>
                      {key}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-center gap-2 sm:gap-4 mb-3">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-blue-500"></div>
                <span className="text-xs sm:text-sm font-semibold">{totalRequests} total</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-red-500"></div>
                <span className="text-xs sm:text-sm font-semibold text-red-600">{totalErrors} failed</span>
              </div>
            </div>

            <div style={{ width: "100%", height: "160px" }} className="sm:h-[200px]">
              {usage?.api_requests && (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={combinedChartData}
                    margin={{ top: 5, right: 5, left: 5, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                    <XAxis
                      dataKey="name"
                      axisLine={false}
                      tickLine={false}
                      tick={{ fontSize: 11, fill: '#64748b' }}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#1e293b',
                        border: 'none',
                        borderRadius: '6px',
                        color: 'white',
                        fontSize: '12px'
                      }}
                    />
                    <Line
                      type="monotone"
                      dataKey="requests"
                      stroke="#3b82f6"
                      strokeWidth={2}
                      dot={false}
                      name="Requests"
                    />
                    <Line
                      type="monotone"
                      dataKey="errors"
                      stroke="#ef4444"
                      strokeWidth={2}
                      dot={false}
                      name="Errors"
                    />
                  </LineChart>
                </ResponsiveContainer>
              )}
            </div>

            <div className="mt-3">
              <Button
                variant="link"
                size="sm"
                className="text-xs sm:text-sm text-blue-600 p-0 h-auto"
                onClick={handleViewAllRequests}
              >
                View all requests
              </Button>
              <span className="text-xs text-slate-500 ml-2 sm:ml-3">
                Updated today {new Date().toLocaleTimeString('en-US', {
                  hour: 'numeric',
                  minute: '2-digit',
                  hour12: true
                })}
              </span>
            </div>
          </div>

          {/* API Keys Section */}
          <div className="lg:col-span-1">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-slate-900">API keys</h3>
              <Button
                variant="link"
                size="sm"
                className="text-xs sm:text-sm text-blue-600 p-0 h-auto"
                onClick={handleManageAPIKeys}
              >
                Manage API keys
              </Button>
            </div>
            <div className="space-y-2">
              <div className="text-xs text-slate-600 mb-1">Standard keys</div>
              <div className="space-y-1">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-slate-600 text-xs sm:text-sm">Publishable key</span>
                  <div className="flex items-center gap-1 sm:gap-2">
                    <code className="text-xs bg-slate-50 px-1 sm:px-2 py-1 rounded truncate max-w-[100px] sm:max-w-none">{publicKey}</code>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => copyToClipboard(publicKey)}
                      className="h-5 w-5 sm:h-6 sm:w-6 p-0"
                    >
                      <Copy className="h-3 w-3" />
                    </Button>
                  </div>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-slate-600 text-xs sm:text-sm">Secret key</span>
                  <div className="flex items-center gap-1 sm:gap-2">
                    <code className="text-xs bg-slate-50 px-1 sm:px-2 py-1 rounded truncate max-w-[100px] sm:max-w-none">
                      {showSecretKey ? secretKey : `${secretKey.slice(0, 7)}...`}
                    </code>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setShowSecretKey(!showSecretKey)}
                      className="h-5 w-5 sm:h-6 sm:w-6 p-0"
                    >
                      {showSecretKey ? <EyeOff className="h-3 w-3" /> : <Eye className="h-3 w-3" />}
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => copyToClipboard(secretKey)}
                      className="h-5 w-5 sm:h-6 sm:w-6 p-0"
                    >
                      <Copy className="h-3 w-3" />
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Second Row: Recent Errors + API Details */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-6">
          {/* Recent Errors - Full width on mobile, 2/3 on desktop */}
          <div className="lg:col-span-2">
            <h3 className="text-sm font-semibold text-slate-900 mb-3">Recent errors</h3>
            {recentErrors.length > 0 ? (
              <div className="space-y-2">
                {recentErrors.map(({ node: log }) => (
                  <div key={log.id} className="flex items-center gap-2 sm:gap-3 p-2 bg-red-50 border border-red-100 rounded">
                    <AlertCircle className="h-4 w-4 text-red-500 flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <div className="text-xs sm:text-sm font-medium text-red-900 truncate">
                        {log.status_code} - {log.method} {log.path}
                      </div>
                      <div className="text-xs text-red-600">
                        {formatDateTimeLong(log.requested_at)}
                      </div>
                    </div>
                    <Badge variant="destructive" className="text-xs flex-shrink-0">
                      {log.status_code}
                    </Badge>
                  </div>
                ))}
                <Button
                  variant="link"
                  size="sm"
                  className="text-xs sm:text-sm text-blue-600 p-0 h-auto"
                  onClick={handleViewAllRequests}
                >
                  View all logs →
                </Button>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-6 sm:py-8 text-center">
                <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-green-50 flex items-center justify-center mb-3">
                  <div className="w-5 h-5 sm:w-6 sm:h-6 rounded-full bg-green-500 flex items-center justify-center">
                    <span className="text-white text-xs">✓</span>
                  </div>
                </div>
                <p className="text-xs sm:text-sm font-medium text-slate-900">Your integration is running smoothly</p>
                <p className="text-xs text-slate-600 mt-1">
                  Come back here to see recent errors and recommendations
                </p>
              </div>
            )}
          </div>

          {/* API Details */}
          <div className="lg:col-span-1">
            <h3 className="text-sm font-semibold text-slate-900 mb-3">API Details</h3>
            <div className="space-y-3">
              {/* API Version */}
              <div>
                <div className="text-xs text-slate-600 mb-1">API Version</div>
                <code className="text-xs sm:text-sm bg-slate-50 px-2 py-1 rounded">{references?.VERSION}</code>
              </div>

              {/* API Endpoints */}
              <div className="space-y-2">
                <div>
                  <div className="text-xs text-slate-600 mb-1">REST API</div>
                  <CopiableLink
                    className="text-xs font-mono bg-slate-50 px-2 py-1 rounded block text-slate-700 hover:bg-slate-100 truncate"
                    text={references?.HOST}
                    title={references?.HOST}
                  />
                </div>
                <div>
                  <div className="text-xs text-slate-600 mb-1">GraphQL API</div>
                  <CopiableLink
                    className="text-xs font-mono bg-slate-50 px-2 py-1 rounded block text-slate-700 hover:bg-slate-100 truncate"
                    text={references?.GRAPHQL}
                    title={references?.GRAPHQL}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
