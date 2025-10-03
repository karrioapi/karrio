import { Prisma } from "@prisma/client";
import Stripe from "stripe";

export type SubscriptionWithPayment = Prisma.SubscriptionGetPayload<{}> & {
  defaultPaymentMethod?: Stripe.PaymentMethod;
};

export const PRODUCT_FEATURES = {
  pro: [
    "Unlimited shipments",
    "Priority support",
    "Custom integrations",
    "Advanced analytics",
  ],
  enterprise: [
    "Everything in Pro",
    "Dedicated support",
    "Custom development",
    "SLA guarantees",
  ],
} as const;

export function formatProjectUrl(domain?: string, path: string = ""): string {
  if (!domain) return "";
  const baseUrl = domain.endsWith("/") ? domain.slice(0, -1) : domain;
  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  return `${baseUrl}${cleanPath}`;
}
