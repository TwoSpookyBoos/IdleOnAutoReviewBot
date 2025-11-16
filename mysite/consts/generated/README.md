# How to update the source strings for generated data dicts correctly

- Find the `make` function for the corresponding definitions in the source code, for example in `scripts.MonsterDefinitions`
- Copy the body of the `make` function (everything after `.make = function ()`)
- Paste it into a separate document/file/tab in your preferred editor
- remove the outermost curly braces `{}` if you copied those
- remove all spaces (` `) and newlines (`\n`). 
  - if using regex, you can replace `\s` (any whitespace) with an empty string in one step
- everything should now be in one line. Replace the corresponding const (for example `script_monster_definitions` in `consts_monster_data.py`) and update the `Last updated in` comment.
- run the application. If the source has changed, the data dicts will be regenerated
