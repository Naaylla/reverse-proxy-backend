# 🎮 Game Logic Design - City Management Clicking Game

## Concept: "Global City Manager"

A city management clicking game where real-world data affects your city's economy, environment, and citizen happiness.

---

## 🎯 Game Loop

```javascript
// Frontend fetches state every 30-60 seconds
setInterval(async () => {
  const state = await fetchGameState();
  updateCityMetrics(state);
  checkCityHealth();
  triggerEvents(state);
}, 30000); // 30 seconds
```

---

## 📊 How Raw Values Transform Into Game Mechanics

### 1. Economy System (from BTC/ETH/SOL prices)

**Raw Value:** `btc_usd: 68421`

**Game Logic:**

```javascript
// Transform crypto prices into city economy metrics
function calculateEconomyHealth(cryptoData) {
  const btcPrice = cryptoData.btc_usd;
  
  // Example thresholds
  let economyStatus;
  let taxRevenue;
  let unemploymentRate;
  
  if (btcPrice > 70000) {
    economyStatus = "BOOMING";
    taxRevenue = 1000; // coins per click
    unemploymentRate = 2; // %
    
  } else if (btcPrice > 50000) {
    economyStatus = "STABLE";
    taxRevenue = 500;
    unemploymentRate = 5;
    
  } else if (btcPrice > 30000) {
    economyStatus = "RECESSION";
    taxRevenue = 250;
    unemploymentRate = 10;
    
  } else {
    economyStatus = "CRISIS";
    taxRevenue = 100;
    unemploymentRate = 20;
  }
  
  return { economyStatus, taxRevenue, unemploymentRate };
}

// Price changes trigger events
function checkEconomyEvents(currentPrice, previousPrice) {
  const percentChange = ((currentPrice - previousPrice) / previousPrice) * 100;
  
  if (percentChange > 10) {
    showNotification("🚀 Economic Boom! Tech sector attracts investors!");
    unlockBuilding("CRYPTO_EXCHANGE");
    
  } else if (percentChange < -10) {
    showNotification("📉 Market Crash! Citizens are worried.");
    increaseCrimeRate(5);
  }
}
```

**Game Effects:**
- 💰 **High BTC** → More tax revenue per click, unlock premium buildings
- 📉 **Low BTC** → Reduced income, citizens demand welfare programs
- 📈 **Rising prices** → Unlock "Crypto Exchange" building
- 💸 **Falling prices** → Trigger "Financial Crisis" event

---

### 2. Weather System (from temperature & wind speed)

**Raw Values:** `temperature: 22, wind_speed: 15.2`

**Game Logic:**

```javascript
function calculateWeatherEffects(weatherData) {
  const temp = weatherData.temperature;
  const wind = weatherData.wind_speed;
  
  // Temperature effects
  let productivityModifier;
  let energyDemand;
  let touristAttraction;
  
  if (temp >= 15 && temp <= 25) {
    // Perfect weather
    productivityModifier = 1.2; // +20% efficiency
    energyDemand = "LOW";
    touristAttraction = 1.5; // +50% tourists
    
  } else if (temp < 0 || temp > 35) {
    // Extreme weather
    productivityModifier = 0.7; // -30% efficiency
    energyDemand = "VERY_HIGH"; // AC/Heating
    touristAttraction = 0.5; // -50% tourists
    
  } else {
    productivityModifier = 1.0;
    energyDemand = "MODERATE";
    touristAttraction = 1.0;
  }
  
  // Wind speed effects
  let windPowerGeneration;
  let constructionSafety;
  
  if (wind > 20) {
    windPowerGeneration = "EXCELLENT"; // Wind turbines at max
    constructionSafety = "DANGEROUS"; // Can't build
    showAlert("⚠️ High winds! Construction halted.");
    
  } else if (wind > 10) {
    windPowerGeneration = "GOOD";
    constructionSafety = "SAFE";
    
  } else {
    windPowerGeneration = "POOR";
    constructionSafety = "SAFE";
  }
  
  return {
    productivityModifier,
    energyDemand,
    touristAttraction,
    windPowerGeneration,
    constructionSafety
  };
}

// Weather changes trigger seasonal events
function checkWeatherEvents(temp) {
  if (temp > 30) {
    triggerEvent({
      title: "🌡️ Heatwave!",
      description: "Citizens need cooling centers",
      action: "Build AC units or lose happiness",
      cost: 5000
    });
  }
  
  if (temp < 5) {
    triggerEvent({
      title: "❄️ Cold Snap!",
      description: "Heating costs surge",
      action: "Energy bills +50%",
      duration: "2 minutes"
    });
  }
}
```

