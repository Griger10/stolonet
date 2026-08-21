import type {MetricType} from "../enums/metric_type.ts";

export interface Telemetry {
  node_id: string;
  metric_type: MetricType;
  value: number;
  unit: string;
  timestamp: string;
}