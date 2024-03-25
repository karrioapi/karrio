import React from "react";
import styles from "./styles.module.css";

const references = require("./references.json");

const CarrierIntegrationDetails = ({ children, id, integration = {} }) => {
  const services = references.services[id];
  const options = references.options[id];

  return (
    <div id="tailwind">

      {/* Overview */}
      <div className="group rounded p-0" style={{ color: "var(--ifm-font-color-base)" }}>
        <div className="flex px-1">
          <div className="text-xl font-semibold text-slate-700">Overview</div>
          <code className="text-sm font-light px-3 my-1">{integration.status}</code>
        </div>

        <table className="table-fixed">
          <tbody>

            <tr>
              <td>Website</td>
              <td>{integration.website}</td>
            </tr>
            <tr>
              <td>Documentation</td>
              <td>{integration.docs}</td>
            </tr>
            <tr>
              <td>Supported Capabilities</td>
              <td>
                <ul class="list-disc list-inside">

                  {integration.features.map((feature, index) => (
                    <li key={index}>{feature}</li>
                  ))}

                </ul>
              </td>
            </tr>

          </tbody>
        </table>
      </div>

      <div className="my-8 text-slate-700 font-semibold" style={{ fontSize: "1.1em" }}>{integration.description}</div>

      <hr className="my-8" style={{}} />

      {/* Environments */}
      {/* <h2 className="text-xl font-semibold text-slate-700 mt-8 mb-6">Environments</h2> */}


      {/* Shipping Services */}
      {!!services && <>
        <h2 className="text-xl font-semibold text-slate-700 mt-8 mb-6">Shipping Services</h2>

        <table className="table-fixed">
          <thead>
            <tr>
              <th className="text-start">API code</th>
              <th>Carrier code</th>
            </tr>
          </thead>
          <tbody>

            {Object.entries(services).map(([code, name], index) => (
              <tr key={index}>
                <td>{code}</td>
                <td>{name}</td>
              </tr>
            ))}

          </tbody>
        </table>
      </>}


      {/* Shipping Options */}
      {!!options && <>
        <h2 className="text-xl font-semibold text-slate-700 mt-8 mb-6">Shipping Options</h2>

        <table className="table-fixed">
          <thead>
            <tr>
              <th className="text-start">API code</th>
              <th>Carrier code</th>
              <th>Type</th>
            </tr>
          </thead>
          <tbody>

            {Object.entries(options).map(([code, option], index) => (
              <tr key={index}>
                <td>{code}</td>
                <td>{option.code}</td>
                <td>{option.type}</td>
              </tr>
            ))}

          </tbody>
        </table>
      </>}

    </div>
  )
};

export default CarrierIntegrationDetails;
