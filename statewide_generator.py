import os
import glob
import csv

year = '2016'
election = '20161108'
path = election+'*precinct.csv'
output_file = election+'__az__general__precinct.csv'

def generate_headers(year, path):
    os.chdir(year)
    os.chdir('counties')
    vote_headers = []
    for fname in glob.glob(path):
        print(fname)
        with open(fname, "r") as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            print(set(list(h for h in headers if h not in ['county','precinct', 'office', 'district', 'candidate', 'party'])))
            #vote_headers.append(h for h in headers if h not in ['county','precinct', 'office', 'district', 'candidate', 'party'])
#    with open('vote_headers.csv', "w") as csv_outfile:
#        outfile = csv.writer(csv_outfile)
#        outfile.writerows(vote_headers)

def generate_offices(year, path):
    os.chdir(year)
    offices = []
    for fname in glob.glob(path):
        with open(fname, "r") as csvfile:
            print(fname)
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not row['office'] in offices:
                    offices.append(row['office'])
    with open('offices.csv', "w") as csv_outfile:
        outfile = csv.writer(csv_outfile)
        outfile.writerows(offices)

def generate_consolidated_file(year, path, output_file):
    results = []
    os.chdir(year)
    os.chdir('counties')
    for fname in glob.glob(path):
        with open(fname, "r") as csvfile:
            print(fname)
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
                if row['office'].strip().title() in ['Straight Party', 'President', 'Governor', 'Secretary Of State', 'State Mine Inspector', 'Corporation Commissioner', 'State Auditor', 'State Treasurer', 'Commissioner of Agriculture & Commerce', 'Commissioner of Insurance', 'Attorney General', 'U.S. House', 'State Senate', 'U.S. Senate', 'State Representative', 'Registered Voters', 'Ballots Cast']:
                    if all(k in set(row) for k in ['early_voting', 'election_day', 'provisional']):
                        results.append([row['county'], row['precinct'], row['office'], row['district'], row['candidate'], row['party'], row['votes'], row['early_voting'], row['election_day'], row['provisional']])
                    else:
                        results.append([row['county'], row['precinct'], row['office'], row['district'], row['candidate'], row['party'], row['votes'], None, None, None])
    os.chdir('..')
    os.chdir('..')
    with open(output_file, "w") as csv_outfile:
        outfile = csv.writer(csv_outfile)
        outfile.writerow(['county','precinct', 'office', 'district', 'candidate', 'party', 'votes', 'early_voting', 'election_day', 'provisional'])
        outfile.writerows(results)
