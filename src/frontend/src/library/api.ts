import { CarrierSettings, References, Shipment, Purplship, Address, Parcel, Customs } from '@purplship/purplship';
import { useEffect, useState } from 'react';
import { Subject, BehaviorSubject } from 'rxjs';
import { distinct } from 'rxjs/operators';
import { RequestError } from '@/library/types';

// Collect API token from the web page
const INITIAL_TOKEN = collectToken();
const DEFAULT_LABEL_DATA = {
    shipment: {
        shipper: {} as Address,
        recipient: {} as Address,
        parcels: [] as Parcel[],
        options: {}
    } as Shipment
};
const DEFAULT_PAGINATED_RESULT = {
    count: 0,
    url: null,
    next: null,
    previous: null,
    results: [],
    fetched: false,
};

export interface UserInfo {
    full_name: string | null;
    email: string | null;
    readonly is_staff: boolean;
}

export interface Connection extends Omit<CarrierSettings, 'id' | 'carrier_name'> {
    id: string | null | undefined;
    carrier_name: CarrierSettings.CarrierNameEnum | 'none';
    [property: string]: any;
}

export interface ConnectionData {
    carrier_name: CarrierSettings.CarrierNameEnum;
    carrier_config: Partial<Connection>;
}

export interface Log {
    id: string;
    requested_at: string;
    response_ms: string;
    path: string;
    view: string;
    view_method: string;
    remote_addr: string;
    host: string;
    method: string;
    query_params: string;
    data: string;
    response: string;
    status_code: string;
}

export interface Template {
    id?: string;
    label?: string;
    address?: Address;
    customs?: Customs;
    parcel?: Parcel;
}

interface PaginatedContent<T> {
    count: Number;
    url?: string | null;
    next?: string | null;
    previous?: string | null;
    results: T[];
    fetched?: boolean;
}

export interface PaginatedLogs extends PaginatedContent<Log> { }
export interface PaginatedShipments extends PaginatedContent<Shipment> { }
export interface PaginatedTemplates extends PaginatedContent<Template> { }
export interface PaginatedConnections extends PaginatedContent<Connection> { }


export enum NotificationType {
    error = "is-danger",
    warning = "is-warning",
    info = "is-info",
    success = "is-success"
}

export interface Notification {
    type: NotificationType;
    message: string | Error | RequestError;
}

export interface LabelData {
    shipment: Shipment;
}

class AppState {
    private token$: BehaviorSubject<string> = new BehaviorSubject<string>(INITIAL_TOKEN);
    private user$: BehaviorSubject<UserInfo> = new BehaviorSubject<UserInfo>({} as UserInfo);
    private shipments$: Subject<PaginatedShipments> = new Subject<PaginatedShipments>();
    private parcels$: Subject<PaginatedTemplates> = new Subject<PaginatedTemplates>();
    private addresses$: Subject<PaginatedTemplates> = new Subject<PaginatedTemplates>();
    private connections$: Subject<PaginatedConnections> = new Subject<PaginatedConnections>();
    private customsInfos$: Subject<PaginatedTemplates> = new Subject<PaginatedTemplates>();
    private references$: Subject<References> = new Subject<References>();
    private logs$: Subject<PaginatedLogs> = new Subject<PaginatedLogs>();
    private notification$: Subject<Notification> = new Subject<Notification>();
    public labelData$: BehaviorSubject<LabelData> = new BehaviorSubject<LabelData>(DEFAULT_LABEL_DATA);

    constructor() {
        this.getUserInfo();
        this.fetchReferences();
    }

