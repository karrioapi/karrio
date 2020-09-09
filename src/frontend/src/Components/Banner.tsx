import React from 'react';
import '@/css/Banner.css';

interface BannerComponent {
}

const Banner: React.FC<BannerComponent> = ({ children }) => {
  return (
    <header className="navbar Banner">
      <section className="navbar-section">
        {React.Children.map(children, c => c)}
      </section>
      <section className="navbar-section">
        <a href="#" className="btn btn-primary btn-sm">New</a>
      </section>
    </header>
  );
}

export default Banner;