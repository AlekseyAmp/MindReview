import Main from './pages/Main/Main';
import Register from './pages/Register/Register';
import Login from './pages/Login/Login';
import Analyze from './pages/Analyze/Analyze';

const routes = [
    {
      path: '/',
      page: Main,
    },
    {
      path: '/register',
      page: Register,
    },
    {
      path: '/login',
      page: Login,
    },
    {
      path: '/analyze',
      page: Analyze,
    }

]

export default routes;