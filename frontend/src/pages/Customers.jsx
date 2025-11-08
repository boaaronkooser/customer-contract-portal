import { useEffect, useState } from "react";

export default function Customers() {
  const [customers, setCustomers] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/customers")
      .then(res => res.json())
      .then(setCustomers)
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Customers</h1>
      <ul className="space-y-2">
        {customers.map(c => (
          <li key={c.id} className="border p-2 rounded bg-white shadow">
            <strong>{c.name}</strong><br />
            {c.email || "no email"}
          </li>
        ))}
      </ul>
    </div>
  );
}
