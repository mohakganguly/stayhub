import './Footer.css';
import { Globe } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="site-footer">
      <div className="container footer-content flex justify-between items-center">
        <div className="footer-left flex items-center gap-4">
          <span>© 2026 stayhub, Inc.</span>
          <span className="dot-divider">·</span>
          <a href="#" className="hover-underline">Terms</a>
          <span className="dot-divider">·</span>
          <a href="#" className="hover-underline">Sitemap</a>
          <span className="dot-divider">·</span>
          <a href="#" className="hover-underline">Privacy</a>
        </div>
        <div className="footer-right flex items-center gap-6">
          <button className="flex items-center gap-2 font-medium">
            <Globe size={16} />
            English (US)
          </button>
          <button className="font-medium">$ USD</button>
          <button className="font-medium">Support & resources</button>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
