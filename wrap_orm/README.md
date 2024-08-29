# Responsibilities

1. Application layer interfaces
   1. Command and Query
   2. Query in JSON?
   3. Query should support => column filtering, pagination, sorting, grouping, row filtering, query, aggregate
   4. migration interface
   5. seed interface
2. Adapters
   1. Get input configurations from entry point
   2. implment application layer interafce
   3. adopt choosen ORM as a strategy
3. wrap_orm
   1. ORM specific Comman and Query
   2. ORM specific Query in JSON?
   3. ORM specific Query should support => column filtering, pagination, sorting, grouping, row filtering, query, aggregate
   4. ORM specific migration interface
   5. ORM specific seed interface
4. Choose an appropriate ORM
