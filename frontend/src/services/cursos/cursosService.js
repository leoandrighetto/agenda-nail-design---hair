/**
 * Serviço responsável pelas requisições HTTP do catálogo de cursos.
 */
import { httpRequest } from '@/services/httpClient'

// busca todos os cursos cadastrados com modalidades e matrículas
export async function listarCursos() {
  return await httpRequest('/cursos')
}

// busca os detalhes de um curso específico pelo identificador
export async function visualizarCurso(id) {
  return await httpRequest(`/cursos/${id}`)
}

// cadastra um novo curso no catálogo
export async function criarCurso(payload) {
  return await httpRequest('/cursos', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

// atualiza os dados e vínculos de um curso existente
export async function atualizarCurso(id, payload) {
  return await httpRequest(`/cursos/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

// remove um curso do catálogo pelo identificador
export async function excluirCurso(id) {
  return await httpRequest(`/cursos/${id}`, {
    method: 'DELETE',
  })
}

