import os
import zipfile

if os.path.exists('opt-cifs'):
	issues = os.listdir(os.path.join('opt-cifs','issues'))
	issues.sort()
elif os.path.exists('opt-cifs.zip'):
	issues = []
	zipped_files = zipfile.ZipFile('opt-cifs.zip').namelist()
	for zipped_file in zipped_files:
		if 'issues' in zipped_file:
			refcode = os.path.basename(zipped_file)
			issues.append(refcode)

with open('issue_tracker.txt','w') as a:
	for issue in issues:
		if issue == issues[-1]:
			a.write(issue.split('.cif')[0])
		else:
			a.write(issue.split('.cif')[0]+'\n')