    private get headers() {
        return {
            "Content-Type": "application/json",
            'Accept': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    }

    private get purplship(): Purplship {
        return new Purplship(this.token$.value, '/v1');
    }

    public get token() {
        const [token, setValue] = useState<string>(this.token$.value);
        useEffect(() => { this.token$.asObservable().pipe(distinct()).subscribe(setValue); });
        return token;
    }

    public get user() {
        const [user, setValue] = useState<UserInfo>({} as UserInfo);
        useEffect(() => { this.user$.asObservable().pipe(distinct()).subscribe(setValue); });
        return user;
    }

    public get shipments() {
        const [shipments, setValue] = useState<PaginatedShipments>();
        useEffect(() => { this.shipments$.asObservable().pipe(distinct()).subscribe(setValue); });
        return shipments;
    }

    public get connections() {
        const [connections, setValue] = useState<PaginatedConnections>();
        useEffect(() => { this.connections$.asObservable().pipe(distinct()).subscribe(setValue); });
        return connections;
    }

    public get addresses() {
        const [addresses, setValue] = useState<PaginatedTemplates>();
        useEffect(() => { this.addresses$.asObservable().pipe(distinct()).subscribe(setValue); });
        return addresses;
    }

    public get parcels() {
        const [parcels, setValue] = useState<PaginatedTemplates>();
        useEffect(() => { this.parcels$.asObservable().pipe(distinct()).subscribe(setValue); });
        return parcels;
    }

    public get customsInfos() {
        const [customsInfos, setValue] = useState<PaginatedTemplates>();
        useEffect(() => { this.customsInfos$.asObservable().pipe(distinct()).subscribe(setValue); });
        return customsInfos;
    }

    public get references() {
        const [references, setValue] = useState<References>();
        useEffect(() => { this.references$.asObservable().subscribe(setValue); });
        return references;
    }

    public get logs() {
        const [logs, setValue] = useState<PaginatedLogs>();
        useEffect(() => { this.logs$.asObservable().subscribe(setValue); });
        return logs;
    }

    public get notification() {
        const [notification, setValue] = useState<Notification>();
        useEffect(() => { this.notification$.asObservable().subscribe(setValue); });
        return notification;
    }

    public get labelData() {
        const [labelData, setValue] = useState<LabelData>(this.labelData$.value);
        useEffect(() => { this.labelData$.asObservable().pipe(distinct()).subscribe(setValue); });
        return labelData;
    }

    private async fetchReferences() {
        const references = await this.purplship.utils.references();
        this.references$.next(references);
        return references;
    }

    public async retrieveShipment(shipment_id: string) {
        return handleFailure(
            this.purplship.shipments.retrieve(shipment_id)
        );
    }

    public async fetchRates(shipment: Shipment) {
        return handleFailure((async () => {
            if (shipment.id !== undefined) {
                const response = await this.purplship.shipments.rates(shipment.id, { headers: this.headers });
                return response.shipment as Shipment;
            } else {
                return this.purplship.shipments.create(shipment, { headers: this.headers });
            }
        })());
    }

    public async buyLabel(shipment: Shipment) {
        const response = handleFailure(
            this.purplship.shipments.purchase(
                { selected_rate_id: shipment.selected_rate_id as string, payment: shipment.payment, label_type: shipment.label_type },
                shipment.id as string,
                { headers: this.headers }
            )
        );
        response.then(() => this.shipments$.next(DEFAULT_PAGINATED_RESULT as any));
        return response;
    }

    public async voidLabel(shipment: Shipment) {
        const response = handleFailure(
            this.purplship.shipments.cancel(shipment.id as string, { headers: this.headers })
        );
        response.then(() => this.fetchShipments());
        return response;
    }

    public async setOptions(shipment_id: string, options: {}) {
        const response = handleFailure(
            this.purplship.shipments.setOptions(options, shipment_id, { headers: this.headers })
        );
        response.then(() => this.shipments$.next(DEFAULT_PAGINATED_RESULT as any));
        return response;
    }

    public async saveAddress(address: Address) {
        const response = handleFailure(
            this.purplship.addresses.create(address, { headers: this.headers })
        );
        return response;
    }

    public async updateAddress(address: Address) {
        const response = handleFailure(
            this.purplship.addresses.update(address, address.id as string, { headers: this.headers })
        );
        response.then(() => this.shipments$.next(DEFAULT_PAGINATED_RESULT as any));
        return response;
    }

    public async saveParcel(parcel: Parcel) {
        const response = handleFailure(
            this.purplship.parcels.create(parcel, { headers: this.headers })
        );
        return response;
    }

    public async updateParcel(parcel: Parcel) {
        const response = handleFailure(
            this.purplship.parcels.update(parcel, parcel.id as string, { headers: this.headers })
        );
        response.then(() => this.shipments$.next(DEFAULT_PAGINATED_RESULT as any));
        return response;
    }

    public async removeParcel(parcel_id: string) {
        const response = handleFailure(
            this.purplship.parcels.remove(parcel_id, { headers: this.headers })
        );
        return response;
    }

    public async addCustoms(shipment_id: string, customs: Customs) {
        const response = handleFailure(
            this.purplship.shipments.addCustoms(customs, shipment_id, { headers: this.headers })
        );
        response.then(() => this.shipments$.next(DEFAULT_PAGINATED_RESULT as any));
        return response;
    }

    public async saveCustoms(customs: Customs) {
        const response = handleFailure(
            this.purplship.customs.create(customs, { headers: this.headers })
        );
        return response;
    }

    public async updateCustoms(customs: Customs) {
        const response = handleFailure(
            this.purplship.customs.update(customs, customs.id as string, { headers: this.headers })
        );
        response.then(() => this.shipments$.next(DEFAULT_PAGINATED_RESULT as any));
        return response;
    }

    public async removeCustoms(customs_id: string) {
        const response = handleFailure(
            this.purplship.customs.discard(customs_id, { headers: this.headers })
        );
        response.then(() => this.shipments$.next(DEFAULT_PAGINATED_RESULT as any));
        return response;
    }

    public async getUserInfo() {
        const response = await http("/user_info", { headers: this.headers });
        if (response.ok) {
            const data = await response.json();
            this.user$.next(data);
            return data;
        } else {
            throw new Error("Unable retrieve user info.");
        }
    }

    public async updateUserInfo(info: Partial<UserInfo>) {
        const response = await http("/user_info", {
            method: "PATCH",
            headers: this.headers,
            body: (JSON.stringify(info) as any)
        });
        if (response.ok) {
            const data = await response.json();
            this.user$.next(data);
            return data;
        } else {
            throw new Error("Failed to update user Info.");
        }
    }

    public async closeAccount() {
        const response = await http("/user_info", {
            method: "DELETE",
            headers: this.headers,
        });
        if (response.ok) {
            document.location.href = "/account/deactivated/";
        } else {
            throw new Error("An error occured during the account deactivation.");
        }
    }

    public async regenerateToken(password: string) {
        const response = await fetch("/token", {
            method: "PUT",
            headers: this.headers,
            body: (JSON.stringify({ username: this.user$.value.email, password }) as any)
        });
        if (response.ok) {
            const data = await response.json();
            this.token$.next((data as any).token);
            return data;
        } else {
            throw new Error("Unable to logIn with the provided credentials.");
        }
    }

    public async connectProvider(info: ConnectionData) {
        const response = await http("/connections", {
            method: "POST",
            headers: this.headers,
            body: (JSON.stringify(info) as any)
        });
        if (response.ok) {
            const data = await response.json();
            this.fetchConnections();
            return data;
        } else {
            throw new Error("Failed to connect the service provider.");
        }
    }

    public async updateConnection(id: string, info: ConnectionData) {
        const response = await http(`/connections/${id}`, {
            method: "PATCH",
            headers: this.headers,
            body: (JSON.stringify(info) as any)
        });
        if (response.ok) {
            const data = await response.json();
            this.fetchConnections();
            return data;
        } else {
            throw new Error("Failed to update the service provider connection.");
        }
    }

    public async disconnectProvider(id: string) {
        const response = await http(`/connections/${id}`, {
            method: "DELETE",
            headers: this.headers,
        });
        if (response.ok) {
            const data = await response.json();
            this.fetchConnections();
            return data;
        } else {
            throw new Error("Failed to disconnect the service provider.");
        }
    }

    public async saveTemplate(payload: Template) {
        const response = await http("/templates", {
            method: "POST",
            headers: this.headers,
            body: (JSON.stringify(payload) as any)
        });
        if (response.ok) {
            const data = await response.json();
            return data;
        } else {
            throw new Error("Failed create a new template.");
        }
    }

    public async updateTemplate(id: string, payload: Template) {
        const response = await http(`/templates/${id}`, {
            method: "PATCH",
            headers: this.headers,
            body: (JSON.stringify(payload) as any)
        });
        if (response.ok) {
            const data = await response.json();
            return data;
        } else {
            throw new Error("Failed to update the template.");
        }
    }

    public async removeTemplate(id: string) {
        const response = await http(`/templates/${id}`, {
            method: "DELETE",
            headers: this.headers,
        });
        if (response.ok) {
            const data = await response.json();
            return data;
        } else {
            throw new Error("Failed to remove the template.");
        }
    }

    public async fetchParcels(url?: string): Promise<PaginatedTemplates> {
        const response = await http(url || `/parcels/templates?limit=20&offset=0`, { headers: this.headers });
        if (response.ok) {
            const data = await response.json();
            this.parcels$.next({...data, fetched: true, url});
            return data;
        } else {
            this.parcels$.next({...DEFAULT_PAGINATED_RESULT, fetched: true});
            throw new Error("Unable fetch parcel templates.");
        }
    }

    public async fetchAddresses(url?: string): Promise<PaginatedTemplates> {
        const response = await http(url || `/addresses/templates?limit=20&offset=0`, { headers: this.headers });
        if (response.ok) {
            const data = await response.json();
            this.addresses$.next({...data, fetched: true, url});
            return data;
        } else {
            this.addresses$.next({...DEFAULT_PAGINATED_RESULT, fetched: true});
            throw new Error("Unable fetch addresses templates.");
        }
    }

    public async fetchCustomsInfos(url?: string): Promise<PaginatedTemplates> {
        const response = await http(url || `/customs_infos/templates?limit=20&offset=0`, { headers: this.headers });
        if (response.ok) {
            const data = await response.json();
            this.customsInfos$.next({...data, fetched: true, url});
            return data;
        } else {
            this.customsInfos$.next({...DEFAULT_PAGINATED_RESULT, fetched: true});
            throw new Error("Unable fetch customs infos templates.");
        }
    }

    public async fetchConnections(url?: string): Promise<PaginatedConnections> {
        const response = await http(url || `/connections?limit=20&offset=0`, { headers: this.headers });
        if (response.ok) {
            const data = await response.json();
            this.connections$.next({...data, fetched: true, url});
            return data;
        } else {
            this.connections$.next({...DEFAULT_PAGINATED_RESULT, fetched: true});
            throw new Error("Unable fetch connected carriers.");
        }
    }

    public async fetchShipments(url?: string): Promise<PaginatedShipments> {
        const response = await http(url || `/shipments?limit=20&offset=0`, { headers: this.headers });
        if (response.ok) {
            const data = await response.json();
            this.shipments$.next({...data, fetched: true, url});
            return data;
        } else {
            this.shipments$.next({...DEFAULT_PAGINATED_RESULT, fetched: true});
            throw new Error("Failed to fetch shipments.");
        }
    }

    public async fetchLogs(url?: string): Promise<PaginatedLogs> {
        const response = await http(url || `/logs?limit=20&offset=0`, { headers: this.headers });
        if (response.ok) {
            const data = await response.json();
            this.logs$.next({...data, fetched: true, url});
            return data;
        } else {
            this.logs$.next({...DEFAULT_PAGINATED_RESULT, fetched: true});
            throw new Error("Failed to fetch logs.");
        }
    }

    public async retrieveLog(id: string): Promise<Log> {
        const response = await http(`/logs/${id}`, { headers: this.headers });
        if (response.ok) {
            const data = await response.json();
            return data;
        } else {
            throw new Error("Failed to fetch log.");
        }
    }

    public setNotification(notification?: Notification) {
        this.notification$.next(notification);
    }

    public setLabelData(data?: LabelData) {
        this.labelData$.next(data || DEFAULT_LABEL_DATA);
    }
}

function collectToken(): string {
    const root = document.getElementById("root");
    const token = (root as HTMLDivElement).getAttribute('data-token') as string;
    (root as HTMLDivElement).removeAttribute('data-token');

    return token;
}

function getCookie(name: string): string {
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

async function http(...args: Parameters<typeof fetch>): ReturnType<typeof fetch> {
    try {
        return await fetch(...args);
    } catch (err) {
        if (err.message === 'Failed to fetch') {
            throw new Error('Oups! Looks like you are offline');
        } else if (err instanceof Response) {
            throw new RequestError(await err.json());
        }
        throw err
    }
}

async function handleFailure<T>(request: Promise<T>): Promise<T> {
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

// Initialize State: Fetch Data
export const state = new AppState();