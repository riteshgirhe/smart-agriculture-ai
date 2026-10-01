import { useEffect, useState } from "react";
import "./styles.css";
import "./workbench.css";

const API_BASE_URL = import.meta.env.VITE_API_URL || "";
const numberField = (key, label, value, min = 0, max = 10000, step = "any") => ({ key, label, type: "number", value: String(value), min, max, step });
const selectField = (key, label, value, options) => ({ key, label, type: "select", value, options });
const dateField = (key, label, value) => ({ key, label, type: "date", value });

const services = [
  {
    id: "crop", title: "Crop recommendation", icon: "sprout", color: "mint",
    description: "Match soil nutrients and climate to a crop from the model's supported classes.",
    endpoint: "/api/crop/recommend", output: "Recommended crop",
    guidance: "Compare this shortlist with local growing conditions and recent field history.",
    fields: [
      numberField("N", "Nitrogen (N)", 90, 0, 200), numberField("P", "Phosphorus (P)", 42, 0, 200),
      numberField("K", "Potassium (K)", 43, 0, 200), numberField("temperature", "Temperature (°C)", 20.88, -20, 60),
      numberField("humidity", "Humidity (%)", 82, 0, 100), numberField("ph", "Soil pH", 6.5, 0, 14),
      numberField("rainfall", "Rainfall (mm)", 202.9, 0, 10000),
    ],
  },
  {
    id: "fertilizer", title: "Fertilizer recommendation", icon: "leaf", color: "violet",
    description: "Use measured soil, crop, season and previous-harvest features.",
    endpoint: "/api/fertilizer/predict", output: "Recommended fertilizer",
    guidance: "Check the result against a current soil test and local application guidance.",
    fields: [
      selectField("Soil_Type", "Soil type", "Clay", ["Clay", "Loamy", "Sandy", "Silt"]),
      numberField("Soil_pH", "Soil pH", 6.07, 0, 14), numberField("Soil_Moisture", "Soil moisture (%)", 34.98, 0, 100),
      numberField("Organic_Carbon", "Organic carbon", 0.32, 0, 10), numberField("Electrical_Conductivity", "Electrical conductivity", 1.87, 0, 100),
      numberField("Nitrogen_Level", "Nitrogen level", 61), numberField("Phosphorus_Level", "Phosphorus level", 44),
      numberField("Potassium_Level", "Potassium level", 84), numberField("Temperature", "Temperature (°C)", 19.84, -20, 60),
      numberField("Humidity", "Humidity (%)", 83.31, 0, 100), numberField("Rainfall", "Rainfall (mm)", 1693.22),
      selectField("Crop_Type", "Crop", "Cotton", ["Cotton", "Maize", "Potato", "Rice", "Sugarcane", "Tomato", "Wheat"]),
      selectField("Crop_Growth_Stage", "Growth stage", "Harvest", ["Flowering", "Harvest", "Sowing", "Vegetative"]),
      selectField("Season", "Season", "Kharif", ["Kharif", "Rabi", "Zaid"]),
      selectField("Irrigation_Type", "Irrigation type", "Canal", ["Canal", "Drip", "Rainfed", "Sprinkler"]),
      selectField("Previous_Crop", "Previous crop", "Wheat", ["Cotton", "Maize", "Potato", "Rice", "Sugarcane", "Tomato", "Wheat"]),
      selectField("Region", "Region", "South", ["Central", "East", "North", "South", "West"]),
      numberField("Fertilizer_Used_Last_Season", "Fertilizer used last season", 297.15),
      numberField("Yield_Last_Season", "Yield last season (t/ha)", 1.19, 0, 100),
    ],
  },
  {
    id: "irrigation", title: "Irrigation prediction", icon: "droplet", color: "blue",
    description: "Estimate irrigation need from soil, weather, crop and field conditions.",
    endpoint: "/api/irrigation/predict", output: "Irrigation need",
    guidance: "Check measured field moisture and near-term rain before scheduling irrigation.",
    fields: [
      selectField("Soil_Type", "Soil type", "Clay", ["Clay", "Loamy", "Sandy", "Silt"]),
      numberField("Soil_pH", "Soil pH", 6.14, 0, 14), numberField("Soil_Moisture", "Soil moisture (%)", 36.48, 0, 100),
      numberField("Organic_Carbon", "Organic carbon", 0.42, 0, 10), numberField("Electrical_Conductivity", "Electrical conductivity", 2.17, 0, 100),
      numberField("Temperature_C", "Temperature (°C)", 21.9, -20, 60), numberField("Humidity", "Humidity (%)", 31.19, 0, 100),
      numberField("Rainfall_mm", "Rainfall (mm)", 1167.7), numberField("Sunlight_Hours", "Sunlight hours", 4.01, 0, 24),
      numberField("Wind_Speed_kmh", "Wind speed (km/h)", 1.97, 0, 300),
      selectField("Crop_Type", "Crop", "Wheat", ["Cotton", "Maize", "Potato", "Rice", "Sugarcane", "Wheat"]),
      selectField("Crop_Growth_Stage", "Growth stage", "Vegetative", ["Flowering", "Harvest", "Sowing", "Vegetative"]),
      selectField("Season", "Season", "Rabi", ["Kharif", "Rabi", "Zaid"]),
      selectField("Irrigation_Type", "Irrigation type", "Rainfed", ["Canal", "Drip", "Rainfed", "Sprinkler"]),
      selectField("Water_Source", "Water source", "Reservoir", ["Groundwater", "Rainwater", "Reservoir", "River"]),
      numberField("Field_Area_hectare", "Field area (hectares)", 4.73, 0.01, 10000),
      selectField("Mulching_Used", "Mulching used", "Yes", ["No", "Yes"]),
      numberField("Previous_Irrigation_mm", "Previous irrigation (mm)", 1.98),
      selectField("Region", "Region", "South", ["Central", "East", "North", "South", "West"]),
    ],
  },
  {
    id: "price", title: "Price prediction", icon: "chart", color: "gold",
    description: "Estimate modal commodity price from the provided market attributes.",
    endpoint: "/api/price/predict", output: "Estimated modal price",
    guidance: "Treat this as a historical-model estimate and confirm current local market prices.",
    fields: [
      dateField("month", "Month", "2025-03-01"),
      selectField("commodity_name", "Commodity", "Maize", ["Barley (Jau)", "Coconut", "Coffee", "Cotton", "Ginger(Dry)", "Groundnut", "Jowar(Sorghum)", "Maize", "Millets", "Rice", "Sugar", "Sugarcane", "Sunflower", "Tea", "Turmeric", "Wheat"]),
      selectField("state_name", "State", "India", ["India"]), selectField("district_name", "District", "All", ["All"]),
      numberField("avg_min_price", "Average minimum price (₹)", 2191.23),
      numberField("avg_max_price", "Average maximum price (₹)", 2402.98),
      selectField("calculationType", "Calculation type", "Monthly", ["Monthly"]),
      numberField("change", "Recent change (%)", -14.43, -100000, 100000),
    ],
  },
  {
    id: "yield", title: "Yield prediction", icon: "chart", color: "orange",
    description: "Estimate yield from crop, field size, planting date and growing inputs.",
    endpoint: "/api/yield/predict", output: "Estimated yield",
    guidance: "Use this estimate for planning; actual yield depends on conditions through harvest.",
    fields: [
      selectField("Crop_Type", "Crop", "Soybean", ["Cotton", "Groundnut", "Maize", "Onion", "Potato", "Rice", "Soybean", "Sugarcane", "Wheat"]),
      numberField("Field_Size_hectares", "Field size (hectares)", 1.04, 0.01, 10000),
      dateField("Planting_Date", "Planting date", "2025-06-08"),
      selectField("Soil_Type", "Soil type", "Loamy", ["Alluvial", "Chalky", "Clay", "Laterite", "Loamy", "Peaty", "Sandy", "Silty"]),
      selectField("Fertilizer_Used", "Fertilizer used", "Urea", ["Ammonium Sulphate", "Biofertilizers", "Compost/Organic Manure", "DAP", "MOP", "NPK", "Urea"]),
      selectField("Irrigation_Type", "Irrigation type", "Furrow/Canal irrigation", ["Drip Irrigation", "Flood Irrigation", "Furrow/Canal irrigation", "Rainfed", "Sprinkler Irrigation"]),
    ],
  },
];

