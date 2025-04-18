return {
    {
        "nvim-neorg/neorg",
        lazy = false,
        version = "*",
        run = ":Neorg sync-parsers",
        dependencies = { "nvim-lua/plenary.nvim" }, -- importante!
        config = function()
            require("neorg").setup({
                load = {
                    ["core.defaults"] = {},
                    ["core.export.markdown"] = {},
                    ["core.concealer"] = {},
                    ["core.summary"] = {},
                    ["core.dirman"] = {
                        config = {
                            workspaces = {
                                notes = "~/notes",
                            },
                        },
                    },
                },
            })
        end,
    },
}
