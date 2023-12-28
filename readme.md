

# script obsidian

a set of scripts which create simple features in obsidian

## partners sheet + full calendar sync

this script search in all partner file (#partner)
  when found:
    - read deadline propertiess and create the relative event note in calendar_cie_beta of the full_calendar obsidian plugin

# how to install

0. clone

```
git clone <git_repo>
```

1. install obsidian and plugins

- full_calendar
- runshellcommand

2. apply rights + create trash dir for events 
```
cd ./script_obsidian_partner_calendar
chmod +x sync_partner_calendar.py
cd <path_to_obsidian_calendar>
```

3. connect runshellcommand and script.py

4. run it through obsidian


# roadmap

- [x] run the script from obsidian
- [ ] test to modify a date to check if it works
- [ ] test if i drop a partner note

