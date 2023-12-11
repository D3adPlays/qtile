-- Read the docs: https://www.lunarvim.org/docs/configuration
-- Example configs: https://github.com/LunarVim/starter.lvim
-- Video Tutorials: https://www.youtube.com/watch?v=sFA9kX-Ud_c&list=PLhoH5vyxr6QqGu0i7tt_XoVK9v-KvZ3m6
-- Forum: https://www.reddit.com/r/lunarvim/
-- Discord: https://discord.com/invite/Xb9B4Ny
vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.opt.wrap = false
vim.opt.relativenumber = true
lvim.transparent_window = true
lvim.builtin.nvimtree.setup.sort_by = "filetype"
lvim.builtin.nvimtree.setup.view.adaptive_size = true

lvim.plugins = {
    {"vimsence/vimsence"},
    { "lukas-reineke/virt-column.nvim",
        event = "BufRead",
        opts = {},
        config = function ()
            require("virt-column").update({
                enabled = true,
                char = "╵",
                virtcolumn = "+1, 80"
            })
        end
    },
}

lvim.autocommands = {
    {
        "BufWritePre",
        {
            pattern = { "*" },
            callback = function ()
                local save_cursor = vim.fn.getpos(".")
                pcall(function() vim.cmd [[%s/\s\+$//e]] end)
                pcall(function() vim.cmd [[%s#\($\n\s*\)\+\%$##]] end)
                vim.fn.setpos(".", save_cursor)
            end
        }
    },
}
