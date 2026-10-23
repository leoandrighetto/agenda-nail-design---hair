<template>
  <v-dialog
    :model-value="modelValue"
    max-width="560px"
    persistent
    :z-index="2500"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <v-card rounded="lg">
      <v-card-title class="bg-primary text-white pa-4 d-flex align-center justify-space-between">
        <div class="d-flex align-center">
          <v-icon class="mr-2">mdi-account-plus</v-icon>
          <span>Novo Cliente</span>
        </div>
        <v-btn icon="mdi-close" variant="text" size="small" @click="fechar"></v-btn>
      </v-card-title>

      <v-card-text class="pa-6">
        <v-form ref="formRef" v-model="formValido" autocomplete="off" @submit.prevent="salvar">
          <v-row density="compact">
            <v-col cols="12">
              <v-text-field
                v-model="dados.nome"
                label="Nome completo *"
                variant="outlined"
                color="primary"
                prepend-inner-icon="mdi-account"
                :rules="regrasNome"
                placeholder="Ex: Maria Oliveira"
                required
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="6">
              <v-text-field
                :model-value="dados.telefone"
                label="Telefone *"
                variant="outlined"
                color="primary"
                prepend-inner-icon="mdi-phone"
                placeholder="(00) 00000-0000"
                maxlength="15"
                :rules="regrasTelefone"
                required
                @update:model-value="(val) => (dados.telefone = formatPhone(val))"
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="6">
              <v-text-field
                :model-value="dados.cpf"
                label="CPF"
                variant="outlined"
                color="primary"
                prepend-inner-icon="mdi-card-account-details"
                placeholder="000.000.000-00"
                maxlength="14"
                :rules="regrasCpf"
                @update:model-value="(val) => (dados.cpf = formatCPF(val))"
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-text-field
                v-model="dados.email"
                label="E-mail"
                type="email"
                variant="outlined"
                color="primary"
                prepend-inner-icon="mdi-email"
                :rules="regrasEmail"
                placeholder="exemplo@email.com"
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-text-field
                v-model="dados.endereco"
                label="Endereço"
                variant="outlined"
                color="primary"
                prepend-inner-icon="mdi-map-marker"
                placeholder="Rua, número, bairro..."
              ></v-text-field>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>

      <v-card-actions class="pa-4 pt-0 d-flex justify-end ga-2">
        <v-btn color="grey-darken-1" variant="text" :disabled="salvando" @click="fechar">
          Cancelar
        </v-btn>
        <v-btn
          color="primary"
          variant="flat"
          :loading="salvando"
          :disabled="!formValido"
          @click="salvar"
        >
          Salvar Cliente
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
/**
 * Modal rápido de cadastro de cliente sobreposto à agenda.
 */
import { ref, watch } from 'vue'
import { criarCliente } from '@/services/clientes/clientesService'
import { formatPhone, formatCPF } from '@/utils/shared/formatters'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue', 'salvo'])

const formRef = ref(null)
const formValido = ref(false)
const salvando = ref(false)

const padraoDados = () => ({
  nome: '',
  telefone: '',
  cpf: '',
  email: '',
  endereco: '',
})

const dados = ref(padraoDados())

// regras de validação idênticas às regras globais de clientes
const regrasNome = [
  (v) => !!v || 'Nome é obrigatório',
  (v) => /^[a-zA-ZÀ-ÿ\s]+$/.test(v) || 'Nome deve conter apenas letras e espaços',
]

const regrasTelefone = [
  (v) => !!v || 'Telefone é obrigatório',
  (v) => (v && String(v).replace(/\D/g, '').length === 11) || 'Telefone deve ter 11 dígitos',
]

const regrasCpf = [
  (v) => !v || String(v).replace(/\D/g, '').length === 11 || 'CPF deve ter 11 dígitos',
]

const regrasEmail = [
  (v) => !v || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'E-mail inválido',
]

watch(
  () => props.modelValue,
  (aberto) => {
    if (aberto) {
      dados.value = padraoDados()
      if (formRef.value) formRef.value.resetValidation()
    }
  },
)

function fechar() {
  emit('update:modelValue', false)
}

async function salvar() {
  if (!formRef.value) return
  const { valid } = await formRef.value.validate()
  if (!valid) return

  salvando.value = true
  try {
    const payload = {
      nome: dados.value.nome.trim(),
      telefone: dados.value.telefone ? String(dados.value.telefone).replace(/\D/g, '') : '',
      cpf: dados.value.cpf ? String(dados.value.cpf).replace(/\D/g, '') : null,
      email: dados.value.email ? dados.value.email.trim() : null,
      endereco: dados.value.endereco ? dados.value.endereco.trim() : '',
    }

    const resposta = await criarCliente(payload)
    emit('salvo', { id: resposta.id, nome: payload.nome, telefone: dados.value.telefone })
    fechar()
  } catch (erro) {
    // erros são tratados pelo caller ou snackbar
    throw erro
  } finally {
    salvando.value = false
  }
}
</script>
