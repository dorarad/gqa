Definition of the scene graphs ontology.
<br> Consists of 3 txt files: [objects.txt](objects.txt), [attributes.txt](attributes.txt), and [relations.txt](relations.txt).
<br> [txt2json.py](txt2json.py) translates these txt files into jsons that are then consumed by create_questions.py.

Each txt file consists of a list objects/attributes/relations, annotated by differnet labels that are used during question generation.

Each line is formatted as: 
<br> In [objects.txt](objects.txt): object name,frequency,category name,annotations
<br> In [attributes.txt](attributes.txt): attribute name;frequency;attribute type;annotations
<br> In [relations.txt](relations.txt): relation,frequency,relation type,annotations

See [txt2json.py](txt2json.py) for the definition of specific extra annotations. 
