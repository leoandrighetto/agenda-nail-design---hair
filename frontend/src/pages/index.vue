<template>
  <v-row class="fill-height mt-5" justify="center">
    <v-col cols="12" md="8">
      <v-card class="pa-8 text-center" elevation="2" rounded="xl">
        <v-icon size="80" color="primary" class="mb-4">mdi-flower-tulip-outline</v-icon>
        <h1 class="text-h3 text-primary font-weight-bold mb-4">Bem-vinda ao Sistema!</h1>
        <p class="text-subtitle-1 text-grey-darken-1 mb-8">
          Utilize o menu lateral para gerenciar sua agenda, seus clientes e seus serviços.
        </p>
        
        <v-row justify="center" class="mt-4" spacing="4">
          <v-col cols="12" sm="5">
            <v-btn color="secondary" size="x-large" block to="/agenda" rounded="pill" elevation="3">
              <v-icon left class="mr-2">mdi-calendar-check</v-icon>
              Ver Agenda de Hoje
            </v-btn>
          </v-col>
          <v-col cols="12" sm="5">
            <v-btn color="accent" size="x-large" block to="/clientes" rounded="pill" elevation="3">
              <v-icon left class="mr-2">mdi-account-plus</v-icon>
              Novo Cliente
            </v-btn>
          </v-col>
        </v-row>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
// Home page
</script>
