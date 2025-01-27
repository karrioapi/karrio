"use client";

import { Button } from "@karrio/insiders/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@karrio/insiders/components/ui/card";
import { Input } from "@karrio/insiders/components/ui/input";
import { Label } from "@karrio/insiders/components/ui/label";

export default function ProfilePage() {
  return (
    <div className="container mx-auto py-10">
      <h1 className="text-3xl font-bold mb-6">Profile</h1>
      <Card>
        <CardHeader>
          <CardTitle>Personal Information</CardTitle>
          <CardDescription>Update your personal details here.</CardDescription>
        </CardHeader>
        <CardContent>
          <form>
            <div className="grid w-full items-center gap-4">
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="name">Name</Label>
                <Input id="name" placeholder="Your name" />
              </div>
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="email">Email</Label>
                <Input id="email" placeholder="Your email" type="email" />
              </div>
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="company">Company</Label>
                <Input id="company" placeholder="Your company name" />
              </div>
              <Button>Save Changes</Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
