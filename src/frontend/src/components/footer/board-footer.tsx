import React from 'react';

interface BoardFooterComponent { }

const BoardFooter: React.FC<BoardFooterComponent> = () => {
    return (
        <footer className="footer py-5">
            <div className="content columns">
                <div className="column"></div>
                <div className="column has-text-centered">
                    <a href="https://purplship.com">
                        <img src="/static/purpleserver/favicon-set/favicon.svg" alt="" width="50" />
                    </a>
                </div>
                <div className="column has-text-right-desktop">
                    <a className="button is-white" target="_blank" href="/api">
                        <span>API Reference</span>
                        <span className="icon is-small">
                            <i className="fas fa-external-link-alt"></i>
                        </span>
                    </a>
                    <a className="button is-white" href="https://docs.purplship.com">
                        <span>Docs</span>
                    </a>
                    <a className="button is-white" href="https://github.com/PurplShip">
                        <span>Contribute</span>
                    </a>
                </div>
            </div>
        </footer>
    );
}

export default BoardFooter;
