import json
import time
from watson_developer_cloud import NaturalLanguageClassifierV1
import os


nlc_usr = '5567e74f-8ed1-4427-810b-de1211d63b5e'
nlc_psw = 'GgcTiEDqydS7'

filename = 'training_csv_files/ownDB_good_level_of_bad.csv'

natural_language_classifier = NaturalLanguageClassifierV1(
  username=nlc_usr,
  password=nlc_psw)

  
# list all the id classifiers
def list_classifiers_name_id():
    classifiers = natural_language_classifier.list()
    list_classifiers = dict()
    x = json.dumps(classifiers, indent=2)
    jsonparser = json.loads(x)
    classi = jsonparser['classifiers']
    for i in range(len(classi)):
        list_classifiers[classi[i]['name']] = classi[i]['classifier_id']
    return list_classifiers
	
def get_id_classifier(name):
    ids = list_classifiers_name_id()
    return ids[name]
	
def get_status(name):
    id = get_id_classifier(name)
    return natural_language_classifier.status(id)['status']
	

# The training data must have at least five records (rows) and no more than 15,000 records
def create_classifier(training_file, name):
    #print ('Name of the new classifier : ' , name)
    #print('Training with',nb , 'percent with the file', training_file)
    #print(list_classifiers_name_id())
    #print(len(list_classifiers_name_id()))
    with open(training_file, 'rb') as training_data:
            t = time.clock()
            #print(training_data)
            #print(name)
            classifier = natural_language_classifier.create(
                    training_data=training_data,
					name = name,
                    language="en")
            
            t = time.clock() - t
    print('creating time : ' + str(t))
    status = get_status(name)
    t = time.clock()
    while status != 'Available':
        status = get_status(name)
    t = time.clock() - t
    print('traning time : ' + str(t))
    return classifier
  
  
def create_list_classifiers(filename):
    files = os.listdir('training_csv_files')
    filename = filename.split('/')
    filename = filename[len(filename) - 1]
    filename = filename.split('.')[0]
    for file in files:
        if file.__contains__(filename):
            nb = file.split('_')
            nb = nb[len(nb) - 1]
            nb = nb.split('.')[0]
            name_classifier = file.split('.csv')[0] + '_classifier_' + nb
            create_classifier('training_csv_files/' + file, name_classifier)
   
#create_list_classifiers(filename) 
#print(list_classifiers_name_id())      
