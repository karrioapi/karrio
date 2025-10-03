"use client";

import { addUrlParam, insertUrlParam, removeUrlParam } from "@karrio/lib";
import { useRouter, useSearchParams } from "next/navigation";

export function useLocation(): any {
  const router = useRouter();
  const searchParams = useSearchParams();

  const updateUrlParam = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams.toString());
    params.set(key, value);

    router.push(location.pathname + "?" + params.toString());
  };

  return {
    ...router,
    addUrlParam,
    updateUrlParam,
    insertUrlParam,
    removeUrlParam,
  };
}
