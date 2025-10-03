import React from 'react';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import ThemedImage from '@theme/ThemedImage';

function FooterLogo({ logo }) {
    const { src, srcDark, alt, href, width, height } = logo;
    const sources = {
        light: useBaseUrl(src),
        dark: useBaseUrl(srcDark || src),
    };

    return (
        <Link
            href={href}
            className="footer__logo"
            target="_blank"
            rel="noopener noreferrer">
            <ThemedImage
                alt={alt}
                sources={sources}
                width={width}
                height={height}
            />
        </Link>
    );
}

export default FooterLogo; 