const iconPaths = {
  grid: <><rect x="3" y="3" width="7" height="7" rx="1" /><rect x="14" y="3" width="7" height="7" rx="1" /><rect x="3" y="14" width="7" height="7" rx="1" /><rect x="14" y="14" width="7" height="7" rx="1" /></>,
  sprout: <><path d="M12 21V11" /><path d="M12 15c-3.8 0-6-2.2-6-6 3.8 0 6 2.2 6 6Z" /><path d="M12 12c0-3.8 2.2-6 6-6 0 3.8-2.2 6-6 6Z" /></>,
  droplet: <path d="M12 3.5S5.8 10.1 5.8 14.7a6.2 6.2 0 0 0 12.4 0C18.2 10.1 12 3.5 12 3.5Z" />,
  chart: <><path d="M4 19V5" /><path d="M4 19h16" /><path d="m7 15 3-4 3 2 5-6" /></>,
  leaf: <><path d="M20 4C10 4 4 8 4 15c0 3 2 5 5 5 7 0 11-6 11-16Z" /><path d="M4 20c3-5 7-8 12-10" /></>,
  arrow: <><path d="M5 12h14" /><path d="m13 6 6 6-6 6" /></>,
  sun: <><circle cx="12" cy="12" r="4" /><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" /></>,
};

