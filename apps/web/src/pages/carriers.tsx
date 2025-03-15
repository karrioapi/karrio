import React from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import TailwindWrapper from '../components/TailwindWrapper';
import KarrioLayout from '../components/KarrioLayout';

export default function Carriers(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();

  return (
    <TailwindWrapper>
      <KarrioLayout>
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16">
              <h1 className="text-5xl font-bold mb-6">Supported Carriers</h1>
              <p className="text-xl max-w-3xl mx-auto mb-8">
                Connect with 30+ major carriers globally through a single integration point.
              </p>
            </div>

            {/* Carrier logos and information would go here */}

          </div>
        </div>
      </KarrioLayout>
    </TailwindWrapper>
  );
}
