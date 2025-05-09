import axios from 'axios';
import { NextRequest, NextResponse } from 'next/server';
import { ADDRESS_AUTO_COMPLETE_SERVICE_KEY, ADDRESS_AUTO_COMPLETE_SERVICE } from '@karrio/lib';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const place_id = searchParams.get('place_id');
  const sessiontoken = searchParams.get('sessiontoken');
  const key = ADDRESS_AUTO_COMPLETE_SERVICE === "google" ? ADDRESS_AUTO_COMPLETE_SERVICE_KEY : undefined;

  if (!place_id || !key) {
    return NextResponse.json({ error: 'Missing required parameters or API key.' }, { status: 400 });
  }

  try {
    const params: Record<string, string> = {
      place_id,
      key,
      fields: 'address_component,formatted_address,geometry,name,place_id',
    };
    if (sessiontoken) params.sessiontoken = sessiontoken;

    const response = await axios.get('https://maps.googleapis.com/maps/api/place/details/json', { params });
    return NextResponse.json(response.data);
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