function Icon({ name, size = 20 }) {
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{iconPaths[name]}</svg>;
}

async function getJSON(path) {
  const response = await fetch(`${API_BASE_URL}${path}`);
  const data = await response.json();
  if (!response.ok) throw new Error(typeof data.detail === "string" ? data.detail : "The service could not complete this request.");
  return data;
}

function formatPrediction(service, value) {
  if (service.id === "price") return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 2 }).format(Number(value));
  if (service.id === "yield") return `${Number(value).toFixed(2)} t/ha`;
  return String(value).replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function PredictionPage({ service, onBack }) {
  const [values, setValues] = useState(() => Object.fromEntries(service.fields.map((field) => [field.key, field.value])));
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_BASE_URL}${service.endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(typeof data.detail === "string" ? data.detail : "Check the submitted values and try again.");
      setPrediction(data.prediction);
    } catch (requestError) {
      setError(requestError.message);
      setPrediction(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="service-page">
      <button className="back-button" onClick={onBack}><Icon name="arrow" size={16} /> All services</button>
      <div className="service-page-header"><div className={`service-page-icon ${service.color}`}><Icon name={service.icon} size={28} /></div><div><span className="section-kicker">MODEL WORKSPACE</span><h1>{service.title}</h1><p>{service.description}</p></div></div>
      <div className="service-layout">
        <form className="input-card" onSubmit={submit}>
          <div className="input-card-heading"><div><span className="section-kicker">MODEL INPUTS</span><h2>Field and market data</h2></div><span className="step-count">{service.fields.length} inputs</span></div>
          <p className="sample-note">Prefilled with an example row from this project's dataset. Edit values to match your case.</p>
          <div className="service-form-grid">{service.fields.map((field) => <label className="field-label" key={field.key}>{field.label}{field.type === "select" ? <select required value={values[field.key]} onChange={(event) => { setValues((current) => ({ ...current, [field.key]: event.target.value })); setPrediction(null); setError(""); }}>{field.options.map((option) => <option key={option} value={option}>{option}</option>)}</select> : <input required type={field.type} min={field.min} max={field.max} step={field.step} value={values[field.key]} onChange={(event) => { setValues((current) => ({ ...current, [field.key]: event.target.value })); setPrediction(null); setError(""); }} />}</label>)}</div>
          <button className="primary-service-button" type="submit" disabled={loading}>{loading ? "Running model…" : "Generate prediction"}<Icon name="arrow" size={17} /></button>
          {error && <p className="form-error" role="alert">{error}</p>}
        </form>
        <aside className={`service-result ${prediction !== null ? "result-ready" : ""}`} aria-live="polite">
          <span className="result-label">MODEL RESULT</span><div className={`result-orb ${service.color}`}><Icon name={service.icon} size={34} /></div>
          <p className="result-intro">{prediction !== null ? service.output : "Result appears after prediction"}</p>
          <strong>{prediction !== null ? formatPrediction(service, prediction) : "—"}</strong>
          <div className="recommendation-note"><span>Next step</span><p>{prediction !== null ? service.guidance : "Submit the inputs to get an output from the trained model."}</p></div>
          <small className="frontend-note">Model output is decision support, not a guaranteed outcome.</small>
        </aside>
      </div>
    </section>
  );
}

