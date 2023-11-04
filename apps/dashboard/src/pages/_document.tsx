// pages/_document.js

import Document, { Html, Head, Main, NextScript } from 'next/document'
import { p } from '@/lib/client';

class AppDocument extends Document {
  render() {
    return (
      <Html>
        <Head>
          <meta charSet="utf-8" />
          <link rel="favicon" sizes="180x180" href={p`/favicon.ico`} />
          <link rel="apple-touch-icon" sizes="180x180" href={p`/apple-touch-icon.png`} />
          <link rel="icon" type="image/png" sizes="32x32" href={p`/favicon-32x32.png`} />
          <link rel="icon" type="image/png" sizes="16x16" href={p`/favicon-16x16.png`} />
          <link rel="manifest" href={p`/manifest.json`} />
          <link rel="mask-icon" href={p`/safari-pinned-tab.svg`} color="#9504af" />
          <meta name="msapplication-TileColor" content="#9504af" />
          <meta name="theme-color" content="#9504af" />
          <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700&display=optional" rel="stylesheet" />
          <meta name="robots" content="NONE,NOARCHIVE" />
          <meta name="theme-color" content="#9504af" />
          <link rel="manifest" href={p`/manifest.json`} />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    )
  }
}

export default AppDocument;
