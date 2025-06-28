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
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@karrio/ui/components/ui/dialog";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@karrio/ui/components/ui/select";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useState } from "react";
import { trpc } from "@karrio/trpc/client";
import { format } from "date-fns";
import { MoreHorizontal } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@karrio/ui/components/ui/dropdown-menu";
import {
  GetUsers_users_edges_node as User,
} from "@karrio/types/graphql/admin/types";

export default function Page() {
  const { toast } = useToast();
  const [isInviteOpen, setIsInviteOpen] = useState(false);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [cursor, setCursor] = useState<string | undefined>(undefined);
  const utils = trpc.useContext();

  // Fetch users and permission groups
  const { data: usersData, isLoading: isLoadingUsers } =
    trpc.admin.users.list.useQuery({
      filter: {
        is_active: true,
        after: cursor,
      },
    });
  const { data: permissionGroupsData, isLoading: isLoadingPermissions } =
    trpc.admin.permission_groups.list.useQuery({});
  const users = usersData?.edges || [];
  const permissionGroups = permissionGroupsData?.edges || [];

  // Mutations
  const createUser = trpc.admin.users.create.useMutation({
    onSuccess: () => {
      toast({ title: "User created successfully" });
      setIsInviteOpen(false);
      utils.admin.users.list.invalidate();
    },
    onError: (error) => {
      toast({
        title: "Failed to create user",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const updateUser = trpc.admin.users.update.useMutation({
    onSuccess: () => {
      toast({ title: "User updated successfully" });
      setIsEditOpen(false);
      utils.admin.users.list.invalidate();
    },
    onError: (error) => {
      toast({
        title: "Failed to update user",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const removeUser = trpc.admin.users.remove.useMutation({
    onSuccess: () => {
      toast({ title: "User removed successfully" });
      utils.admin.users.list.invalidate();
    },
    onError: (error) => {
      toast({
        title: "Failed to remove user",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const inviteUser = trpc.admin.users.create.useMutation({
    onSuccess: () => {
      toast({ title: "User invited successfully" });
      setIsInviteOpen(false);
      utils.admin.users.list.invalidate();
    },
    onError: (error) => {
      toast({
        title: "Failed to invite user",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const handleInvite = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const role = formData.get("role") as "member" | "developer" | "admin";

    inviteUser.mutate({
      data: {
        email: formData.get("email") as string,
        full_name: formData.get("full_name") as string,
        is_staff: role === "admin",
        is_active: true,
        permissions: [],
      },
    });
  };

  const handleCreate = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const permissions = Array.from(formData.getAll("permissions")) as string[];

    createUser.mutate({
      data: {
        email: formData.get("email") as string,
        full_name: formData.get("full_name") as string,
        is_staff: formData.get("is_staff") === "on",
        is_active: true,
        permissions,
      },
    });
  };

  const handleUpdate = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const permissions = Array.from(
      formData.getAll("permission_groups"),
    ) as string[];

    if (!selectedUser) return;

    updateUser.mutate({
      data: {
        id: String(selectedUser.id),
        full_name: formData.get("full_name") as string,
        is_staff: formData.get("is_staff") === "on",
        is_active: formData.get("is_active") === "on",
        permissions,
      },
    });
  };

  const handleRemove = async (user: User) => {
    if (confirm("Are you sure you want to remove this user?")) {
      removeUser.mutate({
        data: {
          id: String(user.id),
        },
      });
    }
  };

  // Fix mutation status checks
  const isInviting = inviteUser.status === "loading";
  const isUpdating = updateUser.status === "loading";
  const isRemoving = removeUser.status === "loading";

  if (isLoadingUsers || isLoadingPermissions) {
    return (
      <div className="flex h-[calc(100vh-4rem)] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight">
          User Management
        </h1>
      </div>

      <Card>
        <CardContent className="p-6">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold">Users</h2>
            <Dialog open={isInviteOpen} onOpenChange={setIsInviteOpen}>
              <DialogTrigger asChild>
                <Button>Invite User</Button>
              </DialogTrigger>
              <DialogContent className="p-4 pb-8">
                <DialogHeader>
                  <DialogTitle>Invite New User</DialogTitle>
                  <DialogDescription>
                    Send an invitation to join your organization.
                  </DialogDescription>
                </DialogHeader>
                <form onSubmit={handleInvite} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input id="email" name="email" type="email" required />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="role">Role</Label>
                    <Select name="role" defaultValue="member">
                      <SelectTrigger>
                        <SelectValue placeholder="Select a role" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="member">Member</SelectItem>
                        <SelectItem value="developer">Developer</SelectItem>
                        <SelectItem value="admin">Admin</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <DialogFooter>
                    <Button type="submit" disabled={isInviting}>
                      {isInviting ? "Sending..." : "Send Invitation"}
                    </Button>
                  </DialogFooter>
                </form>
              </DialogContent>
            </Dialog>
          </div>

          {users.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <p className="text-sm text-muted-foreground">No users found</p>
              <p className="text-sm text-muted-foreground">Invite a user to get started</p>
            </div>
          ) : (
            <>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>MEMBER</TableHead>
                    <TableHead>EMAIL</TableHead>
                    <TableHead>ROLE</TableHead>
                    <TableHead>LAST LOGIN</TableHead>
                    <TableHead className="w-[50px]"></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {users.map(({ node: user }) => (
                    <TableRow key={user.id}>
                      <TableCell>{user.full_name}</TableCell>
                      <TableCell>{user.email}</TableCell>
                      <TableCell>
                        {user.is_staff ? "Admin" : user.is_active ? "Member" : "Inactive"}
                      </TableCell>
                      <TableCell>
                        {user.last_login ? format(new Date(user.last_login), "MMM d, yyyy") : "Never"}
                      </TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="h-8 w-8 p-0">
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem
                              onClick={() => {
                                setSelectedUser(user as unknown as User);
                                setIsEditOpen(true);
                              }}
                            >
                              Edit
                            </DropdownMenuItem>
                            <DropdownMenuItem
                              className="text-destructive"
                              onClick={() => handleRemove(user as unknown as User)}
                            >
                              Remove
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>

              {usersData?.page_info && (
                <div className="mt-4 flex items-center justify-between">
                  <p className="text-sm text-muted-foreground">
                    Showing {users.length} of {usersData.page_info.count} users
                  </p>
                  <div className="flex items-center space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setCursor(usersData.page_info.start_cursor || undefined)}
                      disabled={!usersData.page_info.has_previous_page}
                    >
                      Previous
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setCursor(usersData.page_info.end_cursor || undefined)}
                      disabled={!usersData.page_info.has_next_page}
                    >
                      Next
                    </Button>
                  </div>
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>

      <Dialog open={isEditOpen} onOpenChange={setIsEditOpen}>
        <DialogContent className="p-4 pb-8">
          <DialogHeader>
            <DialogTitle>Edit User</DialogTitle>
            <DialogDescription>
              Update user details and permissions.
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleUpdate} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="full_name">Full Name</Label>
              <Input
                id="full_name"
                name="full_name"
                defaultValue={selectedUser?.full_name}
                required
              />
            </div>
            <div className="flex items-center space-x-2">
              <Checkbox
                id="is_staff"
                name="is_staff"
                defaultChecked={selectedUser?.is_staff}
              />
              <Label htmlFor="is_staff">Admin Access</Label>
            </div>
            <div className="flex items-center space-x-2">
              <Checkbox
                id="is_active"
                name="is_active"
                defaultChecked={selectedUser?.is_active}
              />
              <Label htmlFor="is_active">Active</Label>
            </div>
            <div className="space-y-2">
              <Label>Permission Groups</Label>
              <div className="space-y-2">
                {permissionGroups.map(({ node: group }) => (
                  <div key={group.id} className="flex items-center space-x-2">
                    <Checkbox
                      id={`permission_${group.id}`}
                      name="permission_groups"
                      value={String(group.id)}
                      defaultChecked={selectedUser?.permissions?.includes(String(group.id))}
                    />
                    <Label htmlFor={`permission_${group.id}`}>
                      {group.name}
                    </Label>
                  </div>
                ))}
              </div>
            </div>
            <DialogFooter>
              <Button type="submit" disabled={isUpdating}>
                {isUpdating ? "Updating..." : "Update User"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
