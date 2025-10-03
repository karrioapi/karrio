import { requireRole, isAuthed } from "@karrio/console/trpc/middleware";
import { InviteEmail } from "@karrio/console/emails/invite-member";
import {
  GET_TENANT,
  GET_TENANTS,
  CREATE_TENANT,
  DELETE_TENANT,
  UPDATE_TENANT,
  GET_USAGE_STATS,
  ADD_CUSTOM_DOMAIN,
  DELETE_CUSTOM_DOMAIN,
  GET_CONNECTED_ACCOUNT,
  GET_CONNECTED_ACCOUNTS,
  RESET_TENANT_ADMIN_PASSWORD,
  type GetTenant,
  type CreateTenant,
  type UpdateTenant,
  type GetUsageStats,
  type AddCustomDomain,
  type DeleteCustomDomain,
  type GetConnectedAccount,
  type GetConnectedAccounts,
  type ResetTenantAdminPassword,
} from "@karrio/console/types/graphql/platform";
import {
  PRODUCT_FEATURES,
  SubscriptionWithPayment,
} from "@karrio/console/shared/utils";
import {
  TENANT_DASHBOARD_DOMAIN,
  TENANT_API_DOMAIN,
} from "@karrio/console/shared/constants";
import { procedure, router } from "@karrio/console/trpc/_app";
import { prisma } from "@karrio/console/prisma/client";
import { stripe } from "@karrio/console/shared/stripe";
import { resend } from "@karrio/console/shared/resend";
import { karrio } from "@karrio/console/shared/karrio";
import { TRPCError } from "@trpc/server";
import type { Session } from "next-auth";
import { gqlstr } from "@karrio/lib";
import Stripe from "stripe";
import crypto from "crypto";
import { z } from "zod";

// Create a protected procedure that ensures session type
const protectedProcedure = procedure.use(isAuthed);

const PRICE_IDS = ["price_1QTgRLKRv3SLOrAO7HDpnOKd"] as const;

