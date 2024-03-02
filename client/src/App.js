import React from 'react';
import { Routes, Route } from 'react-router-dom';

import './assets/fonts.scss';
import './assets/reset.scss';
import './assets/global.scss';

import Header from './components/Header/Header';
import Footer from './components/Footer/Footer';

import routes from './routes';

function App() {
  return (
    <div className={`container`}>
      <Header />
      <Routes>
        {routes.map((route) => (
          <Route
            key={route.path}
            path={route.path}
            element={<route.page />}
          />
        ))}
      </Routes>
      <Footer />
    </div>
  );
}

export default App;
