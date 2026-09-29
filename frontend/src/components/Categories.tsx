import { Waves, Flame, Tent, Palmtree, Warehouse, Castle, Mountain, Car, Coffee, Trees } from 'lucide-react';
import './Categories.css';

const CATEGORIES = [
  { label: 'Amazing pools', icon: <Waves size={24} /> },
  { label: 'Trending', icon: <Flame size={24} /> },
  { label: 'Camping', icon: <Tent size={24} /> },
  { label: 'Tropical', icon: <Palmtree size={24} /> },
  { label: 'Cabins', icon: <Warehouse size={24} /> },
  { label: 'Castles', icon: <Castle size={24} /> },
  { label: 'Amazing views', icon: <Mountain size={24} /> },
  { label: 'Camper vans', icon: <Car size={24} /> },
  { label: 'Bed & breakfasts', icon: <Coffee size={24} /> },
  { label: 'National parks', icon: <Trees size={24} /> },
];

const Categories = () => {
  return (
    <div className="categories-container container">
      <div className="categories-scroll">
        {CATEGORIES.map((cat, idx) => (
          <div key={idx} className={`category-item ${idx === 0 ? 'active' : ''}`}>
            {cat.icon}
            <span className="category-label">{cat.label}</span>
          </div>
        ))}
      </div>
      <div className="filters-btn-container">
        <button className="filters-btn">
          <svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" style={{display: 'block', height: '14px', width: '14px', fill: 'currentColor'}} aria-hidden="true" role="presentation" focusable="false"><path d="M5 8c1.306 0 2.418.835 2.83 2H14v2H7.829A3.001 3.001 0 1 1 5 8zm0 2a1 1 0 1 0 0 2 1 1 0 0 0 0-2zm6-8a3 3 0 1 1-2.829 4H2V4h6.17A3.001 3.001 0 0 1 11 2zm0 2a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"></path></svg>
          Filters
        </button>
      </div>
    </div>
  );
};

export default Categories;
