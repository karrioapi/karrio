import { formatCarrierSlug, getInitials, isNoneOrEmpty } from "@karrio/lib";
import { NextApiRequest, NextApiResponse } from "next";

async function ImageFallback(req: NextApiRequest, res: NextApiResponse) {
  const { name } = req.query as { name: string };
  const isIcon = name.includes('_icon');
  const [_name, ..._] = name.replace(isIcon ? "_icon" : "_logo", "").split(".");
  const carrier_name = (isIcon
    ? getInitials(_name).substring(0, 2)
    : formatCarrierSlug(_name)
  );
  const text_color = isNoneOrEmpty(req.query.text_color) ? "#ddd" : decodeURIComponent(req.query.text_color as string);
  const background = isNoneOrEmpty(req.query.background) ? "#7e51e1" : decodeURIComponent(req.query.background as string);
  const props = (isIcon ? 'viewBox="0 0 512 512"' : 'viewBox="0 0 125 25"');
  const path = (isIcon
    ? `<path xmlns="http://www.w3.org/2000/svg" style="fill-rule:evenodd;clip-rule:evenodd;fill:${background};" d="M512,472c0,22.1-17.9,40-40,40H40c-22.1,0-40-17.9-40-40V40C0,17.9,17.9,0,40,0h432c22.1,0,40,17.9,40,40V472z"/>`
    : `<path xmlns="http://www.w3.org/2000/svg" style="fill-rule:evenodd;clip-rule:evenodd;fill:${background};" d="M125,0v25H0V0H125z"/>`
  );

  const content = `<svg ${props} x="0px" y="0px" xmlns="http://www.w3.org/2000/svg">
    <g>
      ${path}

      <text x="50%" y="55%" alignment-baseline="middle" text-anchor="middle" fill="${text_color}" font-weight="bold" font-family="arial"
        font-size="${isIcon ? '16em' : '.95em'}" style="text-transform: uppercase; ${isIcon ? 'border-radius: 40px;' : '4px'}">
        ${carrier_name}
      </text>
    </g>
  </svg>
  `;

  res.setHeader('Content-Type', 'image/svg+xml');
  res.status(302);
  res.send(content);
}

export default ImageFallback;
