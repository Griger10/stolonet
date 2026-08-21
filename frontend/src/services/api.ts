import axios from 'axios'
import {BASE_API_URL} from "../config.ts";


export const api_get_request = async <T>(endpoint: string): Promise<T> => {
  const response = await axios.get(`${BASE_API_URL}/${endpoint}`)

  if (response.status >= 400) {
    throw new Error(response.statusText)
  }
  return response.data
}
