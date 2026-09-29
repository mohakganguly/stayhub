import ListingCard from '../components/ListingCard';
import './Home.css';
import { Map } from 'lucide-react';

const MOCK_LISTINGS = [
  {
    id: '1',
    title: 'Beachfront Villa',
    location: 'Malibu, California',
    distance: '3,210 kilometers away',
    dates: 'Oct 12 - 17',
    price: 450,
    rating: 4.98,
    images: [
      'https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    id: '2',
    title: 'Cozy Cabin',
    location: 'Aspen, Colorado',
    distance: '1,050 kilometers away',
    dates: 'Nov 5 - 10',
    price: 210,
    rating: 4.85,
    images: [
      'https://images.unsplash.com/photo-1510798831971-661eb04b3739?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1449844908441-8829872d2607?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    id: '3',
    title: 'Modern Apartment',
    location: 'New York, New York',
    distance: '4,500 kilometers away',
    dates: 'Dec 1 - 5',
    price: 320,
    rating: 4.92,
    images: [
      'https://images.unsplash.com/photo-1502672260266-1c1529393681?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1484154218962-a197022b5858?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    id: '4',
    title: 'Treehouse Retreat',
    location: 'Bali, Indonesia',
    distance: '12,000 kilometers away',
    dates: 'Jan 15 - 22',
    price: 180,
    rating: 4.99,
    images: [
      'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1472224371017-08207f84aaae?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    id: '5',
    title: 'Desert Oasis',
    location: 'Sedona, Arizona',
    distance: '800 kilometers away',
    dates: 'Feb 10 - 14',
    price: 290,
    rating: 4.88,
    images: [
      'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    id: '6',
    title: 'Historic Castle',
    location: 'Edinburgh, Scotland',
    distance: '7,200 kilometers away',
    dates: 'Mar 1 - 7',
    price: 850,
    rating: 4.95,
    images: [
      'https://images.unsplash.com/photo-1533604100913-718224522956?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    id: '7',
    title: 'Lakeside Cabin',
    location: 'Lake Tahoe, California',
    distance: '2,900 kilometers away',
    dates: 'Apr 12 - 16',
    price: 340,
    rating: 4.75,
    images: [
      'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    id: '8',
    title: 'Ski Chalet',
    location: 'Chamonix, France',
    distance: '8,500 kilometers away',
    dates: 'Jan 5 - 12',
    price: 550,
    rating: 4.82,
    images: [
      'https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
    ]
  }
];

const Home = () => {
  return (
    <div className="home-page">
      <div className="container">
        <div className="listing-grid">
          {MOCK_LISTINGS.map(listing => (
            <ListingCard key={listing.id} listing={listing} />
          ))}
        </div>
      </div>
      
      <div className="map-toggle-container">
        <button className="map-toggle-btn hover-scale">
          Show map <Map size={18} />
        </button>
      </div>
    </div>
  );
};

export default Home;
