import * as React from "react";
import {Loader2, RefreshCw} from "lucide-react";
import type {Telemetry} from "../interfaces/telemetry.ts";
import {useMeasurements} from "../hooks/useMeasurements.ts";
import {NODE_ID} from "../config.ts";
import type {MetricType} from "../enums/metric_type.ts";


type Props = {
  label: string;
  value: number;
  unit: string;
  icon: React.ReactNode;
  accentClass: string;
  sensorKey: MetricType;
}

export const SensorPanel: React.FC<Props> = ({label, value, unit, icon, accentClass, sensorKey}) => {
  const {data: history = [], isLoading, isError, error, refetch} = useMeasurements<Telemetry[]>(NODE_ID, sensorKey)

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-md p-6 w-full">
      <div className="flex items-center gap-2 mb-1 text-gray-500 dark:text-gray-400">
        {icon}
        <span className="text-sm">{label}</span>
      </div>
      <div className="text-3xl font-bold text-gray-900 dark:text-gray-100">
        {value}
        <span className="text-lg text-gray-400 ml-1 font-normal">{unit}</span>
      </div>
      <div className="text-xs text-gray-400 mt-1 mb-4">Последние 100 замеров</div>

      {isLoading ? (
        <div className="flex justify-center py-10">
          <Loader2 className={`animate-spin ${accentClass}`} size={32}/>
        </div>
      ) : isError ? (
        <div className="rounded-lg border border-red-200 bg-red-50 dark:bg-red-950/30 dark:border-red-900 p-3">
          <div className="flex items-start justify-between gap-2">
            <div>
              <p className="text-sm font-medium text-red-700 dark:text-red-400">Ошибка загрузки</p>
              <p className="text-sm text-red-600 dark:text-red-300">{error.message}</p>
            </div>
            <button
              onClick={() => refetch()}
              className="flex items-center gap-1 text-sm text-red-700 dark:text-red-400 hover:underline shrink-0"
            >
              <RefreshCw size={14}/>
              Повторить
            </button>
          </div>
        </div>
      ) : (
        <div className="max-h-100 overflow-y-auto rounded-lg border border-gray-200 dark:border-gray-700">
          <table className="w-full text-sm">
            <thead className="sticky top-0 bg-gray-50 dark:bg-gray-900">
            <tr>
              <th className="text-left px-3 py-2 font-medium text-gray-500 dark:text-gray-400">
                Время
              </th>
              <th className="text-right px-3 py-2 font-medium text-gray-500 dark:text-gray-400">
                Значение
              </th>
            </tr>
            </thead>
            <tbody>
            {history.map((row, i) => (
              <tr
                key={i}
                className={`${
                  i % 2 === 0 ? "bg-white dark:bg-gray-800" : "bg-gray-50 dark:bg-gray-900/50"
                } hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors`}
              >
                <td className="px-3 py-1.5 text-gray-700 dark:text-gray-300">
                  {new Date(row.timestamp).toLocaleString("ru-RU")}
                </td>
                <td className="px-3 py-1.5 text-right text-gray-700 dark:text-gray-300">
                  {row.value} {unit}
                </td>
              </tr>
            ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}