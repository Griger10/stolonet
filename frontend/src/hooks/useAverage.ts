import { useQuery } from '@tanstack/react-query'
import type { MetricType } from '../enums/metric_type.ts'
import { api_get_request } from '../services/api.ts'

export const useAverage = <T>(nodeId: string, sensorKey: MetricType) => {
  return useQuery({
    queryKey: ['average', nodeId, sensorKey],
    queryFn: async () =>
      await api_get_request<T>(
        `/telemetry/${encodeURIComponent(nodeId)}/average?metric_type=${sensorKey}`
      ),
    staleTime: 30_000,
    refetchInterval: 60_000,
    retry: 2,
  })
}
