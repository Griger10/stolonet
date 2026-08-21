import {SensorPanel} from "./components/SensorPanel.tsx";
import {Droplets, Thermometer} from "lucide-react";

function App() {
  return (
    <>
      <div className="max-w-300 mx-auto px-8 py-10">
      <h1 className="text-2xl font-semibold mb-6 text-gray-900 dark:text-gray-100">
        Показания датчиков
      </h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SensorPanel
          label="Температура воздуха"
          value={22.4}
          unit="°C"
          icon={<Thermometer size={22} />}
          accentClass="text-orange-400"
          sensorKey="air_temperature"
        />
        <SensorPanel
          label="Влажность почвы"
          value={38}
          unit="%"
          icon={<Droplets size={22} />}
          accentClass="text-blue-400"
          sensorKey="soil_moisture"
        />
      </div>
    </div>
    </>
  )
}

export default App
