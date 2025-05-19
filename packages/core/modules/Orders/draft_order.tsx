"use client";
import {
  CommodityEditModalProvider,
  CommodityStateContext,
} from "@karrio/ui/core/modals/commodity-edit-modal";
import {
  MetadataEditor,
  MetadataEditorContext,
} from "@karrio/ui/core/forms/metadata-editor";
import { GoogleGeocodingScript } from "@karrio/ui/core/components/google-geocoding-script";
import { CommodityDescription } from "@karrio/ui/core/components/commodity-description";
import { AddressDescription } from "@karrio/ui/core/components/address-description";
import { formatRef, isEqual, isNone, isNoneOrEmpty } from "@karrio/lib";
import { MetadataObjectTypeEnum, PaidByEnum } from "@karrio/types";
import { AddressModalEditor } from "@karrio/ui/core/modals/form-modals";
import { InputField } from "@karrio/ui/core/components/input-field";
import { useLoader } from "@karrio/ui/core/components/loader";
import { ModalProvider } from "@karrio/ui/core/modals/modal";
import { bundleContexts } from "@karrio/hooks/utils";
import { useOrderForm } from "@karrio/hooks/order";
import React, { useEffect, useState } from "react";
import { Spinner } from "@karrio/ui/core/components";
import { AddressType } from "@karrio/types";

const ContextProviders = bundleContexts([
  CommodityEditModalProvider,
  ModalProvider,
]);

export default function Page({ params }: { params: Promise<{ id: string }> }) {
  const Component = (): JSX.Element => {
    const [id, setId] = React.useState<string>();

    React.useEffect(() => {
      params.then(query => {
        setId(query.id);
      });
    }, []);

    if (!id) return <></>;

    return (
      <>
        <DraftOrderComponent orderId={id} />
      </>
    );
  };

  return <Component />;
}
