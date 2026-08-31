export const MetricType = {
  SOIL_MOISTURE: 'soil_moisture',
  AIR_TEMPERATURE: 'air_temperature',
} as const

export type MetricType = (typeof MetricType)[keyof typeof MetricType]
