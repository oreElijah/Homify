'use client';

import React, { useState, ChangeEvent, FormEvent } from 'react';
import './housepage.css'; // create this for styling

type FormData = {
  bedrooms: number;
  bathrooms: number;
  toilets: number;
  parking_space: number;
  title: string;
  town: string;
  state: string;
};

type PredictionResult = {
    price: number;
    message?: string;
}

export default function HousePricePredictor() {
  const [formData, setFormData] = useState<FormData>({
    bedrooms: 1,
    bathrooms: 1,
    toilets: 1,
    parking_space: 0,
    title: '',
    town: '',
    state: ''
  });
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string>('');
  const [visible, setVisible] = useState(false);
//   const [result, setResult] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (
    e: ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: isNaN(Number(value)) ? value : Number(value),
    });
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/house_price_predictor', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data: PredictionResult= await res.json();
      setResult(data);
      setError('');
      setVisible(true);
    } catch (err) {
      setError("❌ Error connecting to backend.");
      setResult(null);
      setVisible(true);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>House Price Predictor</h1>
      <form onSubmit={handleSubmit}>
        <input type="number" name="bedrooms" placeholder="Bedrooms" required onChange={handleChange} />
        <input type="number" name="bathrooms" placeholder="Bathrooms" required onChange={handleChange} />
        <input type="number" name="toilets" placeholder="Toilets" required onChange={handleChange} />
        <input type="number" name="parking_space" placeholder="Parking Space" required onChange={handleChange} />

        <select name="title" required onChange={handleChange}>
          <option value="">Select Title</option>
          {/* Block of Flats:0
Detached Bungalow:1
Detached Duplex:2
Semi Detached Bungalow:3
Semi Detached Duplex:4
Terraced Bungalow:5
Terraced Duplexes:6 */}
          <option value="Block of Flats">Block of Flats</option>
          <option value="Detached Duplex">Detached Duplex</option>
          <option value="Semi Detached Bungalow">Semi Detached Bungalow</option>
          <option value="semi Detached Duplex">semi Detached Duplex</option>
          <option value="Terraced Bungalow">Terraced Bungalow</option>
          <option value="Terraced Duplexes">Terraced Duplexes</option>
        </select>

        <input type="text" name="town" placeholder="Town (e.g., Lekki)" required onChange={handleChange} />
        <input type="text" name="state" placeholder="State (e.g., Lagos)" required onChange={handleChange} />

        <button type="submit">{loading ? 'Predicting...' : 'Predict Price'}</button>
      </form>

      {result && (
        <div className="result visible">
          <h2><strong>Estimated Price:</strong> <span>{result.price }</span></h2>
          <h2><strong>Price range:</strong> <span>{result.message || 'N/A'}</span></h2>
        </div>
      )}
    </div>
  );
}
