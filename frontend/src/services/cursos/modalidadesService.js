/**
 * Serviço responsável pelas requisições HTTP das modalidades de ensino e seus recursos.
 */
import { httpRequest } from '@/services/httpClient'

// busca todas as modalidades cadastradas com materiais e equipamentos vinculados
export async function listarModalidades() {
  return await httpRequest('/modalidades')
}

// cadastra uma nova modalidade de ensino
export async function criarModalidade(payload) {
  return await httpRequest('/modalidades', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

// atualiza os dados e insumos de uma modalidade existente
export async function atualizarModalidade(id, payload) {
  return await httpRequest(`/modalidades/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

// exclui uma modalidade pelo identificador
export async function excluirModalidade(id) {
  return await httpRequest(`/modalidades/${id}`, {
    method: 'DELETE',
  })
}

