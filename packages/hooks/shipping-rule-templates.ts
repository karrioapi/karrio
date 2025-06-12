export interface ShippingRuleTemplate {
    slug: string;
    name: string;
    description: string;
    icon: string;
    conditions: any;
    actions: any;
    priority: number;
}

export const PREDEFINED_SHIPPING_RULE_TEMPLATES: ShippingRuleTemplate[] = [
    {
        slug: "cheapest-option",
        name: "Always Choose Cheapest",
        description: "Automatically select the lowest cost shipping option for all orders",
        icon: "💰",
        conditions: {},
        actions: {
            select_service: {
                strategy: "cheapest"
            }
        },
        priority: 100
    },
    {
        slug: "fastest-option",
        name: "Always Choose Fastest",
        description: "Automatically select the fastest shipping option for all orders",
        icon: "⚡",
        conditions: {},
        actions: {
            select_service: {
                strategy: "fastest"
            }
        },
        priority: 100
    },
    {
        slug: "domestic-free-shipping",
        name: "Free Domestic Shipping",
        description: "Free shipping for domestic orders over a certain weight/value threshold",
        icon: "🏠",
        conditions: {
            destination: {
                country_code: "US"
            },
            weight: {
                min: 0,
                max: 50,
                unit: "lb"
            }
        },
        actions: {
            select_service: {
                strategy: "cheapest",
                carrier_code: "usps"
            }
        },
        priority: 200
    },
    {
        slug: "international-express",
        name: "International Express Only",
        description: "Use express shipping for all international orders",
        icon: "🌍",
        conditions: {
            destination: {
                country_code: "!US"
            }
        },
        actions: {
            select_service: {
                strategy: "fastest",
                carrier_code: "fedex"
            }
        },
        priority: 150
    },
    {
        slug: "heavy-freight",
        name: "Heavy Item Freight",
        description: "Use freight shipping for heavy items over 100 lbs",
        icon: "📦",
        conditions: {
            weight: {
                min: 100,
                unit: "lb"
            }
        },
        actions: {
            select_service: {
                strategy: "preferred",
                carrier_code: "freight"
            }
        },
        priority: 300
    },
    {
        slug: "local-delivery",
        name: "Local Same-Day Delivery",
        description: "Prefer local delivery services for nearby areas",
        icon: "🚚",
        conditions: {
            destination: {
                postal_code: ["90210", "90211", "90212"]
            },
            address_type: {
                type: "residential"
            }
        },
        actions: {
            select_service: {
                strategy: "fastest",
                service_code: "same_day"
            }
        },
        priority: 400
    },
    {
        slug: "block-po-box",
        name: "Block PO Box Shipping",
        description: "Prevent shipping to PO Box addresses for certain carriers",
        icon: "🚫",
        conditions: {
            address_type: {
                type: "po_box"
            }
        },
        actions: {
            block_service: true
        },
        priority: 500
    },
    {
        slug: "carrier-preference",
        name: "Preferred Carrier",
        description: "Always prefer a specific carrier when available",
        icon: "⭐",
        conditions: {},
        actions: {
            select_service: {
                strategy: "preferred",
                carrier_code: "fedex"
            }
        },
        priority: 50
    }
];

export function useShippingRuleTemplates() {
    return {
        templates: PREDEFINED_SHIPPING_RULE_TEMPLATES,
        getTemplate: (slug: string) => PREDEFINED_SHIPPING_RULE_TEMPLATES.find(t => t.slug === slug),
    };
}
