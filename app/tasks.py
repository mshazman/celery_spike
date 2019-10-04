import time
from flask import jsonify
from app import celery
import csv
import json
import random
import os


@celery.task
def example(duration):
    time.sleep(duration)
    return 'Task Completed'

@celery.task()
def extract_matches():
    matches_won_by_team = {}
    seasons = ['2008', '2009', '2010', '2011', '2012', '2013','2014','2015','2016','2017']
    with open('matches.csv') as matches_file:
        matches = csv.DictReader(matches_file)
        for match in matches:
            winner = match['winner']
            season = match['season']
            if winner not in matches_won_by_team:
                matches_won_by_team[winner] = {}
                for each_season in seasons:
                    matches_won_by_team[winner][each_season] = 0
            matches_won_by_team[winner][season] += 1
    filename = str(random.randint(99999, 999999)) + '.json'
    filepath = './app/files/'+ filename
    with open(filepath, 'w') as file:
        json.dump(matches_won_by_team, file)
    time.sleep(30)
    return filename