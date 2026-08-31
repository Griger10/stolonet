import { SensorPanel } from './components/SensorPanel.tsx'
import { Droplets, Thermometer } from 'lucide-react'
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from './services/query_client.ts'

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="max-w-300 mx-auto px-8 py-10">
        <h1 className="text-2xl font-semibold mb-6 text-gray-900">
          Показания датчиков
        </h1>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <SensorPanel
            label="Температура воздуха"
            unit="°C"
            icon={<Thermometer size={22} />}
            accentClass="text-orange-400"
            sensorKey="air_temperature"
          />
          <SensorPanel
            label="Влажность почвы"
            unit="%"
            icon={<Droplets size={22} />}
            accentClass="text-blue-400"
            sensorKey="soil_moisture"
          />
        </div>
      </div>
    </QueryClientProvider>
  )
}

export default App
