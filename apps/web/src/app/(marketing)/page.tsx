import Image from "next/image";
import Link from "next/link";
import { Button } from "@karrio/ui/components/ui/button";
import { CTASection } from "@/components/cta-section";
import { HowItWorksSection } from "@/components/how-it-works-section";
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

export default function Home() {
  return (
    <div className="bg-white text-foreground">
      {/* Hero Section */}
      <section className="py-16 md:py-24">
        <div className="container mx-auto px-4 sm:px-6 lg:px-0 max-w-6xl text-center">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6">
            Programmable shipping<br />APIs for platforms
          </h1>
          <p className="text-lg md:text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
            Karrio is the most flexible way to integrate shipping into your platform. Our
            headless shipping platform enables you to build shipping experiences from live
            rating, label generation, package tracking, and more.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4 mb-16">
            <Button size="lg" className="bg-primary hover:bg-primary/90">
              <Link href="/platform">Get Started</Link>
            </Button>
            <Button size="lg" variant="outline" className="border-gray-300">
              <Link href="/docs/self-hosting">Deploy Open Source</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="py-12 bg-gray-50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-0 max-w-6xl">
          <h2 className="text-3xl font-bold text-center mb-12">Join the community</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center mb-12">
            <div className="p-6 rounded-lg">
              <div className="text-3xl font-bold text-primary mb-2">+30</div>
              <p className="text-gray-600">Supported Carriers</p>
            </div>
            <div className="p-6 rounded-lg">
              <div className="text-3xl font-bold text-primary mb-2">+20K</div>
              <p className="text-gray-600">OSS Downloads</p>
            </div>
            <div className="p-6 rounded-lg">
              <div className="text-3xl font-bold text-primary mb-2">+1M</div>
              <p className="text-gray-600">Live Transactions</p>
            </div>
          </div>

          {/* Carrier Logos */}
          <div className="flex flex-wrap justify-center gap-4 py-4">
            {['canadapost', 'usps', 'purolator', 'fedex', 'dhl_express', 'ups', 'sendle', 'canpar', 'aramex', 'australiapost'].map((carrier) => (
              <div key={carrier} className="h-12 w-12 md:h-16 md:w-16 flex items-center justify-center bg-white rounded-lg p-0 shadow-sm">
                <Image
                  src={`/carriers/${carrier}_icon.svg`}
                  alt={`${carrier} logo`}
                  width={48}
                  height={48}
                  className="h-auto w-auto object-contain"
                />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="py-16 md:py-24 border-t border-gray-100 dark:border-gray-800">
        <div className="container mx-auto px-4 sm:px-6 lg:px-0 max-w-6xl">
          <div className="text-center mb-16">
            <h2 className="text-sm uppercase tracking-wider text-primary font-medium mb-4">The problem</h2>
            <h3 className="text-3xl md:text-5xl font-bold mb-6">Shipping integration is still painful</h3>
            <p className="text-lg text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">Poor developer experience. Long time-to-value. Lack of control.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white dark:bg-white/5 rounded-xl shadow-sm border border-gray-100 dark:border-white/10 p-8 transition-all hover:shadow-md relative overflow-hidden group">
              <div className="absolute -right-10 -top-10 w-24 h-24 rounded-full bg-primary/5 group-hover:bg-primary/10 transition-all"></div>
              <div className="relative z-10">
                <div className="w-12 h-12 flex items-center justify-center rounded-lg bg-primary/10 dark:bg-primary/20 text-primary mb-6">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" />
                  </svg>
                </div>
                <h4 className="text-xl font-semibold mb-4">For engineers</h4>
                <p className="text-gray-600 dark:text-gray-300">
                  Obstacles include arcane technologies, a lack of documentation, multiple and inconsistent APIs, difficult access to accounts and API credentials for development, and more. In short, an overall poor developer experience.
                </p>
              </div>
            </div>

            <div className="bg-white dark:bg-white/5 rounded-xl shadow-sm border border-gray-100 dark:border-white/10 p-8 transition-all hover:shadow-md relative overflow-hidden group">
              <div className="absolute -right-10 -top-10 w-24 h-24 rounded-full bg-secondary/5 group-hover:bg-secondary/10 transition-all"></div>
              <div className="relative z-10">
                <div className="w-12 h-12 flex items-center justify-center rounded-lg bg-secondary/10 dark:bg-secondary/20 text-secondary mb-6">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z" />
                    <line x1="3" y1="6" x2="21" y2="6" />
                    <path d="M16 10a4 4 0 0 1-8 0" />
                  </svg>
                </div>
                <h4 className="text-xl font-semibold mb-4">For brands & retailers</h4>
                <p className="text-gray-600 dark:text-gray-300">
                  Enabling shipping is crucial but expensive, with limited options. Depending on in-house shipping system diverts engineering resources and pushing carrier onboarding. Adopting closed SaaS solutions results in a limited ability to create custom logistics processes.
                </p>
              </div>
            </div>

            <div className="bg-white dark:bg-white/5 rounded-xl shadow-sm border border-gray-100 dark:border-white/10 p-8 transition-all hover:shadow-md relative overflow-hidden group">
              <div className="absolute -right-10 -top-10 w-24 h-24 rounded-full bg-accent/5 group-hover:bg-accent/10 transition-all"></div>
              <div className="relative z-10">
                <div className="w-12 h-12 flex items-center justify-center rounded-lg bg-accent/10 dark:bg-accent/20 text-accent mb-6">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="2" y="7" width="20" height="14" rx="2" ry="2" />
                    <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
                  </svg>
                </div>
                <h4 className="text-xl font-semibold mb-4">For Logistics providers</h4>
                <p className="text-gray-600 dark:text-gray-300">
                  After re-inventing the wheel or adopting a closed-source solution, how much engineering time do you have left? Building a custom-branded shipping experience for your merchants doesn't have to result in a lack of control, vendor lock-in and low margins.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Solution Section */}
      <section className="py-16 md:py-24 bg-gray-50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-0 max-w-6xl">
          <h2 className="text-base md:text-lg text-gray-500 text-center mb-4">The solution</h2>
          <h3 className="text-2xl md:text-3xl lg:text-4xl font-bold text-center mb-12">Headless shipping platform</h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
            <div>
              <Image
                src="/unified-api-illustration.png"
                alt="Universal shipping API illustration"
                width={500}
                height={400}
                className="w-full h-auto"
              />
            </div>
            <div>
              <div className="space-y-8">
                <div>
                  <h4 className="text-xl md:text-2xl font-semibold mb-4">Universal shipping API</h4>
                  <p className="text-gray-600">
                    Feeling the pain or struggling with shipping API integrations? Stop reinventing the
                    wheel and add your carrier accounts on Karrio to start processing shipping transactions.
                  </p>
                </div>

                <div>
                  <h4 className="text-xl md:text-2xl font-semibold mb-4">Out-of-the-box shipping system</h4>
                  <p className="text-gray-600">
                    Karrio's shipping solution offers an API for engineers and a flexible user interface
                    for back-office fulfillment operations. With our composable architecture, you can
                    add carrier extensions and extend Karrio's functionalities.
                  </p>
                </div>

                <div>
                  <h4 className="text-xl md:text-2xl font-semibold mb-4">More control and security</h4>
                  <p className="text-gray-600">
                    Our open source solution gives you an alternative to the build-or-buy dilemma.
                    With Karrio's transparency, you can regain control and visibility over logistics
                    processes and shipping spending. All while achieving carrier, data and security
                    compliance.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <HowItWorksSection />

      {/* Developer Section */}
      <section className="py-16 md:py-24 bg-[#231d48] text-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-0 max-w-6xl">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-6">Made for developers</h2>
              <h3 className="text-xl font-medium mb-6">The flexible headless shipping platform</h3>
              <p className="text-gray-300 mb-6">
                No more painful in-house carrier integrations. No more dependence
                on 3rd party and SaaS vendor lock-in for your logistics automation.
                We obsess over the right abstractions so your teams don't have to
                and won't spend months integrating shipping functionalities. Create
                memorable shipping experiences and powerful extensions through
                WebHooks, REST and GraphQL API.
              </p>
              <Button className="bg-primary text-white hover:bg-primary/90">
                <Link href="/">Read Docs</Link>
              </Button>
            </div>

            <div className="bg-[#17142D] p-6 rounded-lg">
              <div className="flex items-center justify-between border-b border-gray-700 pb-2 mb-4">
                <div className="flex space-x-2">
                  <div className="h-3 w-3 rounded-full bg-red-500"></div>
                  <div className="h-3 w-3 rounded-full bg-yellow-500"></div>
                  <div className="h-3 w-3 rounded-full bg-green-500"></div>
                </div>
              </div>
              <SyntaxHighlighter
                language="bash"
                style={vscDarkPlus}
                customStyle={{
                  background: 'transparent',
                  padding: 0,
                  margin: 0,
                  fontSize: '0.875rem',
                }}
                wrapLongLines={true}
              >
                {`curl \\
  -X POST \\
  -H "Authorization: Token API_KEY" \\
  https://api.karrio.io/v1/proxy/rates \\
  -d '{
    "shipper": {
      "postal_code": "V6M2V9",
      "city": "Vancouver",
      "country_code": "CA",
      "province_code": "BC",
      "address_line1": "5840 Oak St"
    },
    "recipient": {
      "postal_code": "E1C4Z8",
      "city": "Moncton",
      "country_code": "CA",
      "province_code": "NB",
      "address_line1": "125 Church St"
    },
    "parcels": [{
      "weight": 1,
      "weight_unit": "kg",
      "package_preset": "canadapost_corrugated_small_box"
    }],
    "carrier_ids": ["canadapost"]
  }'`}
              </SyntaxHighlighter>
            </div>
          </div>
        </div>
      </section>

      {/* Next Steps Section */}
      <CTASection
        title="Ready to get started?"
        description="Karrio is free to get started, and has an insider sponsorship tier for mission critical and shipping at scale."
      />
    </div>
  );
}
