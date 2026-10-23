/**
 * Serviço responsável pelas requisições HTTP do catálogo de serviços.
 */
import { httpRequest } from '@/services/httpClient'

// busca todos os serviços com seus materiais e equipamentos vinculados
export async function listarServicos() {
  return await httpRequest('/servicos')
}

// cadastra um novo serviço no catálogo
export async function criarServico(payload) {
  return await httpRequest('/servicos', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

// atualiza um serviço existente pelo identificador
export async function atualizarServico(id, payload) {
  return await httpRequest(`/servicos/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

// exclui um serviço do catálogo
export async function excluirServico(id) {
  return await httpRequest(`/servicos/${id}`, {
    method: 'DELETE',
  })
}

