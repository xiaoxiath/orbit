# Bash completion for Orbit CLI

_orbit_list() {
    local cur prev words cword
    _init_completion || return

    # Current command
    cur="${COMP_WORDS[COMP_CWORD]}"

    # Available commands
    commands="list search run interactive export version test"

    # If completing the command itself
    if [[ ${COMP_CWORD} -eq 1 ]]; then
        COMPREPLY=($(compgen -W "${commands}" -- "${cur}"))
        return
    fi

    # Command-specific completions
    case "${COMP_WORDS[1]}" in
        list)
            if [[ ${COMP_CWORD} -eq 2 ]]; then
                COMPREPLY=($(compgen -W "-c --category -s --safety --details -d --count --help -h" -- "${cur}"))
            elif [[ ${COMP_WORDS[2]} == "-c" || ${COMP_WORDS[2]} == "--category" ]]; then
                if [[ ${COMP_CWORD} -eq 3 ]]; then
                    COMPREPLY=($(compgen -W "system files notes reminders calendar mail safari music finder contacts wifi apps" -- "${cur}"))
                fi
            elif [[ ${COMP_WORDS[2]} == "-s" || ${COMP_WORDS[2]} == "--safety" ]]; then
                if [[ ${COMP_CWORD} -eq 3 ]]; then
                    COMPREPLY=($(compgen -W "safe moderate dangerous critical" -- "${cur}"))
                fi
            fi
            ;;

        search)
            if [[ ${COMP_CWORD} -eq 2 ]]; then
                COMPREPLY=($(compgen -W "-c --category -d --details --help -h" -- "${cur}"))
            elif [[ ${COMP_WORDS[2]} == "-c" || ${COMP_WORDS[2]} == "--category" ]]; then
                if [[ ${COMP_CWORD} -eq 3 ]]; then
                    COMPREPLY=($(compgen -W "system files notes reminders calendar mail safari music finder contacts wifi apps" -- "${cur}"))
                fi
            fi
            ;;

        run)
            # List all satellites for completion
            if [[ ${COMP_CWORD} -eq 2 ]]; then
                # Try to get satellite names from orbit
                local satellites=$(python3 -c "from orbit.satellites.all_satellites import all_satellites; print(' '.join([s.name for s in all_satellites]))" 2>/dev/null)
                if [[ -n "$satellites" ]]; then
                    COMPREPLY=($(compgen -W "${satellites}" -- "${cur}"))
                fi
            fi
            ;;

        interactive)
            COMPREPLY=($(compgen -W "-c --category --safe-only --help -h" -- "${cur}"))
            ;;

        export)
            if [[ ${COMP_CWORD} -eq 2 ]]; then
                COMPREPLY=($(compgen -W "openai json json-schema stats" -- "${cur}"))
            elif [[ ${COMP_CWORD} -ge 2 ]]; then
                COMPREPLY=($(compgen -W "-o --output -c --category --indent --help -h" -- "${cur}"))
            fi
            ;;

        *)
            ;;
    esac
}

complete -F _orbit_list orbit
