import React from "react";
import styles from "./styles.module.css";

const references = require("./references.json");

const CarrierIntegrationDetails = ({ children, id, integration = {} }) => {

  return (
    <div id="tailwind">
      <div className="my-8 text-slate-700 font-semibold" style={{ fontSize: "1.1em" }}>{integration.description}</div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-1 lg:mr-8">
        <div
          className="group rounded p-2 border border-slate-300 no-underline"
          style={{ color: "var(--ifm-font-color-base)" }}
        >

          <div className="flex justify-between">
            <div className="text-base font-semibold ">Capabilities</div>
          </div>
          <hr className="my-2" />
          {integration.features.map((feature, index) => (
            <div
              key={index}
              className="px-0 text-sm mt-2 rounded-sm flex justify-between"
            >
              <div>{feature}</div>
            </div>
          ))}

        </div>
      </div>

    </div>
  )
};

export default CarrierIntegrationDetails;