**Game Effects:**
- ☀️ **Perfect weather (15-25°C)** → Productivity boost, more tourists
- 🥵 **Hot weather (>30°C)** → Need cooling, energy costs up
- 🥶 **Cold weather (<5°C)** → Heating demand, construction slowed
- 💨 **Windy (>10 km/h)** → Wind turbines generate bonus power
- 🌪️ **Very windy (>20 km/h)** → Can't build tall buildings

---

### 3. Air Quality System (from PM10 levels)

**Raw Value:** `pm10: 45`

**Game Logic:**

```javascript
function calculateAirQualityEffects(airData) {
  const pm10 = airData.pm10;
  
  // WHO Air Quality Guidelines:
  // Good: 0-20, Moderate: 21-50, Unhealthy: 51-100, Hazardous: 100+
  
  let airQualityStatus;
  let citizenHealth;
  let hospitalLoad;
  let touristWarning;
  
  if (pm10 <= 20) {
    airQualityStatus = "EXCELLENT";
    citizenHealth = 100; // %
    hospitalLoad = "LOW";
    touristWarning = false;
    unlockAchievement("GREEN_CITY");
    
  } else if (pm10 <= 50) {
    airQualityStatus = "MODERATE";
    citizenHealth = 85;
    hospitalLoad = "NORMAL";
    touristWarning = false;
    
  } else if (pm10 <= 100) {
    airQualityStatus = "UNHEALTHY";
    citizenHealth = 60;
    hospitalLoad = "HIGH";
    touristWarning = true;
    showAlert("🏥 Air pollution causing health issues!");
    
  } else {
    airQualityStatus = "HAZARDOUS";
    citizenHealth = 30;
    hospitalLoad = "CRITICAL";
    touristWarning = true;
    triggerCrisis("POLLUTION_EMERGENCY");
  }
  
  // Calculate effects
  const healthcareCost = Math.max(0, (pm10 - 20) * 10); // Cost increases with pollution
  const happinessReduction = Math.max(0, pm10 - 30); // Happiness drops when air is bad
  
  return {
    airQualityStatus,
    citizenHealth,
    hospitalLoad,
    healthcareCost,
    happinessReduction,
    touristWarning
  };
}

// Pollution triggers action requirements
function checkPollutionActions(pm10) {
  if (pm10 > 60) {
    showUrgentAction({
      title: "🚨 Pollution Crisis",
      options: [
        { action: "Build Parks", cost: 10000, effect: "-20% pollution (visual)" },
        { action: "Ban Cars", cost: 0, effect: "Citizens angry, -30 happiness" },
        { action: "Install Filters", cost: 25000, effect: "-40% pollution (visual)" }
      ]
    });
  }
}
```

**Game Effects:**
- 🟢 **Good air (PM10 < 20)** → Unlock "Green City" achievement
- 🟡 **Moderate (20-50)** → Normal operations
- 🟠 **Unhealthy (50-100)** → Healthcare costs increase, happiness drops
- 🔴 **Hazardous (>100)** → Crisis mode! Must build parks/filters

---

## 🎮 Complete Game Loop Example