function WeatherPage({ weather, loading, error, onRetry }) {
  return (
    <section className="workspace-page">
      <div className="workspace-page-heading"><div><span className="section-kicker">WEATHER</span><h1>Local conditions</h1><p>Current conditions and forecast supplied by OpenWeather.</p></div><button className="filter-button" onClick={onRetry} disabled={loading}>{loading ? "Updating…" : "Refresh"}</button></div>
      {error && <div className="state-message error-state" role="alert"><strong>Weather unavailable</strong><p>{error}</p></div>}
      {loading && !weather && <div className="state-message">Loading current conditions…</div>}
      {weather && <><div className="weather-dashboard"><div className="current-weather"><div className="weather-sun large"><Icon name="sun" size={39} /></div><div><strong>{weather.current.temperature}°</strong><span>{weather.current.description}</span><small>{weather.location}{weather.country ? `, ${weather.country}` : ""}</small></div></div><div className="weather-reading"><span>Humidity</span><strong>{weather.current.humidity}%</strong></div><div className="weather-reading"><span>Wind speed</span><strong>{weather.current.wind_speed} km/h</strong></div><div className="weather-reading"><span>Rain chance</span><strong>{weather.current.rain_probability}%</strong></div></div>
        <div className="forecast-card"><div className="panel-heading"><div><span className="section-kicker">FORECAST</span><h3>Upcoming conditions</h3></div></div><div className="forecast-row">{weather.forecast.map((day) => <div key={day.date}><span>{new Date(`${day.date}T12:00:00`).toLocaleDateString(undefined, { weekday: "short" })}</span><Icon name={day.rain_probability > 40 ? "droplet" : "sun"} size={22} /><strong>{day.high}° / {day.low}°</strong><small>{day.rain_probability}% rain</small></div>)}</div></div>
      </>}
    </section>
  );
}

