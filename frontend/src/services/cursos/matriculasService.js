/**
 * Serviço responsável pelas requisições HTTP de matrículas de alunos em cursos.
 */
import { httpRequest } from '@/services/httpClient'

// monta a query string para filtros opcionais de listagem
function montarQueryFiltros(filtros = {}) {
  const params = new URLSearchParams()
  if (filtros.aluno_id) params.append('aluno_id', filtros.aluno_id)
  if (filtros.curso_id) params.append('curso_id', filtros.curso_id)
  if (filtros.status) params.append('status', filtros.status)
  const query = params.toString()
  return query ? `?${query}` : ''
}

// busca todas as matrículas cadastradas, permitindo filtros opcionais
export async function listarMatriculas(filtros = {}) {
  return await httpRequest(`/matriculas${montarQueryFiltros(filtros)}`)
}

// inscreve um aluno em um curso criando uma nova matrícula
export async function criarMatricula(payload) {
  return await httpRequest('/matriculas', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

// atualiza horas realizadas, status, datas ou valor acordado de uma matrícula
export async function atualizarMatricula(id, payload) {
  return await httpRequest(`/matriculas/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

// remove uma matrícula pelo identificador
export async function excluirMatricula(id) {
  return await httpRequest(`/matriculas/${id}`, {
    method: 'DELETE',
  })
}