```javascript
// Main game state manager
class CityManager {
  constructor() {
    this.cityStats = {
      population: 1000,
      happiness: 100,
      money: 10000,
      buildings: [],
      resources: {
        energy: 100,
        food: 100,
        healthcare: 50
      }
    };
    
    this.realWorldState = null;
    this.updateInterval = null;
  }
  
  async start() {
    // Initial fetch
    await this.updateRealWorldState();
    
    // Update every 30 seconds
    this.updateInterval = setInterval(() => {
      this.updateRealWorldState();
    }, 30000);
  }
  
  async updateRealWorldState() {
    try {
      // Call YOUR backend gateway
      const response = await fetch('/api/state', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          economy: { asset: 'btc' }, // or let player choose
          weather: { country: this.cityStats.location },
          air: { country: this.cityStats.location }
        })
      });
      
      const data = await response.json();
      this.realWorldState = data;
      
      // Apply game logic to raw values
      this.applyEconomyEffects(data.economy);
      this.applyWeatherEffects(data.weather);
      this.applyAirQualityEffects(data.air);
      
      // Update UI
      this.render();
      
    } catch (error) {
      console.error('Failed to update city state:', error);
      // Game continues with last known state
    }
  }
  
  applyEconomyEffects(economy) {
    if (!economy) return;
    
    const { economyStatus, taxRevenue } = calculateEconomyHealth(economy);
    
    this.cityStats.taxRevenuePerClick = taxRevenue;
    this.cityStats.economyStatus = economyStatus;
    
    // Update building costs based on economy
    if (economyStatus === "BOOMING") {
      this.cityStats.buildingCostMultiplier = 1.5; // Inflation
    } else if (economyStatus === "CRISIS") {
      this.cityStats.buildingCostMultiplier = 0.7; // Deflation
    }
  }
  
  applyWeatherEffects(weather) {
    if (!weather) return;
    
    const effects = calculateWeatherEffects(weather);
    
    // Modify all production buildings
    this.cityStats.buildings.forEach(building => {
      building.currentProduction = 
        building.baseProduction * effects.productivityModifier;
    });
    
    // Adjust energy demand
    this.cityStats.resources.energyDemand = effects.energyDemand;
    
    // Wind turbines produce more in windy conditions
    const windTurbines = this.cityStats.buildings.filter(b => b.type === 'WIND_TURBINE');
    windTurbines.forEach(turbine => {
      if (weather.wind_speed > 15) {
        turbine.currentProduction *= 2; // Double output!
      }
    });
  }
  
  applyAirQualityEffects(air) {
    if (!air) return;
    
    const effects = calculateAirQualityEffects(air);
    
    // Reduce happiness based on air quality
    this.cityStats.happiness -= effects.happinessReduction / 10;
    
    // Increase healthcare costs
    this.cityStats.expenses.healthcare += effects.healthcareCost;
    
    // Visual effects
    if (effects.airQualityStatus === "HAZARDOUS") {
      this.showPollutionOverlay(); // Gray out the city
    }
  }
  
  // Player clicks to earn money
  onCityClick() {
    const revenue = this.cityStats.taxRevenuePerClick;
    this.cityStats.money += revenue;
    
    showFloatingText(`+$${revenue}`, 'green');
    this.render();
  }
  
  // Player builds something
  buildBuilding(buildingType) {
    const cost = BUILDING_COSTS[buildingType] * this.cityStats.buildingCostMultiplier;
    
    if (this.cityStats.money >= cost) {
      this.cityStats.money -= cost;
      this.cityStats.buildings.push(new Building(buildingType));
      this.render();
    }
  }
}

// Start the game
const game = new CityManager();
game.start();
```

---

## 🎨 UI/UX Integration

### Dashboard Display

```
┌─────────────────────────────────────────┐
│  🏙️ GLOBAL CITY MANAGER                │
├─────────────────────────────────────────┤
│  📍 Location: Algeria                   │
│                                         │
│  💰 ECONOMY: BOOMING                    │
│  ├─ BTC: $68,421 (+5.2%)               │
│  ├─ Tax Revenue: $1,000/click          │
│  └─ Treasury: $45,320                   │
│                                         │
│  🌡️ WEATHER: PERFECT                   │
│  ├─ Temperature: 22°C                   │
│  ├─ Wind: 15.2 km/h                    │
│  └─ Productivity: +20%                  │
│                                         │
│  🌫️ AIR QUALITY: MODERATE              │
│  ├─ PM10: 45 µg/m³                     │
│  ├─ Health: 85%                         │
│  └─ Healthcare Cost: $250/min           │
│                                         │
│  😊 Citizen Happiness: 87%              │
│  👥 Population: 12,450                  │
└─────────────────────────────────────────┘

[CLICK TO COLLECT TAXES]  💰 +$1,000

Buildings Available:
[🏢 Office] $5,000  [🏥 Hospital] $10,000
[🌳 Park] $3,000    [💨 Wind Turbine] $15,000
```

