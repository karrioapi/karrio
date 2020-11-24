import { Address, Parcel } from "@purplship/purplship";
import { PresetCollection } from "@/library/types";


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
    return value !== undefined && value !== undefined && value !== JSON.stringify({});
}

export function formatAddress(address: Address): string {
    return [
        address.person_name,
        address.city,
        address.postal_code,
        address.country_code
    ].filter(a => a !== undefined && a !== "").join(', ');
}

export function formatFullAddress(address: Address, countries?: { [country_code: string]: string }): string {
    const country = countries === undefined ? address.country_code : countries[address.country_code];
    return [
        address.address_line1,
        address.city,
        address.state_code,
        address.postal_code,
        country
    ].filter(a => a !== undefined && a !== "").join(', ');
}

export function formatAddressName(address: Address): string {
    return [
        address.person_name,
        address.company_name
    ].filter(a => a !== undefined && a !== "").join(' - ');
}

export function findPreset(presets: PresetCollection, selected_preset?: string): Partial<Parcel> | undefined {
    const carrier = Object.values(presets).find((carrier) => {
        return Object.keys(carrier).includes(selected_preset as string);
    });

    if (carrier === undefined) return undefined;

    return carrier[selected_preset as string];
}

export function formatValues(separator: string, ...args: any[]): string {
    return args.filter(d => d !== undefined).join(separator);
}

export function formatDimension(parcel?: Partial<Parcel>): string {
    if (parcel !== undefined) {

        const { dimension_unit, height, length, width } = parcel;
        let formatted = formatValues(' x ', width, height, length);

        return `Dimensions: ${formatted} ${dimension_unit}`;
    }
    return 'Dimensions: No specified...';
}

export function formatWeight(parcel?: Partial<Parcel>): string {
    if (parcel !== undefined) {

        const { weight, weight_unit } = parcel;

        return `Weight: ${weight} ${weight_unit}`;
    }
    return 'Weight: Not specified...';
}
