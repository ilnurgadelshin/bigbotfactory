all: create_tables

create_tables:
	for f in *.json; do echo creating $$f; make create_table TABLE_FILE_NAME=$$f; done

create_table:
	aws dynamodb create-table --cli-input-json file://${TABLE_FILE_NAME}
