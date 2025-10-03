"use client"

import { ChevronRight, type LucideIcon } from "lucide-react"

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@karrio/ui/components/ui/collapsible"
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "@karrio/ui/components/ui/sidebar"
import { AppLink } from "@karrio/ui/core/components/app-link"
import { useSidebar } from "@karrio/ui/components/ui/sidebar"

export function NavMain({
  items,
  label = undefined,
}: {
  items: {
    title: string
    url: string
    icon?: LucideIcon
    isActive?: boolean
    external?: boolean
    items?: {
      title: string
      url: string
      external?: boolean
    }[]
  }[]
  label?: string
}) {
  const { setOpenMobile } = useSidebar();

  const handleExternalClick = () => {
    // Close mobile sidebar when clicking external links
    setOpenMobile(false);
  };

  return (
    <SidebarGroup>
      {label && <SidebarGroupLabel>{label}</SidebarGroupLabel>}
      <SidebarMenu>
        {items.map((item) => (
          <Collapsible
            key={item.title}
            asChild
            defaultOpen={item.isActive}
            className="group/collapsible"
          >
            <SidebarMenuItem>
              {item.items ? (
                <>
                  <CollapsibleTrigger asChild>
                    <SidebarMenuButton tooltip={item.title}>
                      {item.icon && <item.icon />}
                      <span>{item.title}</span>
                      <ChevronRight className="ml-auto transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
                    </SidebarMenuButton>
                  </CollapsibleTrigger>
                  <CollapsibleContent>
                    <SidebarMenuSub>
                      {item.items?.map((subItem) => (
                        <SidebarMenuSubItem key={subItem.title}>
                          <SidebarMenuSubButton asChild>
                            {subItem.external ? (
                              <a
                                href={subItem.url}
                                target="_blank"
                                rel="noreferrer"
                                onClick={handleExternalClick}
                              >
                                <span>{subItem.title}</span>
                              </a>
                            ) : (
                              <AppLink href={subItem.url}>
                                <span>{subItem.title}</span>
                              </AppLink>
                            )}
                          </SidebarMenuSubButton>
                        </SidebarMenuSubItem>
                      ))}
                    </SidebarMenuSub>
                  </CollapsibleContent>
                </>
              ) : (
                <SidebarMenuButton asChild tooltip={item.title}>
                  {item.external ? (
                    <a
                      href={item.url}
                      target="_blank"
                      rel="noreferrer"
                      onClick={handleExternalClick}
                    >
                      {item.icon && <item.icon />}
                      <span>{item.title}</span>
                    </a>
                  ) : (
                    <AppLink href={item.url}>
                      {item.icon && <item.icon />}
                      <span>{item.title}</span>
                    </AppLink>
                  )}
                </SidebarMenuButton>
              )}
            </SidebarMenuItem>
          </Collapsible>
        ))}
      </SidebarMenu>
    </SidebarGroup>
  )
}
