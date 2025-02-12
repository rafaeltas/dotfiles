#!/bin/bash

apps=(
  "com.spotify.Client"
  "org.gimp.GIMP"
)

pids=()

for app in "${apps[@]}"; do
  flatpak install -y flathub "$app" & # Roda em background
  pids+=($!)                          # Guarda o ID do processo
done

# Espera todos os processos finalizarem
for pid in "${pids[@]}"; do
  wait "$pid"
done

echo "Todas as instalações foram concluídas!"
