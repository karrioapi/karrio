import React from "react";
import Image from "next/image";

interface CarrierNetworkProps {
  width?: number;
  height?: number;
}

export const CarrierNetwork = ({
  width = 1200,
  height = 1200,
}: CarrierNetworkProps) => {
  const svgString =
    encodeURIComponent(`<svg width="${width}" height="${height}" viewBox="0 0 1200 1200" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="1200" height="1200" fill="none" rx="3" />

    {/* Form Container - centered */}
    <g transform="translate(80, 160)">
      {/* Form Card Background */}
      <rect x="0" y="0" width="900" height="840" rx="24" fill="white" stroke="#D9DEE7" stroke-width="2" />

      {/* Form Title */}
      <text x="110" y="80" style="font-size: 42px; font-weight: 600;" fill="#19212E">Edit Carrier Connection</text>

      {/* Carrier Selector */}
      <g transform="translate(110, 120)">
        <rect width="680" height="70" rx="12" fill="white" stroke="#8C95A6" stroke-width="1.5" />
        <text x="24" y="44" style="font-size: 24px;" fill="#374151">DHL Express</text>
      </g>

      {/* Form Fields */}
      ${[
        { label: "Carrier ID", required: true },
        { label: "Site ID", required: true },
        { label: "Account Number", required: true },
      ]
        .map(
          (field, index) => `
        <g transform="translate(110, ${240 + index * 140})">
          <text x="0" y="0" style="font-size: 24px;" fill="#66758F">
            ${field.label}${field.required ? `<tspan fill="#EF4444">*</tspan>` : ""}
          </text>
          <rect x="0" y="20" width="680" height="70" rx="12" fill="white" stroke="#8C95A6" stroke-width="1.5" />
        </g>
      `,
        )
        .join("")}

      {/* Submit Button */}
      <g transform="translate(110, 700)">
        <rect width="680" height="70" rx="12" fill="#006CFA" />
        <text x="340" y="44" style="font-size: 24px; text-anchor: middle; font-weight: 500;" fill="white">Connect</text>
      </g>
    </g>

    {/* Carrier Logos Container - aligned horizontally */}
    <g transform="translate(920, 230)">
      {/* DHL Logo */}
      <g transform="translate(0, 0)">
        <path fill="#FDCA2E" d="M512 472c0 22.1-17.9 40-40 40H40c-22.1 0-40-17.9-40-40V40C0 17.9 17.9 0 40 0h432c22.1 0 40 17.9 40 40v432z" transform="scale(0.4)" />
        <path fill="#D0131D" d="M198.9 268.2c4.5-9.1 8.3-17 10-20.4 8.1-16.3-.3-39.1-28.3-39.1h-92L72.7 241h85.8c6.7 0 9.1 1.4 7.1 5.6-2 4.1-6.2 12.7-7.4 15.1-1.4 2.9-2.1 6.5 2.4 6.5h38.3z M141.6 271.3c-4.5 0-4.9-3-3.8-5.3.9-1.9 6.9-14.1 8.1-16.4 1.4-2.9 1-5.9-5.9-5.9h-38.9l-29.3 59.6H149c21.1 0 36.4-7.6 46.9-28.9.5-1 1-2.1 1.5-3.1h-55.8z M206.3 271.3l-15.7 32h47.9l15.8-32h-48z M273.7 271.3l-15.7 32h47.9l15.8-32h-48z M323.2 268.2l29.2-59.5h-47.9L288.7 241h-19.6l15.9-32.3h-48l-29.1 59.5h115.3z M364.6 208.7h48l-29.3 59.5h-47.9l29.2-59.5z M333.9 271.3h107.3l-15.7 32h-79.1c-16.5 0-21.8-12.6-15.9-24.8.5-1.4 3.4-7.2 3.4-7.2z M80 271.3l-4.6 9.4H0v-9.4h80z M74.5 282.5l-4.7 9.5H0v-9.5h74.5z M68.9 293.9l-4.7 9.4H0v-9.4h68.9z M512 280.7h-68.8l4.6-9.4H512z M512 292h-74.4l4.6-9.5H512z M512 303.3h-80l4.7-9.4H512z" transform="scale(0.4)" />
      </g>

      {/* UPS Logo */}
      <g transform="translate(0, 250)">
        <path class="st0" d="M461.3,512H50.7C22.7,512,0,489.3,0,461.3V50.7C0,22.7,22.7,0,50.7,0h410.6c28,0,50.7,22.7,50.7,50.7v410.6 C512,489.3,489.3,512,461.3,512z" fill="#341B14" transform="scale(0.4)" />
        <path class="st0" d="M256,446.2c3.3-1.7,89.3-38.9,116.6-61.2c28.1-23.1,43-56.2,43-95.9v-186l-2.5-0.8 c-68.6-37.2-153.8-34.7-157.9-34.7c-3.3,0-88.4-2.5-157.1,34.7l-1.7,0.8v186.8c0,39.7,14.9,72.7,43,95.9 C166.7,408.1,252.7,445.3,256,446.2" fill="#341B14" transform="scale(0.4)" />
        <path class="st1" d="M256,450.3c0,0-90.9-39.7-119-62c-29.8-24.8-43.8-58.7-43.8-97.5V97.3C165.1,58.5,256,61.8,256,61.8 s90.9-3.3,162.8,35.5v192.6c0,38.9-14.1,72.7-43.8,97.5C346.9,410.6,256,450.3,256,450.3 M106.4,290.8c0,36.4,13.2,66.1,38.9,86.8 c23.1,19,91.8,49.6,110.8,57.9c19-8.3,88.4-39.7,110.8-57.9c25.6-20.7,38.9-51.3,38.9-86.8V100.6c-95.9-9.1-210-4.1-299.2,78.5 L106.4,290.8L106.4,290.8z" fill="#FFB406" transform="scale(0.4)" />
        <path class="st1" d="M347.8,263.5c12.4,7.4,17.4,12.4,18.2,21.5c0,9.9-6.6,15.7-17.4,15.7c-9.1,0-19.8-5-27.3-11.6v26.5 c9.1,5,19.8,9.1,31.4,9.1c28.1,0,41.3-19.8,41.3-38c0.8-16.5-4.1-29.8-28.1-43.8c-10.7-6.6-19-10.7-19-20.7s9.1-14.1,16.5-14.1 c9.9,0,19.8,5.8,25.6,11.6v-24.8c-5-4.1-15.7-9.9-31.4-9.1c-19,0.8-38.9,14.1-38.9,37.2C319.7,238.7,324.6,250.2,347.8,263.5 M250.2,323c2.5,0.8,6.6,1.7,13.2,1.7c32.2,0,50.4-28.9,50.4-70.3c0-42.2-19-67.8-52.9-67.8c-15.7,0-28.1,3.3-38.9,9.9v186.8h28.1 V323L250.2,323z M250.2,210.6c2.5-0.8,6.6-2.5,9.9-2.5c16.5,0,23.1,13.2,23.1,45.5c0,31.4-8.3,46.3-24.8,46.3 c-4.1,0-7.4-0.8-9.1-1.7v-87.6H250.2z M163.4,324.6c17.4,0,32.2-4.1,43-11.6V188.3h-28.9v108.3c-3.3,2.5-7.4,3.3-13.2,3.3 c-13.2,0-14.9-12.4-14.9-19.8v-91.8h-28.9v90.1C120.4,308.9,135.3,324.6,163.4,324.6" fill="#FFB406" transform="scale(0.4)" />
      </g>

      {/* USPS Logo */}
      <g transform="translate(0, 500)">
        <path fill="#336" d="M512 472c0 22.1-17.9 40-40 40H40c-22.1 0-40-17.9-40-40V40C0 17.9 17.9 0 40 0h432c22.1 0 40 17.9 40 40v432z" transform="scale(0.4)" />
        <path fill="#FFF" d="M404 383.8l54.4-255.6H102.6L48.3 383.8z" transform="scale(0.4)" />
        <path fill="#336" d="M110 138.3s197.8 40.6 201.7 41.3c45.4 8 44 16.8 44 16.8 31.8-.2 35.8 1.1 41.3 5.8 16.7 14-10.5 55.2-10.5 55.2-3.9 2.9-298.2 116.5-298.2 116.5h307.9l50.3-236.7H110v1.1" transform="scale(0.4)" />
        <path fill="#336" d="M340.3 215c-4.5 2.2-16.1 3.4-21.6 3.9-5.3.4-6.7 1-6.8 3-.1 1.8.8 2.8 8.3 2.8 17.3 0 48.4-6.5 57.8-3.5 5 1.6 1 10.4-3.1 22-1.6 4.5 1.5 4.2 3.3 2.2 1.8-2 9.9-16.7 10.8-24.3 1.2-10.7-7.9-12.3-20.6-12.3h-20.1c-1.1 0-1.9.7-3.2 2.4-1 1.4-1.9 2.3-4.8 3.8" transform="scale(0.4)" />
        <path fill="#336" d="M98.6 191.9L60 373.9s118.4-58.1 132.8-65.5c29.7-15.2 70.7-35.4 108.6-48.3 7.2-2.5 38.2-12 56.2-15.2 7-1.3 9.9-2.4 9.9-3.8-.3-3.7-7.3-4-19.2-3.4-36.3 1.7-105.8 29.4-125.8 39.9l-22.6-70h144.4c6.5-18.2-85.5-15.6-88.3-15.8H98.6v.1" transform="scale(0.4)" />
      </g>
    </g>
  </svg>`);

  return (
    <Image
      src={`data:image/svg+xml,${svgString}`}
      alt="Carrier Network Interface"
      width={width}
      height={height}
      priority
    />
  );
};

export default CarrierNetwork;
