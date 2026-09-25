<template>
  <v-app>
    <!-- Sidebar -->
    <v-navigation-drawer v-model="drawer" color="surface" elevation="1">
      <v-list>
        <v-list-item
          prepend-avatar="https://randomuser.me/api/portraits/women/85.jpg"
          title="Gestão de Salão"
          subtitle="Área Administrativa"
        ></v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <v-list-item prepend-icon="mdi-home" title="Início" value="home" to="/"></v-list-item>
        <v-list-item prepend-icon="mdi-calendar" title="Agenda" value="agenda" to="/agenda"></v-list-item>
        <v-list-item prepend-icon="mdi-account-group" title="Clientes" value="clientes" to="/clientes"></v-list-item>
        <v-list-item prepend-icon="mdi-content-cut" title="Serviços" value="servicos" to="/servicos"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Header -->
    <v-app-bar color="primary" elevation="2">
      <v-app-bar-nav-icon @click="drawer = !drawer" color="white"></v-app-bar-nav-icon>
      <v-app-bar-title class="text-white">Agenda do Salão</v-app-bar-title>
    </v-app-bar>

    <!-- Conteúdo da Página -->
    <v-main class="bg-background">
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'

const drawer = ref(null)
</script>

<style>
.text-white {
  color: white !important;
}
</style>
