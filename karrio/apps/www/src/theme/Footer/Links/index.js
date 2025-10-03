import React from 'react';
import LinkItem from '@theme/Footer/LinkItem';

function FooterLinks({ links }) {
    return (
        <div className="row footer__links">
            {links.map((linkItem, i) => (
                <div key={i} className="col footer__col">
                    {linkItem.title != null ? (
                        <div className="footer__title">{linkItem.title}</div>
                    ) : null}
                    {linkItem.items != null &&
                        Array.isArray(linkItem.items) &&
                        linkItem.items.length > 0 ? (
                        <ul className="footer__items clean-list">
                            {linkItem.items.map((item, key) =>
                                item.html ? (
                                    <li
                                        key={key}
                                        className="footer__item"
                                        // Developer provided the HTML, so assume it's safe.
                                        // eslint-disable-next-line react/no-danger
                                        dangerouslySetInnerHTML={{
                                            __html: item.html,
                                        }}
                                    />
                                ) : (
                                    <li key={item.href || item.to} className="footer__item">
                                        <LinkItem item={item} />
                                    </li>
                                ),
                            )}
                        </ul>
                    ) : null}
                </div>
            ))}
        </div>
    );
}

export default FooterLinks; 