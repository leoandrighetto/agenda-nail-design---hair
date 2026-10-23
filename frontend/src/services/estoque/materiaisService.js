/**
 * Serviço responsável pelas requisições HTTP de materiais e insumos do estoque.
 */
import { httpRequest } from '@/services/httpClient'

// busca todos os materiais cadastrados no estoque
export async function listarMateriais() {
  return await httpRequest('/materiais')
}

// cadastra um novo material no estoque
export async function criarMaterial(payload) {
  return await httpRequest('/materiais', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

// atualiza dados, quantidade ou disponibilidade de um material
export async function atualizarMaterial(id, payload) {
  return await httpRequest(`/materiais/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

// remove um material do estoque
export async function excluirMaterial(id) {
  return await httpRequest(`/materiais/${id}`, {
    method: 'DELETE',
  })
}

