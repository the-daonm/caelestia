require "nvchad.mappings"

-- add yours here

local map = vim.keymap.set

map("n", ";", ":", { desc = "CMD enter command mode" })
map("i", "jk", "<ESC>")
map("t", "jk", "<C-\\><C-n>", { desc = "Terminal normal mode" })

-- map({ "n", "i", "v" }, "<C-s>", "<cmd> w <cr>")
