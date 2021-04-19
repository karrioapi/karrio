import { ConfigurationParameters, PurplshipClient } from "@/api";
import { getCookie, isNone } from "@/library/helper";
import React from "react";


export function initAPIClient() {
    let configuration: Partial<ConfigurationParameters> = {};
    const apiKey = collectToken();

    if (!isNone(apiKey)) {
        configuration = { apiKey, basePath: '' };
    } else {
        configuration = {
            basePath: '',
            headers: {
                "Content-Type": "application/json",
                'Accept': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        };
    }

    return React.createContext<PurplshipClient>(new PurplshipClient(configuration));
}


function collectToken(): string {
    const root = document.getElementById("root");
    const token = (root as HTMLDivElement).getAttribute('data-token') as string;
    (root as HTMLDivElement).removeAttribute('data-token');

    return token;
}


// Init the REST API client
export const RestClient = initAPIClient();