export const appRouter = router({
  users: router({
    get: protectedProcedure.query(async ({ ctx }) => {
      const session = ctx.session as Session;
      return prisma.user.findUnique({
        where: { id: session.user.id },
      });
    }),

    update: protectedProcedure
      .input(
        z.object({
          name: z.string().optional(),
          email: z.string().email().optional(),
        }),
      )
      .mutation(async ({ input, ctx }) => {
        const session = ctx.session as Session;
        return prisma.user.update({
          where: { id: session.user.id },
          data: input,
        });
      }),
  }),

  organizations: router({
    get: protectedProcedure
      .input(z.object({ orgId: z.string() }))
      .query(async ({ input }) => {
        return prisma.organization.findUnique({ where: { id: input.orgId } });
      }),

    getAll: protectedProcedure.query(async ({ ctx }) => {
      const session = ctx.session as Session;
      return prisma.organization.findMany({
        where: {
          members: {
            some: { userId: session.user.id },
          },
        },
        include: { members: true },
      });
    }),

    create: protectedProcedure
      .input(z.object({ name: z.string() }))
      .mutation(async ({ input, ctx }) => {
        const session = ctx.session as Session;
        const userId = session.user.id;
        const userEmail = session.user.email;

        // Create a Stripe customer
        const customer = await stripe.customers.create({
          email: userEmail,
          metadata: { organizationName: input.name },
        });

        return prisma.organization.create({
          data: {
            name: input.name,
            stripeCustomerId: customer.id,
            members: {
              create: {
                userId,
                role: "OWNER",
              },
            },
          },
        });
      }),

    update: protectedProcedure
      .input(
        z.object({
          orgId: z.string(),
          name: z.string(),
        }),
      )
      .use(requireRole(["OWNER", "ADMIN"]))
      .mutation(({ input }) => {
        return prisma.organization.update({
          where: { id: input.orgId },
          data: { name: input.name },
        });
      }),

    getMembers: protectedProcedure
      .input(z.object({ orgId: z.string() }))
      .query(async ({ input }) => {
        return prisma.organizationMembership.findMany({
          where: { orgId: input.orgId },
          include: { user: true },
        });
      }),

    inviteMember: protectedProcedure
      .input(
        z.object({
          orgId: z.string(),
          email: z.string().email(),
        }),
      )
      .use(requireRole(["OWNER"]))
      .mutation(async ({ input, ctx }) => {
        const session = ctx.session as Session;
        const organization = await prisma.organization.findUnique({
          where: { id: input.orgId },
          include: { subscription: true },
        });

        if (!organization) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "Organization not found",
          });
        }

        // Check if user is already a member
        const existingMember = await prisma.organizationMembership.findUnique({
          where: {
            orgId_userId: {
              orgId: input.orgId,
              userId: session.user.id,
            },
          },
        });

        if (existingMember) {
          throw new TRPCError({
            code: "CONFLICT",
            message: "User is already a member",
          });
        }

        // Create invitation token
        const token = crypto.randomBytes(32).toString("hex");
        const expires = new Date();
        expires.setHours(expires.getHours() + 24); // 24 hour expiry

        // Create invitation
        const invitation = await prisma.organizationInvitation.create({
          data: {
            email: input.email,
            token,
            expires,
            orgId: input.orgId,
            inviterId: session.user.id,
          },
        });

        // Generate invite URL
        const inviteUrl = `${process.env.NEXTAUTH_URL}/invite/${token}`;

        // Send invitation email
        await resend.emails.send({
          from: "Karrio <no-reply@karrio.io>",
          to: input.email,
          subject: `Join ${organization.name} on Karrio`,
          react: InviteEmail({
            inviteUrl,
            organizationName: organization.name,
            inviterName: session.user.name || "A team member",
          }),
        });

        return invitation;
      }),

    acceptInvitation: protectedProcedure
      .input(z.object({ token: z.string() }))
      .mutation(async ({ input, ctx }) => {
        const session = ctx.session as Session;

        const invitation = await prisma.organizationInvitation.findUnique({
          where: { token: input.token },
          include: { organization: true },
        });

        if (!invitation || invitation.expires < new Date()) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "Invalid or expired invitation",
          });
        }

        if (invitation.email !== session.user.email) {
          throw new TRPCError({
            code: "FORBIDDEN",
            message: "Invitation is for a different email address",
          });
        }

        // Create membership and delete invitation
        await prisma.$transaction([
          prisma.organizationMembership.create({
            data: {
              orgId: invitation.orgId,
              userId: session.user.id,
              role: "MEMBER",
            },
          }),
          prisma.organizationInvitation.delete({
            where: { id: invitation.id },
          }),
        ]);

        return invitation.organization;
      }),

    removeMember: protectedProcedure
      .input(
        z.object({
          orgId: z.string(),
          userId: z.string(),
        }),
      )
      .use(requireRole(["OWNER", "ADMIN"]))
      .mutation(async ({ input }) => {
        return prisma.organizationMembership.delete({
          where: {
            orgId_userId: {
              orgId: input.orgId,
              userId: input.userId,
            },
          },
        });
      }),
  }),

  projects: router({
    create: protectedProcedure
      .input(z.object({ name: z.string(), orgId: z.string() }))
      .use(requireRole(["OWNER", "ADMIN"]))
      .mutation(async ({ input, ctx }) => {
        const session = ctx.session as Session;
        const org = await prisma.organization.findUnique({
          where: { id: input.orgId },
          include: {
            subscription: true,
            projects: true,
          },
        });

        if (!org?.subscription || org.subscription.status !== "active") {
          throw new TRPCError({
            code: "FORBIDDEN",
            message: "Active subscription required to create projects",
          });
        }

        // Get the subscription plan details
        const price = await stripe.prices.retrieve(
          org.subscription.stripePriceId!,
          { expand: ["product"] },
        );
        const product = price.product as Stripe.Product;
        const projectLimit = parseInt(product.metadata.max_projects || "0");

        if (org.projects.length >= projectLimit) {
          throw new TRPCError({
            code: "FORBIDDEN",
            message: `Project limit (${projectLimit}) reached for your plan`,
          });
        }

        // Create project first with PENDING status
        const project = await prisma.project.create({
          data: {
            name: input.name,
            orgId: input.orgId,
            status: "PENDING",
            statusMessage: "Project created, initializing tenant deployment",
            metadata: {
              deployment_started_at: new Date().toISOString(),
            },
          },
        });

        // Helper function to create tenant - extracted for reuse
        const createTenantForProject = async (project: any, isRetry: boolean = false, projectName?: string) => {
          const logPrefix = isRetry ? "RETRY" : "INITIAL";

          try {
            // If this is a retry, first check if tenant already exists with this schema_name
            if (isRetry) {
              const existingTenantResponse = await karrio<{ tenants: { edges: Array<{ node: { id: string; schema_name: string } }> } }>(
                gqlstr(GET_TENANTS),
                { filter: { schema_name: project.id, first: 1 } },
                "Failed to check existing tenants",
                {
                  operation: "CHECK_EXISTING_TENANT",
                  userId: session.user.id,
                  orgId: project.orgId,
                },
              );

              const existingTenant = existingTenantResponse?.tenants?.edges?.[0]?.node;
              if (existingTenant) {
                console.log(`[TRPC] ${logPrefix}_CREATE_TENANT: Existing tenant found`, {
                  projectId: project.id,
                  existingTenantId: existingTenant.id,
                  timestamp: new Date().toISOString(),
                });

                // Update project with existing tenant info
                await prisma.project.update({
                  where: { id: project.id },
                  data: {
                    tenantId: existingTenant.id,
                    status: "ACTIVE",
                    statusMessage: "Linked to existing tenant successfully",
                    metadata: {
                      ...(project.metadata as Record<string, any>),
                      tenant_linked_at: new Date().toISOString(),
                      linked_tenant_id: existingTenant.id,
                      deployment_completed_at: new Date().toISOString(),
                    },
                  },
                });
                return;
              }
            }

            // Attempt to create new tenant
            const response = await karrio<CreateTenant>(
              gqlstr(CREATE_TENANT),
              {
                input: {
                  name: projectName || input.name,
                  schema_name: project.id,
                  admin_email: session.user.email,
                  domain: `${project.id}.${TENANT_API_DOMAIN!.split(":")[0]}`,
                  app_domains: [`${project.id}.${TENANT_DASHBOARD_DOMAIN}`],
                },
              },
              "Failed to create tenant",
              {
                operation: "CREATE_TENANT",
                userId: session.user.id,
                orgId: project.orgId,
              },
            );

            console.log(`[TRPC] ${logPrefix}_CREATE_TENANT Success for project ${project.id}`, {
              projectId: project.id,
              tenantId: response?.create_tenant?.tenant?.id,
              errors: response?.create_tenant?.errors,
            });

            if (response?.create_tenant?.tenant) {
              await prisma.project.update({
                where: { id: project.id },
                data: {
                  tenantId: response.create_tenant.tenant.id,
                  status: "ACTIVE",
                  statusMessage: "Tenant deployed successfully",
                  metadata: {
                    ...(project.metadata as Record<string, any>),
                    deployment_completed_at: new Date().toISOString(),
                    tenant_created_at: new Date().toISOString(),
                    tenant_response: {
                      id: response.create_tenant.tenant.id,
                      schema_name: response.create_tenant.tenant.schema_name,
                    },
                  },
                },
              });
            } else if (response?.create_tenant?.errors && response.create_tenant.errors.length > 0) {
              const errorDetails = response.create_tenant.errors.map(error =>
                `${error.field}: ${error.messages.join(", ")}`
              ).join("; ");
              throw new Error(`GraphQL validation errors: ${errorDetails}`);
            } else {
              throw new Error("Tenant creation response is invalid - no tenant or errors returned");
            }
          } catch (error: any) {
            console.error(`[TRPC] ${logPrefix}_CREATE_TENANT Failed for project ${project.id}`, {
              projectId: project.id,
              errorMessage: error.message,
              errorCause: error.cause,
              errorData: error.data,
              timestamp: new Date().toISOString(),
            });

            await prisma.project.update({
              where: { id: project.id },
              data: {
                status: "FAILED",
                statusMessage: `Tenant deployment failed: ${error.message}`,
                metadata: {
                  ...(project.metadata as Record<string, any>),
                  deployment_failed_at: new Date().toISOString(),
                  error_details: {
                    message: error.message,
                    cause: error.cause,
                    data: error.data,
                    stack: error.stack,
                  },
                },
              },
            });
          }
        };

        // Dispatch tenant creation asynchronously
        createTenantForProject(project, false);

        return project;
      }),

    get: protectedProcedure
      .input(z.object({ id: z.string(), orgId: z.string() }))
      .query(async ({ input }) => {
        const project = await prisma.project.findFirst({
          where: {
            id: input.id,
            orgId: input.orgId,
          },
        });

        if (!project) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "Project not found",
          });
        }

        return project;
      }),

    update: protectedProcedure
      .input(
        z.object({
          id: z.string(),
          name: z.string(),
          orgId: z.string(),
        }),
      )
      .use(requireRole(["OWNER", "ADMIN"]))
      .mutation(async ({ input }) => {
        return prisma.project.update({
          where: { id: input.id },
          data: { name: input.name },
        });
      }),

    getAll: protectedProcedure
      .input(z.object({ orgId: z.string() }))
      .query(async ({ input }) => {
        const org = await prisma.organization.findUnique({
          where: { id: input.orgId },
          include: {
            subscription: true,
            projects: true,
          },
        });

        let projectLimit = 0;
        if (org?.subscription?.stripePriceId) {
          const price = await stripe.prices.retrieve(
            org.subscription.stripePriceId,
            { expand: ["product"] },
          );
          const product = price.product as Stripe.Product;
          projectLimit = parseInt(product.metadata.max_projects || "0");
        }

        const hasActiveSubscription = org?.subscription?.status === "active";

        return {
          projects: org?.projects || [],
          limit: projectLimit,
          count: org?.projects.length || 0,
          canCreate:
            hasActiveSubscription && (org?.projects.length || 0) < projectLimit,
          subscriptionRequired: !hasActiveSubscription,
        };
      }),

    delete: protectedProcedure
      .input(z.object({ id: z.string(), orgId: z.string() }))
      .use(requireRole(["OWNER", "ADMIN"]))
      .mutation(async ({ input }) => {
        const project = await prisma.project.findUnique({
          where: { id: input.id },
        });

        if (project?.tenantId) {
          // Delete Karrio tenant
          await karrio(
            gqlstr(DELETE_TENANT),
            { input: { id: project.tenantId } },
            "Failed to delete tenant",
          );
        }

        return prisma.project.delete({
          where: { id: input.id },
        });
      }),

    tenant: router({
      get: protectedProcedure
        .input(z.object({ projectId: z.string() }))
        .query(async ({ input }) => {
          const project = await prisma.project.findUnique({
            where: { id: input.projectId },
          });
          if (!project?.tenantId) {
            throw new TRPCError({
              code: "NOT_FOUND",
              message: "Project not found",
            });
          }

          const response = await karrio<GetTenant>(
            gqlstr(GET_TENANT),
            { id: project.tenantId },
            "Failed to fetch tenant details",
          );

          if (!response?.tenant) {
            throw new TRPCError({
              code: "NOT_FOUND",
              message: "Tenant not found",
            });
          }

          return response.tenant;
        }),

      updateDashboardDomains: protectedProcedure
        .input(
          z.object({
            projectId: z.string(),
            domains: z.array(z.string()),
          }),
        )
        .mutation(async ({ input }) => {
          const project = await prisma.project.findUnique({
            where: { id: input.projectId },
          });
          if (!project?.tenantId) {
            throw new TRPCError({
              code: "NOT_FOUND",
              message: "Project not found",
            });
          }

          const response = await karrio<UpdateTenant>(
            gqlstr(UPDATE_TENANT),
            {
              input: {
                id: project.tenantId,
                app_domains: input.domains,
              },
            },
            "Failed to update domains",
          );

          if (!response?.update_tenant?.tenant) {
            throw new TRPCError({
              code: "INTERNAL_SERVER_ERROR",
              message: "Failed to update tenant",
            });
          }

          return response.update_tenant.tenant;
        }),

      addApiDomain: protectedProcedure
        .input(
          z.object({
            projectId: z.string(),
            domain: z.string(),
          }),
        )
        .mutation(async ({ input }) => {
          const project = await prisma.project.findUnique({
            where: { id: input.projectId },
          });
          if (!project?.tenantId) {
            throw new TRPCError({
              code: "NOT_FOUND",
              message: "Project not found",
            });
          }

          const response = await karrio<AddCustomDomain>(
            gqlstr(ADD_CUSTOM_DOMAIN),
            {
              input: {
                id: project.tenantId,
                domain: input.domain,
              },
            },
            "Failed to add custom domain",
          );

          return response.add_custom_domain.domain;
        }),

      removeApiDomain: protectedProcedure
        .input(
          z.object({
            projectId: z.string(),
            domain: z.string(),
          }),
        )
        .mutation(async ({ input }) => {
          const project = await prisma.project.findUnique({
            where: { id: input.projectId },
          });
          if (!project?.tenantId) {
            throw new TRPCError({
              code: "NOT_FOUND",
              message: "Project not found",
            });
          }

          await karrio<DeleteCustomDomain>(
            gqlstr(DELETE_CUSTOM_DOMAIN),
            {
              input: {
                id: project.tenantId,
                domain: input.domain,
              },
            },
            "Failed to remove custom domain",
          );

          return input.domain;
        }),

      getUsageStats: protectedProcedure
        .input(
          z.object({
            projectId: z.string(),
            filter: z
              .object({
                date_after: z.string().optional(),
                date_before: z.string().optional(),
              })
              .optional(),
          }),
        )
        .query(async ({ input }) => {
          const project = await prisma.project.findUnique({
            where: { id: input.projectId },
          });
          if (!project?.tenantId) {
            throw new TRPCError({
              code: "NOT_FOUND",
              message: "Project not found",
            });
          }

          const response = await karrio<GetUsageStats>(
            gqlstr(GET_USAGE_STATS),
            {
              tenant_id: project.tenantId,
              filter: input.filter,
            },
            "Failed to fetch usage statistics",
          );

          return response.usage_stats;
        }),

      getConnectedAccount: protectedProcedure
        .input(
          z.object({
            projectId: z.string(),
            accountId: z.string().optional(),
          }),
        )
        .query(async ({ input }) => {
          const project = await prisma.project.findUnique({
            where: { id: input.projectId },
          });
          if (!project?.tenantId) {
            throw new TRPCError({
              code: "NOT_FOUND",
              message: "Project not found",
            });
          }

          const response = await karrio<GetConnectedAccount>(
            gqlstr(GET_CONNECTED_ACCOUNT),
            {
              tenant_id: project.tenantId,
              id: input.accountId,
            },
            "Failed to fetch connected account",
          );

          return response.connected_account;
        }),

      getConnectedAccounts: protectedProcedure
        .input(
          z.object({
            projectId: z.string(),
            filter: z
              .object({
                search: z.string().optional(),
                cursor: z.string().optional(),
                limit: z.number().optional(),
              })
              .optional(),
          }),
        )
        .query(async ({ input }) => {
          const project = await prisma.project.findUnique({
            where: { id: input.projectId },
          });
          if (!project?.tenantId) {
            throw new TRPCError({
              code: "NOT_FOUND",
              message: "Project not found",
            });
          }

          const response = await karrio<GetConnectedAccounts>(
            gqlstr(GET_CONNECTED_ACCOUNTS),
            {
              tenant_id: project.tenantId,
              filter: input.filter,
            },
            "Failed to fetch connected accounts",
          );

          return response.connected_accounts;
        }),

      resetAdminPassword: protectedProcedure
        .input(
          z.object({
            projectId: z.string(),
          }),
        )
        .mutation(async ({ input, ctx }) => {
          const session = ctx.session as Session;
          const project = await prisma.project.findUnique({
            where: { id: input.projectId },
          });
          if (!project?.tenantId) {
            throw new TRPCError({
              code: "NOT_FOUND",
              message: "Project not found",
            });
          }

          // Check if password was given before by looking at metadata
          const metadata = project.metadata as Record<string, any> || {};
          const passwordGivenBefore = metadata.admin_password_given_at !== undefined;

          const response = await karrio<ResetTenantAdminPassword>(
            gqlstr(RESET_TENANT_ADMIN_PASSWORD),
            {
              input: {
                id: project.tenantId,
                email: session.user.email,
              },
            },
            "Failed to reset admin password",
          );

          if (!response.reset_tenant_admin_password.success) {
            throw new TRPCError({
              code: "INTERNAL_SERVER_ERROR",
              message: "Failed to reset admin password",
            });
          }

          // Update project metadata to track password delivery
          await prisma.project.update({
            where: { id: input.projectId },
            data: {
              metadata: {
                ...metadata,
                admin_password_given_at: new Date().toISOString(),
                admin_password_reset_count: (metadata.admin_password_reset_count || 0) + 1,
              },
            },
          });

          return {
            success: true,
            password: response.reset_tenant_admin_password.password,
            isFirstTime: !passwordGivenBefore,
          };
        }),
    }),

    // Add a new procedure to check tenant health
    checkTenantHealth: protectedProcedure
      .input(z.object({ projectId: z.string() }))
      .mutation(async ({ input }) => {
        return prisma.project.update({
          where: { id: input.projectId },
          data: {
            status: "PENDING",
            statusMessage: "Checking tenant health...",
          },
        });
      }),

    retryDeployment: protectedProcedure
      .input(z.object({ projectId: z.string() }))
      .mutation(async ({ input, ctx }) => {
        const session = ctx.session as Session;
        const project = await prisma.project.findUnique({
          where: { id: input.projectId },
        });

        if (!project) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "Project not found",
          });
        }

        // Update project status to pending
        await prisma.project.update({
          where: { id: input.projectId },
          data: {
            status: "PENDING",
            statusMessage: "Retrying deployment...",
            metadata: {
              ...(project.metadata as Record<string, any>),
              deployment_retry_at: new Date().toISOString(),
            },
          },
        });

        // Helper function to create tenant - same as in create mutation
        const createTenantForProject = async (project: any, isRetry: boolean = false, projectName?: string) => {
          const logPrefix = isRetry ? "RETRY" : "INITIAL";

          try {
            // If this is a retry, first check if tenant already exists with this schema_name
            if (isRetry) {
              const existingTenantResponse = await karrio<{ tenants: { edges: Array<{ node: { id: string; schema_name: string } }> } }>(
                gqlstr(GET_TENANTS),
                { filter: { schema_name: project.id, first: 1 } },
                "Failed to check existing tenants",
                {
                  operation: "CHECK_EXISTING_TENANT",
                  userId: session.user.id,
                  orgId: project.orgId,
                },
              );

              const existingTenant = existingTenantResponse?.tenants?.edges?.[0]?.node;
              if (existingTenant) {
                console.log(`[TRPC] ${logPrefix}_CREATE_TENANT: Existing tenant found`, {
                  projectId: project.id,
                  existingTenantId: existingTenant.id,
                  timestamp: new Date().toISOString(),
                });

                // Update project with existing tenant info
                await prisma.project.update({
                  where: { id: project.id },
                  data: {
                    tenantId: existingTenant.id,
                    status: "ACTIVE",
                    statusMessage: "Linked to existing tenant successfully",
                    metadata: {
                      ...(project.metadata as Record<string, any>),
                      tenant_linked_at: new Date().toISOString(),
                      linked_tenant_id: existingTenant.id,
                      deployment_completed_at: new Date().toISOString(),
                    },
                  },
                });
                return;
              }
            }

            // Attempt to create new tenant
            const response = await karrio<CreateTenant>(
              gqlstr(CREATE_TENANT),
              {
                input: {
                  name: projectName || project.name,
                  schema_name: project.id,
                  admin_email: session.user.email,
                  domain: `${project.id}.${TENANT_API_DOMAIN!.split(":")[0]}`,
                  app_domains: [`${project.id}.${TENANT_DASHBOARD_DOMAIN}`],
                },
              },
              "Failed to create tenant",
              {
                operation: "CREATE_TENANT",
                userId: session.user.id,
                orgId: project.orgId,
              },
            );

            console.log(`[TRPC] ${logPrefix}_CREATE_TENANT Success for project ${project.id}`, {
              projectId: project.id,
              tenantId: response?.create_tenant?.tenant?.id,
              errors: response?.create_tenant?.errors,
            });

            if (response?.create_tenant?.tenant) {
              await prisma.project.update({
                where: { id: project.id },
                data: {
                  tenantId: response.create_tenant.tenant.id,
                  status: "ACTIVE",
                  statusMessage: "Tenant deployed successfully",
                  metadata: {
                    ...(project.metadata as Record<string, any>),
                    deployment_completed_at: new Date().toISOString(),
                    tenant_created_at: new Date().toISOString(),
                    tenant_response: {
                      id: response.create_tenant.tenant.id,
                      schema_name: response.create_tenant.tenant.schema_name,
                    },
                  },
                },
              });
            } else if (response?.create_tenant?.errors && response.create_tenant.errors.length > 0) {
              const errorDetails = response.create_tenant.errors.map(error =>
                `${error.field}: ${error.messages.join(", ")}`
              ).join("; ");
              throw new Error(`GraphQL validation errors: ${errorDetails}`);
            } else {
              throw new Error("Tenant creation response is invalid - no tenant or errors returned");
            }
          } catch (error: any) {
            console.error(`[TRPC] ${logPrefix}_CREATE_TENANT Failed for project ${project.id}`, {
              projectId: project.id,
              errorMessage: error.message,
              errorCause: error.cause,
              errorData: error.data,
              timestamp: new Date().toISOString(),
            });

            await prisma.project.update({
              where: { id: project.id },
              data: {
                status: "FAILED",
                statusMessage: `Tenant deployment failed: ${error.message}`,
                metadata: {
                  ...(project.metadata as Record<string, any>),
                  deployment_failed_at: new Date().toISOString(),
                  error_details: {
                    message: error.message,
                    cause: error.cause,
                    data: error.data,
                    stack: error.stack,
                  },
                },
              },
            });
          }
        };

        // Dispatch tenant creation asynchronously with retry flag
        createTenantForProject(project, true, project.name);

        return project;
      }),

    // Debug endpoint to help diagnose configuration issues
    debug: protectedProcedure
      .input(z.object({ projectId: z.string() }))
      .query(async ({ input }) => {
        const project = await prisma.project.findUnique({
          where: { id: input.projectId },
          include: {
            organization: {
              include: {
                subscription: true,
              },
            },
          },
        });

        if (!project) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "Project not found",
          });
        }

        return {
          project: {
            id: project.id,
            name: project.name,
            status: project.status,
            statusMessage: project.statusMessage,
            tenantId: project.tenantId,
            metadata: project.metadata,
            createdAt: project.createdAt,
            updatedAt: project.updatedAt,
          },
          organization: {
            id: project.organization.id,
            name: project.organization.name,
            hasActiveSubscription: project.organization.subscription?.status === "active",
            subscriptionStatus: project.organization.subscription?.status,
          },
          environment: {
            apiUrl: process.env.KARRIO_PLATFORM_API_URL,
            apiKeyConfigured: !!process.env.KARRIO_PLATFORM_API_KEY,
            tenantApiDomain: process.env.TENANT_API_DOMAIN,
            tenantDashboardDomain: process.env.TENANT_DASHBOARD_DOMAIN,
            nodeEnv: process.env.NODE_ENV,
          },
          tenantConfiguration: project.tenantId ? {
            expectedApiDomain: `${project.id}.${process.env.TENANT_API_DOMAIN?.split(":")[0]}`,
            expectedDashboardDomain: `${project.id}.${process.env.TENANT_DASHBOARD_DOMAIN}`,
          } : null,
        };
      }),
  }),

  billing: router({
    getSubscription: protectedProcedure
      .input(z.object({ orgId: z.string() }))
      .query(async ({ input }): Promise<SubscriptionWithPayment | null> => {
        const subscription = await prisma.subscription.findUnique({
          where: { orgId: input.orgId },
          include: {
            organization: true,
          },
        });

        if (!subscription) return null;

        if (subscription.organization.stripeCustomerId) {
          const paymentMethods = await stripe.paymentMethods.list({
            customer: subscription.organization.stripeCustomerId,
            type: "card",
          });
          return {
            ...subscription,
            defaultPaymentMethod: paymentMethods.data[0],
          };
        }

        return subscription;
      }),

    getPlans: protectedProcedure.query(async () => {
      const prices = await stripe.prices.list({
        active: true,
        expand: ["data.product"],
        type: "recurring",
      });

      return prices.data
        .filter((price) =>
          PRICE_IDS.includes(price.id as (typeof PRICE_IDS)[number]),
        )
        .map((price) => {
          const product = price.product as Stripe.Product;
          return {
            id: price.id,
            name: product.name,
            description: product.description,
            price: price.unit_amount ? price.unit_amount / 100 : 0,
            currency: price.currency,
            interval: price.recurring?.interval || "month",
            features: product.metadata.features
              ? JSON.parse(product.metadata.features)
              : [],
            metadata: product.metadata || {},
          };
        })
        .sort((a, b) => a.price - b.price);
    }),

    createCheckoutSession: protectedProcedure
      .input(
        z.object({
          orgId: z.string(),
          priceId: z.string(),
        }),
      )
      .mutation(async ({ input }) => {
        const org = await prisma.organization.findUnique({
          where: { id: input.orgId },
        });

        if (!org?.stripeCustomerId) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "No customer found",
          });
        }

        const session = await stripe.checkout.sessions.create({
          customer: org.stripeCustomerId,
          mode: "subscription",
          payment_method_types: ["card"],
          line_items: [
            {
              price: input.priceId,
              quantity: 1,
            },
          ],
          success_url: `${process.env.NEXTAUTH_URL}/orgs/${input.orgId}/billing?success=true`,
          cancel_url: `${process.env.NEXTAUTH_URL}/orgs/${input.orgId}/billing?canceled=true`,
        });

        return { url: session.url };
      }),

    getPlan: protectedProcedure
      .input(z.object({ orgId: z.string() }))
      .query(async ({ input }) => {
        const subscription = await prisma.subscription.findUnique({
          where: { orgId: input.orgId },
        });

        if (subscription?.stripePriceId) {
          const price = await stripe.prices.retrieve(
            subscription.stripePriceId,
            {
              expand: ["product"],
            },
          );

          const product = price.product as Stripe.Product;
          const interval = price.recurring?.interval || "month";

          // Handle different subscription states
          let status = subscription.status;
          let statusMessage = "";

          switch (subscription.status) {
            case "incomplete":
              statusMessage = "Payment required to activate subscription";
              break;
            case "incomplete_expired":
              status = "inactive";
              statusMessage = "Payment failed, please update payment method";
              break;
            case "trialing":
              statusMessage = `Trial ends on ${subscription.currentPeriodEnd ? new Date(subscription.currentPeriodEnd).toLocaleDateString() : "N/A"}`;
              break;
            case "active":
              statusMessage = `Renews on ${subscription.currentPeriodEnd ? new Date(subscription.currentPeriodEnd).toLocaleDateString() : "N/A"}`;
              break;
            case "past_due":
              statusMessage = "Payment past due, please update payment method";
              break;
            case "canceled":
              status = "inactive";
              statusMessage = "Subscription has been canceled";
              break;
            case "unpaid":
              status = "inactive";
              statusMessage =
                "Subscription unpaid, please update payment method";
              break;
            case "canceling":
              statusMessage = `Access until ${subscription.currentPeriodEnd ? new Date(subscription.currentPeriodEnd).toLocaleDateString() : "N/A"}`;
              break;
          }

          return {
            name: product.name,
            amount: price.unit_amount ? price.unit_amount / 100 : 0,
            currency: price.currency,
            interval: interval,
            features:
              PRODUCT_FEATURES[
              product.metadata.tier as keyof typeof PRODUCT_FEATURES
              ] || [],
            description: product.description,
            maxProjects: parseInt(product.metadata.max_projects || "0"),
            maxUsers: parseInt(product.metadata.max_users || "0"),
            status,
            statusMessage,
            currentPeriodEnd: subscription.currentPeriodEnd,
            tier: product.metadata.tier || "free",
          };
        }

        // Return initial state details
        return {
          name: "No Active Plan",
          amount: 0,
          currency: "usd",
          interval: "month",
          features: [],
          description: "Select a plan to start using Karrio",
          maxProjects: 0,
          maxUsers: 0,
          status: "inactive",
          statusMessage: "Please select a plan to get started",
          currentPeriodEnd: null,
          tier: "none",
        };
      }),

    getInvoices: protectedProcedure
      .input(z.object({ orgId: z.string() }))
      .query(async ({ input }) => {
        const subscription = await prisma.subscription.findUnique({
          where: { orgId: input.orgId },
          include: { organization: true },
        });

        if (!subscription?.organization.stripeCustomerId) return [];

        const invoices = await stripe.invoices.list({
          customer: subscription.organization.stripeCustomerId,
          limit: 100,
        });

        return invoices.data;
      }),

    createPortalSession: protectedProcedure
      .input(z.object({ orgId: z.string() }))
      .mutation(async ({ input }) => {
        const org = await prisma.organization.findUnique({
          where: { id: input.orgId },
        });

        if (!org?.stripeCustomerId) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "No customer found",
          });
        }

        const session = await stripe.billingPortal.sessions.create({
          customer: org.stripeCustomerId,
          return_url: `${process.env.NEXTAUTH_URL}/orgs/${input.orgId}/billing`,
        });

        return { url: session.url };
      }),

    getBillingInfo: protectedProcedure
      .input(z.object({ orgId: z.string() }))
      .query(async ({ input }) => {
        const org = await prisma.organization.findUnique({
          where: { id: input.orgId },
        });

        if (!org?.stripeCustomerId) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "No customer found",
          });
        }

        const customer = (await stripe.customers.retrieve(
          org.stripeCustomerId,
        )) as Stripe.Customer;
        return {
          email: customer.email,
          address: customer.address,
          name: customer.name,
          phone: customer.phone,
          defaultPaymentMethod: customer.invoice_settings
            ?.default_payment_method as string,
        };
      }),

    updatePaymentMethod: protectedProcedure
      .input(
        z.object({
          orgId: z.string(),
          paymentMethodId: z.string(),
        }),
      )
      .mutation(async ({ input }) => {
        const org = await prisma.organization.findUnique({
          where: { id: input.orgId },
        });

        if (!org?.stripeCustomerId) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "No customer found",
          });
        }

        await stripe.customers.update(org.stripeCustomerId, {
          invoice_settings: {
            default_payment_method: input.paymentMethodId,
          },
        });

        return { success: true };
      }),

    updateBillingInfo: protectedProcedure
      .input(
        z.object({
          orgId: z.string(),
          email: z.string().email().optional(),
          address: z
            .object({
              line1: z.string(),
              line2: z.string().optional(),
              city: z.string(),
              state: z.string(),
              postal_code: z.string(),
              country: z.string(),
            })
            .optional(),
          taxId: z
            .object({
              type: z.string(),
              value: z.string(),
            })
            .optional(),
        }),
      )
      .mutation(async ({ input }) => {
        const org = await prisma.organization.findUnique({
          where: { id: input.orgId },
        });

        if (!org?.stripeCustomerId) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "No customer found",
          });
        }

        const updateData: any = {};
        if (input.email) updateData.email = input.email;
        if (input.address) updateData.address = input.address;
        if (input.taxId) {
          updateData.tax_id_data = [
            {
              type: input.taxId.type,
              value: input.taxId.value,
            },
          ];
        }

        const customer = await stripe.customers.update(
          org.stripeCustomerId,
          updateData,
        );

        return customer;
      }),

    createSetupIntent: protectedProcedure
      .input(z.object({ orgId: z.string() }))
      .mutation(async ({ input }) => {
        const org = await prisma.organization.findUnique({
          where: { id: input.orgId },
        });

        if (!org?.stripeCustomerId) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "No customer found",
          });
        }

        const setupIntent = await stripe.setupIntents.create({
          customer: org.stripeCustomerId,
          payment_method_types: ["card"],
        });

        return {
          setupIntent: setupIntent.client_secret,
        };
      }),

    getPaymentMethods: protectedProcedure
      .input(z.object({ orgId: z.string() }))
      .query(async ({ input }) => {
        const org = await prisma.organization.findUnique({
          where: { id: input.orgId },
        });

        if (!org?.stripeCustomerId) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "No customer found",
          });
        }

        const paymentMethods = await stripe.paymentMethods.list({
          customer: org.stripeCustomerId,
          type: "card",
        });

        return paymentMethods.data;
      }),

    setDefaultPaymentMethod: protectedProcedure
      .input(
        z.object({
          orgId: z.string(),
          paymentMethodId: z.string(),
        }),
      )
      .mutation(async ({ input }) => {
        const org = await prisma.organization.findUnique({
          where: { id: input.orgId },
        });

        if (!org?.stripeCustomerId) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "No customer found",
          });
        }

        // Update the customer's default payment method
        await stripe.customers.update(org.stripeCustomerId, {
          invoice_settings: {
            default_payment_method: input.paymentMethodId,
          },
        });

        return { success: true };
      }),

    deletePaymentMethod: protectedProcedure
      .input(
        z.object({
          orgId: z.string(),
          paymentMethodId: z.string(),
        }),
      )
      .mutation(async ({ input }) => {
        const org = await prisma.organization.findUnique({
          where: { id: input.orgId },
        });

        if (!org?.stripeCustomerId) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "No customer found",
          });
        }

        // Detach the payment method from the customer
        await stripe.paymentMethods.detach(input.paymentMethodId);

        return { success: true };
      }),

    createSubscription: protectedProcedure
      .input(
        z.object({
          orgId: z.string(),
          priceId: z.string(),
        }),
      )
      .mutation(async ({ input }) => {
        const org = await prisma.organization.findUnique({
          where: { id: input.orgId },
          include: {
            subscription: true,
          },
        });

        if (!org?.stripeCustomerId) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "No customer found",
          });
        }

        // Get customer's default payment method
        const customer = (await stripe.customers.retrieve(
          org.stripeCustomerId,
        )) as Stripe.Customer;

        if (!customer.invoice_settings?.default_payment_method) {
          throw new TRPCError({
            code: "BAD_REQUEST",
            message: "Please add a payment method first",
          });
        }

        try {
          let subscription;

          if (org.subscription?.stripeSubscriptionId) {
            // Get current subscription status
            const currentSubscription = await stripe.subscriptions.retrieve(
              org.subscription.stripeSubscriptionId,
            );

            if (currentSubscription.status === "canceled") {
              // Create new subscription if the current one is canceled
              subscription = await stripe.subscriptions.create({
                customer: org.stripeCustomerId,
                items: [{ price: input.priceId }],
                default_payment_method: customer.invoice_settings
                  .default_payment_method as string,
                payment_settings: {
                  payment_method_types: ["card"],
                  save_default_payment_method: "on_subscription",
                },
                expand: ["latest_invoice.payment_intent"],
              });
            } else {
              // Update existing subscription
              subscription = await stripe.subscriptions.update(
                org.subscription.stripeSubscriptionId,
                {
                  items: [
                    {
                      id: currentSubscription.items.data[0].id,
                      price: input.priceId,
                    },
                  ],
                  proration_behavior: "always_invoice",
                },
              );
            }
          } else {
            // Create new subscription
            subscription = await stripe.subscriptions.create({
              customer: org.stripeCustomerId,
              items: [{ price: input.priceId }],
              default_payment_method: customer.invoice_settings
                .default_payment_method as string,
              payment_settings: {
                payment_method_types: ["card"],
                save_default_payment_method: "on_subscription",
              },
              expand: ["latest_invoice.payment_intent"],
            });
          }

          // Update subscription in database
          await prisma.subscription.upsert({
            where: {
              orgId: input.orgId,
            },
            create: {
              orgId: input.orgId,
              stripeSubscriptionId: subscription.id,
              stripePriceId: input.priceId,
              status: subscription.status,
              currentPeriodEnd: new Date(
                subscription.current_period_end * 1000,
              ),
            },
            update: {
              stripeSubscriptionId: subscription.id,
              stripePriceId: input.priceId,
              status: subscription.status,
              currentPeriodEnd: new Date(
                subscription.current_period_end * 1000,
              ),
            },
          });

          return { subscription };
        } catch (error: any) {
          throw new TRPCError({
            code: "INTERNAL_SERVER_ERROR",
            message: error?.message || "Failed to create subscription",
          });
        }
      }),

    cancelSubscription: protectedProcedure
      .input(z.object({ orgId: z.string() }))
      .mutation(async ({ input }) => {
        const org = await prisma.organization.findUnique({
          where: { id: input.orgId },
          include: { subscription: true },
        });

        if (!org?.subscription?.stripeSubscriptionId) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "No active subscription found",
          });
        }

        try {
          // Cancel the subscription at period end
          await stripe.subscriptions.update(
            org.subscription.stripeSubscriptionId,
            {
              cancel_at_period_end: true,
            },
          );

          // Update subscription in database
          await prisma.subscription.update({
            where: { orgId: input.orgId },
            data: {
              status: "canceling",
            },
          });

          return { success: true };
        } catch (error: any) {
          throw new TRPCError({
            code: "INTERNAL_SERVER_ERROR",
            message: error?.message || "Failed to cancel subscription",
          });
        }
      }),

    reactivateSubscription: protectedProcedure
      .input(z.object({ orgId: z.string() }))
      .mutation(async ({ input }) => {
        const org = await prisma.organization.findUnique({
          where: { id: input.orgId },
          include: { subscription: true },
        });

        if (!org?.subscription?.stripeSubscriptionId) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "No subscription found",
          });
        }

        try {
          // Remove the cancellation schedule
          await stripe.subscriptions.update(
            org.subscription.stripeSubscriptionId,
            {
              cancel_at_period_end: false,
            },
          );

          // Update subscription in database
          await prisma.subscription.update({
            where: { orgId: input.orgId },
            data: {
              status: "active",
            },
          });

          return { success: true };
        } catch (error: any) {
          throw new TRPCError({
            code: "INTERNAL_SERVER_ERROR",
            message: error?.message || "Failed to reactivate subscription",
          });
        }
      }),

    deleteOrganization: protectedProcedure
      .input(z.object({ orgId: z.string() }))
      .mutation(async ({ input }) => {
        const org = await prisma.organization.findUnique({
          where: { id: input.orgId },
          include: {
            subscription: true,
            members: true,
          },
        });

        if (!org) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "Organization not found",
          });
        }

        try {
          // Cancel any active subscription immediately
          if (org.subscription?.stripeSubscriptionId) {
            await stripe.subscriptions.cancel(
              org.subscription.stripeSubscriptionId,
            );
          }

          // Delete customer in Stripe
          if (org.stripeCustomerId) {
            await stripe.customers.del(org.stripeCustomerId);
          }

          // Delete organization and all related data
          await prisma.$transaction([
            // Delete subscription
            prisma.subscription.deleteMany({
              where: { orgId: input.orgId },
            }),
            // Delete members
            prisma.organizationMembership.deleteMany({
              where: { orgId: input.orgId },
            }),
            // Delete organization
            prisma.organization.delete({
              where: { id: input.orgId },
            }),
          ]);

          return { success: true };
        } catch (error: any) {
          throw new TRPCError({
            code: "INTERNAL_SERVER_ERROR",
            message: error?.message || "Failed to delete organization",
          });
        }
      }),

    retrySubscriptionPayment: protectedProcedure
      .input(
        z.object({
          orgId: z.string(),
          paymentMethodId: z.string(),
        }),
      )
      .mutation(async ({ input }) => {
        const org = await prisma.organization.findUnique({
          where: { id: input.orgId },
          include: { subscription: true },
        });

        if (!org?.subscription?.stripeSubscriptionId) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "No subscription found",
          });
        }

        try {
          const subscription = await stripe.subscriptions.retrieve(
            org.subscription.stripeSubscriptionId,
            { expand: ["latest_invoice"] },
          );

          if (
            subscription.status === "incomplete" &&
            subscription.latest_invoice
          ) {
            const invoice = subscription.latest_invoice as Stripe.Invoice;

            // Update the default payment method for the subscription
            await stripe.subscriptions.update(subscription.id, {
              default_payment_method: input.paymentMethodId,
            });

            // Retry the payment with the selected payment method
            await stripe.invoices.pay(invoice.id, {
              payment_method: input.paymentMethodId,
            });

            // Update subscription status in database
            await prisma.subscription.update({
              where: { orgId: input.orgId },
              data: {
                status: "active",
              },
            });
          }

          return { success: true };
        } catch (error: any) {
          throw new TRPCError({
            code: "INTERNAL_SERVER_ERROR",
            message: error?.message || "Failed to process payment",
          });
        }
      }),
  }),
});

export type AppRouter = typeof appRouter;
