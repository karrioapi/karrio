import React from 'react';
import { Link } from "@reach/router";
import '@/css/NavBar.css';

const NavBar: React.FC = () => {
  return (
    <header className="navbar header">
      <section className="navbar-section">
        <img className="navbar-brand mr-2" src="/static/purpleserver/img/logo-monochrome.png" width="100" height="20" alt="PurplShip" />
      </section>

      <section className="navbar-center col-5">
        <div className="input-group input-inline container">
          <input className="form-input" type="text" placeholder="search" />
        </div>
      </section>

      <section className="navbar-section">
        <div className="dropdown dropdown-right">
          <a href="#" className="btn btn-link dropdown-toggle" tabIndex={0}>
            <i className="icon icon-apps"></i>
          </a>

          <ul className="menu">
            <li className="menu-item">
              <Link to="dashboard">Dashboard</Link>
            </li>
            <li className="menu-item">
              <Link to="/">Shipments</Link>
            </li>
          </ul>
        </div>

        <div className="dropdown dropdown-right">
          <a href="#" className="btn btn-link dropdown-toggle" tabIndex={0}>
            <i className="icon icon-people"></i>
          </a>

          <ul className="menu">
            <li className="menu-item">
              <Link to="settings">Settings</Link>
            </li>
            <li className="menu-item">
              <Link to="logout">Logout</Link>
            </li>
          </ul>
        </div>
      </section>
    </header>
  );
}

export default NavBar;