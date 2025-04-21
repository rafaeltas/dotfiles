return {
    {
        "akinsho/toggleterm.nvim",
        opts = {
            -- configurações opcionais
        },
        keys = {
            {
                "<leader>fy",
                function()
                    local Terminal = require("toggleterm.terminal").Terminal
                    local yazi = Terminal:new({
                        cmd = "yazi",
                        hidden = true,
                        direction = "float",
                        float_opts = {
                            border = "rounded",
                        },
                    })
                    yazi:toggle()
                end,
                desc = "Open Yazi (File Manager)",
            },
        },
    },
}
