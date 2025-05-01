-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

-- Mapeia a tecla Tab para z= no modo normal
vim.api.nvim_set_keymap("n", "<Tab>", ":call SpellSuggest()<CR>", { noremap = true, silent = true })

-- Função para verificar se o cursor está sobre uma palavra com erro ortográfico e chamar z=
vim.cmd([[
function! SpellSuggest()
  if !col('.') == col('$') && spellbadword() != ''
    execute "normal z="
  endif
endfunction
]])
