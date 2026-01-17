require("nvchad.configs.lspconfig").defaults()

local servers = {
  "clangd",
  "pyright",
  "gopls",
  "rust_analyzer",
  "bashls",
  "fish_lsp",
  "yamlls",
  "gh_actions_ls",
  "docker_language_server",
  "helm_ls",
}

vim.lsp.config('yamlls', {
  settings = {
    yaml = {
      schemas = {
        kubernetes = "*.yaml",
        ["http://json.schemastore.org/github-workflow"] = ".github/workflows/*",
        ["http://json.schemastore.org/kustomization"] = "kustomization.yaml",
      },
    },
  },
})

vim.lsp.enable(servers)

-- read :h vim.lsp.config for changing options of lsp servers
