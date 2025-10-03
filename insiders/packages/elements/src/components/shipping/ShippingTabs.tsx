import { Tabs, TabsList, TabsTrigger, TabsContent } from '@karrio/ui/components/ui/tabs';
import { ShippingRateCalculator } from './ShippingRateCalculator';
import { ShippingRates } from './ShippingRates';
import { AddressForm } from './AddressForm';
import * as React from 'react';

interface ShippingTabsProps {
  className?: string;
}

/**
 * Tabbed interface for shipping-related components
 */
export function ShippingTabs({ className }: ShippingTabsProps) {
  const [activeTab, setActiveTab] = React.useState("address");
  const [rates, setRates] = React.useState<Array<any>>([]);

  const handleCalculateRates = (data: any) => {
    console.log('Calculating rates with:', data);
    // Simulate fetching rates
    setTimeout(() => {
      setRates([
        {
          id: 'rate_1',
          carrier: 'USPS',
          service: 'Priority Mail',
          price: 12.99,
          currency: 'USD',
          delivery_time: '1-3 business days'
        },
        {
          id: 'rate_2',
          carrier: 'UPS',
          service: 'Ground',
          price: 14.50,
          currency: 'USD',
          delivery_time: '3-5 business days'
        },
        {
          id: 'rate_3',
          carrier: 'FedEx',
          service: 'Express Saver',
          price: 28.75,
          currency: 'USD',
          delivery_time: '3 business days'
        }
      ]);
      setActiveTab('rates');
    }, 1000);
  };

  const handleSelectRate = (rate: any) => {
    console.log('Selected rate:', rate);
    // Handle rate selection logic here
  };

  return (
    <Tabs value={activeTab} onValueChange={setActiveTab} className={className}>
      <TabsList className="w-full mb-4">
        <TabsTrigger value="address">Address</TabsTrigger>
        <TabsTrigger value="calculator">Rate Calculator</TabsTrigger>
        <TabsTrigger value="rates">Shipping Rates</TabsTrigger>
      </TabsList>

      <TabsContent value="address">
        <AddressForm
          onSave={(data) => {
            console.log('Address saved:', data);
            setActiveTab('calculator');
          }}
        />
      </TabsContent>

      <TabsContent value="calculator">
        <ShippingRateCalculator onCalculate={handleCalculateRates} />
      </TabsContent>

      <TabsContent value="rates">
        <ShippingRates rates={rates} onSelect={handleSelectRate} />
      </TabsContent>
    </Tabs>
  );
}
