import { useQuery } from '@tanstack/react-query'
import { api_get_request } from '../services/api.ts'
import type { MetricType } from '../enums/metric_type.ts'

export const useMeasurements = <T>(nodeId: string, sensorKey: MetricType) => {
  return useQuery({
    queryKey: ['measurements', nodeId, sensorKey],
    queryFn: async () =>
      await api_get_request<T>(
        `/telemetry/${encodeURIComponent(nodeId)}?metric_type=${sensorKey}`
      ),
    staleTime: 30_000,
    refetchInterval: 60_000,
    retry: 2,
  })
}
