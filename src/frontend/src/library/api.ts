import { CarrierSettings, References, Shipment, Purplship, Address, Parcel, Rate, RateRequest, RateResponse, ShippingRequest, ShipmentResponse, OperationConfirmation, OperationResponse, ShipmentCancelRequest } from '@purplship/purplship';
import { useEffect, useState } from 'react';
import { Subject, BehaviorSubject } from 'rxjs';
import { distinct } from 'rxjs/operators';

// Collect API token from the web page
const INITIAL_TOKEN = collectToken();
const DEFAULT_LABEL_DATA = {
    shipment: {
        shipper: {} as Address,
        recipient: {} as Address,
        parcels: [] as Parcel[],
    } as Shipment
}

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

interface PaginatedContent<T> {
    count: Number;
    next?: string | null;
    previous?: string | null;
    results: T[];
}

export interface PaginatedLogs extends PaginatedContent<Log> { }
export interface PaginatedShipments extends PaginatedContent<Shipment> { }
export interface PaginatedConnections extends PaginatedContent<Connection> { }


export enum NotificationType {
    error = "is-danger",
    warning = "is-warning",
    info = "is-info",
    success = "is-success"
}

export interface Notification {
    type: NotificationType;
    message: JSX.Element | string;
}

export interface LabelData {
    shipment: Shipment;
}

class AppState {
    private token$: BehaviorSubject<string> = new BehaviorSubject<string>(INITIAL_TOKEN);
    private user$: BehaviorSubject<UserInfo> = new BehaviorSubject<UserInfo>({} as UserInfo);
    private connections$: Subject<PaginatedConnections> = new Subject<PaginatedConnections>();
    private shipments$: Subject<PaginatedShipments> = new Subject<PaginatedShipments>();
    private references$: Subject<References> = new Subject<References>();
    private logs$: Subject<PaginatedLogs> = new Subject<PaginatedLogs>();
    private notification$: Subject<Notification> = new Subject<Notification>();
    private labelData$: BehaviorSubject<LabelData> = new BehaviorSubject<LabelData>(DEFAULT_LABEL_DATA);

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
        useEffect(() => { this.labelData$.asObservable().subscribe(setValue); });
        return labelData;
    }

    private async fetchReferences() {
        const references = await this.purplship.utils.references();
        this.references$.next(references);
        return references;
    }

    public async fetchShipmentRates(request: RateRequest): Promise<RateResponse> {
        return this.purplship.rates.fetch(request, { headers: this.headers })
            .catch(async err => {
                let error: Error & { response?: {} } = new Error("Unable fetch shipment rates.");
                try {
                    error.response = await err.json();
                } catch (e) { }
                throw error;
            });
    }

    public async buyShipmentLabel(request: ShippingRequest): Promise<ShipmentResponse> {
        return this.purplship.shipping.buyLabel(request, { headers: this.headers })
            .then(response => {
                this.fetchShipments();
                return response;
            })
            .catch(async err => {
                let error: Error & { response?: {} } = new Error("Failed to buy the shipment label.");
                try {
                    error.response = await err.json();
                } catch (e) { }
                throw error;
            });
    }

    public async cancelShipment(shipment: Shipment): Promise<OperationResponse> {
        return this.purplship.shipping.voidLabel(
            shipment as ShipmentCancelRequest,
            shipment.carrier_name as string,
            shipment.test_mode,
            { headers: this.headers }
        ).catch(async err => {
            let error: Error & { response?: {} } = new Error("Failed to cancel the shipment.");
            try {
                error.response = await err.json();
            } catch (e) { }
            throw error;
        });
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

    public async fetchConnections(url?: string): Promise<PaginatedConnections> {
        const response = await http(url || `/connections?limit=20&offset=0`, { headers: this.headers });
        if (response.ok) {
            const connections = await response.json();
            this.connections$.next(connections);
            return connections;
        } else {
            throw new Error("Unable fetch connected carriers.");
        }
    }

    public async fetchShipments(url?: string): Promise<PaginatedShipments> {
        const response = await http(url || `/shipments?limit=20&offset=0`, { headers: this.headers });
        if (response.ok) {
            const data = await response.json();
            this.shipments$.next(data);
            return data;
        } else {
            throw new Error("Failed to fetch shipments.");
        }
    }

    public async fetchLogs(url?: string): Promise<PaginatedLogs> {
        const response = await http(url || `/logs?limit=20&offset=0`, { headers: this.headers });
        if (response.ok) {
            const data = await response.json();
            this.logs$.next(data);
            return data;
        } else {
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
        }
        throw err
    }
}

// Initialize State: Fetch Data
export const state = new AppState();