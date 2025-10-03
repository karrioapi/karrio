import { stripe } from "@karrio/console/shared/stripe";
import { prisma } from "@karrio/console/prisma/client";
import { headers } from "next/headers";

export async function POST(req: Request) {
  const body = await req.text();
  const signature = (await headers()).get("stripe-signature") as string;

  try {
    const event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!,
    );

    switch (event.type) {
      case "checkout.session.completed": {
        const session = event.data.object;
        const orgId = session.metadata?.orgId || null;

        if (!orgId) {
          throw new Error("Organization ID is required");
        }

        // Update the organization with the stripeCustomerId
        await prisma.organization.update({
          where: { id: orgId },
          data: {
            stripeCustomerId: session.customer as string,
          },
        });

        await prisma.subscription.upsert({
          where: { orgId },
          create: {
            orgId,
            stripeSubscriptionId: session.subscription as string,
            stripePriceId: session.metadata?.priceId,
            status: "active",
            currentPeriodEnd: new Date(session.expires_at * 1000),
          },
          update: {
            stripeSubscriptionId: session.subscription as string,
            stripePriceId: session.metadata?.priceId,
            status: "active",
            currentPeriodEnd: new Date(session.expires_at * 1000),
          },
        });
        break;
      }

      case "invoice.payment_succeeded": {
        const invoice = event.data.object;
        const subscriptionId = invoice.subscription;
        const subscription = await prisma.subscription.findFirst({
          where: { stripeSubscriptionId: subscriptionId as string },
        });

        if (subscription) {
          await prisma.subscription.update({
            where: { id: subscription.id },
            data: {
              status: "active",
              currentPeriodEnd: new Date(invoice.period_end * 1000),
            },
          });
        }
        break;
      }
    }

    return new Response(null, { status: 200 });
  } catch (err) {
    console.error(err);
    return new Response(JSON.stringify({ error: "Failed to handle webhook" }), {
      status: 400,
    });
  }
}
