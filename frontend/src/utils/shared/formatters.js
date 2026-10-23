/**
 * Utilitários puros de formatação de texto, documentos, moeda, data e horário.
 */

// aplica máscara de telefone brasileiro (00) 00000-0000
export function formatPhone(val) {
  if (!val) return ''
  let v = String(val).replace(/\D/g, '')
  if (v.length > 11) v = v.substring(0, 11)

  if (v.length <= 2) {
    return v.length > 0 ? `(${v}` : v
  } else if (v.length <= 7) {
    return `(${v.substring(0, 2)}) ${v.substring(2)}`
  } else {
    return `(${v.substring(0, 2)}) ${v.substring(2, 7)}-${v.substring(7)}`
  }
}

// aplica máscara de CPF 000.000.000-00
export function formatCPF(val) {
  if (!val) return ''
  let v = String(val).replace(/\D/g, '')
  if (v.length > 11) v = v.substring(0, 11)

  if (v.length <= 3) {
    return v
  } else if (v.length <= 6) {
    return `${v.substring(0, 3)}.${v.substring(3)}`
  } else if (v.length <= 9) {
    return `${v.substring(0, 3)}.${v.substring(3, 6)}.${v.substring(6)}`
  } else {
    return `${v.substring(0, 3)}.${v.substring(3, 6)}.${v.substring(6, 9)}-${v.substring(9)}`
  }
}

// formata valor numérico para moeda BRL com símbolo (R$ 0,00) ou "A consultar"
export function formatCurrency(val) {
  if (val === null || val === undefined || val === '') return 'A consultar'
  return Number(val).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

// formata valor numérico para decimal brasileiro (0,00) sem o prefixo R$
export function formatarMoeda(valor) {
  if (valor === null || valor === undefined || valor === '') return '0,00'
  return Number(valor).toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
}

// formata minutos totais em representação amigável (ex: 90 -> "1h 30min")
export function formatDuration(mins) {
  if (!mins) return '30 min'
  if (mins < 60) return `${mins} min`
  const h = Math.floor(mins / 60)
  const m = mins % 60
  return m > 0 ? `${h}h ${m}min` : `${h}h`
}

// converte data ISO (YYYY-MM-DD) para o padrão brasileiro (DD/MM/YYYY)
export function formatarDataBr(dataIso) {
  if (!dataIso || !dataIso.includes('-')) return dataIso || ''
  const [ano, mes, dia] = dataIso.split('-')
  return `${dia}/${mes}/${ano}`
}

// soma minutos a um horário no formato HH:MM e retorna o novo horário HH:MM
export function somarMinutosNaHora(horaStr, minutos) {
  if (!horaStr || !horaStr.includes(':')) return ''
  const [h, m] = horaStr.split(':').map(Number)
  const totalMinutos = h * 60 + m + (Number(minutos) || 30)
  const horasFinais = Math.floor(totalMinutos / 60) % 24
  const minutosFinais = totalMinutos % 60
  return `${String(horasFinais).padStart(2, '0')}:${String(minutosFinais).padStart(2, '0')}`
}


// aplica máscara de data brasileira DD/MM/AAAA enquanto o usuário digita
export function mascaraData(val) {
  if (!val) return ''
  const v = String(val).replace(/\D/g, '').substring(0, 8)
  if (v.length <= 2) return v
  if (v.length <= 4) return `${v.substring(0, 2)}/${v.substring(2)}`
  return `${v.substring(0, 2)}/${v.substring(2, 4)}/${v.substring(4)}`
}

// aplica máscara de horário HH:MM enquanto o usuário digita
export function mascaraHora(val) {
  if (!val) return ''
  const v = String(val).replace(/\D/g, '').substring(0, 4)
  if (v.length <= 2) return v
  return `${v.substring(0, 2)}:${v.substring(2)}`
}

// converte data brasileira (DD/MM/AAAA) para ISO (YYYY-MM-DD); retorna null se inválida
export function dataBrParaIso(dataBr) {
  const partes = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(dataBr || '')
  if (!partes) return null
  const [, dia, mes, ano] = partes
  const data = new Date(Number(ano), Number(mes) - 1, Number(dia))
  const valida =
    data.getFullYear() === Number(ano) &&
    data.getMonth() === Number(mes) - 1 &&
    data.getDate() === Number(dia)
  return valida ? `${ano}-${mes}-${dia}` : null
}

// verifica se o texto é um horário válido no formato HH:MM (00:00 a 23:59)
export function horaValida(hora) {
  return /^([01]\d|2[0-3]):[0-5]\d$/.test(hora || '')
}
