import { Heart, Star, ChevronLeft, ChevronRight } from 'lucide-react';
import './ListingCard.css';
import { useState } from 'react';

interface ListingProps {
  id: string;
  title: string;
  location: string;
  distance: string;
  dates: string;
  price: number;
  rating: number;
  images: string[];
}

const ListingCard = ({ listing }: { listing: ListingProps }) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [isHovered, setIsHovered] = useState(false);

  const nextImage = (e: React.MouseEvent) => {
    e.preventDefault();
    setCurrentImageIndex((prev) => (prev + 1) % listing.images.length);
  };

  const prevImage = (e: React.MouseEvent) => {
    e.preventDefault();
    setCurrentImageIndex((prev) => (prev - 1 + listing.images.length) % listing.images.length);
  };

  return (
    <div 
      className="listing-card hover-scale"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="listing-image-container">
        <img 
          src={listing.images[currentImageIndex]} 
          alt={listing.title} 
          className="listing-image" 
        />
        
        <button className="favorite-btn">
          <Heart size={24} fill="rgba(0,0,0,0.5)" stroke="white" strokeWidth={2} />
        </button>

        {isHovered && listing.images.length > 1 && (
          <>
            <button className="carousel-btn prev" onClick={prevImage}>
              <ChevronLeft size={16} />
            </button>
            <button className="carousel-btn next" onClick={nextImage}>
              <ChevronRight size={16} />
            </button>
          </>
        )}
        
        <div className="carousel-dots">
          {listing.images.map((_, idx) => (
            <span 
              key={idx} 
              className={`dot ${idx === currentImageIndex ? 'active' : ''}`}
            ></span>
          ))}
        </div>
      </div>

      <div className="listing-info">
        <div className="flex justify-between items-center mt-3">
          <h3 className="listing-location">{listing.location}</h3>
          <span className="listing-rating">
            <Star size={14} fill="var(--text-dark)" /> {listing.rating}
          </span>
        </div>
        <p className="listing-distance">{listing.distance}</p>
        <p className="listing-dates">{listing.dates}</p>
        <div className="listing-price-container mt-2">
          <span className="listing-price">${listing.price}</span> night
        </div>
      </div>
    </div>
  );
};

export default ListingCard;
