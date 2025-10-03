"use client";

import { ForgotPasswordForm } from "@karrio/console/components/forgot-password-form";
import Link from "next/link";

export default function ForgotPassword() {
  return (
    <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div className="bg-white px-4 py-8 shadow sm:rounded-lg sm:px-10">
        <h2 className="mb-6 text-center text-2xl font-bold text-gray-900">
          Reset your password
        </h2>
        <ForgotPasswordForm />
        <p className="mt-6 text-center text-sm text-gray-600">
          Remember your password?{" "}
          <Link
            href="/signin"
            className="font-medium text-indigo-600 hover:text-indigo-500"
          >
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
