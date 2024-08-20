from django.shortcuts import render, redirect
from django.http import HttpResponse
from pymongo import MongoClient
from bson.objectid import ObjectId

# Configuration MongoDB
def get_mongo_client():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['your_database_name']  # Remplacez par le nom de votre base de données MongoDB
    return db

def create_person(request):
    db = get_mongo_client()
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']

        person = {"name": name, "age": int(age)}
        db.persons.insert_one(person)

        return redirect('list_person')
    return render(request, 'create_person.html')

def create_cours(request):
    db = get_mongo_client()
    if request.method == 'POST':
        libelle = request.POST['libelle']

        cours = {"libelle": libelle}
        db.courses.insert_one(cours)

        return redirect('create_cours')
    return render(request, 'create_cours.html')

def create_relation(request):
    db = get_mongo_client()
    if request.method == 'POST':
        name1 = request.POST['name1']
        name2 = request.POST['name2']
        relation = request.POST['relation']

        person1 = db.persons.find_one({"name": name1})
        person2 = db.persons.find_one({"name": name2})

        if person1 and person2:
            relation_data = {
                "person1_id": person1["_id"],
                "person2_id": person2["_id"],
                "relation": relation
            }
            db.relations.insert_one(relation_data)

        return redirect('create_relation')
    return render(request, 'create_relation.html')

def list_person(request):
    db = get_mongo_client()
    persons = db.persons.find()
    persons_list = [{'name': person['name'], 'age': person['age'], 'id': str(person['_id'])} for person in persons]

    return render(request, 'list_person.html', {'persons': persons_list})

def update_person(request, person_id):
    db = get_mongo_client()

    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')

        if not name or not age:
            return HttpResponse("Les champs 'name' et 'age' sont requis", status=400)

        db.persons.update_one(
            {"_id": ObjectId(person_id)},
            {"$set": {"name": name, "age": int(age)}}
        )

        return redirect('list_person')

    person = db.persons.find_one({"_id": ObjectId(person_id)})

    if person:
        person_data = {
            'name': person['name'],
            'age': person['age']
        }
    else:
        return HttpResponse("Personne non trouvée", status=404)

    return render(request, 'update_person.html', {'person': person_data})

def delete_person(request, person_id):
    db = get_mongo_client()
    db.persons.delete_one({"_id": ObjectId(person_id)})

    return redirect('list_person')
