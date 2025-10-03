"use client";

import { useSession } from "next-auth/react";

export function UserProfile() {
  const { data: session } = useSession();

  if (!session) return null;

  return (
    <div>
      <img src={session.user.image!} alt={session.user.name!} />
      <h2>{session.user.name}</h2>
      <p>{session.user.email}</p>
      <p>Role: {session.organization?.role}</p>
    </div>
  );
}
