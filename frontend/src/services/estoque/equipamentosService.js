/**
 * Serviço responsável pelas requisições HTTP de equipamentos do salão.
 */
import { httpRequest } from '@/services/httpClient'

// busca todos os equipamentos cadastrados
export async function listarEquipamentos() {
  return await httpRequest('/equipamentos')
}

// cadastra um novo equipamento
export async function criarEquipamento(payload) {
  return await httpRequest('/equipamentos', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

// atualiza dados, quantidade ou disponibilidade de um equipamento
export async function atualizarEquipamento(id, payload) {
  return await httpRequest(`/equipamentos/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

// remove um equipamento pelo identificador
export async function excluirEquipamento(id) {
  return await httpRequest(`/equipamentos/${id}`, {
    method: 'DELETE',
  })
}

