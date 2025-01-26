import { CardElement, useElements } from "@stripe/react-stripe-js";
import { Button } from "@karrio/insiders/components/ui/button";
import { useStripe } from "@stripe/react-stripe-js";
import { trpc } from "@karrio/console/trpc/client";
import { useState } from "react";

interface PaymentMethodFormProps {
  organizationId: string;
  onSuccess: () => void;
  clientSecret: string | null;
}

export function PaymentMethodForm({
  organizationId,
  onSuccess,
  clientSecret,
}: PaymentMethodFormProps) {
  const stripe = useStripe();
  const elements = useElements();
  const [error, setError] = useState<string | null>(null);
  const [processing, setProcessing] = useState(false);
  const utils = trpc.useContext();
  const updatePaymentMethod = trpc.billing.updatePaymentMethod.useMutation({
    onSuccess: () => {
      utils.billing.getPaymentMethods.invalidate();
      utils.billing.getSubscription.invalidate();
    },
  });
  const createSetupIntent = trpc.billing.createSetupIntent.useMutation();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!stripe || !elements) {
      return;
    }

    setProcessing(true);
    setError(null);

    try {
      // First, create a setup intent
      const { setupIntent: clientSecret } = await createSetupIntent.mutateAsync(
        {
          organizationId,
        },
      );

      if (!clientSecret) {
        throw new Error("Failed to create setup intent");
      }

      // Confirm the setup intent with the card element
      const { error: confirmError, setupIntent } =
        await stripe.confirmCardSetup(clientSecret, {
          payment_method: {
            card: elements.getElement(CardElement)!,
            billing_details: {}, // Add billing details if needed
          },
        });

      if (confirmError) {
        setError(confirmError.message || "An error occurred");
        return;
      }

      if (!setupIntent?.payment_method) {
        throw new Error("No payment method returned");
      }

      // Update the organization's payment method
      await updatePaymentMethod.mutateAsync({
        organizationId,
        paymentMethodId: setupIntent.payment_method as string,
      });

      // Clear the card element
      elements.getElement(CardElement)?.clear();
      onSuccess();
    } catch (error: any) {
      console.error("Payment method error:", error);
      setError(error?.message || "Failed to add payment method");
    } finally {
      setProcessing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-4">
        <div className="rounded-md border p-4">
          <CardElement
            options={{
              style: {
                base: {
                  fontSize: "16px",
                  color: "#424770",
                  "::placeholder": {
                    color: "#aab7c4",
                  },
                },
                invalid: {
                  color: "#9e2146",
                },
              },
              hidePostalCode: true,
            }}
          />
        </div>

        {error && (
          <div className="text-sm text-destructive bg-destructive/10 p-3 rounded-md">
            {error}
          </div>
        )}

        <Button
          type="submit"
          disabled={!stripe || processing}
          className="w-full"
        >
          {processing ? "Processing..." : "Add Card"}
        </Button>
      </div>
    </form>
  );
}
