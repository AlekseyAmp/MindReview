import Register from "./pages/Register/Register";
import Login from "./pages/Login/Login";
import Main from "./pages/Main/Main";
import Analyze from "./pages/Analyze/Analyze";
import Archive from "./pages/Archive/Archive";
import Feedback from "./pages/Feedback/Feedback";
import Profile from "./pages/Profile/Profile";
import Premium from "./pages/Premium/Premium";
import Admin from "./pages/Admin/Admin";

const routes = [
  {
    path: "/",
    page: Main,
  },
  {
    path: "/register",
    page: Register,
  },
  {
    path: "/login",
    page: Login,
  },
  {
    path: "/analyze/:analyze_id",
    page: Analyze,
  },
  {
    path: "/archive",
    page: Archive,
  },
  {
    path: "/feedback",
    page: Feedback,
  },
  {
    path: "/profile",
    page: Profile,
  },
  {
    path: "/premium",
    page: Premium,
  },
  {
    path: "/admin",
    page: Admin,
  },
];

export default routes;
