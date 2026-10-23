/**
 * Cliente HTTP base para comunicação com a API Flask do backend.
 */
export const API_BASE = 'http://127.0.0.1:5000/api'

// executa uma requisição HTTP padronizada e trata erros de resposta da API
export async function httpRequest(endpoint, options = {}) {
  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  }

  const response = await fetch(`${API_BASE}${endpoint}`, config)
  const data = await response.json().catch(() => null)

  if (!response.ok) {
    const mensagemErro = (data && data.erro) || `Erro na requisição (${response.status})`
    throw new Error(mensagemErro)
  }

  return data
}

