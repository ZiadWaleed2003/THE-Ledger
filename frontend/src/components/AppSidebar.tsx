import { Package, Bot, Database } from "lucide-react";
import { NavLink } from "@/components/NavLink";
import { ThemeToggle } from "@/components/ThemeToggle";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
  SidebarFooter,
} from "@/components/ui/sidebar";

const navItems = [
  {
    title: "Asset Registry",
    url: "/",
    icon: Package,
  },
  {
    title: "AI Assistant",
    url: "/assistant",
    icon: Bot,
  },
];

export function AppSidebar() {
  return (
    <Sidebar className="border-r border-border">
      <SidebarHeader className="p-4 border-b border-border">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center h-10 w-10 rounded-lg bg-primary text-primary-foreground">
              <Database className="h-5 w-5" />
            </div>
            <div className="flex flex-col">
              <span className="font-semibold text-foreground">AI Asset</span>
              <span className="text-xs text-muted-foreground">Management</span>
            </div>
          </div>
          <ThemeToggle />
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {navItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <NavLink
                      to={item.url}
                      end
                      className="flex items-center gap-3 px-3 py-2 rounded-md transition-colors hover:bg-muted/50"
                      activeClassName="bg-muted text-foreground font-medium"
                    >
                      <item.icon className="h-4 w-4" />
                      <span>{item.title}</span>
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="p-4 border-t border-border">
        <p className="text-xs text-muted-foreground text-center">
          Connected to FastAPI Backend
        </p>
      </SidebarFooter>
    </Sidebar>
  );
}
