import { useEffect, useState } from "react";

export default function Events() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/events")
      .then(res => res.json())
      .then(setEvents)
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Events</h1>
      <ul className="space-y-2">
        {events.map(e => (
          <li key={e.id} className="border p-2 rounded bg-white shadow">
            <strong>{e.event_type}</strong> — {e.timestamp}
          </li>
        ))}
      </ul>
    </div>
  );
}
