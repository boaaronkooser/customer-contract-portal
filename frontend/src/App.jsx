import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import Customers from "./pages/Customers";
import Contracts from "./pages/Contracts";
import Events from "./pages/Events";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/customers" element={<Customers />} />
        <Route path="/contracts" element={<Contracts />} />
        <Route path="/events" element={<Events />} />
      </Routes>
    </Router>
  );
}

export default App;

