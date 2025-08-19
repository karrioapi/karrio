import { formatWeight, isNoneOrEmpty } from "@karrio/lib";
import { CommodityType } from "@karrio/types";
import React from "react";
import { cn } from "@karrio/ui/lib/utils";

interface CommodityDescriptionComponent extends React.HTMLAttributes<any> {
  commodity: CommodityType;
  prefix?: string;
  suffix?: string;
  comments?: string;
}

export const CommodityDescription = ({
  commodity,
  prefix,
  suffix,
  comments,
  className,
  ...props
}: CommodityDescriptionComponent): JSX.Element => {
  return (
    <div className={cn("flex", className)} {...props}>
      <div className="flex-grow p-0 truncate">
        <p className="text-xs my-1 font-semibold">
          {prefix} {`${commodity.title || commodity.description || "Item"}`}{" "}
          {suffix}
        </p>
        <p className="text-xs my-1 font-semibold text-muted-foreground">
          {isNoneOrEmpty(commodity.sku)
            ? " SKU: 0000000"
            : ` SKU: ${commodity.sku}`}
          {isNoneOrEmpty(commodity.hs_code)
            ? ""
            : ` | HS code: ${commodity.hs_code}`}
        </p>
      </div>

      <div
        className="flex-shrink-0 p-0 text-right"
        style={{ minWidth: "90px" }}
      >
        <p className="text-xs my-1 font-semibold">
          {commodity.quantity}
          {" x "}
          {formatWeight(commodity)}
        </p>
        <p className="text-xs my-1 font-semibold text-blue-600">
          {comments}
        </p>
      </div>
    </div>
  );
};