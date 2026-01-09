if status is-interactive
    # Starship custom prompt
    starship init fish | source

    # Direnv
    if command -v direnv &>/dev/null
        direnv hook fish | source
    end

    # FZF
    if command -v fzf &>/dev/null
        fzf --fish | source
    end

    # Zoxide
    if command -v zoxide &>/dev/null
        zoxide init fish --cmd cd | source
    end

    # FZF Configuration with fd
    if command -v fd &>/dev/null
        set -gx FZF_DEFAULT_COMMAND "fd --type f --hidden --follow --exclude .git --exclude '.steam*' --exclude 'steam'"
        set -gx FZF_CTRL_T_COMMAND "$FZF_DEFAULT_COMMAND"
    end

    # Better ls
    alias ls='eza --icons --group-directories-first -1'

    # Abbrs
    abbr nv nvim
    abbr cl clear
    abbr gsudo 'sudo -E'
    abbr ld lazydocker
    abbr lg lazygit
    abbr gd 'git diff'
    abbr ga 'git add .'
    abbr gc 'git commit -am'
    abbr gl 'git log'
    abbr gs 'git status'
    abbr gst 'git stash'
    abbr gsp 'git stash pop'
    abbr gp 'git push'
    abbr gpl 'git pull'
    abbr gsw 'git switch'
    abbr gsm 'git switch main'
    abbr gb 'git branch'
    abbr gbd 'git branch -d'
    abbr gco 'git checkout'
    abbr gsh 'git show'

    abbr l ls
    abbr ll 'ls -l'
    abbr la 'ls -a'
    abbr lla 'ls -la'

    # Apps
    abbr fm nemo

    # Custom colours
    cat ~/.local/state/caelestia/sequences.txt 2>/dev/null

    # For jumping between prompts in foot terminal
    function mark_prompt_start --on-event fish_prompt
        echo -en "\e]133;A\e\\"
    end
end
