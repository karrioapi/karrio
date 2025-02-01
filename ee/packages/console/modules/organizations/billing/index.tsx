"use client";

import { PaymentMethodForm } from "@karrio/console/components/payment-method-form";
import { DashboardHeader } from "@karrio/console/components/dashboard-header";
import {
  CheckIcon,
  ChevronRight,
  DownloadIcon,
  FileIcon,
  PlusIcon,
} from "lucide-react";
import { Button } from "@karrio/insiders/components/ui/button";
import { useToast } from "@karrio/insiders/hooks/use-toast";
import { trpc } from "@karrio/console/trpc/client";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@karrio/insiders/components/ui/card";
import { Input } from "@karrio/insiders/components/ui/input";
import { Elements } from "@stripe/react-stripe-js";
import { cn } from "@karrio/insiders/lib/utils";
import { loadStripe } from "@stripe/stripe-js";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@karrio/insiders/components/ui/dialog";
import {
  RadioGroup,
  RadioGroupItem,
} from "@karrio/insiders/components/ui/radio-group";
import { CreditCard } from "lucide-react";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@karrio/insiders/components/ui/alert-dialog";
import { PlanSelection } from "@karrio/console/components/plan-selection";

const formatCurrency = (amount: number, currency: string) => {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: currency.toUpperCase(),
  }).format(amount);
};

// Initialize Stripe
const stripePromise = loadStripe(
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!,
);

