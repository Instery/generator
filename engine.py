class Generator(object):
    def __init__(self): 
        self.classes = set()

    def parse_yaml(self, file_name):
        from yaml import load
        with open(file_name, 'r') as yaml_source:
            self.dump = load(yaml_source.read())

    def generate(self):
        for name in self.dump:
            
            out ="CREATE TABLE \"{}\" (\n".format(name.lower())#, self.dump[name]['fields'])
            out += "\t\"{}_id\" SERIAL PRIMARY KEY,\n".format(name.lower())
            for class_field in self.dump[name]["fields"]:
                out += "\t\"{}_{}\" ".format(name.lower(), class_field)
                for field_value in self.dump[name]["fields"][class_field]:
                    out +="{}".format(field_value)
                out += ",\n"
            out += "\t\"{}_created\" INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER),\n".format(name.lower())
            out += "\t\"{}_updated\" INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER),\n".format(name.lower())
            out += ");\n"
            self.classes.add(out)
        print(self.dump)

    def build_tables(self):
        with open('tables.sql', 'w') as out:
            out.write('\n'.join(self.classes))

if __name__ == "__main__":
    gen = Generator()
    gen.parse_yaml('schema.yaml')
    gen.generate()
    gen.build_tables()
