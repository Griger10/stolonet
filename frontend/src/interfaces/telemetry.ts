import type {MetricType} from "../enums/metric_type.ts";

export interface Telemetry {
  node_id: string;
  metric: MetricType;
  value: number;
  unit: string;
  timestamp: string;
}

export interface MetricAverage {
  node_id: string;
  metric: MetricType;
  average_value: number | null;
  unit: string;
  hours: number;
}
