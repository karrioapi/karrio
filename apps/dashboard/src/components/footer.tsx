import { useAPIMetadata } from '@/context/api-metadata';
import React from 'react';


const Footer: React.FC = () => {
  const { references } = useAPIMetadata();

  return (
    <footer className="footer p-0 pt-6">
      <div className="content columns">
        <div className="column has-text-right-desktop">
          <a className="button is-white footer-api-reference-link"
            target="_blank"
            rel="noreferrer"
            href={references.OPENAPI}>
            <span>API Reference</span>
            <span className="icon is-small">
              <i className="fas fa-external-link-alt"></i>
            </span>
          </a>
          <a className="button is-white footer-api-reference-link"
            target="_blank"
            rel="noreferrer"
            href={references.GRAPHQL}>
            <span>GraphQL</span>
            <span className="icon is-small">
              <i className="fas fa-external-link-alt"></i>
            </span>
          </a>
          <a className="button is-white footer-docs-link"
            target="_blank"
            rel="noreferrer"
            href="https://docs.karrio.io">
            <span>Docs</span>
            <span className="icon is-small">
              <i className="fas fa-external-link-alt"></i>
            </span>
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
