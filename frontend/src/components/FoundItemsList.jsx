import React, { useEffect, useState } from "react";
import api from "../api";
import "../styles/FoundItemsList.css";
import { ACCESS_TOKEN, REFRESH_TOKEN, GOOGLE_ACCESS_TOKEN } from "../token";
const FoundItemsList = () => {
  const [foundItems, setFoundItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFoundItems = async () => {
      setLoading(true);
      try {
        const token = localStorage.getItem(GOOGLE_ACCESS_TOKEN);
        if (!token) {
          setError("User is not authenticated. Please log in again.");
          setLoading(false);
          return;
        }

        const response = await api.get("/api/lost-found/list/?status=found", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setFoundItems(response.data);
      } catch (error) {
        console.error("Error fetching found items:", error);
        setError("Failed to fetch found items. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchFoundItems();
  }, []);

  if (loading) {
    return <p className="loading-indicator">Loading found items...</p>;
  }

  if (error) {
    return <p className="error-message">{error}</p>;
  }

  return (
    <div className="found-items-container">
      <h2>Found Items</h2>
      {foundItems.length === 0 ? (
        <p>No found items available at the moment.</p>
      ) : (
        <div className="found-items-grid">
          {foundItems.map((item) => (
            <div key={item.id} className="found-item">
              <h3>{item.title}</h3>
              <p>{item.description}</p>
              {item.image && (
                <img
                  src={item.image}
                  alt={item.title}
                  className="found-item-image"
                />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FoundItemsList;
