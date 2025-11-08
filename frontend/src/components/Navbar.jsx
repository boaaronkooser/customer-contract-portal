import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-blue-700 text-white p-4 shadow-md flex justify-between items-center">
      <h1 className="text-xl font-semibold">Bank Backoffice Portal</h1>
      <div className="flex gap-6">
        <Link className="hover:text-yellow-300" to="/">Dashboard</Link>
        <Link className="hover:text-yellow-300" to="/customers">Customers</Link>
        <Link className="hover:text-yellow-300" to="/contracts">Contracts</Link>
        <Link className="hover:text-yellow-300" to="/events">Events</Link>
      </div>
    </nav>
  );
}
