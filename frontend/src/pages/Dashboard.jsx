import { useEffect, useState } from "react";

export default function Dashboard() {
  const [stats, setStats] = useState({ customers: 0, contracts: 0, events: 0 });

  useEffect(() => {
    Promise.all([
      fetch("http://127.0.0.1:8000/customers").then(r => r.json()),
      fetch("http://127.0.0.1:8000/contracts").then(r => r.json()),
      fetch("http://127.0.0.1:8000/events").then(r => r.json())
    ]).then(([cust, cont, ev]) =>
      setStats({
        customers: cust.length,
        contracts: cont.length,
        events: ev.length,
      })
    );
  }, []);

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-3 gap-6">
        <div className="bg-white p-4 rounded-lg shadow hover:shadow-lg transition">
          <h2 className="text-gray-500">Customers</h2>
          <p className="text-3xl font-bold text-blue-600">{stats.customers}</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow hover:shadow-lg transition">
          <h2 className="text-gray-500">Contracts</h2>
          <p className="text-3xl font-bold text-blue-600">{stats.contracts}</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow hover:shadow-lg transition">
          <h2 className="text-gray-500">Events</h2>
          <p className="text-3xl font-bold text-blue-600">{stats.events}</p>
        </div>
      </div>
    </div>
  );
}
