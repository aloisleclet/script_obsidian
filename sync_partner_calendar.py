#!/bin/python3

from os import listdir, replace
from os.path import isfile, join, exists
from datetime import datetime

root_path = "/home/dev/Documents/notes";
calendar_path = root_path + "/calendar_cie_beta";
trash_path = root_path + "/trash";
tag = "#partenaire";

# utils

def date_fr_to_us(date_fr):
    d = date_fr.split("/");
    date_us = d[2] + "-" + d[1] + "-" + d[0];

    return date_us;

# create event note from partner

def create_event_if_not_exist(partner):

    date_us = partner['date'];

    filename_event = partner['date']+ " " + partner['title'] + ".md" ;
    partner_link = ""'[[{title}]]'"".format(title = partner['title']);
    title = partner['title'];

    print("create event "+ filename_event);

    content = """---
title: {title}
allDay: true
date: {date_us}
completed: 
note: "{partner_link}"
---\n""".format(date_us = date_us, partner_link = partner_link, title = title);

    # create note

    file_path = calendar_path+"/"+filename_event;
    
    if not exists(file_path):
        f = open(file_path, 'a+') # open file in append mode
        f.write(content);
        f.close();


def get_partners():
    only_files = [f for f in listdir(root_path) if isfile(join(root_path, f))]
    
    partners = [];
    partner_files = []; 

    for file in only_files:
    
        file_path = root_path + "/" + file;
    
        with open(file_path, encoding = "ISO-8859-1") as f:
            for line in f:
                pass
            last_line = line;
   
            # check if it's a partner file
            if last_line.find(tag) != -1:
                partner_files.append(file_path);

        f.close();

    for file_path in partner_files:
        
        title = file_path.split('/')[-1][0:-3];
        deadline_property = "deadlines:";
 
        f = open(file_path, "r");

        lines = f.readlines();
        i = 0;
        dates = [];

        while i < len(lines):
            
            if lines[i].find(deadline_property) != -1:
                i += 1;
                while i < len(lines) and lines[i][0:4] == "  - ":
                    dates.append(lines[i][4:-1]);
                    i += 1;
            i += 1;
            
        for date in dates:
            date_us = date_fr_to_us(date);
            partners.append({'date': date_us, 'title': title, 'match': 0});

    return partners;

def get_events():
    only_files = [f for f in listdir(calendar_path) if isfile(join(calendar_path, f))]
    
    events = [];
    
    for file in only_files:
    
        file_path = calendar_path + "/" + file;
   
        event = {}; 

        with open(file_path, encoding = "ISO-8859-1") as f:
            for line in f:
                if line.find(":") != -1:
                    key_value = line.split(": ");
                    key = key_value[0];
                    value = key_value[1][0:-1];
                    event[key] = value;

            if (event["title"].find("deadline") != -1):
                event["parent_partner_title"] = event["note"][3:-3];
                event["filename"] = event['date'] + " " + event['parent_partner_title'] + ".md";
                event["match"] = 0;
                events.append(event);

    return events;

# move event into trash folder

def drop_event(event):
    filename = event['date'] + " " + event["title"] + ".md";
    
    src_path = """{calendar_path}/{filename}""".format(calendar_path = calendar_path, filename = filename);
    dest_path = """{trash_path}/{filename}""".format(trash_path = trash_path, filename = filename);

    replace(src_path, dest_path);
    
    print('drop event'+filename);

# create matching notes for each partners deadlines

def sync_partner_calendar(partners, events):
    
    # check partner / event match
    
    i = 0;
    j = 0;
    
    while i < len(partners):
        j = 0;
    
        while j < len(events):
            if (partners[i]['date'] == events[j]['date'] and partners[i]['title'] == events[j]['parent_partner_title']):
                partners[i]['match'] = 1;
                events[j]['match'] = 1;
            j += 1;
        i += 1;
    
    # create file when partner as no event
    
    for partner in partners:
        if (partner['match'] == 0):
            create_event_if_not_exist(partner);
    
    # drop files when event as no partner
    
    for event in events:
        if (event['match'] == 0):
            drop_event(event);

# update year of each date(deadlines) to current year for partners notes
# it only upgrade events files (partner files remained unchanged)

def update_partners_deadlines(partners):

    i = 0;
    j = 0;

    while i < len(partners):
        date = partners[i]['date'];
        
        if len(date) > 0:
            d = date.split('-');
            year = d[0];
            month = d[1];
            day = d[2]; 
            now_year = datetime.today().strftime('%Y');

            if year != now_year:
                partners[i]['date'] = now_year+ "-" +month+ "-" + day;
                print(partners[i]);
        i += 1;
    return partners;

# main

partners = get_partners();
partners = update_partners_deadlines(partners);
  
events = get_events();

sync_partner_calendar(partners, events);


