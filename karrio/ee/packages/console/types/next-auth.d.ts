import "next-auth";

interface Organization {
  id: string;
  name: string;
  role: string;
}

declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      email: string;
      name?: string | null;
      image?: string | null;
    };
    organization?: Organization;
  }

  interface User {
    id: string;
    email: string;
    name?: string | null;
    image?: string | null;
  }
}
