# voyage

## Overview
This is a voyage implementation that uses google keep as it front end.
See the README in the main branch on what the voyage TODO system is.

## Setup
1. Clone and switch into this branch.
2. Setup a google [apps password](https://support.google.com/accounts/answer/185833?hl=en) (this is necessary because google does not provide an official keep API).
3. Configure your sync.py see the config section.
4. Run `python3 voyage.py "<gmail_email>" "<app_password>"`

## Config
Configuration is done in sync.py, which hypothetically can be modified while
voyage is running.
Some major points of interest:
- To add voyage headings put them in the HEEADINGS array.
- To actually have waypoint be added to these headings you will need to put the
  code that adds them in the try block of the gen_manifest function. A function
  to add ical events as waypoints to headings has been provided.
- If you really send your keep to high hell you can always remove all waypoint
  cards from keep with the -n option.
