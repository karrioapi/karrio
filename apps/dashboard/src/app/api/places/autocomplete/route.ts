import axios from 'axios';
import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@karrio/core/context/auth';
import { ADDRESS_AUTO_COMPLETE_SERVICE_KEY, ADDRESS_AUTO_COMPLETE_SERVICE } from '@karrio/lib';

export async function GET(req: NextRequest) {
  // The key is the deployment's Google quota: only signed-in users may spend it.
  const session = await auth();
  if (!session || (session as any).error === 'RefreshAccessTokenError') {
    return NextResponse.json({ error: 'Authentication required.' }, { status: 401 });
  }

  const { searchParams } = new URL(req.url);
  const input = searchParams.get('input');
  const country = searchParams.get('country');
  const sessiontoken = searchParams.get('sessiontoken');
  const key = ADDRESS_AUTO_COMPLETE_SERVICE === "google" ? ADDRESS_AUTO_COMPLETE_SERVICE_KEY : undefined;
  console.log('[Autocomplete] input:', input);
  console.log('[Autocomplete] country:', country);
  console.log('[Autocomplete] sessiontoken:', sessiontoken);
  if (!input || !key) {
    return NextResponse.json({ error: 'Missing required parameters or API key.' }, { status: 400 });
  }

  try {
    const params: Record<string, string> = {
      input,
      key,
    };
    if (country) params.components = `country:${country}`;
    if (sessiontoken) params.sessiontoken = sessiontoken;

    const response = await axios.get('https://maps.googleapis.com/maps/api/place/autocomplete/json', { params });
    return NextResponse.json(response.data);
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
