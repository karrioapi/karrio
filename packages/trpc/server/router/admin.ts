import { router } from "@karrio/trpc/server/_app";
import { protectedProcedure } from "@karrio/trpc/server/middleware";
import { z } from "zod";
import {
  GET_USERS,
  CREATE_USER,
  UPDATE_USER,
  REMOVE_USER,
  GET_CONFIGS,
  UPDATE_CONFIGS,
  GET_SURCHARGE,
  GET_SURCHARGES,
  CREATE_SURCHARGE,
  UPDATE_SURCHARGE,
  DELETE_SURCHARGE,
  GET_RATE_SHEET,
  GET_RATE_SHEETS,
  CREATE_RATE_SHEET,
  UPDATE_RATE_SHEET,
  DELETE_RATE_SHEET,
  UPDATE_SERVICE_ZONE,
  GET_SYSTEM_CONNECTIONS,
  GET_SYSTEM_CONNECTION,
  CREATE_SYSTEM_CONNECTION,
  UPDATE_SYSTEM_CONNECTION,
  DELETE_SYSTEM_CONNECTION,
  GET_ACCOUNTS,
  CREATE_ORGANIZATION_ACCOUNT,
  UPDATE_ORGANIZATION_ACCOUNT,
  DISABLE_ORGANIZATION_ACCOUNT,
  DELETE_ORGANIZATION_ACCOUNT,
  GET_PERMISSION_GROUPS,
} from "@karrio/types/graphql/admin/queries";
import { gqlstr } from "@karrio/lib";
import type {
  GetUsers,
  GetConfigs,
  GetSurcharge,
  GetSurcharges,
  GetSystemConnections,
  GetSystemConnection,
  GetAccounts,
  GetPermissionGroups,
  CreateUser,
  UpdateUser,
  RemoveUser,
  UpdateConfigs,
  CreateSurcharge,
  UpdateSurcharge,
  DeleteSurcharge,
  GetRateSheet,
  GetRateSheets,
  CreateRateSheet,
  UpdateRateSheet,
  DeleteRateSheet,
  UpdateServiceZone,
  CreateSystemConnection,
  UpdateSystemConnection,
  DeleteSystemConnection,
  CreateOrganizationAccount,
  UpdateOrganizationAccount,
  DisableOrganizationAccount,
  DeleteOrganizationAccount,
} from "@karrio/types/graphql/admin/types";
import { TRPCError } from "@trpc/server";
import { CarrierNameEnum } from "@karrio/types/graphql/admin/types";

interface GraphQLError {
  field: string;
  messages: string[];
}

function handleErrors(response: any) {
  // If the response itself is an error (e.g. network error)
  if (response instanceof Error) {
    throw new TRPCError({
      code: "INTERNAL_SERVER_ERROR",
      message: response.message || "A network error occurred",
      cause: response
    });
  }

  // Handle GraphQL response errors (from client)
  if (response?.errors) {
    const errorMessage = response.errors
      .map((error: any) => {
        if (error.message) return error.message;
        if (error.field && error.messages) return `${error.field}: ${error.messages.join(", ")}`;
        return JSON.stringify(error);
      })
      .join("\n");
    throw new TRPCError({
      code: "BAD_REQUEST",
      message: errorMessage,
      cause: response.errors
    });
  }

  // Handle mutation/query specific errors (from resolvers)
  if (response?.response?.errors) {
    const errorMessage = response.response.errors
      .map((error: any) => error.message || JSON.stringify(error))
      .join("\n");
    throw new TRPCError({
      code: "BAD_REQUEST",
      message: errorMessage,
      cause: response.response.errors
    });
  }

  // Handle unexpected response structure
  if (response && typeof response === 'object' && 'message' in response) {
    throw new TRPCError({
      code: "INTERNAL_SERVER_ERROR",
      message: response.message || "An unexpected server error occurred",
      cause: response
    });
  }

  return response;
}

