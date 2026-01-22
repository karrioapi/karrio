import { formatWeight, isNoneOrEmpty } from "@karrio/lib";
import { CommodityType, CustomsCommodityType } from "@karrio/types";
import React from "react";
import { cn } from "@karrio/ui/lib/utils";

interface CommodityDescriptionComponent extends React.HTMLAttributes<any> {
  commodity: CommodityType | CustomsCommodityType;
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
    <div className={cn("flex items-center", className)} {...props}>
      <div className="flex-1 min-w-0 p-0">
        <p className="text-xs my-1 font-semibold truncate">
          {prefix} {`${"title" in commodity ? (commodity.title || commodity.description || "Item") : (commodity.description || "Item")}`}{" "}
          {suffix}
        </p>
        <p className="text-xs my-1 font-semibold text-muted-foreground truncate">
          {isNoneOrEmpty(commodity.sku)
            ? " SKU: 0000000"
            : ` SKU: ${commodity.sku}`}
          {isNoneOrEmpty(commodity.hs_code)
            ? ""
            : ` | HS code: ${commodity.hs_code}`}
        </p>
      </div>

      <div className="flex-shrink-0 p-0 text-right ml-2 min-w-fit">
        <p className="text-xs my-1 font-semibold whitespace-nowrap">
          {commodity.quantity}
          {" x "}
          {formatWeight(commodity)}
        </p>
        <p className="text-xs my-1 font-semibold text-blue-600 truncate">
          {comments}
        </p>
      </div>
    </div>
  );
};