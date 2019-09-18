SELECT ci.NAME_VALUE NAME_VALUE,
        ctle.ENTRY_TIMESTAMP
    FROM ct_log_entry ctle
    INNER JOIN certificate_identity ci on ci.certificate_id = ctle.certificate_id
    WHERE
        ctle.ENTRY_TIMESTAMP between '2019-09-15 00:00:00' and '2019-09-15 06:00:00'
        AND lower(ci.NAME_VALUE) LIKE 'test.%'
    limit 10;



SELECT ci.NAME_VALUE
    FROM certificate_identity ci
    WHERE lower(ci.NAME_VALUE) > 'test' and lower(ci.NAME_VALUE) < 'testZ'
    limit 10;


certwatch=> \d certificate_identity;
             Table "public.certificate_identity"
     Column     |   Type    | Collation | Nullable | Default
----------------+-----------+-----------+----------+---------
 certificate_id | integer   |           | not null |
 name_type      | name_type |           | not null |
 name_value     | text      |           | not null |
 issuer_ca_id   | integer   |           |          |
Indexes:
    "ci_uniq" UNIQUE, btree (certificate_id, lower(name_value) text_pattern_ops, name_type)
    "ci_ca" btree (issuer_ca_id, lower(name_value) text_pattern_ops, name_type)
    "ci_ca_reverse" btree (issuer_ca_id, reverse(lower(name_value)) text_pattern_ops, name_type)
    "ci_forward" btree (lower(name_value) text_pattern_ops, issuer_ca_id, name_type)
    "ci_reverse" btree (reverse(lower(name_value)) text_pattern_ops, issuer_ca_id, name_type)
Foreign-key constraints:
    "ci_c_fk" FOREIGN KEY (certificate_id) REFERENCES certificate(id)
    "ci_ca_fk" FOREIGN KEY (issuer_ca_id) REFERENCES ca(id)
