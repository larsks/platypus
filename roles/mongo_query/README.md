# mongo_query

A module for evaluating an expression against a [MongoDB][] database.

[mongodb]: https://mongodb.com/

## Options

- `connection` -- a mongodb connection uri
- `query` -- the expression to evaluate

## Example playbook

    - hosts: localhost
      roles:
        - mongo_query

      tasks:
        - mongo_query:
            connection: mongodb://localhost:27017/mydatabase
            query: db.stats()
          register: result

        - debug:
            var: result
