import {
  formatCustomsLabel,
  formatRef,
  isNone,
  isNoneOrEmpty,
} from "@karrio/lib";
import { CustomsType } from "@karrio/types";
import React from "react";

interface CustomsInfoDescriptionComponent {
  customs: CustomsType;
}

export const CustomsInfoDescription = ({
  customs,
}: CustomsInfoDescriptionComponent): JSX.Element => {
  return (
    <>
      <p className="text-xs my-1 font-semibold">
        {formatCustomsLabel(customs)}
      </p>

      {Object.entries(customs.options || {}).map(([key, value]: any, index) => (
        <React.Fragment key={index + "option-info"}>
          {!isNoneOrEmpty(value) && (
            <p className="text-xs my-1 font-semibold text-muted-foreground">
              <span>
                {formatRef(key).toLowerCase()}: <strong>{String(value)}</strong>
              </span>
            </p>
          )}
        </React.Fragment>
      ))}

      <p className="text-xs my-1 font-semibold text-muted-foreground">
        {isNone(customs?.invoice) ? (
          ""
        ) : (
          <span>
            Invoice Number: <strong>{customs.invoice}</strong>
          </span>
        )}
      </p>
      <p className="text-xs my-1 font-semibold text-muted-foreground">
        {isNone(customs?.invoice_date) ? (
          ""
        ) : (
          <span>
            Invoice Date: <strong>{customs.invoice_date}</strong>
          </span>
        )}
      </p>
      <p className="text-xs my-1 font-semibold text-muted-foreground">
        {!customs?.signer ? (
          ""
        ) : (
          <span>
            {customs?.certify && `Certified and `}Signed By{" "}
            <strong>{customs.signer}</strong>
          </span>
        )}
      </p>
      <p className="text-xs my-1 font-semibold text-muted-foreground">
        {isNone(customs?.content_description) ? (
          ""
        ) : (
          <span>
            <strong>Content:</strong> {customs.content_description}
          </span>
        )}
      </p>

      {/* Options section */}
      {Object.values((customs.duty as object) || {}).length > 0 && (
        <div className="py-1">
          <p className="text-xs my-2 font-semibold">
            DUTIES
          </p>

          {Object.entries(customs.duty || {}).map(
            ([key, value]: any, index) => (
              <React.Fragment key={index + "option-info"}>
                {!isNoneOrEmpty(value) && (
                  <p className="text-xs my-1 font-semibold text-muted-foreground">
                    <span>
                      {formatRef(key).toLowerCase()}:{" "}
                      <strong>{formatRef(String(value))}</strong>
                    </span>
                  </p>
                )}
              </React.Fragment>
            ),
          )}
        </div>
      )}
    </>
  );
};