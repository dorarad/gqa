Definition of the scene graphs ontology.
Consists of 3 txt files: objects.txt, attributes.txt, and relations.txt.
txt2json.py translates these txt files into jsons that are then consumed by create_questions.

Each txt file consists of a list objects/attributes/relations, annotated by differnet labels that are used during question generation.

Each line is formatted as: 
In objects.txt: object name,frequency,category name,annotations
In attributes.txt: attribute name;frequency;attribute type;annotations
In relations.txt: relation,frequency,relation type,annotations

See txt2json.py for the definition of specific extra annotations. 
