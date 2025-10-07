"use client";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@karrio/ui/components/ui/dropdown-menu";
import { useRateSheetMutation, useRateSheet, useRateSheets } from "@karrio/hooks/rate-sheet";
import { Plus, Search, MoreHorizontal, Edit3, Copy, Trash2 } from "lucide-react";
import { RateSheetEditor } from "@karrio/ui/components/rate-sheet-editor";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { useToast } from "@karrio/ui/hooks/use-toast";
import React, { useMemo, useState } from "react";
import { p } from '@karrio/lib';

export default function RateSheetsPage() {
  const Component = (): JSX.Element => {
    const { toast } = useToast();
    const [rateSheetEditorOpen, setRateSheetEditorOpen] = useState(false);
    const [selectedRateSheetId, setSelectedRateSheetId] = useState<string | null>(null);
    const [search, setSearch] = useState("");
    const { query: listQuery, rate_sheets } = useRateSheets();
    const { deleteRateSheet } = useRateSheetMutation();

    const openRateSheetEditor = (id: string = 'new') => {
      setSelectedRateSheetId(id);
      setRateSheetEditorOpen(true);
    };

    const filtered = useMemo(() => {
      const edges = rate_sheets?.edges || [];
      if (!search) return edges;
      const s = search.toLowerCase();
      return edges.filter(({ node }) =>
        node.name?.toLowerCase().includes(s) ||
        node.carrier_name?.toLowerCase().includes(s) ||
        node.id?.toLowerCase().includes(s)
      );
    }, [rate_sheets, search]);

    return (
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">Carrier Connections</h1>
            <p className="text-sm text-gray-600 mt-1">Manage your shipping carrier integrations and configurations</p>
          </div>
          <Button onClick={() => openRateSheetEditor('new')}>
            <Plus className="mr-2 h-4 w-4" />
            Add rate sheet
          </Button>
        </div>

        {/* Tabs mimic */}
        <div className="flex items-center border-b border-gray-200">
          <nav className="flex space-x-8 overflow-x-auto">
            <AppLink href={`/connections`} className="whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300">Your Accounts</AppLink>
            <AppLink href={`/connections/system`} className="whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300">System Accounts</AppLink>
            <span className="whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium border-purple-500 text-purple-600">Rate Sheets</span>
          </nav>
        </div>

        {/* Search */}
        <div className="p-4 bg-gray-50 rounded-lg">
          <div className="flex h-9 w-full items-center rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-within:ring-2 focus-within:ring-ring focus-within:ring-offset-2">
            <Search className="h-4 w-4 text-muted-foreground mr-2 flex-shrink-0" />
            <Input
              placeholder="Search rate sheets..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="flex-1 bg-transparent border-0 px-0 py-0 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-0 focus-visible:ring-0"
              autoComplete="off"
            />
          </div>
        </div>

        {/* List */}
        {filtered.length === 0 ? (
          <div className="text-center py-12">
            <div className="mx-auto mb-4 text-gray-400">
              <svg className="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-500 mb-2">
              No rate sheets found
            </h3>
            <p className="text-sm text-gray-400 mb-4">
              {search
                ? "No rate sheets match your search criteria."
                : "Get started by creating your first rate sheet to manage custom carrier pricing."
              }
            </p>
            {!search && (
              <Button onClick={() => openRateSheetEditor('new')}>
                <Plus className="mr-2 h-4 w-4" />
                Create Your First Rate Sheet
              </Button>
            )}
          </div>
        ) : (
          <div className="space-y-3">
            {filtered.map(({ node: sheet }) => (
              <div key={sheet.id} className="group relative flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 rounded-lg border border-gray-200 hover:border-gray-300 hover:shadow-sm transition-all duration-200 bg-white gap-3">
                <div className="flex items-start sm:items-center gap-3 flex-1 w-full sm:w-auto">
                  <div className="flex-shrink-0">
                    <CarrierImage carrier_name={sheet.carrier_name} width={48} height={48} className="rounded-lg" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex flex-col sm:flex-row sm:items-center gap-2 mb-2">
                      <h3 className="font-medium text-gray-900 text-base">{sheet.name}</h3>
                    </div>
                    <div className="flex flex-col sm:flex-row sm:items-center gap-2 text-sm">
                      <span className="text-gray-600 font-mono">{sheet.carrier_name}</span>
                      <span className="hidden sm:inline text-gray-400">•</span>
                      <div className="text-xs px-2 py-0.5 bg-gray-100 text-gray-700 rounded inline-block">
                        {(sheet.services?.length ?? 0)} services
                      </div>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="icon" className="h-9 w-9 hover:bg-muted">
                        <MoreHorizontal className="h-4 w-4" />
                        <span className="sr-only">Open menu</span>
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuLabel>Actions</DropdownMenuLabel>
                      <DropdownMenuItem onClick={() => openRateSheetEditor(sheet.id)}>
                        <Edit3 className="mr-2 h-4 w-4" />
                        Edit Rate Sheet
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => navigator.clipboard.writeText(sheet.id)}>
                        <Copy className="mr-2 h-4 w-4" />
                        Copy ID
                      </DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem className="text-red-600" onClick={() => deleteRateSheet.mutate({ id: sheet.id }, {
                        onSuccess: () => toast({ title: "Rate sheet deleted" }),
                        onError: (e: any) => toast({ title: "Failed to delete", description: e?.message || "", variant: "destructive" })
                      })}>
                        <Trash2 className="mr-2 h-4 w-4" />
                        Delete
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
                <div className="absolute left-0 top-0 bottom-0 w-1 rounded-l-lg bg-gray-300" />
              </div>
            ))}
          </div>
        )}

        {/* Editor */}
        {rateSheetEditorOpen && selectedRateSheetId && (
          <RateSheetEditor
            rateSheetId={selectedRateSheetId}
            onClose={() => { setRateSheetEditorOpen(false); setSelectedRateSheetId(null); listQuery.refetch(); }}
            // No connection context here; editor will default to 'generic' for new, and user selects carrier
            isAdmin={false}
            useRateSheet={useRateSheet}
            useRateSheetMutation={useRateSheetMutation}
          />
        )}
      </div>
    );
  };

  return (
    <Component />
  );
}
