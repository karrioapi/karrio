import { AddressType, CustomsType, ParcelType, PresetCollection, RequestError } from "@/library/types";


export function formatRef(s: string): string {
    return s.replaceAll('_', ' ').toLocaleUpperCase();
}

export function formatDate(date: string): string {
    let [month, day, year] = (new Date(date)).toLocaleDateString().split("/");
    return `${day}/${month}/${year}`;
}

export function formatDateTime(date_string: string): string {
    const date = new Date(date_string);
    let [hour, minute, second] = date.toLocaleTimeString().split(/:| /);
    return `${formatDate(date_string)}, ${hour}:${minute}:${second}`;
}

export function notEmptyJSON(value?: string | null): boolean {
    return !isNone(value) && value !== JSON.stringify({});
}

export function formatAddress(address: AddressType): string {
    return [
        address.person_name,
        address.city,
        address.postal_code,
        address.country_code
    ].filter(a => !isNone(a) && a !== "").join(', ');
}

export function formatFullAddress(address: AddressType, countries?: { [country_code: string]: string }): string {
    const country = countries === undefined ? address.country_code : countries[address.country_code];
    return [
        address.address_line1,
        address.city,
        address.state_code,
        address.postal_code,
        country
    ].filter(a => !isNone(a) && a !== "").join(', ');
}

export function formatAddressName(address: AddressType): string {
    return [
        address.person_name,
        address.company_name
    ].filter(a => !isNone(a) && a !== "").join(' - ');
}

export function formatCustomsLabel(customs: CustomsType): string {
    return [
        customs.content_type,
        customs.incoterm
    ]
        .filter(c => !isNone(c))
        .map(c => formatRef('' + c)).join(' - ');
}

export function findPreset(presets: PresetCollection, package_preset?: string): Partial<ParcelType> | undefined {
    const carrier = Object.values(presets).find((carrier) => {
        return Object.keys(carrier).includes(package_preset as string);
    });

    if (carrier === undefined) return undefined;

    return { ...carrier[package_preset as string], package_preset };
}

export function formatValues(separator: string, ...args: any[]): string {
    return args.filter(d => d !== undefined).join(separator);
}

export function formatDimension(parcel?: Partial<ParcelType>): string {
    if (parcel !== undefined) {

        const { dimension_unit, height, length, width } = parcel;
        let formatted = formatValues(' x ', width, height, length);

        return `Dimensions: ${formatted} ${dimension_unit}`;
    }
    return 'Dimensions: None specified...';
}

export function formatWeight(parcel?: Partial<ParcelType>): string {
    if (parcel !== undefined) {

        const { weight, weight_unit } = parcel;

        return `Weight: ${weight} ${weight_unit}`;
    }
    return 'Weight: None specified...';
}

export function isNone(value: any): boolean {
    return value === null || value === undefined;
}

export function deepEqual(value1?: object | null, value2?: object | null): boolean {
    return JSON.stringify(value1, Object.keys(value1 || {}).sort()) === JSON.stringify(value2, Object.keys(value2 || {}).sort());
}

// Remove undefined values from objects
export function cleanDict<T = object>(value: object): T {
    return JSON.parse(JSON.stringify(value)) as T;
}

export function formatParcelLabel(parcel?: ParcelType): string {
    if (isNone(parcel) || (parcel && isNone(parcel?.package_preset) && isNone(parcel?.packaging_type))) {
        return '';
    }
    if (!isNone(parcel?.package_preset)) {
        return formatRef(parcel?.package_preset as string);
    }
    else if (!isNone(parcel?.packaging_type)) {
        return formatRef(parcel?.packaging_type as string);
    }
    return '';
}


export const COUNTRY_WITH_POSTAL_CODE = [
    'CA', 'US', 'UK', 'FR', //TODO:: Add more countries with postal code here.
];

export function getCookie(name: string): string {
    var cookieValue = "";
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export async function handleFailure<T>(request: Promise<T>): Promise<T> {
    try {
        const response = await request;
        return response
    } catch (err) {
        if (err.message === 'Failed to fetch') {
            throw new Error('Oups! Looks like you are offline');
        } else if (err instanceof Response) {
            throw new RequestError(await err.json());
        }
        throw err
    }
}


export function getCursorPagination(cursor?: string): { limit?: number; offset?: number; } {
    const [_, queryString] = (cursor || '').split('?');
    const params = (queryString || '').split('&');
  
    const [_limit, limit] = (params.find(p => p.includes('limit')) || '').split('=');
    const [_offset, offset] = (params.find(p => p.includes('offset')) || '').split('=');
  
    return { 
      ...(limit === undefined ? {} : { limit: parseInt(limit) }),
      ...(offset === undefined ? {} : { offset: parseInt(offset) })
     };
  }
