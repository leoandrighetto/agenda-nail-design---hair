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
                @update:model-value="aoAlterarTelefone"
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
                @update:model-value="aoAlterarCpf"
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
import { useNovoClienteModal } from '@/composables/clientes/useNovoClienteModal'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue', 'salvo'])

const {
  formRef,
  formValido,
  salvando,
  dados,
  regrasNome,
  regrasTelefone,
  regrasCpf,
  regrasEmail,
  aoAlterarTelefone,
  aoAlterarCpf,
  fechar,
  salvar,
} = useNovoClienteModal(props, emit)
</script>
