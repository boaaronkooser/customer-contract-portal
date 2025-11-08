import { useEffect, useState } from "react";

export default function Contracts() {
  const [contracts, setContracts] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/contracts")
      .then(res => res.json())
      .then(setContracts)
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Contracts</h1>
      <table className="w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th>ID</th>
            <th>Customer ID</th>
            <th>Status</th>
            <th>Type</th>
          </tr>
        </thead>
        <tbody>
          {contracts.map(c => (
            <tr key={c.id} className="border-t">
              <td>{c.id}</td>
              <td>{c.customer_id}</td>
              <td>{c.status}</td>
              <td>{c.type}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