const usersRouter = router({
  list: protectedProcedure
    .input(
      z.object({
        filter: z
          .object({
            email: z.string().optional(),
            is_staff: z.boolean().optional(),
            is_active: z.boolean().optional(),
            is_superuser: z.boolean().optional(),
            order_by: z.string().optional(),
            after: z.string().optional(),
          })
          .optional(),
      }),
    )
    .query(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { users } = await client.admin.request<GetUsers>(
          gqlstr(GET_USERS),
          {
            filter: input.filter,
          },
        );
        return users;
      } catch (error) {
        handleErrors(error);
      }
    }),
  create: protectedProcedure
    .input(
      z.object({
        data: z.object({
          email: z.string(),
          full_name: z.string(),
          is_staff: z.boolean().optional(),
          is_active: z.boolean().optional(),
          is_superuser: z.boolean().optional(),
          permissions: z.array(z.string()).optional(),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { create_user } = await client.admin.request<CreateUser>(
          gqlstr(CREATE_USER),
          {
            data: input.data,
          },
        );
        handleErrors(create_user);
        return create_user.user;
      } catch (error) {
        handleErrors(error);
      }
    }),
  update: protectedProcedure
    .input(
      z.object({
        data: z.object({
          id: z.string(),
          email: z.string().optional(),
          full_name: z.string().optional(),
          is_staff: z.boolean().optional(),
          is_active: z.boolean().optional(),
          is_superuser: z.boolean().optional(),
          permissions: z.array(z.string()).optional(),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { update_user } = await client.admin.request<UpdateUser>(
          gqlstr(UPDATE_USER),
          {
            data: input.data,
          },
        );
        handleErrors(update_user);
        return update_user.user;
      } catch (error) {
        handleErrors(error);
      }
    }),
  remove: protectedProcedure
    .input(
      z.object({
        data: z.object({
          id: z.string(),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { remove_user } = await client.admin.request<RemoveUser>(
          gqlstr(REMOVE_USER),
          {
            data: input.data,
          },
        );
        handleErrors(remove_user);
        return { id: remove_user.id };
      } catch (error) {
        handleErrors(error);
      }
    }),
});

const configsRouter = router({
  list: protectedProcedure.query(async ({ ctx }) => {
    const client = ctx.karrio;
    try {
      const { configs } = await client.admin.request<GetConfigs>(
        gqlstr(GET_CONFIGS),
      );
      return configs;
    } catch (error) {
      handleErrors(error);
    }
  }),
  update: protectedProcedure
    .input(
      z.object({
        data: z.object({
          // Platform Config
          APP_NAME: z.string().optional(),
          APP_WEBSITE: z.string().optional(),

          // Email Config
          EMAIL_USE_TLS: z.boolean().optional(),
          EMAIL_HOST_USER: z.string().optional(),
          EMAIL_HOST_PASSWORD: z.string().optional(),
          EMAIL_HOST: z.string().optional(),
          EMAIL_PORT: z.number().optional(),
          EMAIL_FROM_ADDRESS: z.string().optional(),

          // Address Validation Service
          GOOGLE_CLOUD_API_KEY: z.string().optional(),
          CANADAPOST_ADDRESS_COMPLETE_API_KEY: z.string().optional(),

          // Data Retention
          ORDER_DATA_RETENTION: z.number().optional(),
          TRACKER_DATA_RETENTION: z.number().optional(),
          SHIPMENT_DATA_RETENTION: z.number().optional(),
          API_LOGS_DATA_RETENTION: z.number().optional(),

          // System Settings
          AUDIT_LOGGING: z.boolean().optional(),
          ALLOW_SIGNUP: z.boolean().optional(),
          ALLOW_ADMIN_APPROVED_SIGNUP: z.boolean().optional(),
          ALLOW_MULTI_ACCOUNT: z.boolean().optional(),

          // Feature Flags
          ADMIN_DASHBOARD: z.boolean().optional(),
          MULTI_ORGANIZATIONS: z.boolean().optional(),
          ORDERS_MANAGEMENT: z.boolean().optional(),
          APPS_MANAGEMENT: z.boolean().optional(),
          DOCUMENTS_MANAGEMENT: z.boolean().optional(),
          DATA_IMPORT_EXPORT: z.boolean().optional(),
          WORKFLOW_MANAGEMENT: z.boolean().optional(),
          PERSIST_SDK_TRACING: z.boolean().optional(),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const response = await client.admin.request<UpdateConfigs>(
          gqlstr(UPDATE_CONFIGS),
          { data: input.data },
        );
        if (!response || !response.update_configs) {
          throw new Error('Invalid response from server');
        }
        handleErrors(response.update_configs);
        return response.update_configs.configs;
      } catch (error) {
        handleErrors(error);
      }
    }),
});

const surchargesRouter = router({
  list: protectedProcedure
    .input(
      z.object({
        filter: z
          .object({
            keyword: z.string().optional(),
            active: z.boolean().optional(),
            surcharge_type: z.string().optional(),
            order_by: z.string().optional(),
            page: z.number().optional(),
          })
          .optional(),
      }),
    )
    .query(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { surcharges } = await client.admin.request<GetSurcharges>(
          gqlstr(GET_SURCHARGES),
          {
            filter: input.filter,
          },
        );
        return surcharges;
      } catch (error) {
        handleErrors(error);
      }
    }),
  get: protectedProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { surcharge } = await client.admin.request<GetSurcharge>(
          gqlstr(GET_SURCHARGE),
          {
            id: input.id,
          },
        );
        return surcharge;
      } catch (error) {
        handleErrors(error);
      }
    }),
  create: protectedProcedure
    .input(
      z.object({
        data: z.object({
          name: z.string(),
          amount: z.number(),
          surcharge_type: z.string(),
          active: z.boolean().optional(),
          carriers: z.array(z.string()).optional(),
          services: z.array(z.string()).optional(),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { create_surcharge } = await client.admin.request<CreateSurcharge>(
          gqlstr(CREATE_SURCHARGE),
          {
            data: input.data,
          },
        );
        handleErrors(create_surcharge);
        return create_surcharge.surcharge;
      } catch (error) {
        handleErrors(error);
      }
    }),
  update: protectedProcedure
    .input(
      z.object({
        data: z.object({
          id: z.string(),
          name: z.string().optional(),
          amount: z.number().optional(),
          surcharge_type: z.string().optional(),
          active: z.boolean().optional(),
          carriers: z.array(z.string()).optional(),
          services: z.array(z.string()).optional(),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { update_surcharge } = await client.admin.request<UpdateSurcharge>(
          gqlstr(UPDATE_SURCHARGE),
          {
            data: input.data,
          },
        );
        handleErrors(update_surcharge);
        return update_surcharge.surcharge;
      } catch (error) {
        handleErrors(error);
      }
    }),
  delete: protectedProcedure
    .input(
      z.object({
        data: z.object({
          id: z.string(),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { delete_surcharge } = await client.admin.request<DeleteSurcharge>(
          gqlstr(DELETE_SURCHARGE),
          {
            data: input.data,
          },
        );
        handleErrors(delete_surcharge);
        return { id: delete_surcharge.id };
      } catch (error) {
        handleErrors(error);
      }
    }),
});

const rateSheetsRouter = router({
  list: protectedProcedure
    .input(
      z.object({
        filter: z
          .object({
            keyword: z.string().optional(),
          })
          .optional(),
      }),
    )
    .query(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { rate_sheets } = await client.admin.request<GetRateSheets>(
          gqlstr(GET_RATE_SHEETS),
          {
            filter: input.filter,
          },
        );
        return rate_sheets;
      } catch (error) {
        handleErrors(error);
      }
    }),
  get: protectedProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { rate_sheet } = await client.admin.request<GetRateSheet>(
          gqlstr(GET_RATE_SHEET),
          {
            id: input.id,
          },
        );
        return rate_sheet;
      } catch (error) {
        handleErrors(error);
      }
    }),
  create: protectedProcedure
    .input(
      z.object({
        data: z.object({
          name: z.string(),
          carrier_name: z.string(),
          metadata: z.record(z.any()).optional(),
          services: z.array(z.any()).optional(),
          carriers: z.array(z.string()).optional(),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { create_rate_sheet } = await client.admin.request<CreateRateSheet>(
          gqlstr(CREATE_RATE_SHEET),
          {
            data: input.data,
          },
        );
        handleErrors(create_rate_sheet);
        return create_rate_sheet.rate_sheet;
      } catch (error) {
        handleErrors(error);
      }
    }),
  update: protectedProcedure
    .input(
      z.object({
        data: z.object({
          id: z.string(),
          name: z.string().optional(),
          carrier_name: z.string().optional(),
          metadata: z.record(z.any()).optional(),
          services: z.array(z.any()).optional(),
          carriers: z.array(z.string()).optional(),
          remove_missing_services: z.boolean().optional(),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { update_rate_sheet } = await client.admin.request<UpdateRateSheet>(
          gqlstr(UPDATE_RATE_SHEET),
          {
            data: input.data,
          },
        );
        handleErrors(update_rate_sheet);
        return update_rate_sheet.rate_sheet;
      } catch (error) {
        handleErrors(error);
      }
    }),
  update_service_zone: protectedProcedure
    .input(
      z.object({
        data: z.object({
          id: z.string(),
          service_id: z.string(),
          zone_index: z.number(),
          zone: z.object({
            rate: z.number().optional(),
            label: z.string().optional(),
            min_weight: z.number().optional(),
            max_weight: z.number().optional(),
            transit_days: z.number().optional(),
            transit_time: z.number().optional(),
            radius: z.number().optional(),
            latitude: z.number().optional(),
            longitude: z.number().optional(),
            cities: z.array(z.string()).optional(),
            postal_codes: z.array(z.string()).optional(),
            country_codes: z.array(z.string()).optional(),
          }),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { update_service_zone } = await client.admin.request<UpdateServiceZone>(
          gqlstr(UPDATE_SERVICE_ZONE),
          {
            data: input.data,
          },
        );
        handleErrors(update_service_zone);
        return update_service_zone.rate_sheet;
      } catch (error) {
        handleErrors(error);
      }
    }),
  delete: protectedProcedure
    .input(
      z.object({
        data: z.object({
          id: z.string(),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { delete_rate_sheet } = await client.admin.request<DeleteRateSheet>(
          gqlstr(DELETE_RATE_SHEET),
          {
            data: input.data,
          },
        );
        handleErrors(delete_rate_sheet);
        return { id: delete_rate_sheet.id };
      } catch (error) {
        handleErrors(error);
      }
    }),
});

const systemConnectionsRouter = router({
  list: protectedProcedure
    .input(
      z.object({
        filter: z.object({
          active: z.boolean().optional(),
          metadata_key: z.string().optional(),
          metadata_value: z.string().optional(),
          carrier_name: z.array(z.string()).optional(),
          offset: z.number().optional(),
          first: z.number().optional(),
        }).optional(),
      })
    )
    .query(async ({ ctx, input }) => {
      const client = ctx.karrio;
      const { system_carrier_connections } = await client.admin.request<GetSystemConnections>(
        gqlstr(GET_SYSTEM_CONNECTIONS),
        {
          filter: input.filter,
        },
      );
      return system_carrier_connections;
    }),
  get: protectedProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      const client = ctx.karrio;
      const { system_carrier_connection } = await client.admin.request<GetSystemConnection>(
        gqlstr(GET_SYSTEM_CONNECTION),
        { id: input.id },
      );
      return system_carrier_connection;
    }),
  create: protectedProcedure
    .input(
      z.object({
        data: z.object({
          carrier_name: z.nativeEnum(CarrierNameEnum),
          carrier_id: z.string(),
          credentials: z.record(z.any()),
          active: z.boolean().optional(),
          config: z.record(z.any()).optional(),
          metadata: z.record(z.any()).optional(),
          capabilities: z.array(z.string()).optional(),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      const { create_system_carrier_connection } = await client.admin.request<CreateSystemConnection>(
        gqlstr(CREATE_SYSTEM_CONNECTION),
        {
          data: {
            carrier_name: input.data.carrier_name,
            carrier_id: input.data.carrier_id,
            credentials: input.data.credentials,
            active: input.data.active,
            config: input.data.config || {},
            metadata: input.data.metadata || {},
            capabilities: input.data.capabilities || [],
          }
        },
      );

      handleErrors(create_system_carrier_connection.errors);
      return create_system_carrier_connection.connection;
    }),
  update: protectedProcedure
    .input(
      z.object({
        data: z.object({
          id: z.string(),
          active: z.boolean().optional(),
          carrier_id: z.string().optional(),
          credentials: z.record(z.any()).optional(),
          config: z.record(z.any()).optional(),
          metadata: z.record(z.any()).optional(),
          capabilities: z.array(z.string()).optional(),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      const { update_system_carrier_connection } = await client.admin.request<UpdateSystemConnection>(
        gqlstr(UPDATE_SYSTEM_CONNECTION),
        {
          data: {
            id: input.data.id,
            active: input.data.active,
            carrier_id: input.data.carrier_id,
            credentials: input.data.credentials,
            config: input.data.config,
            metadata: input.data.metadata,
            capabilities: input.data.capabilities,
          }
        },
      );

      handleErrors(update_system_carrier_connection.errors);
      return update_system_carrier_connection.connection;
    }),
  delete: protectedProcedure
    .input(
      z.object({
        data: z.object({
          id: z.string(),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      const { delete_system_carrier_connection } = await client.admin.request<DeleteSystemConnection>(
        gqlstr(DELETE_SYSTEM_CONNECTION),
        { data: input.data },
      );

      handleErrors(delete_system_carrier_connection.errors);
      return { id: delete_system_carrier_connection.id };
    }),
});

const organizationAccountsRouter = router({
  list: protectedProcedure
    .input(
      z.object({
        filter: z
          .object({
            keyword: z.string().optional(),
            is_active: z.boolean().optional(),
            order_by: z.string().optional(),
          })
          .optional(),
      }),
    )
    .query(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { accounts } = await client.admin.request<GetAccounts>(
          gqlstr(GET_ACCOUNTS),
          {
            filter: input.filter,
          },
        );
        return accounts;
      } catch (error) {
        handleErrors(error);
      }
    }),
  create: protectedProcedure
    .input(
      z.object({
        data: z.object({
          name: z.string(),
          slug: z.string(),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { create_organization_account } =
          await client.admin.request<CreateOrganizationAccount>(
            gqlstr(CREATE_ORGANIZATION_ACCOUNT),
            { data: input.data },
          );
        handleErrors(create_organization_account);
        return create_organization_account.account;
      } catch (error) {
        handleErrors(error);
      }
    }),
  update: protectedProcedure
    .input(
      z.object({
        data: z.object({
          id: z.string(),
          name: z.string().optional(),
          slug: z.string().optional(),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { update_organization_account } =
          await client.admin.request<UpdateOrganizationAccount>(
            gqlstr(UPDATE_ORGANIZATION_ACCOUNT),
            { data: input.data },
          );
        handleErrors(update_organization_account);
        return update_organization_account.account;
      } catch (error) {
        handleErrors(error);
      }
    }),
  disable: protectedProcedure
    .input(
      z.object({
        data: z.object({
          id: z.string(),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { disable_organization_account } =
          await client.admin.request<DisableOrganizationAccount>(
            gqlstr(DISABLE_ORGANIZATION_ACCOUNT),
            { data: input.data },
          );
        handleErrors(disable_organization_account);
        return disable_organization_account.account;
      } catch (error) {
        handleErrors(error);
      }
    }),
  delete: protectedProcedure
    .input(
      z.object({
        data: z.object({
          id: z.string(),
        }),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { delete_organization_account } =
          await client.admin.request<DeleteOrganizationAccount>(
            gqlstr(DELETE_ORGANIZATION_ACCOUNT),
            { data: input.data },
          );
        handleErrors(delete_organization_account);
        return delete_organization_account.account;
      } catch (error) {
        handleErrors(error);
      }
    }),
});

const permissionGroupsRouter = router({
  list: protectedProcedure
    .input(
      z.object({
        filter: z
          .object({
            keyword: z.string().optional(),
            order_by: z.string().optional(),
          })
          .optional(),
      }),
    )
    .query(async ({ ctx, input }) => {
      const client = ctx.karrio;
      try {
        const { permission_groups } =
          await client.admin.request<GetPermissionGroups>(
            gqlstr(GET_PERMISSION_GROUPS),
            {
              filter: input.filter,
            },
          );
        return permission_groups;
      } catch (error) {
        handleErrors(error);
      }
    }),
});

export const adminRouter = router({
  users: usersRouter,
  configs: configsRouter,
  surcharges: surchargesRouter,
  rate_sheets: rateSheetsRouter,
  system_connections: systemConnectionsRouter,
  organization_accounts: organizationAccountsRouter,
  permission_groups: permissionGroupsRouter,
});

export type AdminRouter = typeof adminRouter;
