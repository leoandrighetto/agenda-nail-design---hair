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
          <v-icon class="mr-2">mdi-plus-circle-outline</v-icon>
          <span>Novo Procedimento</span>
        </div>
        <v-btn icon="mdi-close" variant="text" size="small" @click="fechar"></v-btn>
      </v-card-title>

      <v-card-text class="pa-6">
        <v-form ref="formRef" v-model="formValido" autocomplete="off" @submit.prevent="salvar">
          <v-row density="compact">
            <v-col cols="12">
              <v-text-field
                v-model="dados.nome"
                label="Nome do procedimento *"
                variant="outlined"
                color="primary"
                prepend-inner-icon="mdi-content-cut"
                :rules="regrasNome"
                placeholder="Ex: Manicure Simples, Mechas, Escova"
                required
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="6">
              <v-text-field
                v-model.number="dados.duracao_minutos"
                label="Duração (minutos) *"
                type="number"
                min="5"
                step="5"
                variant="outlined"
                color="primary"
                prepend-inner-icon="mdi-clock-outline"
                :rules="regrasDuracao"
                required
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="6">
              <v-text-field
                v-model.number="dados.preco"
                label="Preço sugerido (R$)"
                type="number"
                min="0"
                step="0.01"
                variant="outlined"
                color="primary"
                prepend-inner-icon="mdi-currency-brl"
                placeholder="0,00"
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-textarea
                v-model="dados.descricao"
                label="Descrição / Observações"
                variant="outlined"
                color="primary"
                rows="2"
                prepend-inner-icon="mdi-text-box-outline"
                placeholder="Detalhes ou cuidados sobre a execução do procedimento..."
              ></v-textarea>
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
          Salvar Procedimento
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
/**
 * Modal rápido de cadastro de procedimento/serviço sobreposto à agenda.
 */
import { ref, watch } from 'vue'
import { criarServico } from '@/services/servicos/servicosService'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue', 'salvo'])

const formRef = ref(null)
const formValido = ref(false)
const salvando = ref(false)

const padraoDados = () => ({
  nome: '',
  duracao_minutos: 30,
  preco: null,
  descricao: '',
})

const dados = ref(padraoDados())

const regrasNome = [
  (v) => !!v || 'O nome do procedimento é obrigatório',
]

const regrasDuracao = [
  (v) => (v != null && v > 0) || 'Informe a duração em minutos',
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
      duracao_minutos: Number(dados.value.duracao_minutos) || 30,
      preco: dados.value.preco != null && dados.value.preco !== '' ? Number(dados.value.preco) : null,
      descricao: dados.value.descricao ? dados.value.descricao.trim() : '',
    }

    const resposta = await criarServico(payload)
    emit('salvo', {
      id: resposta.id,
      nome: payload.nome,
      preco: payload.preco,
      duracao_minutos: payload.duracao_minutos,
    })
    fechar()
  } catch (erro) {
    throw erro
  } finally {
    salvando.value = false
  }
}
</script>
