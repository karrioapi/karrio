import Stripe from "stripe";

// Lazily initialise so a missing STRIPE_SECRET_KEY doesn't crash the build.
let _stripe: Stripe | null = null;

export const stripe = new Proxy({} as Stripe, {
  get(_target, prop) {
    if (!_stripe) {
      _stripe = new Stripe(process.env.STRIPE_SECRET_KEY ?? "sk_placeholder");
    }
    return (_stripe as any)[prop];
  },
});