export default function BillingPage({ params }: { params: { orgId: string } }) {
  const { toast } = useToast();
  const router = useRouter();
  const utils = trpc.useUtils();
  const { data: subscription } = trpc.billing.getSubscription.useQuery({
    orgId: params.orgId,
  });
  const { data: billingInfo } = trpc.billing.getBillingInfo.useQuery({
    orgId: params.orgId,
  });
  const { data: currentPlan } = trpc.billing.getPlan.useQuery({
    orgId: params.orgId,
  });
  const { data: invoices } = trpc.billing.getInvoices.useQuery({
    orgId: params.orgId,
  });
  const updateBilling = trpc.billing.updateBillingInfo.useMutation();
  const createSetupIntent = trpc.billing.createSetupIntent.useMutation();
  const [billingEmail, setBillingEmail] = useState("");
  const [billingAddress, setBillingAddress] = useState({
    line1: "",
    line2: "",
    city: "",
    state: "",
    postal_code: "",
    country: "US",
  });
  const [taxIdType, setTaxIdType] = useState("");
  const [taxIdNumber, setTaxIdNumber] = useState("");
  const [showPaymentForm, setShowPaymentForm] = useState(false);
  const [setupIntentSecret, setSetupIntentSecret] = useState<string | null>(
    null,
  );

  const [isMounted, setIsMounted] = useState(false);
  const { data: paymentMethods } = trpc.billing.getPaymentMethods.useQuery({
    orgId: params.orgId,
  });
  const setDefaultPaymentMethod =
    trpc.billing.setDefaultPaymentMethod.useMutation();
  const deletePaymentMethod = trpc.billing.deletePaymentMethod.useMutation({
    onSuccess: () => {
      utils.billing.getPaymentMethods.invalidate();
      utils.billing.getSubscription.invalidate();
      toast({
        title: "Success",
        description: "Payment method removed successfully",
      });
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: error.message || "Failed to remove payment method",
        variant: "destructive",
      });
    },
  });

  const [selectedPlan, setSelectedPlan] = useState<string | null>(null);
  const [showPlanSelection, setShowPlanSelection] = useState(false);
  const { data: plans } = trpc.billing.getPlans.useQuery();

  const refreshAllResources = () => {
    utils.billing.getSubscription.invalidate();
    utils.billing.getBillingInfo.invalidate();
    utils.billing.getPlan.invalidate();
    utils.billing.getInvoices.invalidate();
    utils.billing.getPaymentMethods.invalidate();
  };

  const createSubscription = trpc.billing.createSubscription.useMutation({
    onSuccess: () => {
      refreshAllResources();
      setShowPlanSelection(false);
      toast({
        title: "Success",
        description: "Subscription updated successfully",
      });
    },
  });

  const [showCancelDialog, setShowCancelDialog] = useState(false);

  const cancelSubscription = trpc.billing.cancelSubscription.useMutation({
    onSuccess: () => {
      utils.billing.getSubscription.invalidate();
      toast({
        title: "Success",
        description:
          "Your subscription will be canceled at the end of the billing period",
      });
    },
  });

  const reactivateSubscription =
    trpc.billing.reactivateSubscription.useMutation({
      onSuccess: () => {
        utils.billing.getSubscription.invalidate();
        toast({
          title: "Success",
          description: "Your subscription has been reactivated",
        });
      },
    });

  const retrySubscriptionPayment =
    trpc.billing.retrySubscriptionPayment.useMutation({
      onSuccess: () => {
        utils.billing.getSubscription.invalidate();
        utils.billing.getPlan.invalidate();
        toast({
          title: "Success",
          description: "Payment processed successfully",
        });
      },
      onError: (error) => {
        toast({
          title: "Error",
          description: error.message || "Failed to process payment",
          variant: "destructive",
        });
      },
    });

  useEffect(() => {
    setIsMounted(true);
  }, []);

  useEffect(() => {
    if (billingInfo) {
      setBillingEmail(billingInfo.email || "");
      setBillingAddress({
        line1: billingInfo.address?.line1 || "",
        line2: billingInfo.address?.line2 || "",
        city: billingInfo.address?.city || "",
        state: billingInfo.address?.state || "",
        postal_code: billingInfo.address?.postal_code || "",
        country: billingInfo.address?.country || "US",
      });
    }
  }, [billingInfo]);

  const handleUpdateBilling = async () => {
    try {
      await updateBilling.mutateAsync({
        orgId: params.orgId,
        email: billingEmail,
        address: billingAddress,
      });

      toast({
        title: "Success",
        description: "Billing information updated successfully",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update billing information",
        variant: "destructive",
      });
    }
  };

  const handleUpdateTaxId = async () => {
    try {
      await updateBilling.mutateAsync({
        orgId: params.orgId,
        taxId: {
          type: taxIdType,
          value: taxIdNumber,
        },
      });

      toast({
        title: "Success",
        description: "Tax ID updated successfully",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update tax ID",
        variant: "destructive",
      });
    }
  };

  const handleAddCard = async () => {
    try {
      const setupIntent = await createSetupIntent.mutateAsync({
        orgId: params.orgId,
      });

      setSetupIntentSecret(setupIntent.setupIntent);
      setShowPaymentForm(true);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to initialize card setup",
        variant: "destructive",
      });
    }
  };

  const handleSetDefaultPaymentMethod = async (paymentMethodId: string) => {
    try {
      await setDefaultPaymentMethod.mutateAsync({
        orgId: params.orgId,
        paymentMethodId,
      });
      toast({
        title: "Success",
        description: "Default payment method updated",
      });
      router.refresh();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update default payment method",
        variant: "destructive",
      });
    }
  };

  const handleDeletePaymentMethod = async (paymentMethodId: string) => {
    try {
      await deletePaymentMethod.mutateAsync({
        orgId: params.orgId,
        paymentMethodId,
      });
    } catch (error) {
      // Error is handled by the mutation callbacks
    }
  };

  const handleSubscribe = async () => {
    if (!selectedPlan) return;

    // Check if payment methods exist
    if (!paymentMethods || paymentMethods.length === 0) {
      setShowPlanSelection(false);
      setShowPaymentForm(true);
      toast({
        title: "Payment Method Required",
        description: "Please add a payment method before subscribing to a plan",
        variant: "destructive",
      });
      return;
    }

    try {
      await createSubscription.mutateAsync({
        orgId: params.orgId,
        priceId: selectedPlan,
      });
    } catch (error: any) {
      if (error.message.includes("payment method")) {
        setShowPlanSelection(false);
        setShowPaymentForm(true);
        toast({
          title: "Payment Method Required",
          description:
            "Please add a payment method before subscribing to a plan",
          variant: "destructive",
        });
      } else {
        toast({
          title: "Error",
          description: error.message || "Failed to create subscription",
          variant: "destructive",
        });
      }
    }
  };

  if (!isMounted) {
    return null;
  }

  return (
    <>
      <DashboardHeader
        title="Billing"
        description="Manage your billing settings"
      />

      <div className="p-8 bg-background">
        <div className="max-w-7xl mx-auto space-y-16">
          <section>
            <div className="flex flex-col md:flex-row gap-12">
              <div className="w-full md:w-2/5">
                <h3 className="text-lg font-medium mb-1">Current Plan</h3>
                <p className="text-sm text-muted-foreground">
                  View your current subscription plan and upgrade if needed.
                </p>
              </div>

              <Card className="flex-1">
                <CardHeader className="flex flex-col md:flex-row items-start md:items-center justify-between">
                  <div className="space-y-1.5">
                    <CardTitle className="flex items-center gap-2">
                      {currentPlan?.name}
                      {currentPlan?.status !== "inactive" && (
                        <span
                          className={cn(
                            "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",
                            currentPlan?.status === "active"
                              ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                              : currentPlan?.status === "canceling"
                                ? "bg-yellow-50 text-yellow-700 border border-yellow-200"
                                : "bg-red-50 text-red-700 border border-red-200",
                          )}
                        >
                          {currentPlan?.status}
                        </span>
                      )}
                    </CardTitle>
                    <CardDescription className="text-lg font-semibold">
                      {currentPlan?.amount ? (
                        <>
                          {formatCurrency(
                            currentPlan.amount,
                            currentPlan.currency,
                          )}
                          <span className="text-sm font-normal text-muted-foreground">
                            /{currentPlan.interval}
                          </span>
                        </>
                      ) : (
                        "No active subscription"
                      )}
                    </CardDescription>
                  </div>
                  {currentPlan?.status === "inactive" ? (
                    <Button
                      variant="default"
                      onClick={() => setShowPlanSelection(true)}
                    >
                      Select a Plan
                    </Button>
                  ) : (
                    <Button
                      variant="outline"
                      onClick={() => setShowPlanSelection(true)}
                      disabled={currentPlan?.status === "incomplete"}
                    >
                      {currentPlan?.status === "incomplete"
                        ? "Complete payment"
                        : "Change Plan"}
                    </Button>
                  )}
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="text-sm text-muted-foreground">
                    {currentPlan?.description}
                  </div>

                  {currentPlan?.statusMessage && (
                    <div
                      className={cn(
                        "text-sm rounded-md p-3",
                        currentPlan.status === "active"
                          ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                          : currentPlan.status === "canceling"
                            ? "bg-yellow-50 text-yellow-700 border border-yellow-200"
                            : currentPlan.status === "inactive"
                              ? "bg-blue-50 text-blue-700 border border-blue-200"
                              : "bg-red-50 text-red-700 border border-red-200",
                      )}
                    >
                      {currentPlan.statusMessage}
                    </div>
                  )}

                  {currentPlan?.features && currentPlan.features.length > 0 && (
                    <div className="grid gap-4">
                      <div className="text-sm font-medium">Plan Features:</div>
                      <ul className="grid gap-2">
                        {currentPlan?.features.map((feature, index) => (
                          <li
                            key={index}
                            className="flex items-center gap-2 text-sm"
                          >
                            <CheckIcon className="h-4 w-4 text-emerald-500" />
                            {feature}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {currentPlan?.status === "incomplete" && (
                    <div className="pt-6 border-t">
                      <div className="space-y-4">
                        <div className="space-y-1">
                          <p className="text-sm font-medium">
                            Complete payment with existing payment method:
                          </p>
                          {paymentMethods && paymentMethods.length > 0 ? (
                            <RadioGroup
                              className="space-y-2 mt-2"
                              onValueChange={async (value) => {
                                try {
                                  await retrySubscriptionPayment.mutateAsync({
                                    orgId: params.orgId,
                                    paymentMethodId: value,
                                  });
                                  utils.billing.getSubscription.invalidate();
                                  utils.billing.getPlan.invalidate();
                                  toast({
                                    title: "Success",
                                    description:
                                      "Payment processed successfully",
                                  });
                                } catch (error: any) {
                                  toast({
                                    title: "Error",
                                    description:
                                      error.message ||
                                      "Failed to process payment",
                                    variant: "destructive",
                                  });
                                }
                              }}
                            >
                              {paymentMethods.map((method) => (
                                <div
                                  key={method.id}
                                  className="flex items-center space-x-4 rounded-md border p-4"
                                >
                                  <RadioGroupItem
                                    value={method.id}
                                    id={method.id}
                                  />
                                  <div className="flex items-center space-x-4">
                                    <CreditCard className="h-6 w-6 text-muted-foreground" />
                                    <div>
                                      <div className="text-sm font-medium">
                                        {method.card?.brand?.toUpperCase()} ••••{" "}
                                        {method.card?.last4}
                                      </div>
                                      <div className="text-sm text-muted-foreground">
                                        Expires {method.card?.exp_month}/
                                        {method.card?.exp_year}
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              ))}
                            </RadioGroup>
                          ) : null}
                        </div>
                        <div className="flex items-center gap-4">
                          <div className="text-sm text-muted-foreground">
                            Or add a new payment method:
                          </div>
                          <Button
                            variant="outline"
                            onClick={() => setShowPaymentForm(true)}
                          >
                            Add New Card
                          </Button>
                        </div>
                      </div>
                    </div>
                  )}

                  {currentPlan?.status === "active" && (
                    <div className="pt-6 border-t">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                          <CreditCard className="h-4 w-4" />
                          Next billing date:{" "}
                          {subscription?.currentPeriodEnd
                            ? new Date(
                              subscription.currentPeriodEnd,
                            ).toLocaleDateString()
                            : "N/A"}
                        </div>
                        <div className="flex items-center gap-4">
                          <Button
                            variant="link"
                            className="text-sm p-0 h-auto"
                            onClick={() => setShowPaymentForm(true)}
                          >
                            Update payment method
                            <ChevronRight className="h-4 w-4 ml-1" />
                          </Button>
                          <Button
                            variant="ghost"
                            className="text-sm text-destructive hover:text-destructive"
                            onClick={() => setShowCancelDialog(true)}
                          >
                            Cancel subscription
                          </Button>
                        </div>
                      </div>
                    </div>
                  )}

                  {currentPlan?.status === "canceling" && (
                    <div className="pt-6 border-t">
                      <div className="flex items-center justify-between">
                        <div className="space-y-1">
                          <p className="text-sm text-muted-foreground">
                            Your subscription will end on{" "}
                            {subscription?.currentPeriodEnd
                              ? new Date(
                                subscription.currentPeriodEnd,
                              ).toLocaleDateString()
                              : "N/A"}
                          </p>
                          <p className="text-sm text-muted-foreground">
                            You can continue using all features until then.
                          </p>
                        </div>
                        <Button
                          variant="outline"
                          onClick={() =>
                            reactivateSubscription.mutateAsync({
                              orgId: params.orgId,
                            })
                          }
                          disabled={reactivateSubscription.status === "loading"}
                        >
                          {reactivateSubscription.status === "loading"
                            ? "Processing..."
                            : "Reactivate subscription"}
                        </Button>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </section>

          <div className="border-t" />

          <section>
            <div className="flex flex-col md:flex-row gap-12">
              <div className="w-full md:w-2/5">
                <h3 className="text-lg font-medium mb-1">Payment Methods</h3>
                <p className="text-sm text-muted-foreground">
                  Add or remove payment methods for your subscription
                </p>
              </div>

              <Card className="flex-1">
                <CardHeader className="flex flex-col md:flex-row items-start md:items-center justify-between">
                  <div>
                    <CardTitle>Payment Methods</CardTitle>
                    <CardDescription>
                      Manage your payment methods
                    </CardDescription>
                  </div>
                  <Button variant="outline" onClick={handleAddCard}>
                    <PlusIcon className="h-4 w-4 mr-2" />
                    Add new card
                  </Button>
                </CardHeader>
                <CardContent>
                  {paymentMethods && paymentMethods.length > 0 ? (
                    <RadioGroup
                      value={billingInfo?.defaultPaymentMethod || ""}
                      onValueChange={handleSetDefaultPaymentMethod}
                      className="space-y-4"
                    >
                      {paymentMethods.map((method) => (
                        <div
                          key={method.id}
                          className="flex items-center justify-between space-x-4 rounded-md border p-4"
                        >
                          <div className="flex items-center space-x-4">
                            <RadioGroupItem value={method.id} id={method.id} />
                            <div className="flex items-center space-x-4">
                              <CreditCard className="h-6 w-6 text-muted-foreground" />
                              <div>
                                <div className="text-sm font-medium">
                                  {method.card?.brand?.toUpperCase()} ••••{" "}
                                  {method.card?.last4}
                                </div>
                                <div className="text-sm text-muted-foreground">
                                  Expires {method.card?.exp_month}/
                                  {method.card?.exp_year}
                                </div>
                              </div>
                            </div>
                          </div>
                          {method.id !== billingInfo?.defaultPaymentMethod && (
                            <Button
                              variant="ghost"
                              size="sm"
                              className="text-destructive"
                              onClick={() =>
                                handleDeletePaymentMethod(method.id)
                              }
                              disabled={deletePaymentMethod.status === "loading"}
                            >
                              {deletePaymentMethod.status === "loading"
                                ? "Removing..."
                                : "Remove"}
                            </Button>
                          )}
                        </div>
                      ))}
                    </RadioGroup>
                  ) : (
                    <div className="text-center py-6">
                      <CreditCard className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                      <div className="text-sm text-muted-foreground">
                        No payment methods added yet
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </section>

          <div className="border-t" />

          <section>
            <div className="flex flex-col md:flex-row gap-12">
              <div className="w-full md:w-2/5">
                <h3 className="text-lg font-medium mb-1">Email Recipient</h3>
                <p className="text-sm text-muted-foreground">
                  The email address where all billing-related communications
                  will be sent, including invoices and payment notifications.
                </p>
              </div>

              <Card className="flex-1">
                <CardHeader>
                  <CardTitle>Email Recipient</CardTitle>
                  <CardDescription>
                    All billing correspondence will go to this email
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-col md:flex-row gap-4">
                    <Input
                      value={billingEmail}
                      onChange={(e) => setBillingEmail(e.target.value)}
                      placeholder="Billing email address"
                    />
                    <Button onClick={handleUpdateBilling} variant="outline">
                      Update
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </section>

          <div className="border-t" />

          <section>
            <div className="flex flex-col md:flex-row gap-12">
              <div className="w-full md:w-2/5">
                <h3 className="text-lg font-medium mb-1">Billing Address</h3>
                <p className="text-sm text-muted-foreground">
                  Your billing address will appear on your invoices and is used
                  to determine tax rates. Changes will apply to future invoices.
                </p>
              </div>

              <Card className="flex-1">
                <CardHeader>
                  <CardTitle>Billing Address</CardTitle>
                  <CardDescription>
                    This will be reflected in every upcoming invoice
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid gap-4">
                    <Input
                      value={billingAddress.line1}
                      onChange={(e) =>
                        setBillingAddress({
                          ...billingAddress,
                          line1: e.target.value,
                        })
                      }
                      placeholder="Address line 1"
                    />
                    <Input
                      value={billingAddress.line2}
                      onChange={(e) =>
                        setBillingAddress({
                          ...billingAddress,
                          line2: e.target.value,
                        })
                      }
                      placeholder="Address line 2"
                    />
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <Input
                        value={billingAddress.city}
                        onChange={(e) =>
                          setBillingAddress({
                            ...billingAddress,
                            city: e.target.value,
                          })
                        }
                        placeholder="City"
                      />
                      <Input
                        value={billingAddress.state}
                        onChange={(e) =>
                          setBillingAddress({
                            ...billingAddress,
                            state: e.target.value,
                          })
                        }
                        placeholder="State"
                      />
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <Input
                        value={billingAddress.postal_code}
                        onChange={(e) =>
                          setBillingAddress({
                            ...billingAddress,
                            postal_code: e.target.value,
                          })
                        }
                        placeholder="Postal code"
                      />
                      <Input
                        value={billingAddress.country}
                        onChange={(e) =>
                          setBillingAddress({
                            ...billingAddress,
                            country: e.target.value,
                          })
                        }
                        placeholder="Country"
                      />
                    </div>
                    <div className="flex justify-end">
                      <Button onClick={handleUpdateBilling}>
                        Save Address
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </section>

          <div className="border-t" />

          <section>
            <div className="flex flex-col md:flex-row gap-12">
              <div className="w-full md:w-2/5">
                <h3 className="text-lg font-medium mb-1">Tax ID</h3>
                <p className="text-sm text-muted-foreground">
                  Add your tax ID to have it included on your invoices. This
                  helps with tax compliance and reporting.
                </p>
              </div>

              <Card className="flex-1">
                <CardHeader>
                  <CardTitle>Tax ID</CardTitle>
                  <CardDescription>
                    Add a tax ID to your invoices
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <select
                    className="w-full bg-background border rounded-md p-2"
                    value={taxIdType}
                    onChange={(e) => setTaxIdType(e.target.value)}
                  >
                    <option value="">None</option>
                    <option value="vat">VAT ID</option>
                    <option value="gst">GST Number</option>
                  </select>

                  <div className="flex flex-col gap-2">
                    <Input
                      placeholder="Enter your tax ID number"
                      className="w-full"
                      value={taxIdNumber}
                      onChange={(e) => setTaxIdNumber(e.target.value)}
                    />
                    <div className="flex justify-end">
                      <Button onClick={handleUpdateTaxId}>Save Tax ID</Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </section>

          <div className="border-t" />

          <section>
            <div className="flex flex-col md:flex-row gap-12">
              <div className="w-full md:w-2/5">
                <h3 className="text-lg font-medium mb-1">Invoices</h3>
                <p className="text-sm text-muted-foreground">
                  View and download your past invoices
                </p>
              </div>

              <div className="flex-1">
                <div className="rounded-lg border">
                  <div className="grid grid-cols-1 md:grid-cols-1 md:grid-cols-[1fr,1fr,2fr,1fr,auto] gap-4 p-4 border-b text-sm text-muted-foreground">
                    <div className="hidden md:block">Date</div>
                    <div className="hidden md:block">Amount</div>
                    <div className="hidden md:block">Invoice number</div>
                    <div className="hidden md:block">Status</div>
                    <div className="hidden md:block"></div>
                    <div className="md:hidden font-medium">Invoices</div>
                  </div>

                  {invoices?.map((invoice) => (
                    <div
                      key={invoice.id}
                      className="grid grid-cols-1 md:grid-cols-[1fr,1fr,2fr,1fr,auto] gap-4 p-4 items-center hover:bg-muted/50"
                    >
                      <div className="flex items-center gap-2">
                        <FileIcon className="w-4 h-4 text-muted-foreground" />
                        <span className="md:hidden font-medium mr-2">
                          Date:
                        </span>
                        {
                          new Date(invoice.created * 1000)
                            .toISOString()
                            .split("T")[0]
                        }
                      </div>
                      <div>
                        <span className="md:hidden font-medium mr-2">
                          Amount:
                        </span>
                        ${(invoice.amount_paid / 100).toFixed(2)}
                      </div>
                      <div>
                        <span className="md:hidden font-medium mr-2">
                          Invoice:
                        </span>
                        {invoice.number}
                      </div>
                      <div>
                        <span className="md:hidden font-medium mr-2">
                          Status:
                        </span>
                        <span
                          className={cn(
                            "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",
                            invoice.status === "paid"
                              ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                              : "bg-yellow-50 text-yellow-700 border border-yellow-200",
                          )}
                        >
                          {(invoice.status || "pending")
                            .charAt(0)
                            .toUpperCase() +
                            (invoice.status || "pending").slice(1)}
                        </span>
                      </div>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() =>
                          invoice.invoice_pdf &&
                          window.open(invoice.invoice_pdf, "_blank")
                        }
                      >
                        <DownloadIcon className="w-4 h-4" />
                      </Button>
                    </div>
                  ))}

                  {invoices?.length === 0 && (
                    <div className="p-4 text-center text-sm text-muted-foreground">
                      No invoices found
                    </div>
                  )}
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>

      <Dialog open={showPaymentForm} onOpenChange={setShowPaymentForm}>
        <DialogTrigger asChild>
          {/* Trigger handled by handleAddCard */}
        </DialogTrigger>
        <DialogContent className="bg-background">
          <DialogHeader>
            <DialogTitle>Add Payment Method</DialogTitle>
            <DialogDescription>
              Add a new credit or debit card
            </DialogDescription>
          </DialogHeader>

          <Elements stripe={stripePromise}>
            <PaymentMethodForm
              orgId={params.orgId}
              onSuccess={() => {
                refreshAllResources();
                setShowPaymentForm(false);
                router.refresh();
              }}
              clientSecret={setupIntentSecret}
            />
          </Elements>
        </DialogContent>
      </Dialog>

      <Dialog open={showPlanSelection} onOpenChange={setShowPlanSelection}>
        <DialogContent className="max-w-4xl bg-background">
          <DialogHeader>
            <DialogTitle>Select a Plan</DialogTitle>
            <DialogDescription>
              Choose the plan that best fits your needs
            </DialogDescription>
          </DialogHeader>

          <PlanSelection
            plans={(plans || []) as any}
            selectedPlan={selectedPlan}
            onPlanSelect={setSelectedPlan}
            onConfirm={handleSubscribe}
            onCancel={() => setShowPlanSelection(false)}
            isLoading={createSubscription.status === "loading"}
            hasPaymentMethod={paymentMethods && paymentMethods.length > 0}
          />
        </DialogContent>
      </Dialog>

      <AlertDialog open={showCancelDialog} onOpenChange={setShowCancelDialog}>
        <AlertDialogContent className="bg-background">
          <AlertDialogHeader>
            <AlertDialogTitle>Cancel Subscription</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to cancel your subscription? You will lose
              access to premium features at the end of your current billing
              period.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
              onClick={() => {
                cancelSubscription.mutateAsync({
                  orgId: params.orgId,
                });
                setShowCancelDialog(false);
              }}
            >
              Continue
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}
