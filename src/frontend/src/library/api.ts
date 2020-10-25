import { CarrierSettings, References, Shipment, Purplship } from '@purplship/purplship';
import { useEffect, useState } from 'react';
import { Subject, BehaviorSubject } from 'rxjs';
import { distinct } from 'rxjs/operators';

// Collect API token from the web page
const INITIAL_TOKEN = collectToken();

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

export interface PaginatedLogs extends PaginatedContent<Log>{}
export interface PaginatedShipments extends PaginatedContent<Shipment>{}
export interface PaginatedConnections extends PaginatedContent<Connection>{}

class AppState {
    private token$: BehaviorSubject<string> = new BehaviorSubject<string>(INITIAL_TOKEN);
    private user$: BehaviorSubject<UserInfo> = new BehaviorSubject<UserInfo>({} as UserInfo);
    private connections$: Subject<PaginatedConnections> = new Subject<PaginatedConnections>();
    private shipments$: Subject<PaginatedShipments> = new Subject<PaginatedShipments>();
    private references$: Subject<References> = new Subject<References>();
    private logs$: Subject<PaginatedLogs> = new Subject<PaginatedLogs>();

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

    private async fetchReferences() {
        const references = await this.purplship.utils.references();
        this.references$.next(references);
        return references;
    }

    public async getUserInfo() {
        const response = await fetch("/user_info" , { headers: this.headers });
        if (response.ok) {
            const data = await response.json();
            this.user$.next(data);
            return data;
        } else {
            throw new Error("Unable fetch user info.");
        }
    }

    public async updateUserInfo(info: Partial<UserInfo>) {
        const response = await fetch("/user_info", {
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
        await fetch("/user_info", { 
            method: "DELETE",
            headers: this.headers,
        });
        document.location.href="/";
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
            throw new Error("Unable to log in with provided credentials.");
        }
    }

    public async connectProvider(info: ConnectionData) {
        const response = await fetch("/connections", {
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
        const response = await fetch(`/connections/${id}`, { 
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
        const response = await fetch(`/connections/${id}`, { 
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
        const response = await fetch(url || `/connections?limit=20&offset=0` , { headers: this.headers });
        if (response.ok) {
            const connections = await response.json();
            this.connections$.next(connections);
            return connections;
        } else {
            throw new Error("Unable fetch connected carriers.");
        }
    }

    public async fetchShipments(url?: string): Promise<PaginatedShipments> {
        const response = await fetch(url || `/shipments?limit=20&offset=0`, { headers: this.headers });
        if (response.ok) {
            const data = await response.json();
            this.shipments$.next(data);
            return data;
        } else {
            throw new Error("Failed to fetch shipments.");
        }
    }

    public async fetchLogs(url?: string): Promise<PaginatedLogs> {
        const response = await fetch(url || `/logs?limit=20&offset=0`, { headers: this.headers });
        if (response.ok) {
            const data = await response.json();
            this.logs$.next(data);
            return data;
        } else {
            throw new Error("Failed to fetch logs.");
        }
    }

    public async retrieveLog(id: string): Promise<Log> {
        const response = await fetch(`/logs/${id}`, { headers: this.headers });
        if (response.ok) {
            const data = await response.json();
            return data;
        } else {
            throw new Error("Failed to fetch log.");
        }
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

// Initialize State: Fetch Data
export const state = new AppState();