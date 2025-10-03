import React from 'react';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';

function FooterLinkItem({ item }) {
    const { to, href, label, prependBaseUrlToHref, ...props } = item;
    const toUrl = useBaseUrl(to);
    const normalizedHref = useBaseUrl(href, {
        forcePrependBaseUrl: prependBaseUrlToHref,
    });

    return (
        <Link
            className="footer__link-item"
            {...(href
                ? {
                    href: normalizedHref,
                }
                : {
                    to: toUrl,
                })}
            {...props}>
            {label}
        </Link>
    );
}

export default FooterLinkItem; 