function App() {
  const [page, setPage] = useState("overview");
  const [selectedService, setSelectedService] = useState(null);
  const [health, setHealth] = useState(null);
  const [healthLoading, setHealthLoading] = useState(true);
  const [healthError, setHealthError] = useState("");
  const [weather, setWeather] = useState(null);
  const [weatherError, setWeatherError] = useState("");
  const [weatherLoading, setWeatherLoading] = useState(false);

  const loadWeather = async () => {
    setWeatherLoading(true);
    setWeatherError("");
    try {
      setWeather(await getJSON("/api/weather"));
    } catch (requestError) {
      setWeatherError(requestError.message);
    } finally {
      setWeatherLoading(false);
    }
  };

  useEffect(() => {
    getJSON("/health").then(setHealth).catch((requestError) => setHealthError(requestError.message)).finally(() => setHealthLoading(false));
    loadWeather();
  }, []);

  const goOverview = () => {
    setSelectedService(null);
    setPage("overview");
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <button className="brand" onClick={goOverview} aria-label="AgriSense AI overview"><span className="brand-mark"><Icon name="leaf" size={22} /></span><span>AgriSense <b>AI</b></span></button>
        <div className="workspace-label">WORKSPACE</div>
        <nav className="main-nav" aria-label="Main navigation"><button className={`nav-item ${page === "overview" && !selectedService ? "active" : ""}`} onClick={goOverview}><Icon name="grid" size={19} /><span>Overview</span></button><button className={`nav-item ${page === "weather" ? "active" : ""}`} onClick={() => { setSelectedService(null); setPage("weather"); }}><Icon name="sun" size={19} /><span>Weather</span></button></nav>
        <div className="sidebar-bottom"><div className="sidebar-note"><Icon name="sprout" size={20} /><strong>Decision support for agriculture</strong><p>Five trained models and live weather in one workspace.</p></div></div>
      </aside>
      <main className="main-content">
        <header className="topbar"><button className="mobile-menu" onClick={goOverview} aria-label="Go to overview"><Icon name="grid" /></button><div className="breadcrumb"><span>AgriSense AI</span><b>/</b><strong>{selectedService?.title || (page === "weather" ? "Weather" : "Overview")}</strong></div><div className="top-actions"><span className={`sync-status ${health?.status === "ok" ? "online" : ""}`}><i />{health?.status === "ok" ? "API connected" : healthLoading ? "Checking API" : "API unavailable"}</span><div className="user-badge"><span className="user-avatar">RG</span><span className="user-name">Ritesh Girhe</span></div></div></header>
        <nav className="mobile-nav" aria-label="Mobile navigation"><button className={!selectedService && page === "overview" ? "active" : ""} onClick={goOverview}>Overview</button><button className={page === "weather" ? "active" : ""} onClick={() => { setSelectedService(null); setPage("weather"); }}>Weather</button></nav>
        <div className="page-content">{selectedService ? <PredictionPage key={selectedService.id} service={selectedService} onBack={goOverview} /> : page === "weather" ? <WeatherPage weather={weather} loading={weatherLoading} error={weatherError} onRetry={loadWeather} /> : <section className="workspace-page">
          <div className="workspace-page-heading"><div><span className="section-kicker">AGRICULTURE INTELLIGENCE</span><h1>AgriSense AI</h1><p>Move from field inputs to model output and a practical next step.</p></div><span className={`live-chip ${health?.status === "ok" ? "healthy" : ""}`}><i />{health?.status === "ok" ? "API online" : healthLoading ? "Connecting" : "API unavailable"}</span></div>
          <div className="connection-grid"><article className="connection-card"><span>API status</span><strong>{health?.status === "ok" ? "Online" : healthLoading ? "Checking" : "Unavailable"}</strong><small>{health?.service || healthError || "Waiting for backend health check"}</small></article><article className="connection-card"><span>Model artifacts</span><strong>{health ? `${health.models_available} / ${health.models_total}` : "—"}</strong><small>Available to serve predictions</small></article><article className="connection-card"><span>Weather source</span><strong>{weather ? `${weather.current.temperature}°` : weatherLoading ? "Loading" : "Unavailable"}</strong><small>{weather ? `${weather.location} · ${weather.current.description}` : weatherError || "Live provider data"}</small></article></div>
          <div className="section-heading services-heading"><div><span className="section-kicker">PREDICTION WORKFLOWS</span><h2>Choose a model</h2></div><p>Each result is generated from submitted inputs.</p></div>
          <div className="services-grid">{services.map((service) => <button className="service-card" key={service.id} onClick={() => setSelectedService(service)}><span className={`service-icon ${service.color}`}><Icon name={service.icon} size={25} /></span><span className="service-card-copy"><strong>{service.title}</strong><small>{service.description}</small><em>Open model <Icon name="arrow" size={14} /></em></span></button>)}</div>
          {weatherError && <div className="state-message weather-inline"><strong>Weather integration unavailable</strong><p>{weatherError}</p><button className="text-button" onClick={loadWeather}>Retry weather request <Icon name="arrow" size={15} /></button></div>}
        </section>}</div>
      </main>
    </div>
  );
}

export default App;