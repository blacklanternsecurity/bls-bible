<!---------------------------------------------------------------------------------
Copyright: (c) BLS OPS LLC.
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
--------------------------------------------------------------------------------->
# tmux

### Tags

- <details><summary>(Click to expand)</summary><p>
	- `#@linux #@bash #@tmux #@cheat #@sheet #@cheatsheet #@tool`

### References

- [tmux cheat sheet](https://tmuxcheatsheet.com/)

### Overview

- Commands starting with `tmux` are ran from bash
- Commands starting with `:` are ran from the tmux console
	- To access the tmux console press `CTRL+b` , `:`
- Otherwise, commands are hotkey combinations to be pressed while in an active tmux session


- <details><summary>Sessions</summary><p>
	- <details><summary>Start a new session</summary><p>
		- `tmux`
		- `tmux new`
		- `tmux new-session`
		- `:new`
	- <details><summary>Start a new session with the name `mysession`</summary><p>
		- `tmux new -s mysession`
		- `:new -s mysession`
	- <details><summary>Kill/delete session with the name `mysession`</summary><p>
		- `tmux kill-ses -t mysession`
		- `tmux kill-session -t mysession`
	- <details><summary>Kill/delete all sessions except current one</summary><p>
		- `tmux kill-session -a`
	- <details><summary>Kill/delete all sessions except session with the name `mysession`</summary><p>
		- `tmux kill-session -a -t mysession`
	- <details><summary>Show all sessions</summary><p>
		- `tmux ls`
		- `tmux list-sessions`
		- `CTRL+b` , `s`
	- <details><summary>Attach to last session</summary><p>
		- `tmux a`
		- `tmux at`
		- `tmux attach`
		- `tmux attach-session`
	- <details><summary>Attach to a session with the name `mysession`</summary><p>
		- `tmux a -t mysession`
		- `tmux at -t mysession`
		- `tmux attach -t mysession`
		- `tmux attach-session -t mysession`
	- <details><summary>Rename session</summary><p>
		- `CTRL+b` , `$`
	- <details><summary>Detach from session</summary><p>
		- `CTRL+b` , `d`
	- <details><summary>Session and window preview</summary><p>
		- `CTRL+b` , `w`
	- <details><summary>Move to previous session</summary><p>
		- `CTRL+b,` , `(`
	- <details><summary>Move to next session</summary><p>
		- `CTRL+b` , `)`
	- <details><summary>Detach others on session</summary><p>
		- `:attach -d`

- <details><summary>Windows</summary><p>
	- <details><summary>Create window</summary><p>
		- `CTRL+b` , `c`
	- <details><summary>Rename current window</summary><p>
		- `CTRL+b` , `,`
	- <details><summary>Close current window</summary><p>
		- `CTRL+b` , `&`
	- <details><summary>Previous window</summary><p>
		- `CTRL+b` , `p`
	- <details><summary>Next window</summary><p>
		- `CTRL+b` , `n`
	- <details><summary>Switch/select window by number</summary><p>
		- `CTRL+b` , `<number>`
	- <details><summary>Toggle last active window</summary><p>
		- `CTRL+b` , `l`
	- <details><summary>Reorder window, swap window number 2 (src) and 1 (dst)</summary><p>
		- `:swap-window -s 2 -t 1`
	- <details><summary>Move current window to the left by one</summary><p>
		- `:swap-window -t -1`

- <details><summary>Panes</summary><p>
	- <details><summary>Toggle last active pane</summary><p>
		- `CTRL+b` , `;`
	- <details><summary>Split pane with horizontal layout</summary><p>
		- `CTRL+b` , `%`
	- <details><summary>Split pane with vertical layout</summary><p>
		- `CTRL+b` , `"`
	- <details><summary>Move the current pane left</summary><p>
		- `CTRL+b` , `{`
	- <details><summary>Move the current pane right</summary><p>
		- `CTRL+b` , `}`
	- <details><summary>Switch pane to the direction</summary><p>
		- `CTRL+b` , `<arrow-key>`
	- <details><summary>Toggle synchronize-panes (send command to all panes)</summary><p>
		- `:setw synchronize-panes`
	- <details><summary>Toggle between pane layouts</summary><p>
		- `CTRL+b` , `spacebar`
	- <details><summary>Switch to next pane</summary><p>
		- `CTRL+b` , `o`
	- <details><summary>Show pane numbers</summary><p>
		- `CTRL+b` , `q`
	- <details><summary>Switch/select pane by number</summary><p>
		- `CTRL+b` , `q` , `<number>`
	- <details><summary>Toggle pane zoom</summary><p>
		- `CTRL+b` , `z`
	- <details><summary>Convert pane to a window</summary><p>
		- `CTRL+b` , `!`
	- <details><summary>Resize current pane height (holding second key is optional)</summary><p>
		- `CTRL+b` , `<up/down>` or `CTRL+<up/down>`
	- <details><summary>Resize current pane width (holding second key is optional)</summary><p>
		- `CTRL+b` , `<left/right>` or `CTRL+<left/right>`
	- <details><summary>Close current pane</summary><p>
		- `CTRL+b` , `x`

- <details><summary>Copy Mode</summary><p>
	- <details><summary>use vi keys in buffer</summary><p>
		- `:setw -g mode-keys vi`
	- <details><summary>Enter copy mode</summary><p>
		- `CTRL+b` , `[`
	- <details><summary>Enter copy mode and scroll one page up</summary><p>
		- `CTRL+b` , `PgUp` 
	- <details><summary>Quit mode</summary><p>
		- `q`
	- <details><summary>Go to top line</summary><p>
		- `g`
	- <details><summary>Go to bottom line</summary><p>
		- `G`
	- <details><summary>Scroll up</summary><p>
		- `<up-arrow>`
	- <details><summary>Scroll down</summary><p>
		- `<down-arrow>`
	- <details><summary>Move cursor left</summary><p>
		- `h`
	- <details><summary>Move cursor down</summary><p>
		- `j`
	- <details><summary>Move cursor up</summary><p>
		- `k`
	- <details><summary>Move cursor right</summary><p>
		- `l`
	- <details><summary>Move cursor forward one word at a time</summary><p>
		- `w`
	- <details><summary>Move cursor backward one word at a time</summary><p>
		- `b`
	- <details><summary>Search forward</summary><p>
		- `/`
	- <details><summary>Search backward</summary><p>
		- `?`
	- <details><summary>Next keyword occurance</summary><p>
		- `n`
	- <details><summary>Previous keyword occurance</summary><p>
		- `N`
	- <details><summary>Start selection</summary><p>
		- `spacebar`
	- <details><summary>Clear selection</summary><p>
		- `esc`
	- <details><summary>Copy selection</summary><p>
		- `enter`
	- <details><summary>Paste contents of buffer_0</summary><p>
		- `CTRL+b` , `]`
	- <details><summary>display buffer_0 contents</summary><p>
		- `:show-buffer`
	- <details><summary>copy entire visible contents of pane to a buffer</summary><p>
		- `:capture-pane`
	- <details><summary>Show all buffers</summary><p>
		- `:list-buffers`
	- <details><summary>Show all buffers and paste selected</summary><p>
		- `:choose-buffer`
	- <details><summary>Save buffer contents to buf.txt</summary><p>
		- `save-buffer buf.txt`
	- <details><summary>delete buffer_1</summary><p>
		- `delete-buffer -b 1`

- <details><summary>Misc</summary><p>
	- <details><summary>Enter command mode</summary><p>
		- `CTRL+b` , `:`
	- <details><summary>Set OPTION for all sessions</summary><p>
		- `:set -g OPTION`
	- <details><summary>Set OPTION for all windows</summary><p>
		- `:setw -g OPTION`
	- <details><summary>Enable mouse mode</summary><p>
		- `:set mouse on`
	- <details><summary>Enable mouse mode on all windows</summary><p>
		- `:setw -g mouse on`
	
- <details><summary>Help</summary><p>
	- <details><summary>List key bindings</summary><p>
		- `tmux list-keys`
		- `:list-keys`
		- `CTRL+b` , `?`
	- <details><summary>Show every session, window, pane, etc</summary><p>
		- `tmux info`
