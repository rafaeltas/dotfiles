#!/bin/bash

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
  "org.gimp.GIMP"
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
