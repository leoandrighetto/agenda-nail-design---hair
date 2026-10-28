/**
 * Serviço responsável pelas requisições HTTP da gestão de alunos.
 */
import { httpRequest } from '@/services/httpClient'

// busca todos os alunos ativos cadastrados no sistema
export async function listarAlunos() {
  return await httpRequest('/alunos')
}

// cadastra um novo aluno ou ativa o papel de aluno em uma pessoa existente
export async function criarAluno(payload) {
  return await httpRequest('/alunos', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

// atualiza os dados cadastrais de um aluno existente
export async function atualizarAluno(id, payload) {
  return await httpRequest(`/alunos/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

// desativa o papel de aluno preservando o histórico no banco
export async function excluirAluno(id) {
  return await httpRequest(`/alunos/${id}`, {
    method: 'DELETE',
  })
}

