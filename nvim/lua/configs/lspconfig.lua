require("nvchad.configs.lspconfig").defaults()

local servers = { "html", "cssls", "clangd", "pyright", "gopls", "rust_analyzer", "bashls", "fish_lsp", "ast_grep" }
vim.lsp.enable(servers)

-- read :h vim.lsp.config for changing options of lsp servers
