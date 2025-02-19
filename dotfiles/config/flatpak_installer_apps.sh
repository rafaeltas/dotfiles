#!/bin/bash

# Lista de apps a instalar
apps=(
  "org.gimp.GIMP"
  "app.drey.Dialect"
  "com.github.tchx84.Flatseal"
  "com.mattjakeman.ExtensionManager"
  "com.obsproject.Studio"
  "com.stremio.Stremio"
  "com.usebottles.bottles"
  "com.valvesoftware.Steam"
  "fr.handbrake.ghb"
  "io.freetubeapp.FreeTube"
  "io.github.flattool.Warehouse"
  "io.github.giantpinkrobots.flatsweep"
  "io.github.peazip.PeaZip"
  "io.github.zen_browser.zen"
  "io.gitlab.adhami3310.Converter"
  "it.mijorus.gearlever"
  "it.mijorus.smile"
  "net.ankiweb.Anki"
  "net.pcsx2.PCSX2"
  "nl.hjdskes.gcolor3"
  "org.blender.Blender"
  "org.duckstation.DuckStation"
  "org.gnome.Solanum"
  "org.gnome.gitlab.YaLTeR.VideoTrimmer"
  "org.godotengine.Godot"
  "org.kde.krita"
  "org.localsend.localsend_app"
  "org.nickvision.tubeconverter"
  "org.qbittorrent.qBittorrent"
  "org.ryujinx.Ryujinx"
  "org.videolan.VLC"
  "io.github.nokse22.Exhibit"
  "com.github.neithern.g4music"
  "se.sjoerd.Graphs"
  "dev.bragefuglseth.Keypunch"
)

# Verifica quais apps já estão instalados e cria um array com os que faltam
to_install=()
for app in "${apps[@]}"; do
  flatpak info "$app" &>/dev/null || to_install+=("$app") &  # Check assíncrono
done

# Espera todos os processos do loop acima terminarem
wait

# Se houver Flatpaks para instalar, instala cada um em paralelo
if [ ${#to_install[@]} -gt 0 ]; then
  echo "Instalando os seguintes Flatpaks: ${to_install[*]}"
  pids=()
  for app in "${to_install[@]}"; do
    flatpak install -y flathub "$app" &  # Instalação assíncrona
    pids+=($!)  # Guarda o ID do processo
  done

  # Espera todas as instalações finalizarem
  for pid in "${pids[@]}"; do
    wait "$pid"
  done

  echo "Todas as instalações foram concluídas!"
else
  echo "Todos os Flatpaks já estão instalados!"
fi
