import Purplship from '@purplship/purplship';
import { CarrierSettings, Shipment } from '@purplship/purplship/dist';
import { useEffect, useState } from 'react';
import { of, Subject } from 'rxjs';
import { distinct } from 'rxjs/operators';

interface UserInfo {
    name: string;
    email: string;
    username: string;
    token: string;
}

class AppState {
    private user$: Subject<UserInfo | null> = new Subject<UserInfo | null>();
    private carriers$: Subject<CarrierSettings[]> = new Subject<CarrierSettings[]>();
    public shipments$: Subject<Shipment[]> = new Subject<Shipment[]>();

    constructor() {
        this.fetchCarriers();
        this.fetchShipments();
    }

    public get shipments() {
        const [shipments, setValue] = useState<Shipment[]>([]);
        useEffect(() => { this.shipments$.asObservable().pipe(distinct()).subscribe(setValue); });
        return shipments
    }

    public get carriers() {
        const [carriers, setValue] = useState<CarrierSettings[]>([]);
        useEffect(() => { this.carriers$.asObservable().pipe(distinct()).subscribe(setValue); });
        return carriers
    }

    public fetchCarriers() {
        purplship.carriers.list().then(_ => this.carriers$.next(_));
    }

    public fetchShipments() {
        purplship.shipments.list().then(_ => this.shipments$.next(_));
    }
}

// Collect API token from the web page
const gate = document.getElementById("gate");
const token = (gate as HTMLInputElement).value;
gate?.remove();

// Initializer Purplship API
export const purplship = new Purplship(token, '/v1');

// Initialize State: Fetch Data
export const state = new AppState();