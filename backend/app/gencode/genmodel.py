from black import format_str, FileMode
import argparse
import yaml
from jinja2 import Environment, FileSystemLoader


def prep_data(file: str):
    sqlalchemy_util_types = ["EmailType", "URLType", "IPAddressType", "JSONType"]
    pydantic_types = ["NameEmail", "HttpUrl", "EmailStr"]

    data = yaml.load(open(file), Loader=yaml.FullLoader)
    data["has_update"] = False
    data["has_program_id"] = False
    data["sqlalchemy_util_types"] = set([])
    data["pydantic_types"] = set([])
    data["column_types"] = set(["Integer"])
    # data['creation_required_fields'] = []
    for field in data["fields"]:
        # Check if there are Update schema fields
        if "is_update" in field["schema"] and data["has_update"] == False:
            data["has_update"] = True

        # Check if it has a program id
        if field["name"] == "program_id":
            data["has_program_id"] = True

        # Check if ForeignKey needs to be imported
        if "fk" in field:
            data["column_types"].add("ForeignKey")

        # Load column types
        column_type = field["column_type"]
        if column_type in sqlalchemy_util_types:
            data["sqlalchemy_util_types"].add(column_type)
        else:
            data["column_types"].add(column_type)

        # Load field types
        field_type = field["type"]
        if field_type in pydantic_types:
            data["pydantic_types"].add(field_type)

        # Find all of the required fields for creation
        # if "is_base" in field["schema"]:
        #     if "is_optional" in field["schema"]["is_base"]:
        #         if not field["schema"]["is_base"]["is_optional"]:
        #             if field not in data['creation_required_fields']:
        #                 data['creation_required_fields'].append(field)
        #     else:
        #         if field not in data['creation_required_fields']:
        #             data['creation_required_fields'].append(field)
        # if "is_create" in field["schema"]:
        #     if "is_optional" in field["schema"]["is_create"]:
        #         if not field["schema"]["is_create"]["is_optional"]:
        #             if field not in data['creation_required_fields']:
        #                 data['creation_required_fields'].append(field)
        #     else:
        #         if field not in data['creation_required_fields']:
        #             data['creation_required_fields'].append(field)
    return data


def main(file: str):
    data = prep_data(file)

    env = Environment(
        loader=FileSystemLoader("./gencode/templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # Model
    model_template = env.get_template("model.py.j2")
    model_code = format_str(model_template.render(data), mode=FileMode())
    with open(f"./app/models/{data['lower_name']}.py", "w") as model_file:
        model_file.write(model_code)

    # Schema
    schema_template = env.get_template("schema.py.j2")
    schema_code = format_str(schema_template.render(data), mode=FileMode())
    with open(f"./app/schemas/{data['lower_name']}.py", "w") as schema_file:
        schema_file.write(schema_code)

    # Crud
    crud_template = env.get_template("crud.py.j2")
    crud_code = format_str(crud_template.render(data), mode=FileMode())
    with open(f"./app/crud/crud_{data['lower_name']}.py", "w") as crud_file:
        crud_file.write(crud_code)

    # Tests util
    test_util_template = env.get_template("test_utils.py.j2")
    test_util_code = format_str(test_util_template.render(data), mode=FileMode())
    with open(f"./app/tests/utils/{data['lower_name']}.py", "w") as test_util_file:
        test_util_file.write(test_util_code)

    # Crud tests
    test_crud_template = env.get_template("test_crud.py.j2")
    test_crud_code = format_str(test_crud_template.render(data), mode=FileMode())
    with open(f"./app/tests/crud/test_{data['lower_name']}.py", "w") as test_crud_file:
        test_crud_file.write(test_crud_code)

    # Api Endpoint
    if data["is_api"]:
        # Api endpoint
        api_template = env.get_template("api.py.j2")
        api_code = format_str(api_template.render(data), mode=FileMode())
        filepath = f"./app/api/api_v1/endpoints/{data['lower_name']}s.py"
        with open(filepath, "w") as api_file:
            api_file.write(api_code)

        # Api tests
        test_api_template = env.get_template("test_api.py.j2")
        test_api_code = format_str(test_api_template.render(data), mode=FileMode())
        with open(
            f"./app/tests/api/api_v1/test_{data['lower_name']}.py", "w"
        ) as test_api_file:
            test_api_file.write(test_api_code)

    # Imports
    imports_template = env.get_template("imports.py.j2")
    # Todo if you wanted to get fancy you could open all these files and modify them
    print(imports_template.render(data))

    # Tests


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="input file")
    args = parser.parse_args()
    main(args.input)
