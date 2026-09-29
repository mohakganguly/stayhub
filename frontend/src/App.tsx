import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Navbar from './components/Navbar';
import Categories from './components/Categories';
import Footer from './components/Footer';

function App() {
  return (
    <Router>
      <div className="app-layout">
        <header style={{ position: 'fixed', top: 0, width: '100%', zIndex: 100, backgroundColor: 'var(--bg-color)', borderBottom: '1px solid var(--border-color)' }}>
          <Navbar />
          <Categories />
        </header>
        
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
          </Routes>
        </main>

        <Footer />
      </div>
    </Router>
  );
}

export default App;
