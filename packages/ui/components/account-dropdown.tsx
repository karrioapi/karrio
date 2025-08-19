"use client";

import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@karrio/ui/components/ui/dropdown-menu";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { AppLink } from '@karrio/ui/core/components/app-link';
import { Button } from "@karrio/ui/components/ui/button";
import { useUser } from "@karrio/hooks/user";
import { signOut } from "next-auth/react";
import { Settings, ExternalLink, LogOut, User, Wrench } from "lucide-react";

export function AccountDropdown() {
  const { references } = useAPIMetadata();
  const {
    query: { data: { user } = {} },
  } = useUser();

  return (
    <DropdownMenu modal={false}>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size="icon" className="rounded-full">
          <Settings className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        {user?.full_name && (
          <>
            <DropdownMenuLabel className="font-normal">
              <div className="flex flex-col space-y-1">
                <p className="text-sm font-medium leading-none">{user.full_name}</p>
                <p className="text-xs leading-none text-muted-foreground">{user.email}</p>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
          </>
        )}
        <DropdownMenuItem asChild>
          <AppLink href="/settings/account" className="flex items-center">
            <User className="h-4 w-4 mr-2" />
            My Account
          </AppLink>
        </DropdownMenuItem>
        {user?.is_staff && (
          <DropdownMenuItem asChild>
            <a
              href={references.ADMIN}
              target="_blank"
              rel="noreferrer"
              className="flex items-center"
            >
              <Wrench className="h-4 w-4 mr-2" />
              Admin Console
              <ExternalLink className="h-3 w-3 ml-auto" />
            </a>
          </DropdownMenuItem>
        )}
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={() => signOut()} className="flex items-center">
          <LogOut className="h-4 w-4 mr-2" />
          Logout
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
