import { useState } from "react";


function WeatherCard({ city, temp, description, humidity, ai_summary }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 mt-4 max-w-sm">
      <h2 className="text-2xl font-bold text-gray-800">{city}</h2>
      <p className="text-5xl font-light text-green-600 my-2">{temp}°C</p>
      <p className="text-gray-500 capitalize">{description}</p>
      <p className="text-gray-500">Humidity: {humidity}%</p>
      <p className="text-blue-700 italic mt-3">{ai_summary}</p>
    </div>
  );
}

function App() {
  const [city, setCity] = useState("");
  const [weather, setWeather] = useState(null);

  async function handleSearch(event) {
    event.preventDefault();
    if (!city.trim()) return;

    setWeather(null); 
    try {
      const res = await fetch(`http://localhost:8000/api/weather/?city=${city}`);
      if (!res.ok) throw new Error("City not found");
      const data = await res.json();
      setWeather(data); 
    } catch (err) {
      alert(err.message);
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center pt-20">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Weather App</h1>

      <form onSubmit={handleSearch} className="flex gap-2">
        <input
          value={city}
          onChange={(e) => setCity(e.target.value)}
          placeholder="Enter a city..."
          className="border rounded px-4 py-2 w-64"
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Search
        </button>
      </form>

      {/* Only show the card if we have weather data */}
      {weather && (
        <WeatherCard
          city={weather.city}
          temp={weather.temp}
          description={weather.description}
          humidity={weather.humidity}
          ai_summary={weather.ai_summary}
        />
      )}
    </div>
  );
}

export default App;