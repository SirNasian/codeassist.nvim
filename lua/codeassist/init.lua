local M = {}

local root_path = vim.fs.dirname(vim.fs.dirname(vim.fs.dirname(debug.getinfo(1, "S").source:sub(2))))
local venv_path = vim.fs.joinpath(root_path, "venv")
local python = vim.fs.joinpath(venv_path, "bin", "python")
local pip = vim.fs.joinpath(venv_path, "bin", "pip")

local code_assist = function(opts, callback)
	local context = table.concat(vim.api.nvim_buf_get_lines(0, opts.line1-1, opts.line2, false), "\n")
	vim.ui.input({ prompt = "Query: " }, function(query)
		vim.fn.jobstart({
			python,
			vim.fs.joinpath(root_path, "python", "script.py"),
			opts.mode,
			vim.bo.filetype,
			query,
			context,
		}, {
			stdout_buffered = true,
			on_stdout = callback,
		})
	end)
end

local code_assist_ask = function(opts)
	opts.mode = "ask"
	code_assist(opts, function(_, data)
		if data then
			print(table.concat(data, "\n"))
		end
	end)
end

local code_assist_replace = function(opts)
	opts.mode = "replace"
	code_assist(opts, function(_, data)
		if data then
			vim.api.nvim_buf_set_lines(0, opts.line1-1, opts.line2, false, data)
		end
	end)
end

M.setup = function(opts)
	-- TODO: configuration options
	opts = opts or {}

	vim.system({ "python", "-m", "venv", venv_path })
	vim.system({ pip, "install", "-r", vim.fs.joinpath(root_path, "python", "requirements.txt") })

	vim.api.nvim_create_user_command("CodeAssist", code_assist_ask, { range = true, desc = "" })
	vim.api.nvim_create_user_command("CodeAssistReplace", code_assist_replace, { range = true, desc = "" })
end

return M
