import './Navbar.css';
import { Search, Globe, Menu, UserCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="container flex items-center justify-between navbar-inner">
        
        {/* Logo */}
        <Link to="/" className="navbar-logo">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="var(--primary)">
            <path d="M16 1.488C7.592 1.488 0 8.878 0 17.518c0 4.29 1.687 8.167 4.436 11.026.177.185.422.288.68.288h21.768c.258 0 .503-.103.68-.288C30.313 25.685 32 21.808 32 17.518 32 8.878 24.408 1.488 16 1.488zm0 2.215c7.323 0 13.785 6.452 13.785 13.815 0 3.737-1.503 7.155-3.955 9.68H6.17c-2.452-2.525-3.955-5.943-3.955-9.68 0-7.363 6.462-13.815 13.785-13.815zm0 5.438c-4.108 0-7.442 3.328-7.442 7.426 0 2.766 1.47 5.187 3.69 6.43l3.752 2.062 3.752-2.062c2.22-1.243 3.69-3.664 3.69-6.43 0-4.098-3.334-7.426-7.442-7.426zm0 2.215c2.89 0 5.227 2.333 5.227 5.21 0 1.957-1.076 3.668-2.678 4.542l-2.549 1.401-2.549-1.401c-1.602-.874-2.678-2.585-2.678-4.542 0-2.877 2.337-5.21 5.227-5.21z" />
          </svg>
          <span className="logo-text">stayhub</span>
        </Link>

        {/* Search Bar */}
        <div className="search-bar hover-scale shadow-sm">
          <button className="search-btn font-medium">Anywhere</button>
          <span className="search-divider"></span>
          <button className="search-btn font-medium">Any week</button>
          <span className="search-divider"></span>
          <button className="search-btn search-guests">
            <span className="guest-text">Add guests</span>
            <div className="search-icon-wrapper">
              <Search size={14} strokeWidth={3} />
            </div>
          </button>
        </div>

        {/* User Menu */}
        <div className="user-menu flex items-center">
          <button className="host-btn">Airbnb your home</button>
          <button className="globe-btn">
            <Globe size={18} />
          </button>
          <button className="profile-btn shadow-sm hover-scale">
            <Menu size={18} />
            <UserCircle size={30} color="var(--text-light)" />
          </button>
        </div>

      </div>
    </nav>
  );
};

export default Navbar;
