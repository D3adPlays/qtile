return {
    s("header", {
        t({
            "/*",
            "** EPITECH PROJECT, " .. os.date("%Y"),
            "** " .. vim.fn.fnamemodify(vim.fn.expand('%'),':t'),
            "** File description:",
            "** FD",
            "*/",
            ""
        })
    }),
}
