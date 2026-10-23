/**
 * Serviço responsável pelas requisições HTTP da área de clientes.
 */
import { httpRequest } from '@/services/httpClient'

// busca todos os clientes cadastrados
export async function listarClientes() {
  return await httpRequest('/clientes')
}

// cadastra um novo cliente
export async function criarCliente(payload) {
  return await httpRequest('/clientes', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

// atualiza os dados de um cliente existente
export async function atualizarCliente(id, payload) {
  return await httpRequest(`/clientes/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

// remove um cliente pelo identificador
export async function excluirCliente(id) {
  return await httpRequest(`/clientes/${id}`, {
    method: 'DELETE',
  })
}

