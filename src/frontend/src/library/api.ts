import Purplship from '@purplship/purplship';
import { CarrierSettings, Shipment } from '@purplship/purplship/dist';
import { useEffect, useState } from 'react';
import { fromFetch } from 'rxjs/fetch';
import { Subject, BehaviorSubject } from 'rxjs';
import { distinct, switchMap } from 'rxjs/operators';

// Collect API token from the web page
const INITIAL_TOKEN = collectToken();

interface UserInfo {
    name: string;
    email: string;
    username: string;
    token: string;
}

class AppState {
    private token$: BehaviorSubject<string> = new BehaviorSubject<string>(INITIAL_TOKEN);
    private user$: BehaviorSubject<UserInfo> = new BehaviorSubject<UserInfo>({ username: "dan" } as UserInfo);
    private carriers$: Subject<CarrierSettings[]> = new Subject<CarrierSettings[]>();
    public shipments$: Subject<Shipment[]> = new Subject<Shipment[]>();

    constructor() {
        this.fetchCarriers();
        this.fetchShipments();
    }

    private get purplship(): Purplship {
        return new Purplship(this.token$.value, '/v1');
    }

    public get shipments() {
        const [shipments, setValue] = useState<Shipment[]>([]);
        useEffect(() => { this.shipments$.asObservable().pipe(distinct()).subscribe(setValue); });
        return shipments;
    }

    public get carriers() {
        const [carriers, setValue] = useState<CarrierSettings[]>([]);
        useEffect(() => { this.carriers$.asObservable().pipe(distinct()).subscribe(setValue); });
        return carriers;
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

    public async regenerateToken(password: string) {
        const response = await fetch("/token", {
            method: "PUT",
            headers: { "Content-Type": "application/json", "Authorization": `Token ${this.token$.value}` },
            body: (JSON.stringify({ username: this.user$.value.username, password }) as any)
        });
        if (response.ok) {
            const data = await response.json();
            this.token$.next((data as any).token);
        } else {
            throw new Error("Unable to log in with provided credentials.");
        }
    }

    public async fetchCarriers() {
        return this.purplship.carriers.list().then(_ => this.carriers$.next(_));
    }

    public async fetchShipments() {
        return this.purplship.shipments.list().then(_ => this.shipments$.next(_));
    }
}

function collectToken(): string {
    const gate = document.getElementById("gate");
    const token = (gate as HTMLInputElement).value;
    gate?.remove();

    return token;
}

// Initialize State: Fetch Data
export const state = new AppState();