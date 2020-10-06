import Purplship from '@purplship/purplship';
import { CarrierSettings, References, Shipment } from '@purplship/purplship/dist';
import React from 'react';
import { useEffect, useState } from 'react';
import { Subject, BehaviorSubject } from 'rxjs';
import { distinct } from 'rxjs/operators';

// Collect API token from the web page
const INITIAL_TOKEN = collectToken();

export interface UserInfo {
    firstName: string | null;
    email: string | null;
    username: string | null;
}

export interface Provider extends Omit<CarrierSettings, 'id'> {
    id: string | null | undefined;
    [property: string]: any;
}

export interface ProviderData {
    carrier_name: CarrierSettings.CarrierNameEnum;
    carrier_config: Partial<Provider>;
}

class AppState {
    private token$: BehaviorSubject<string> = new BehaviorSubject<string>(INITIAL_TOKEN);
    private user$: BehaviorSubject<UserInfo> = new BehaviorSubject<UserInfo>({} as UserInfo);
    private providers$: Subject<CarrierSettings[]> = new Subject<CarrierSettings[]>();
    private shipments$: Subject<Shipment[]> = new Subject<Shipment[]>();
    private references$: BehaviorSubject<References> = new BehaviorSubject<References>({} as References);

    constructor() {
        this.getUserInfo();
        this.fetchProviders();
        this.fetchShipments();
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

    public get shipments() {
        const [shipments, setValue] = useState<Shipment[]>([]);
        useEffect(() => { this.shipments$.asObservable().pipe(distinct()).subscribe(setValue); });
        return shipments;
    }

    public get providers() {
        const [providers, setValue] = useState<Provider[]>([]);
        useEffect(() => { this.providers$.asObservable().pipe(distinct()).subscribe(setValue); });
        return providers;
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

    public get references() {
        const [references, setValue] = useState<References>({} as References);
        useEffect(() => { this.references$.asObservable().subscribe(setValue); });
        return references;
    }

    private async fetchReferences() {
        const references = await this.purplship.utils.references();
        this.references$.next(references);
        return references;
    }

    public async fetchShipments() {
        const shipments = await this.purplship.shipments.list();
        this.shipments$.next(shipments);
        return shipments;
    }

    public async fetchProviders() {
        const response = await fetch("/v1/providers" , { headers: this.headers });
        if (response.ok) {
            const providers = await response.json();
            this.providers$.next(providers);
            return providers;
        } else {
            throw new Error("Unable fetch user info.");
        }
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
            body: (JSON.stringify({ username: this.user$.value.username, password }) as any)
        });
        if (response.ok) {
            const data = await response.json();
            this.token$.next((data as any).token);
            return data;
        } else {
            throw new Error("Unable to log in with provided credentials.");
        }
    }

    public async connectProvider(info: ProviderData) {
        const response = await fetch("/v1/providers", {
            method: "POST",
            headers: this.headers,
            body: (JSON.stringify(info) as any)
        });
        if (response.ok) {
            const data = await response.json();
            this.fetchProviders();
            return data;
        } else {
            throw new Error("Failed to connect the service provider.");
        }
    }

    public async updateProvider(id: string, info: ProviderData) {
        const response = await fetch(`/v1/providers/${id}`, { 
            method: "PATCH",
            headers: this.headers,
            body: (JSON.stringify(info) as any)
        });
        if (response.ok) {
            const data = await response.json();
            this.fetchProviders();
            return data;
        } else {
            throw new Error("Failed to update the service provider connection.");
        }
    }

    public async disconnectProvider(id: string) {
        const response = await fetch(`/v1/providers/${id}`, { 
            method: "DELETE",
            headers: this.headers,
        });
        if (response.ok) {
            const data = await response.json();
            this.fetchProviders();
            return data;
        } else {
            throw new Error("Failed to disconnect the service provider.");
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