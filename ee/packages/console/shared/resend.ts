import { Resend } from "resend";

// Lazily initialise so a missing RESEND_API_KEY doesn't crash the build.
let _resend: Resend | null = null;

export const resend = new Proxy({} as Resend, {
  get(_target, prop) {
    if (!_resend) {
      _resend = new Resend(process.env.RESEND_API_KEY ?? "placeholder");
    }
    return (_resend as any)[prop];
  },
});
