"use client";

import { GitHubIcon, Spinner } from "@karrio/insiders/components/icons";
import { Button } from "@karrio/insiders/components/ui/button";
import { Input } from "@karrio/insiders/components/ui/input";
import { Label } from "@karrio/insiders/components/ui/label";
import { useToast } from "@karrio/insiders/hooks/use-toast";
import { cn } from "@karrio/insiders/lib/utils";
import { signIn } from "next-auth/react";
import { useState } from "react";
import Image from "next/image";
import * as React from "react";
import Link from "next/link";

interface UserAuthFormProps extends React.HTMLAttributes<HTMLDivElement> {}

export function SignUpClient({ className, ...props }: UserAuthFormProps) {
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleEmailSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const result = await signIn("email", {
        email,
        redirect: false,
        callbackUrl: "/orgs/create",
      });

      if (result?.error) {
        toast({
          title: "Error",
          description: "Failed to send signup link",
          variant: "destructive",
        });
      } else {
        toast({
          title: "Check your email",
          description: "A sign up link has been sent to your email address",
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Something went wrong",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container relative hidden h-[100vh] flex-col items-center justify-center md:grid lg:max-w-none lg:grid-cols-2 lg:px-0">
      <div className="lg:p-8">
        <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
          <div className="flex flex-col space-y-2">
            <h1 className="text-2xl font-semibold tracking-tight">
              Get Started
            </h1>
            <p className="text-sm text-muted-foreground">
              Create a new account
            </p>
          </div>
          <div className={cn("grid gap-6", className)} {...props}>
            <Button
              variant="outline"
              type="button"
              onClick={() => signIn("github", { callbackUrl: "/orgs/create" })}
              disabled={isLoading}
            >
              {isLoading ? (
                <Spinner className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <GitHubIcon className="mr-2 h-4 w-4" />
              )}{" "}
              GitHub
            </Button>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-background px-2 text-muted-foreground">
                  Or continue with
                </span>
              </div>
            </div>

            <form onSubmit={handleEmailSignUp}>
              <div className="grid gap-2">
                <div className="grid gap-1">
                  <Label className="sr-only" htmlFor="email">
                    Email
                  </Label>
                  <Input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="name@example.com"
                    className="border-border bg-transparent text-foreground"
                    disabled={isLoading}
                    required
                  />
                </div>

                <Button
                  type="submit"
                  className="w-full bg-primary py-6 hover:bg-primary/90"
                  disabled={isLoading}
                >
                  {isLoading && <Spinner className="mr-2 h-4 w-4" />}
                  Sign up with Email
                </Button>
              </div>
            </form>

            <p className="text-center text-sm text-muted-foreground">
              Already have an account?{" "}
              <Link
                href="/signin"
                className="font-semibold text-primary hover:underline"
              >
                Sign In Now
              </Link>
            </p>
          </div>
          <p className="px-8 text-center text-xs text-muted-foreground mt-8">
            By clicking continue, you agree to our{" "}
            <Link
              href="/terms"
              className="underline underline-offset-4 hover:text-primary"
            >
              Terms of Service
            </Link>{" "}
            and{" "}
            <Link
              href="/privacy"
              className="underline underline-offset-4 hover:text-primary"
            >
              Privacy Policy
            </Link>
            .
          </p>
        </div>
      </div>
      <div className="relative hidden h-full flex-col bg-muted p-10 text-white dark:border-r lg:flex">
        <div className="absolute inset-0 bg-zinc-900" />
        <div className="relative z-20 flex items-center text-lg font-medium">
          <Image src="/logo.svg" alt="Karrio" width={100} height={100} />
        </div>
        <div className="relative z-20 mt-auto">
          <blockquote className="space-y-2">
            <p className="text-lg">
              &ldquo;Karrio is a game changer for our business. It has
              streamlined our shipping processes and reduced our costs
              significantly.&rdquo;
            </p>
            <footer className="text-sm">John Doe</footer>
          </blockquote>
        </div>
      </div>
    </div>
  );
}
