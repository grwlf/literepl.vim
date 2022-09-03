LitREPL.vim
-----------

**LitREPL** is a macro processing Python library and a Vim plugin for Literate
programming and code execution right from the editor.

<img src="https://github.com/grwlf/litrepl-media/blob/main/demo.gif?raw=true" width="400"/>

**Features**

* Lightweight: Runs on a system where only a few Python packages are installed.
* Supported document formats: Markdown [[MD]](https://raw.githubusercontent.com/grwlf/litrepl.vim/main/doc/example.md), Latex
  [[TEX]]()[[PDF]](./doc/example.pdf)
* Supported interpreters: Python, IPython
* Supported editor: Vim
* Nix/NixOS - friendly

**Requirements:**

* POSIX-compatible OS, typically a Linux. The plugin depends on UNIX pipes and
  certain shell commands.
* More or less recent `Vim`
* Python3 with the following libraries: `lark-parser`
  (Required), `setuptools_scm`, `ipython` (Optional).
* `GNU socat` application (Optional).

_Currently, the plugin is at the proof-of-concept stage. No code is packaged,
clone this repository to reproduce the results!_

Contents
--------


 1. [LitREPL.vim](#litrepl.vim)
 2. [Contents](#contents)
 3. [Install](#install)
    * [Pip and Plug](#pip-and-plug)
    * [Nix](#nix)
 4. [Develop](#develop)
 5. [Usage](#usage)
    * [Basics](#basics)
    * [Commands](#commands)
    * [Arguments](#arguments)
    * [Formatting](#formatting)
      * [Markdown](#markdown)
      * [Latex](#latex)
    * [Batch processing](#batch-processing)
 6. [Gallery](#gallery)
 7. [Technical details](#technical-details)
 8. [Limitations](#limitations)
 9. [Related projects](#related-projects)
10. [Third-party issues](#third-party-issues)

Install
-------

To run the setup, one needs to install a Python package and a Vim plugin. The
Vim plugin relies on the `litrepl` script and on some third-party UNIX tools
available via the system `PATH`. We advise users to git-clone the same
repository with all the package managers involved to match the versions. Below
are the instructions for some packaging system combinations.

### Pip and Plug

Instructions for the Pip and [Plug](https://github.com/junegunn/vim-plug)
manager of Vim:

1. Install the Python package.
   ```sh
   $ pip install lark setuptool_scm
   $ pip install git+https://github.com/grwlf/litrepl.vim
   $ litrepl --version
   ```
2. Install the Vim plugin by adding the following line between the
   `plug#begin` and `plug#end` lines of your `.vimrc` file:
   ```vim
   Plug 'https://github.com/grwlf/litrepl.vim' , { 'rtp': 'vim' }
   ```

### Nix

[default.nix](./default.nix) contains a set of Nix exressions. Expressions
prefixed with `shell-` are to be opened with `nix-shell -A NAME`. Other
expressions need to be built with `nix-build -A NAME` and run with
`./result/bin/...`. Some expressions are:

* `litrepl` - Litrepl script and Python lib
* `vim-litrepl` - Litrepl vim plugin
* `vim-test` - a minimalistic vim with a single litrepl plugin
* `vim-demo` - vim for recording screencasts
* `vim-plug` - vim configured to use the Plug manager
* `shell-demo` - shell for recording screencasts
* `shell` - Full development shell

Develop
-------

1. `git clone --recursive https://github.com/grwlf/litrepl.vim; cd litrepl.vim`
2. Enter the development environment
   * (Nix/NixOS systems) `nix-shell`
   * (Other Linuxes) `. env.sh`
   Read the warnings and install missing packages if required. The
   environment script will add `./sh` and `./python` folders to the current
   shell's PATH/PYTHONPATH.  The former folder contains the back-end script, the
   latter one contains the Python library.
3. Run the `vim_litrepl_dev` (a thin wrapper around Vim) to run the Vim with the
   LitREPL plugin from the `./vim` folder.
4. (Optional) Run `test.sh`

Usage
-----

### Basics

LitREPL works with text documents organized in a Jupyter-Notebooks manner: main
text separates the code blocks followed by the result blocks followed by the
more text and so on. The markup is up to user, the plugin works with what it
could find.

````markdown
Some text text

<!-- Code block 1 -->
```python
print("Hello, World!")
```

More text text

<!-- Result block 1 -->
```lresult
Hello, World!
```

More text text
````

Vim command `:LitEval1` executes the code block under the cursor and pastes the
result into the afterward one or many result sections. The execution taked place
in the background interpreter which is tied to the UNIX pipes saved in the
filesystem. Thus, the state of the interpreter is persistent between the
executions and in fact even between the Vim edit sessions.

There are no key bindings defined in the plugin, but users are free to

```vim
nnoremap <F5> :LitEval1<CR>
```

### Commands

Most of the commands could be sent from the command line or from Vim directly.

| Vim             | Command line     | Description                          |
|-----------------|------------------|--------------------------------------|
| `:LitEval1`     | `lirtepl eval-sections (N\|L:C)`   | Evaluate the section under the cursor |
| `:LitEvalAbove` | `lirtepl eval-sections 0..(N\|L:C)`| Evaluate the sections above and under the cursor |
| `:LitEvalBelow` | `lirtepl eval-sections (N\|L:C)..$`| Evaluate the sections below and under the cursor |
| `:LitRepl`      | `lirtepl repl`   | Open the terminal to the interpreter |
| `:LitStart`     | `litepl start`   | Start the interpreter                |
| `:LitStop`      | `litepl stop`    | Stop the interpreter                 |
| `:LitRestart`   | `litrepl restart`| Restart the interpreter              |

Where

* `N` denotes the number of code section starting from 0.
* `L:C` denotes line:column of the cursor.

### Arguments

| Vim setting       | CLI argument      | Description                       |
|-------------------|------------------|-----------------------------------|
| `set filetype`    | `--filetype=T`   | Input file type: `latex`\|`markdown`  |
|                   | `--interpreter=I`   | The interpreter to use: `python`\|`ipython`\|`auto`, defaulting to `auto` |

* `I` is taken into account by the `start` command and by the first
  `eval-sections` only.


### Formatting

#### Markdown

```` markdown
Executable sections are marked with the "python" tag. Putting the cursor on one
of the typing the :LitEval1 command executes its code in a background Python
interpreter.

```python
W='Hello, World!'
print(W)
```

Verbatim sections next to the executable section are result sections. The output
of the code from the executable section is pasted here. The original
content of the section is replaced with the output of the last execution.

```lresult
Hello, World!
```

Markdown comment-like tags `lcode`/`lnocode`/`lresult`/`lnoresult` also mark
executable and result sections.  This way we could produce the markdown document
markup.

<!--lcode
print("Hello, LitREPL")
lnocode-->

<!--lresult-->
Hello, LitREPL
<!--lnoresult-->
````

#### Latex

````latex
\documentclass{article}
\usepackage[utf8]{inputenc}
\begin{document}

LitREPL for latex recognizes \texttt{lcode} environments as code and
\texttt{lresult} as result sections. The tag names is currently hardcoded into
the simple parser the tool is using, so we need to additionally introduce it to
the Latex system. Here we do it in a most simple way.

\newenvironment{lcode}{\begin{texttt}}{\end{texttt}}
\newenvironment{lresult}{\begin{texttt}}{\end{texttt}}
\newcommand{\linline}[2]{#2}

Executable section is the text between the \texttt{lcode} begin/end tags.
Putting the cursor on it and typing the \texttt{:LitEval1} executes it in the
background Python interpreter.

\begin{lcode}
W='Hello, World!'
print(W)
\end{lcode}

\texttt{lresult} tags next to the executable section mark the result section.
The output of the executable section will be pasted here. The
original content of the section will be replaced.

\begin{lresult}
Hello, World!
\end{lresult}

Commented \texttt{lresult}/\texttt{lnoresult} tags also marks result sections.
This way we could customise the Latex markup for every particular section.

\begin{lcode}
print("Hi!")
\end{lcode}

%lresult
Hi!
%lnoresult

Additionally, VimREPL for Latex recognises \texttt{linline} tags for which it
prints its first argument and pastes the result in place of the second argument.

\linline{W}{Hello, World!}

\end{document}
````

### Batch processing

To evaluate the document run the following command

```sh
$ cat doc/example.md | \
  litrepl --filetype=markdown --interpreter=ipython eval-sections 0..$
```

Gallery
-------

Using LitREPL in combination with the [Vimtex](https://github.com/lervag/vimtex)
plugin to edit Latex documents on the fly.


<video controls src="https://user-images.githubusercontent.com/4477729/187065835-3302e93e-6fec-48a0-841d-97986636a347.mp4" muted="true"></video>


Technical details
-----------------

The following events should normally happen upon typing the `LitEval1` command:

1. On the first run, the Python interpreter will be started in the
   background. Its standard input and output will be redirected into UNIX
   pipes in the current directory. Its PID will be saved into the
   `./_pid.txt` file.
2. The code from the Markdown code section under the cursor will be piped
   through the interpreter.
3. The result will be pasted into the Markdown section next after the current
   one.

Limitations
-----------

* Formatting: Nested code sections are not supported.
* Formatting: Special symbols in the Python output could invalidate the
  document.
* Interpreter: Extra newline is required after Python function definitions.
* Interpreter: Stdout and stderr are joined together.
* Interpreter: Evaluation of a code section locks the editor.
* Interpreter: Tweaking `os.ps1`/`os.ps2` prompts of the Python interpreter
  could break the session.
* Interpreter: No asynchronous code execution.
* ~~Interpreter: Background Python interpreter couldn't be interrupted~~

Related projects
----------------

Documenting

* https://github.com/lervag/vimtex
* https://github.com/preservim/vim-markdown

Code execution

* https://github.com/metakirby5/codi.vim
* https://github.com/gpoore/pythontex
* https://github.com/gpoore/pythontex
* https://github.com/gpoore/codebraid
* https://github.com/hanschen/vim-ipython-cell
* https://github.com/ivanov/vim-ipython
* https://github.com/goerz/jupytext.vim
* https://github.com/ivanov/ipython-vimception

Graphics

* https://github.com/sergei-grechanik/vim-terminal-images

Third-party issues
------------------

* https://github.com/junegunn/vim-plug/issues/1010#issuecomment-1221614232


