require "nvchad.autocmds"

vim.filetype.add({
  pattern = {
    -- Matches docker-compose.yml, docker-compose.yaml, compose.yml, compose.yaml
    ["docker-compose.*%.ya?ml"] = "yaml.docker-compose",
    ["compose.*%.ya?ml"] = "yaml.docker-compose",
  },
})