### Event System

```javascript
// Random events based on real-world data
function triggerDynamicEvents(state) {
  // Economic events
  if (state.economy.btc_usd > 70000) {
    showEvent({
      title: "💎 Tech Boom",
      description: "Silicon Valley companies want to open offices in your city!",
      choices: [
        { text: "Accept", effect: "+5000 population, +$50k" },
        { text: "Decline", effect: "Keep current pace" }
      ]
    });
  }
  
  // Weather events
  if (state.weather.temperature > 30 && state.weather.wind_speed < 5) {
    showEvent({
      title: "🔥 Heatwave Crisis",
      description: "Citizens are suffering! Air conditioning demand surges.",
      action: "Energy costs +100% for 2 minutes"
    });
  }
  
  // Pollution events
  if (state.air.pm10 > 80) {
    showEvent({
      title: "😷 Health Alert",
      description: "Air pollution is causing respiratory problems!",
      choices: [
        { text: "Build 3 Parks", cost: 30000, effect: "Improve air (visual)" },
        { text: "Ignore", effect: "-20 happiness, +hospital costs" }
      ]
    });
  }
}
```

---

## 🎯 Game Progression

### Early Game (First 5 minutes)
- Learn clicking mechanic
- See how BTC price affects income
- Build first few buildings
- Notice weather affecting productivity

### Mid Game (5-15 minutes)
- Manage multiple systems simultaneously
- Deal with pollution from growth
- Optimize buildings based on real-world conditions
- Unlock special buildings based on data

### Late Game (15+ minutes)
- Automated systems
- Balance all three metrics
- Compete on leaderboards
- Unlock different cities/countries

---

## 🏆 Achievement Ideas

Based on real-world data:

- **"Perfect Storm"** - Play during ideal conditions (temp 20-25°C, PM10 < 20, BTC > $60k)
- **"Green Champion"** - Maintain PM10 below 20 for 10 minutes
- **"Bull Market"** - Collect taxes during BTC > $70k
- **"Climate Survivor"** - Survive extreme weather event (temp < 0 or > 35)
- **"Crypto Millionaire"** - Earn $1M during economic boom
- **"Wind Master"** - Generate 100% of energy from wind during high winds

---

## 💡 Why This Architecture Works

**Backend (Your Gateway):**
- ✅ Just provides raw numbers
- ✅ No game logic = easy to maintain
- ✅ Can reuse for different games
- ✅ Real-world data stays accurate

**Frontend (Game):**
- ✅ All creativity lives here
- ✅ Change rules anytime
- ✅ Different games from same data
- ✅ Fast iteration without backend changes

---

## 🎮 Sample Frontend Code Structure

```
frontend/
├── src/
│   ├── game/
│   │   ├── GameManager.js          # Main game loop
│   │   ├── CityState.js            # City statistics
│   │   ├── buildings/              # Building definitions
│   │   ├── events/                 # Event system
│   │   └── calculations/
│   │       ├── economyLogic.js     # BTC → game effects
│   │       ├── weatherLogic.js     # Weather → game effects
│   │       └── airQualityLogic.js  # Air → game effects
│   ├── api/
│   │   └── gateway.js              # Calls /api/state
│   └── ui/
│       ├── Dashboard.jsx           # Main UI
│       ├── Buildings.jsx           # Building menu
│       └── Events.jsx              # Event popups
```

This way, you can change ALL the game logic, thresholds, and mechanics without ever touching the backend! 🎉
