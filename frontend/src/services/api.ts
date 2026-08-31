import axios from 'axios'
import { BASE_API_URL } from '../config.ts'

export const api_get_request = async <T>(endpoint: string): Promise<T> => {
  try {
    const response = await axios.get<T>(`${BASE_API_URL}${endpoint}`)
    return response.data
  } catch (err) {
    if (axios.isAxiosError(err)) {
      const detail = err.response?.data?.detail
      if (typeof detail === 'string') {
        throw new Error(detail, { cause: err })
      }
      if (Array.isArray(detail) && detail.length > 0) {
        const message = detail
          .map((item: { msg?: string }) => item.msg)
          .filter(Boolean)
          .join(', ')
        if (message) {
          throw new Error(message, { cause: err })
        }
      }
    }
    throw err
  }
}
